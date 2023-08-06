pipeline
========

This package is inspired by Elixirs pipelines. You can define an interable 
of callables and define them as pieline. The second element then gets the 
result of the first element and so on. 

Example
-------

Say you have some callables (see `test/test_pipeline.py`):

```python

def add_age(item):
    item.age = 22
    return item

def add_name(name):
    def fun(item):
        item.name = name
        return item
    return fun

class AddHeight:

    def __init__(self, height):
        self.height = height

    def __call__(self, item):
        item.height = 192
        return item
```

Then you can compose them to a pipeline:

```python
def some_name(arg):
    return pipeline(
        arg,
        add_age,
        inspect,
        add_name('Tom'),
        inspect(print),
        AddHeight(192),
    )
```

And use it as one:

```python
class Plain:
    pass

plain_obj = Plain()
res = some_name(plain_obj)

assert res.age == 22
assert res.name == 'Tom'
assert res.height == 192
```

Inspect
-------

For debugging, it is quite useful to inspect the intermediate result
between two steps in the pipeline. This is easy with `inspect`:

```python
def some_name(arg):
    return pipeline(
        arg,
        add_age,
        inspect,
        add_name('Tom'),
        inspect(print),
        AddHeight(192),
    )
```

Note that you can just use inspect, which usese `pprint` as default 
printer or pass a custom method in to print.