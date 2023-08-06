map_as_object
==========

Sometimes, you want to define an oject without an class. Thus 
this package allows you to define an object via a map of its 
attributes:

```python
m = as_object({'a': 1})
assert m.a == 1
```

You can even assign lambdas in that way. 