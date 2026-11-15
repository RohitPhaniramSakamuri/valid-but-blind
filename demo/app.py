"""Live laptop demo: Tent with the released monitor and the entropy-free twin alarm on the same CIFAR-100-C stream.

Labels are used only to build Dirichlet streams and to colour results for the audience. Neither monitor sees them.
Differences from the recorded runs: CPU instead of GPU; no autocast in calibration; alarms use only data seen so far, so before batch 30
the confidence-sequence tuning value comes from the prefix. Recalibrating every 5 batches is a disclosed speed option, not the paper's setting.
"""
import base64
import io
import json
import os
import threading
import time
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import numpy as np
import torch
import torch.nn as nn
from confseq.conjmix_bounded import conjmix_empbern_lower_cs
from confseq.predmix import predmix_empbern_lower_cs
from PIL import Image

from arch_resnext import ResNeXt29
from arch_wide_resnet import WideResNet

ROOT = os.path.dirname(os.path.abspath(__file__))
SPLIT_SEED, BATCH, TOTAL = 20261031, 100, 120
ALPHA, AL1, TOL = 0.15, 0.025, 0.1
Q_GRID = torch.arange(0.001, 0.99, 0.001)
CORRUPTIONS = ["gaussian_noise", "shot_noise", "impulse_noise", "defocus_blur", "glass_blur", "motion_blur", "zoom_blur", "snow", "frost", "fog", "brightness", "contrast", "elastic_transform", "pixelate", "jpeg_compression"]
FINE = "apple aquarium_fish baby bear beaver bed bee beetle bicycle bottle bowl boy bridge bus butterfly camel can castle caterpillar cattle chair chimpanzee clock cloud cockroach couch crab crocodile cup dinosaur dolphin elephant flatfish forest fox girl hamster house kangaroo keyboard lamp lawn_mower leopard lion lizard lobster man maple_tree motorcycle mountain mouse mushroom oak_tree orange orchid otter palm_tree pear pickup_truck pine_tree plain plate poppy porcupine possum rabbit raccoon ray road rocket rose sea seal shark shrew skunk skyscraper snail snake spider squirrel streetcar sunflower sweet_pepper table tank telephone television tiger tractor train trout tulip turtle wardrobe whale willow_tree wolf woman worm".split()
torch.set_num_threads(os.cpu_count() or 4)


class Norm(nn.Module):
    def __init__(self, inner):
        super().__init__()
        self.inner = inner

    def forward(self, x):
        return self.inner((x - 0.5) / 0.5)


def build(name):
    if name == "Hendrycks2020AugMix_WRN":
        m = Norm(WideResNet(depth=40, widen_factor=2, sub_block1=False, num_classes=100))
        sd = torch.load(f"{ROOT}/models/{name}.pt", map_location="cpu", weights_only=False)
        sd = sd.get("state_dict", sd)
        sd = {k.replace("module.", "", 1).replace("model.", "", 1): v for k, v in sd.items() if k not in ("mu", "sigma")}
        m.inner.load_state_dict(sd, strict=True)
    else:
        m = ResNeXt29()
        sd = torch.load(f"{ROOT}/models/{name}.pt", map_location="cpu", weights_only=True)
        sd = sd.get("state_dict", sd)
        m.load_state_dict({k.replace("module.", ""): v for k, v in sd.items()}, strict=False)
    return m.eval()


def adaptive(name):
    m = build(name).requires_grad_(False)
    params = []
    for b in m.modules():
        if isinstance(b, nn.BatchNorm2d):
            b.requires_grad_(True)
            b.track_running_stats = False
            b.running_mean = None
            b.running_var = None
            params += [b.weight, b.bias]
    return m, params


def proxy(logits):
    return 1 - logits.softmax(1).max(1).values


def max_f1(err, prox):
    grid = Q_GRID.view(-1, 1)
    pos = prox.view(1, -1) > grid
    e = err.view(1, -1)
    tp, fp, fn = (pos & e).sum(1).float(), (pos & ~e).sum(1).float(), (~pos & e).sum(1).float()
    return grid[(2 * tp / (2 * tp + fp + fn).clamp_min(1)).argmax()].item()


def lower_last(x):
    """Latest value of the lower confidence sequence, using only the data seen so far."""
    x = np.asarray(x, dtype=float)
    if len(x) < 2:
        return 0.0, False
    m = np.cumsum(x) / np.arange(1, len(x) + 1)
    t = min(len(x) - 1, int(TOTAL * 0.25))
    v = max(float(np.cumsum((x - np.append(0.5, m[:-1])) ** 2)[t] * t), 1e-6)
    try:
        return float(np.asarray(conjmix_empbern_lower_cs(x=x, alpha=ALPHA, v_opt=v))[-1]), False
    except RuntimeError:
        return float(np.asarray(predmix_empbern_lower_cs(x=x, alpha=ALPHA))[-1]), True


def seed_of(*parts):
    return zlib.crc32("|".join(map(str, parts)).encode()) % 2**31


class Store:
    def __init__(self):
        c = np.load(f"{ROOT}/data/clean_test.npz")
        self.clean, self.labels = c["x"], c["y"].astype(np.int64)
        lp = f"{ROOT}/data/CIFAR-100-C/labels.npy"
        if os.path.exists(lp):
            assert (np.load(lp)[:10000] == self.labels).all(), "clean labels differ from CIFAR-100-C"
        perm = np.random.RandomState(SPLIT_SEED).permutation(10000)
        self.calib, self.ids = perm[:1000], perm[5000:9000]
        self.cx = torch.from_numpy(self.clean[self.calib]).permute(0, 3, 1, 2).float().div_(255)
        self.cy = torch.from_numpy(self.labels[self.calib])

    def images(self, corruption, severity):
        if corruption == "clean":
            return self.clean
        arr = np.load(f"{ROOT}/data/CIFAR-100-C/{corruption}.npy", mmap_mode="r")
        return np.array(arr[(severity - 1) * 10000:severity * 10000])

    def stream(self, kind, corruption, severity, draw):
        rng = np.random.RandomState(seed_of("exp004-factorial", corruption, severity, draw))
        if kind == "by_class":
            seq = np.concatenate([self.ids[np.argsort(self.labels[self.ids], kind="stable")] for _ in range(3)])
            return [seq[i * BATCH:(i + 1) * BATCH] for i in range(TOTAL)]
        p = np.full(100, 0.01) if kind == "balanced" else rng.dirichlet(np.full(100, 0.1))
        counts = np.bincount(self.labels[self.ids], minlength=100)
        w = p[self.labels[self.ids]] / counts[self.labels[self.ids]]
        w /= w.sum()
        return [rng.choice(self.ids, BATCH, replace=True, p=w) for _ in range(TOTAL)]


STORE = None
CAL = {}


def calibrate(name):
    if name in CAL:
        return CAL[name]
    src = build(name).requires_grad_(False)
    with torch.inference_mode():
        lg = src(STORE.cx)
    e0, p0 = lg.argmax(1) != STORE.cy, proxy(lg)
    q0 = max_f1(e0, p0)
    twin, _ = adaptive(name)
    twin.requires_grad_(False)
    with torch.inference_mode():
        lt = twin(STORE.cx)
    et, pt = lt.argmax(1) != STORE.cy, proxy(lt)
    qt = max_f1(et, pt)
    ft = pt > qt
    w = (np.log(2) - np.log(AL1)) / (2 * len(STORE.cy))
    CAL[name] = dict(r0=float(e0.float().mean()), q0=q0, qt=qt, fp0=float(((p0 > q0) & ~e0).float().mean()), fpt=float((ft & ~et).float().mean()), fnt=float((~ft & et).float().mean()), w=w, twin=twin)
    return CAL[name]


class Run(threading.Thread):
    def __init__(self, cfg):
        super().__init__(daemon=True)
        self.cfg = cfg
        self.lock = threading.Lock()
        self.batches, self.status, self.message = [], "loading", "Calibrating on 1,000 clean images..."
        self.go = threading.Event()
        self.go.set()
        self.steps = 0
        self.stop_flag = False
        self.info = {}

    def control(self, action):
        if action == "pause":
            self.go.clear()
            self.status = "paused"
        elif action == "resume":
            self.steps = 0
            self.go.set()
            self.status = "running"
        elif action == "step":
            self.steps = 1
            self.go.set()
            self.status = "running"
        elif action == "stop":
            self.stop_flag = True
            self.go.set()

    def run(self):
        try:
            self._run()
        except Exception as e:  # shown on screen for the presenter
            self.status, self.message = "error", repr(e)

    def _run(self):
        c = self.cfg
        cal = calibrate(c["model"])
        twin = cal["twin"]
        model, params = adaptive(c["model"])
        opt = torch.optim.Adam(params, lr=float(c["lr"]), betas=(0.9, 0.999), weight_decay=0.0)
        imgs = STORE.images(c["corruption"], int(c["severity"]))
        order = STORE.stream(c["kind"], c["corruption"], int(c["severity"]), int(c["draw"]))
        L_rel, L_tw = cal["fp0"] + cal["w"], cal["fpt"] + cal["fnt"] + cal["w"]
        level = cal["r0"] + TOL
        self.info = dict(r0=cal["r0"], level=level, q0=cal["q0"], qt=cal["qt"], L_released=L_rel, L_twin=L_tw, threads=torch.get_num_threads(), recal_every=int(c["recal"]))
        self.status, self.message = "running", ""
        zr, zt, errs, qr = [], [], [], cal["q0"]
        alarm_r, alarm_t = None, None
        for t, ids in enumerate(order, 1):
            self.go.wait()
            if self.stop_flag:
                self.status = "stopped"
                return
            t0 = time.time()
            raw = imgs[ids]
            x = torch.from_numpy(raw).permute(0, 3, 1, 2).float().div_(255)
            y = torch.from_numpy(STORE.labels[ids])
            logits = model(x)
            loss = -(logits.softmax(1) * logits.log_softmax(1)).sum(1).mean()
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            logits = logits.detach()
            t1 = time.time()
            with torch.inference_mode():
                lw = twin(x)
            t2 = time.time()
            if (t - 1) % int(c["recal"]) == 0:
                with torch.inference_mode():
                    lc = model(STORE.cx)
                qr = max_f1(lc.argmax(1) != STORE.cy, proxy(lc))
            t3 = time.time()
            ut, uw = proxy(logits), proxy(lw)
            pt, pw = logits.argmax(1), lw.argmax(1)
            E = pt != y
            F_r = ut > qr
            F_t = (uw > cal["qt"]) | (pt != pw)
            zr.append(float(F_r.float().mean()))
            zt.append(float(F_t.float().mean()))
            errs.append(float(E.float().mean()))
            cr, fbr = lower_last(zr)
            ct, fbt = lower_last(zt)
            br, bt = max(cr - L_rel, 0.0), max(ct - L_tw, 0.0)
            if alarm_r is None and br > level:
                alarm_r = t
            if alarm_t is None and bt > level:
                alarm_t = t
            sprite = Image.new("RGB", (320, 320))
            for i, a in enumerate(raw):
                sprite.paste(Image.fromarray(a), ((i % 10) * 32, (i // 10) * 32))
            buf = io.BytesIO()
            sprite.save(buf, "PNG")
            rec = dict(t=t, sprite=base64.b64encode(buf.getvalue()).decode(), y=y.tolist(), pt=pt.tolist(), pw=pw.tolist(), ct=[round(float(v), 3) for v in 1 - ut], cw=[round(float(v), 3) for v in 1 - uw], E=E.int().tolist(), Fr=F_r.int().tolist(), Ft=F_t.int().tolist(), err=errs[-1], run_err=float(np.mean(errs)), zr=zr[-1], zt=zt[-1], br=br, bt=bt, alarm_r=alarm_r, alarm_t=alarm_t, qr=qr, conf_t=float((1 - ut).mean()), conf_w=float((1 - uw).mean()), twin_err=float((pw != y).float().mean()), fallback=bool(fbr or fbt), sec=dict(tent=t1 - t0, twin=t2 - t1, recal=t3 - t2, total=time.time() - t0), source_note=None)
            with self.lock:
                self.batches.append(rec)
            d = float(c.get("delay", 0))
            if d:
                time.sleep(d)
            if self.steps:
                self.steps = 0
                self.go.clear()
                self.status = "paused"
        self.status, self.message = "finished", ""


class ReplayRun(threading.Thread):
    """Plays a saved run at the live pace. The page says it is recorded."""

    def __init__(self):
        super().__init__(daemon=True)
        self.lock = threading.Lock()
        self.batches, self.status, self.message, self.info, self.cfg = [], "running", "", {}, {}
        self.stop_flag = False

    def control(self, action):
        self.stop_flag = action == "stop" or self.stop_flag

    def run(self):
        saved = json.load(open(f"{ROOT}/recorded_run.json"))
        self.info = saved["info"]
        for b in saved["batches"]:
            if self.stop_flag:
                return
            with self.lock:
                self.batches.append(b)
            time.sleep(2.2)
        self.status = "finished"


RUN = None
HTML = None
REPLAY = os.environ.get("REPLAY") == "1"


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/":
            page = open(f"{ROOT}/simple.html", "rb").read()
            if REPLAY:
                page = page.replace(b"<script>", b"<script>window.RECORDED=true;", 1)
            return self._send(page, "text/html; charset=utf-8")
        if u.path == "/full":
            return self._send(open(f"{ROOT}/index.html", "rb").read(), "text/html; charset=utf-8")
        if u.path == "/api/meta":
            avail = [] if REPLAY else [c for c in CORRUPTIONS if os.path.exists(f"{ROOT}/data/CIFAR-100-C/{c}.npy")]
            return self._send(json.dumps(dict(corruptions=avail, classes=FINE, models=[m for m in ("Hendrycks2020AugMix_WRN", "Hendrycks2020AugMix_ResNeXt") if os.path.exists(f"{ROOT}/models/{m}.pt")])))
        if u.path == "/api/state":
            since = int(parse_qs(u.query).get("since", ["0"])[0])
            if RUN is None:
                return self._send(json.dumps(dict(status="idle", batches=[], info={}, message="", cfg={})))
            with RUN.lock:
                new = RUN.batches[since:]
            return self._send(json.dumps(dict(status=RUN.status, message=RUN.message, info=RUN.info, batches=new, cfg=RUN.cfg)))
        self.send_error(404)

    def do_POST(self):
        global RUN
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/api/start":
            if RUN is not None:
                RUN.control("stop")
            RUN = ReplayRun() if REPLAY else Run(body)
            RUN.start()
        elif self.path == "/api/control" and RUN is not None:
            RUN.control(body.get("action"))
        self._send("{}")


if __name__ == "__main__":
    if not REPLAY:
        STORE = Store()
    port = int(os.environ.get("PORT", 8765))
    print(f"Open http://127.0.0.1:{port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
