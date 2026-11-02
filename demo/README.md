# Live demo: Valid but Blind

Runs Tent on this laptop's CPU, with the released monitor and the entropy-free twin alarm watching the same stream. Every image is marked caught, missed (FN), false flag (FP) or quiet for both monitors.

**Start:** `./run_demo.sh`, then open http://127.0.0.1:8765. It uses uv and needs `data/` and `models/` in this folder.

**Controls:** presets or free settings; Start; Pause or Space; Step; the batch slider or arrow keys to review earlier batches; filter chips; click an image for labels, predictions and confidence.

**What is live:** Tent, the twin and both alarms are computed here as you watch. Labels only colour the screen.

**Differences from the recorded runs:** CPU, no autocast in calibration, and alarms use only data seen so far, so the tuning value before batch 30 comes from the prefix. "Every 5 batches" recalibration is a demo speed option and is disclosed on screen; the paper recalibrates every batch.

**Checked against recorded GPU runs, AugMix WRN-40-2 (`check_results.json`):**

| Stream | Recalibration | Tent error, live / recorded | Twin alarm, live / recorded | Released alarm |
| --- | --- | --- | --- | --- |
| Frost 5, draw 0 | Every batch | 0.569 / 0.565 | 25 / 26 | None in both |
| Frost 5, draw 0 | Every 5 | 0.569 / 0.565 | 25 / 26 | None in both |
| Fog 3, draw 1 | Every 5 | 0.351 / 0.352 | None in both | None in both |
| Frost 3, draw 1 | Every 5 | 0.412 / 0.411 | 80 / 84 | None in both |

Preset 4 (learning rate 5e-2) uses the same settings style as the harm test but not its exact draw, so it has no recorded counterpart. The ResNeXt-29 option has not been run through this check.
