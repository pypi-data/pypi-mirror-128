# time_profiler

This is a Python module for profiling a function's time usage. It's quite useful for determining how long a function will take to execute.

# Installation

Install via pip:

```
pip install timer
```

# Usage

First decorate the function you would like to profile with **@timer()** and then run that file containing function.

In the following example, we create a simple function called **sample_func** that allocates lists a, b and then deletes b:

```
from time_profiler import timer

@timer()
def sample_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    
    return a

if __name__ == '__main__':
    sample_func()
```

Then execute the code normally. For example, if the file name was *example.py*, this would result in:

```
python example.py
```

Output will be displayed in the terminal as follow:

```
11-24-2021 10:07:05 AM - timer - INFO - sample_func function ran in 0.10 secs
```

# Parameters

This decorator(@timer()) takes two optional paramaters.
- file_log: By default is set to false, which means that log file is not created but when set to true there should be a log file named **timer.log**. Breifly this argument is of boelen type.

- exp_time: Here you can try to estimate the time to be used. When estimated time is less than actual used time, you get warning log instead of info.

# Development

Latest sources are available from github:

> [https://github.com/harerakalex/timer](https://github.com/harerakalex/timer)

# Author

Carlos Harerimana

# License

MIT
