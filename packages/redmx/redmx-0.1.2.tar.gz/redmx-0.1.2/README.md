# redmx

[![CI](https://github.com/locp/redmx/actions/workflows/ci.yml/badge.svg?event=push)](https://github.com/locp/redmx/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/redmx/badge/?version=latest)](https://redmx.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/redmx.svg)](https://badge.fury.io/py/redmx)

Rate, Errors and Duration Metrics

## Basic Example

```python
import time
from redmx import RateErrorDuration
metrics = RateErrorDuration()
time.sleep(1)
metrics.increment_count(1)
metrics.increment_count(1)
metrics.rate()
print(metrics)
```

Will produce the following output:

`rate = 1.9904 tps, errors = 0 in 2 (0.0%), duration = 502.4475 milliseconds per transaction.
`


For full documentation please go to https://redmx.readthedocs.io/en/latest/
