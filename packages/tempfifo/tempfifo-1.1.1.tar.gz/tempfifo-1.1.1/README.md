# tempfifo

This module creates temporary named pipes

## Installation

```sh
pip3 install tempfifo
```
or
```sh
pip3 install --user tempfifo
```

## Example

A `NamedTemporaryFIFO` class is provided and is intended to be used as a
context manager. The filename of the created pipe is accessible as its `name`
attribute. For example:

```python
from tempfifo import NamedTemporaryFIFO
with NamedTemporaryFIFO() as ntf:
    print(ntf.name)
```
