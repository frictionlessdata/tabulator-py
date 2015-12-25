# Tutorial: How to Write a Processor

Processors is an essential Tabulator concept. Items emitted by loader-parser are processed by pipeline of processors added by user.

On every iteration every processor gets an `iterator` instance in a `process` call to modify the iteration headers or values, call skip, stop etc. A processor doesn't have to return anything:

```python
from tabulator import processors

class MyProcessor(processors.API):

    def process(self, iterator):
        # work with iterator

    def handle(self, iterator):
        # will be called on exception
```

Let's explore the iterator interface:

```
Iterator
    + skip()
    + stop()
    + index
    + count
    + keys
    + values [writable]
    + headers [writable before any data is emitted]
    + exception
```

Having this knowledge we can simply to write a processor to do the following things:

- skip any odd items
- process only 5 items
- multiply by two the second column values

```python
from tabulator import processors

class MyProcessor(processors.API):

    def process(self, iterator):
        # Skip
        if iterator.index % 2 == 0:
            iterator.skip()
        # Stop
        if iterator.index == 4:
            iterator.stop()
        # Multiply
        values = list(iterator.values)
        values[1] *= 2
        iterator.values = tuple(values)

    def handle(self, iterator):
        # will be called on exception
```
