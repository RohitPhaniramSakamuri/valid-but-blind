"""Cross-region ownership of exp008 so duplicate queued jobs do not both run. Usage: claim.py claim|beat|done <job>."""
import json, sys, time, boto3
import os
B, K = "vbb-exp008-286879406788-use1", f"claims/{os.environ.get('CLAIM_KEY', 'exp008')}.json"
s3 = boto3.client("s3", region_name="us-east-1"); cmd, job = sys.argv[1], sys.argv[2]; ngpu = int(sys.argv[3]) if len(sys.argv) > 3 else 1
put = lambda **kw: s3.put_object(Bucket=B, Key=K, Body=json.dumps(dict(owner=job, t=time.time(), ngpu=ngpu, **kw)).encode())
if cmd == "claim":
    try:
        cur = json.loads(s3.get_object(Bucket=B, Key=K)["Body"].read())
    except Exception:
        cur = None
    faster = ngpu >= 4 and cur is not None and cur.get("ngpu", 1) < 4 and not cur.get("done")  # a 4-GPU job runs even if a 1-GPU job owns the claim
    if cur and not faster and (cur.get("done") or (cur["owner"] != job and time.time() - cur["t"] < 1800)): print("owned by", cur); sys.exit(1)
    try: s3.put_object(Bucket=B, Key=K, Body=json.dumps(dict(owner=job, t=time.time(), ngpu=ngpu)).encode(), **({"IfNoneMatch": "*"} if cur is None else {}))
    except Exception as e: print("claim race lost or unsupported:", e); time.sleep(5); cur = json.loads(s3.get_object(Bucket=B, Key=K)["Body"].read()); sys.exit(0 if cur["owner"] == job else 1)
    sys.exit(0)
elif cmd == "beat": put()
elif cmd == "done": put(done=True)
