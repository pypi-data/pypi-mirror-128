Safe
====

This is quite a simple package. It catches all exceptions within a given 
callable and returns None, if they occur and the return-value of the 
callable if not.

```python

def boom():
    raise Exception()
    return 1

def non_boom():
    return 2

a = safe(lambda: boom())
b = safe(lambda: non_boom())

assert a == None
assert b == 2
```