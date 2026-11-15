import os, subprocess, sys
sys.exit(subprocess.call(["bash", os.path.join(os.path.dirname(os.path.abspath(__file__)), "job.sh")]))
