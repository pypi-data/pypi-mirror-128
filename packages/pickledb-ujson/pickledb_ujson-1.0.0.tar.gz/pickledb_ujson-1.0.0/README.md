![Download badge](http://pepy.tech/badge/pickledb_ujson)

# pickleDB
pickleDB is lightweight, fast, and simple database based on the
[ujson](https://github.com/ultrajson/ultrajson) module.
And it's BSD licensed!


## pickleDB is Fun
```python
>>> import pickledb

>>> db = pickledb.load('test.db', False)

>>> db.set('key', 'value')

>>> db.get('key')
'value'

>>> db.dump()
True
```

## Easy to Install
```python
$ pip install pickledb
```

## Links
* [website](https://patx.github.io/pickledb)
* [documentation](https://patx.github.io/pickledb/commands.html)
* [pypi](http://pypi.python.org/pypi/pickleDB)
* [github repo](https://github.com/patx/pickledb)


## Latest Release Notes (version: 1.0.0)
* Use ujson instead of json
