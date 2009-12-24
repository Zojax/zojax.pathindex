==========
Path index
==========

The PathIndex is an index that index object by it's traversal path

    >>> from zojax.pathindex.index import PathIndex
    >>> index = PathIndex()
    >>> index.documentCount()
    0
    >>> index.wordCount()
    0
    >>> index.maxValue() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError:...
    >>> index.minValue() # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ValueError:...
    >>> list(index.values())
    []
    >>> len(index.apply({'any_of': (root,)}))
    0

We can index traversable object

    >>> data = {1: root,
    ...         2: root['folder1'],
    ...         3: root['folder1']['folder1_1'],
    ...         4: root['folder1']['folder1_1']['folder1_1_1'],
    ...         5: root['folder2'],
    ...         6: root['folder2']['folder2_2'],
    ...         7: root['folder2']['folder2_2']['folder2_2_2']
    ... }

    >>> for k, v in data.items():
    ...     index.index_doc(k, v)


After indexing, the statistics and values match the newly entered content.

    >>> len(list(index.values()))
    5
    >>> index.documentCount()
    6
    >>> index.wordCount()
    5
    >>> list(index.ids())
    [2, 3, 4, 5, 6, 7]

The index supports five types of query but only 'any_of' is usefulle
for PathIndex.  The first is 'any_of'.  It
takes an iterable of values, and returns an iterable of document ids that
contain any of the values.  The results are weighted.

    >>> list(index.apply({'any_of':(root['folder1'],)}))
    [3, 4]

    >>> list(index.apply({'any_of':(root['folder1']['folder1_1'],)}))
    [4]

    >>> list(index.apply({'any_of':(root['folder2'],)}))
    [6, 7]

    >>> list(index.apply({'any_of':(root['folder1'], root['folder2'],)}))
    [3, 4, 6, 7]

    >>> list(index.apply({'any_of':(
    ...   root['folder1'], root['folder1']['folder1_1'], root['folder2'],)}))
    [3, 4, 6, 7]

    >>> print index.apply({'all_of': (root,)})
    None

    >>> print index.apply({'between': (root,)})
    None

    >>> list(index.apply({'any': None}))
    [2, 3, 4, 5, 6, 7]

We can't index value that doesn't have parents

    >>> index.index_doc(100, 'string')
    >>> index.apply({'any_of': ('string',)}) is None
    True
