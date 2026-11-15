"""Run exp010 stream tasks on the GPUs present. TASKS env: space-separated ds:model:arm:nshards. Each worker pulls the next ready task; a task retries (resuming finished streams) up to 4 times. Exits when all tasks finish or their data failed."""
import os, subprocess, sys, threading, time
WORK, OUT, HERE = os.environ["WORK"], os.environ["OUT"], os.path.dirname(os.path.abspath(__file__))
ngpu = max(1, int(subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True).stdout.count("GPU "))) if os.environ.get("SMOKE") is None else 1
PER_GPU = int(os.environ.get("PER_GPU", "4")); T = []
for spec in os.environ["TASKS"].split():
    ds, m, a, n = spec.split(":"); T += [(ds, m, a, sh, int(n)) for sh in range(int(n))]
ready = lambda t: os.path.exists(f"{WORK}/{t[0]}/READY")
pending, lock, log = list(T), threading.Lock(), open(f"{OUT}/logs/launcher.log", "a"); failed = []
def say(*a):
    with lock: print(time.strftime("%H:%M:%S"), *a, file=log, flush=True); print(*a, flush=True)
def worker(i):
    gpu = i % ngpu
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
            r = subprocess.run([sys.executable, f"{HERE}/run10.py", ds, m, a, str(sh), str(n)], env={**os.environ, "CUDA_VISIBLE_DEVICES": str(gpu)}, stdout=open(lg, "a"), stderr=subprocess.STDOUT)
            if r.returncode == 0: say("done", pick, "gpu", gpu); break
            say("retry", attempt, pick, "rc", r.returncode); time.sleep(2 if os.environ.get("SMOKE") else 30 * (attempt + 1))
        else: say("FAILED", pick); failed.append(pick)
say("gpus", ngpu, "workers", ngpu * PER_GPU, "tasks", len(T))
th = [threading.Thread(target=worker, args=(i,)) for i in range(ngpu * PER_GPU)]
[t.start() for t in th]; [t.join() for t in th]
say("ALL TASKS FINISHED", "left:", pending, "failed:", failed)
