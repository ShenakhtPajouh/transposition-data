from collections import defaultdict


class Paragraph(object):
    def __init__(self, text, id=None, book_id=None, next_id=None, prev_id=None, tags=set()):
        if id is not None:
            assert isinstance(id, int)
            assert id > 0
        if book_id is not None:
            assert isinstance(book_id, int)
            assert book_id > 0
        if next_id is not None:
            assert isinstance(next_id, int)
            assert next_id > 0
        if prev_id is not None:
            assert isinstance(prev_id, int)
            assert prev_id > 0
        assert isinstance(tags, set)
        assert isinstance(text, list)
        assert all([isinstance(sent, list) for sent in text])
        assert all([all([isinstance(word, str) for word in sent]) for sent in text])
        self._id = id
        self._text = text
        self._book_id = book_id
        self._tags = tags
        self._next_id = next_id
        self._prev_id = prev_id

    @property
    def id(self):
        return self._id

    @property
    def has_book(self):
        return self._book_id is not None

    @property
    def book_id(self):
        return self._book_id

    @property
    def next_id(self):
        return self._next_id

    @next_id.setter
    def next_id(self, next_id):
        if next_id is not None:
            assert isinstance(next_id, int)
            assert next_id > 0
            self._next_id = next_id

    @property
    def prev_id(self):
        return self._prev_id

    @prev_id.setter
    def prev_id(self, prev_id):
        if prev_id is not None:
            assert isinstance(prev_id, int)
            assert prev_id > 0
            self._prev_id = prev_id

    @property
    def tags(self):
        return self._tags.copy()

    def add_tag(self, new_tags):
        if isinstance(new_tags, int):
            new_tags = {new_tags}
        self._tags = self._tags | set(new_tags)

    @property
    def metadata(self):
        return paragraph_metadata(self.id, self.book_id, self.prev_id, self.next_id, self.tags)

    def text(self, format="sentences", lowercase=False):
        """

        Return the text of Paragraphs

        Args:
            format: if it is "sentences" then the output will be a list of lists each list contain the tokens of a sentence.
                    if it is "words" then the output will be the list of tokens.
                    if it is "text" then the output will be a string; the text of paragraph
            lowercase: a boolean. if it is true then the output will be lowercase

        Returns:
            depend on format, a list of strings, a list of lists of strings or a string

        """
        if format == "sentences":
            if lowercase:
                return [[word.lower() for word in sent] for sent in self._text]
            else:
                return [[word for word in sent] for sent in self._text]
        elif format == "words":
            words = sum([sent for sent in self._text], [])
            if lowercase:
                return [word.lower() for word in words]
            else:
                return words
        elif format == "text":
            words = sum([sent for sent in self._text], [])
            text = " ".join(words)
            if lowercase:
                return text.lowercase()
            else:
                return text
        else:
            raise ValueError('format should be one of ["sentences", "words", "text"]')


def create_paragraphs(paragraph_metadata, paragraph_text):
    assert set(paragraph_metadata) == set(paragraph_text)
    pars = []
    for i, met in paragraph_metadata.items():
        mt = defaultdict(lambda : None, met)
        if "tags" not in met:
            tags = dict()
        else:
            tags = met["tags"]
        par = Paragraph(text=paragraph_text[i], id=mt["id"], book_id=mt["book_id"], next_id=mt["next_id"],
                        prev_id=mt["prev_id"], tags=tags)
        pars.append((i, par))
    return dict(pars)


def paragraph_metadata(id=None, book_id=None, prev_id=None, next_id=None, tags=None):
    """

    A helper for creating metadata

    Args:
        id, book_id, prev_id, next_id, are integers. tags is either integer or list, set and ... of integers.
        if one of them is None, it will be ignored in return

    Returns:
         a dictionary of metadata form for a book with keys which are given

    """
    res = dict()

    x = id
    name = "id"
    if x is not None:
        if not isinstance(x, int):
            raise TypeError()
        res[name] = x

    x = book_id
    name = "book_id"
    if x is not None:
        if not isinstance(x, int):
            raise TypeError()
        res[name] = x

    x = prev_id
    name = "prev_id"
    if x is not None:
        if not isinstance(x, int):
            raise TypeError()
        res[name] = x

    x = next_id
    name = "next_id"
    if x is not None:
        if not isinstance(x, int):
            raise TypeError()
        res[name] = x

    x = tags
    name = "tags"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)

    return res



