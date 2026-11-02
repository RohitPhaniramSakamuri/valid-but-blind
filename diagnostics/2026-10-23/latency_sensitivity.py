"""Separate deployment arithmetic from sklearn wrapper latency, no new tuning."""
import os
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[name]='1'
from pathlib import Path
import json,time
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from threadpoolctl import threadpool_limits

HERE=Path(__file__).resolve().parent


def measure(fn,x):
    for _ in range(20):fn(x)
    timings=[]
    for _ in range(300):
        start=time.perf_counter_ns();fn(x);timings.append((time.perf_counter_ns()-start)/1e6)
    return float(np.median(timings))


with threadpool_limits(limits=1):
    d=np.load(HERE/'outcomes.npz');train=d['splits']=='train';test=(d['splits']=='test')&d['heldout_family']
    outputs={}
    for channel in ['cheap','rich']:
        x=d[channel];model=make_pipeline(StandardScaler(),Ridge(alpha=10)).fit(x[train],d['errors'][train])
        scaler,reg=model.steps[0][1],model.steps[1][1]
        matrix=reg.coef_.T/scaler.scale_[:,None]
        bias=reg.intercept_ - scaler.mean_@matrix
        direct=lambda a:a@matrix+bias
        error=float(np.max(np.abs(model.predict(x)-direct(x))))
        pipeline_ms=measure(model.predict,x[:1]);numpy_ms=measure(direct,x[:1])
        actions=direct(x[test]).argmin(axis=1)
        action_ms=d['action_cost_ms'][test][np.arange(test.sum()),actions]
        total=d['cheap_cost_ms'][test]+action_ms+numpy_ms
        if channel=='rich':total+=d['rich_extra_cost_ms'][test]
        outputs[channel]={'sklearn_pipeline_predict_ms':pipeline_ms,'compiled_numpy_predict_ms':numpy_ms,
                          'maximum_prediction_difference':error,'action_choices_equal':bool(np.array_equal(actions,model.predict(x[test]).argmin(axis=1))),
                          'mean_allin_compiled_route_ms':float(total.mean()),'query_error':float(d['errors'][test][np.arange(test.sum()),actions].mean())}
    outputs['direct_source_query_ms']=float(d['action_cost_ms'][test,0].mean())
    outputs['scope']='Post-hoc implementation sensitivity; same trained linear functions and predictions, no hyperparameter/final-label fitting. Acquisition gates were not refit in this sensitivity.'
    (HERE/'latency_sensitivity.json').write_text(json.dumps(outputs,indent=2)+'\n')
    print(json.dumps(outputs,indent=2))
