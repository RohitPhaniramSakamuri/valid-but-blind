#!/usr/bin/env bash
# Live:     ./start.sh
# Recorded: ./start.sh recorded
cd "$(dirname "$0")"
pkill -f '[a]pp.py' 2>/dev/null; sleep 1
[ "$1" = recorded ] && export REPLAY=1
./run_demo.sh > demo.log 2>&1 &
for i in $(seq 1 60); do
  if curl -s -m 2 http://127.0.0.1:8765/api/meta >/dev/null; then
    echo "Ready: http://127.0.0.1:8765"; xdg-open http://127.0.0.1:8765 >/dev/null 2>&1 &
    echo "Leave this window open. Press Ctrl+C to stop."; wait; exit 0
  fi
  sleep 2
done
echo "Did not start. Run: ./start.sh recorded"; tail -5 demo.log
