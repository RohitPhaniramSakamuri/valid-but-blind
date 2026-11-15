"""Run all exp008 stream tasks on however many GPUs exist. Each worker is pinned to one GPU and pulls the next ready task; a task retries (resuming finished streams) up to 4 times."""
import os, subprocess, sys, threading, time, queue
WORK, OUT, HERE = os.environ["WORK"], os.environ["OUT"], os.path.dirname(os.path.abspath(__file__))
ngpu = int(subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True).stdout.count("GPU "))
PER_GPU = int(os.environ.get("PER_GPU", "4"))
T = []
CIF = [("Addepalli2022Efficient_WRN_34_10", 4), ("Addepalli2021Towards_WRN34", 3), ("Hendrycks2020AugMix_ResNeXt", 3), ("Hendrycks2020AugMix_WRN", 2), ("Addepalli2021Towards_PARN18", 1), ("Modas2021PRIMEResNet18", 1)]
MED = [(ds, a, sh, 2) for ds in ("oct", "organc", "pneumonia") for a in ("tent0.001", "tent0.005") for sh in range(2)]
cif = [("cifar", m, "tent0.001", sh, n) for m, n in CIF for sh in range(n)]
med = [(ds, ds, a, sh, n) for ds, a, sh, n in MED]
while cif or med:  # interleave heavy CIFAR and medical tasks so each GPU gets a mix
    if cif: T.append(cif.pop(0))
    if med: T.append(med.pop(0))
ready = lambda t: os.path.exists(f"{WORK}/{'cifar' if t[0] == 'cifar' else t[0]}/READY")
pending, lock, log = list(T), threading.Lock(), open(f"{OUT}/logs/launcher.log", "a")
def say(*a):
    with lock: print(time.strftime("%H:%M:%S"), *a, file=log, flush=True); print(*a, flush=True)
def worker(i):
    gpu = i % max(ngpu, 1)
    while True:
        with lock:
            pick = next((t for t in pending if ready(t)), None)
            if pick: pending.remove(pick)
            elif not pending: return
        if not pick:
            if all(os.path.exists(f"{WORK}/{d}/FAILED") for d in {t[0] for t in pending}): return
            time.sleep(15); continue
        ds, m, a, sh, n = pick; lg = f"{OUT}/logs/{ds}_{m}_{a}_{sh}.log"
        for attempt in range(4):
            r = subprocess.run([sys.executable, f"{HERE}/run8.py", ds, m, a, str(sh), str(n)], env={**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu)}, stdout=open(lg, "a"), stderr=subprocess.STDOUT)
            if r.returncode == 0: say("done", pick, "gpu", gpu); break
            say("retry", attempt, pick, "rc", r.returncode); time.sleep(30 * (attempt + 1))
        else: say("FAILED", pick)
say("gpus", ngpu, "workers", ngpu * PER_GPU, "tasks", len(T))
th = [threading.Thread(target=worker, args=(i,)) for i in range(max(ngpu, 1) * PER_GPU)]
[t.start() for t in th]; [t.join() for t in th]
say("ALL TASKS FINISHED", "left:", pending)
