class GutenbergBook(object):
    def __init__(self, id, metadata):
        """

        Args:
            id: the gutenberg ID
            metadata: metadata is a dictionary which includes ["title", "authors", "language", "bookshelves"]
        """
        if not isinstance(id, int):
            raise TypeError("id must be a positive integer")
        if id <= 0:
            raise TypeError("id must be a positive integer")
        self._id = id
        self._title = list(metadata["title"])[0]
        self._authors = metadata["authors"]
        self._language = list(metadata["language"])[0]
        self._bookshelves = metadata["bookshelves"]

    def __hash__(self):
        return hash(self._id)

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def authors(self):
        return self._authors.copy()

    @property
    def language(self):
        return self._language

    @property
    def bookshelves(self):
        return self._bookshelves.copy()

    @property
    def metadata(self):
        return book_metadata(self.id, self.title, self.authors, self.language, self.bookshelves)

    def add_bookshelf(self, shelf):
        if not isinstance(shelf, str):
            raise TypeError("shelf should be a string")
        self._bookshelves = self._bookshelves | {shelf}


def create_gutenberg_books(inputs, dic=False):
    """

    Create a list of GutenbergBook objects from gutenberg ids or a metadata

    Args:
        inputs: a dictionary including metadata for each gutenberg id {id: metadata(id)}
        dic: if True then the output will be in dictionary form {id: GutenbergBook(id)}

    Return:
        a set or dictionary of gutenberg books objects
    """
    if not isinstance(inputs, dict):
        raise TypeError("inputs must be a dictionary")
    res = {i: GutenbergBook(i, metadata) for i, metadata in inputs.items()}
    if dic:
        return res
    else:
        return set(res.values())


def book_metadata(id=None ,title=None, authors=None, language=None, bookshelves=None):
    """

    A helper for creating metadata

    Args:
        tittle, metdata, language and bookshelves are either string or simple list, set or ... of strings.
        if one of them is None, it will be ignored in return

    Returns:
         a dictionary of metadata form for a book with keys which are given

    """
    res = dict()

    x = id
    name = "id"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)

    x = title
    name = "title"
    if x is not None:
        if isinstance(x, str):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, str) for s in x])
            res[name] = set(x)

    x = authors
    name = "authors"
    if x is not None:
        if isinstance(x, str):
            res[name] = {x}
        else:
            assert len(x) >= 1
            assert all([isinstance(s, str) for s in x])
            res[name] = set(x)

    x = language
    name = "language"
    if x is not None:
        if isinstance(x, str):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, str) for s in x])
            res[name] = set(x)

    x = bookshelves
    name = "bookshelves"
    if x is not None:
        if isinstance(x, str):
            res[name] = {x}
        else:
            assert all([isinstance(s, str) for s in x])
            res[name] = set(x)
    return res






