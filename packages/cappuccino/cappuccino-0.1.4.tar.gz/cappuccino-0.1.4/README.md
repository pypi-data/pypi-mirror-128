# Java Garbage Collection parser written in Python
[![PyPI Latest Release](https://img.shields.io/pypi/v/cappucino.svg)](https://pypi.org/project/cappucino/)

## What is it?


**cappuccino** is a Python package that provides a way of parsing Java Garbage Collection Logs.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/vidigalp/cappuccino


Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/cappuccino).

```sh
# or PyPI
pip install cappuccino
```

## How to Run

```python
python cappuccino <input_directory>

gc_log1.log: 100%|██████████| 93842/93842 [00:00<00:00, 146317.63it/s]
gc_log2.log: 100%|██████████| 89468/89468 [00:00<00:00, 147814.29it/s]
gc_log3.log: 100%|██████████| 84950/84950 [00:00<00:00, 148095.09it/s]
gc_log4.log: 100%|██████████| 89549/89549 [00:00<00:00, 147173.26it/s]
gc_log5.log: 100%|██████████| 86187/86187 [00:00<00:00, 147973.24it/s]
                           count      mean       std   min   25%    50%  \
pause_type                                                                
G1 Evacuation Pause      16348.0  0.040432  0.141196  0.00  0.01  0.020   
G1 Humongous Allocation     34.0  0.228824  0.394222  0.03  0.07  0.105   
GCLocker Initiated GC        1.0  0.040000       NaN  0.04  0.04  0.040   
Metadata GC Threshold       15.0  0.024667  0.010601  0.01  0.02  0.020   

                           75%   max  
pause_type                            
G1 Evacuation Pause      0.030  4.58  
G1 Humongous Allocation  0.200  1.74  
GCLocker Initiated GC    0.040  0.04  
Metadata GC Threshold    0.035  0.04  

```

## Dependencies
- [Pandas - pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.](https://pandas.pydata.org)
- [NumPy - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate on these arrays](https://www.numpy.org)
- [python-dateutil - Provides powerful extensions to the standard datetime module](https://dateutil.readthedocs.io/en/stable/index.html)
- [pytz - Brings the Olson tz database into Python which allows accurate and cross platform timezone calculations](https://github.com/stub42/pytz)
- [Click - Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.](https://click.palletsprojects.com/)
- [tqdm - Instantly make your loops show a smart progress meter - just wrap any iterable with tqdm(iterable), and you're done!](https://tqdm.github.io)

