# thinknet-observer-python

A library use for collect metrics, log and tracing.

  

## Installation
```

pip install thinknet-observer

```

  

## Get started

### Metrics
How to collect metrics with this lib:

  

```Python

from thinknet_observer import PrometheusMiddleware


# Instantiate a app framework
app = Flask(__name__) # or app = FastAPI()

# use middleware to collect default metrics
middleware = PrometheusMiddleware(app) # or PrometheusMiddleware(app,is_multiprocessing = True) when us multiprocess
middleware.register_metrics()

# add exclude (optional)
list_exclude = [{"route": "/healthz"}]
middleware.add_exclude(list_exclude)

```

to create custom metrics can be done with following code

```Python
from  thinknet_observer  import  MetricCollector

# NOTE: metrics name(1st param) must be unique for each metrics

# Custom gauge 
# (for gauge metrics if using multiprocess add param 'multiprocess_mode="livesum"')
CUSTOM_GAUGE = MetricCollector.gauge(
    "CUSTOM_GAUGE", "desc of CUSTOM_GAUGE", ["something"]
)
CUSTOM_GAUGE_NOLABEL = MetricCollector.gauge(
    "CUSTOM_GAUGE_NOLABEL", "desc of CUSTOM_GAUGE_NOLABEL"
)


# Custom summary
CUSTOM_SUMMARY = MetricCollector.summary(
    "CUSTOM_SUMMARY", "desc of CUSTOM_SUMMARY", ["something"]
)
CUSTOM_SUMMARY_NOLABEL = MetricCollector.summary(
    "CUSTOM_SUMMARY_NOLABEL",
    "desc of CUSTOM_SUMMARY_NOLABEL",
)


# Custom histogram
CUSTOM_HISTOGRAM = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM", "desc of CUSTOM_HISTOGRAM", ["something"]
)
CUSTOM_HISTOGRAM_NOLABEL = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM_NOLABEL", "desc of CUSTOM_HISTOGRAM_NOLABEL"
)
CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET = MetricCollector.histogram(
    "CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET",
    "desc of CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET",
    buckets=[0.5, 0.75, 1],
)


# Custom counter
CUSTOM_COUNTER = MetricCollector.counter(
    "CUSTOM_COUNTER", "desc of CUSTOM_COUNTER", ["something"]
)
CUSTOM_COUNTER_NOLABEL = MetricCollector.counter(
    "CUSTOM_COUNTER_NOLABEL", "desc of CUSTOM_COUNTER_NOLABEL"
)
```

Example of custom metrics usage
```Python

@app_flask.route("/inc_gauge/<number>", methods=["POST"])
def inc_gauge(number):
    CUSTOM_GAUGE.labels("something'value").inc(float(number))
    CUSTOM_GAUGE_NOLABEL.inc(float(number))
    return {"msg": f"inc {number}"}

@app_flask.route("/dec_gauge/<number>", methods=["POST"])
def dec_gauge(number):
    CUSTOM_GAUGE.labels("something'value").dec(float(number))
    CUSTOM_GAUGE_NOLABEL.dec(float(number))
    return {"msg": f"dec {number}"}

@app_flask.route("/summary_observe/<number>", methods=["POST"])
def summary_observe(number):
    CUSTOM_SUMMARY.labels("something'value").observe(float(number))
    CUSTOM_SUMMARY_NOLABEL.observe(float(number))
    return {"msg": f"summary_observe {number}"}

@app_flask.route("/histogram_observe/<number>", methods=["POST"])
def histogram_observe(number):
    CUSTOM_HISTOGRAM.labels("something'value").observe(float(number))
    CUSTOM_HISTOGRAM_NOLABEL.observe(float(number))
    return {"msg": f"histogram_observe {number}"}

@app_flask.route("/histogram_observe2/<number>", methods=["POST"])
def histogram_observe2(number):
    CUSTOM_HISTOGRAM_NOLABEL_CUSTOMBUCKET.observe(float(number))
    return {"msg": f"histogram_observe {number}"}

@app_flask.route("/count/<number>", methods=["POST"])
def count_metric(number):
    CUSTOM_COUNTER.labels("something'value").inc(float(number))
    CUSTOM_COUNTER_NOLABEL.inc(float(number))
    return {"msg": f"count {number}"}

```

### Additionally must include those environment variable when using multiprocess mode
```
PROMETHEUS_MULTIPROC_DIR=./prometheus_multiproc/ (folder for multiprocess metrics)
```
> **Note:** only include variable **PROMETHEUS_MULTIPROC_DIR** when use multiprocess otherwise don't

### In case of using gunicorn, gunicorn.config.py file must include
in order to make multiprocess work
```Python
import os

from pathlib import Path
from multiprocessing import cpu_count
from os import environ
from prometheus_client import multiprocess
from thinknet_observer import clear_multiproc_dir

def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)

def max_workers():    
    return cpu_count()

clear_multiproc_dir()

```