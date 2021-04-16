import HP
import pickle
import os
from gutenberg_book import *
from paragraph import *


def get_books(books_list=None, books_features=None, book_object=True):
    """

    Args:
        books_list: (Optional) list of books gutenberg ID to create books. if it is None then it will return all books.
        books_features: (Optional) features to get books with that feature. a dictionary which values are set or list.
        book_object: if it is True then returns GutenbergBooks else it will return metadata

    Returns:
         a dictionary of books objects {id: GutenbergBook(id)/metadata(id)}
    """
    if books_list is not None and books_features is not None:
        raise AttributeError(
            "only one of books_list and books_features should be identified")
    if os.path.isfile(HP.BOOKS_DATA_PATH):
        pk = open(HP.BOOKS_DATA_PATH, "rb")
        books_metadata = pickle.load(pk)
        pk.close()
        assert isinstance(books_metadata, dict)

    else:
        books_metadata = dict()

    if books_list is not None:
        books_list = books_list & set(books_metadata)
        books_metadata = {id: books_metadata[id] for id in books_list}
    if books_features is not None:
        for feature, items in books_features.items():
            books_metadata = {
                id: metadata
                for id, metadata in books_metadata.items()
                if items.issubset(metadata[feature])
            }
    if book_object:
        return create_gutenberg_books(books_metadata, dic=True)
    return books_metadata


def get_bookshelves(bookshelves_list=None):
    """

    Args:
        bookshelves_list: (Optional) list of bookshelves to return. if it is None then it will return all bookshelves

    Returns:
        a dictionary of bookshelves {bookshelf: bookshelf_elements_id}

    """
    if os.path.isfile(HP.BOOK_SHELVES_PATH):
        pk = open(HP.BOOK_SHELVES_PATH, "rb")
        bookshelves = pickle.load(pk)
        pk.close()
        assert isinstance(bookshelves, dict)
        if bookshelves_list is not None:
            bookshelves_list = bookshelves_list & set(bookshelves)
            bookshelves = {
                bookshelf: bookshelves[bookshelf]
                for bookshelf in bookshelves_list
            }
    else:
        bookshelves = dict()
    return bookshelves


def get_paragraphs(paragraph_id=None,
                   books=None,
                   tags=None,
                   num_sequential=1,
                   paragraph_object=True,
                   lowercase=False):
    """

    Get paragraphs from args.

    Args:
        paragraph_id: (Optional) a list of ints
        books: (Optional) a list of books id or GutenbergBooks
        tags: (Optional) a list of tags. if an element of list is a set,
              list or ... it means the tag should be at least one of those tags. for instance tags = [3, {4, 5}]
              means that paragraphs with tag 3 and 4 or 5
        num_sequential: the number of sequential paragraphs
        paragraph_object: if it is True outputs will be type of Paragraph
        lowercase: if it is True, then the output will be lowercase. it does not have effect if paragraph_object=True.

    Returns:
        a list of paragraphs or list of tuples of paragraphs if num_sequential > 1

    """
    if paragraph_id is not None and (books is not None or tags is not None):
        raise ValueError(
            "if paragraph_id is given, books and tags can't be accepted.")
    with open(HP.PARAGRAPH_METADATA_PATH, "rb") as pkl:
        met_data = pickle.load(pkl)
    with open(HP.PARAGRAPH_DATA_PATH, "rb") as pkl:
        text = pickle.load(pkl, encoding='latin1')
    pars = create_paragraphs(met_data, text)
    if paragraph_id is not None:
        pars = {i: par for i, par in pars.items() if par.id in paragraph_id}
    if books is not None:
        books = {i for i in books if isinstance(i, int)} | {
            book.id for book in books if isinstance(book, GutenbergBook)
        }
        pars = {i: par for i, par in pars.items() if par.book_id in books}
    if tags is not None:
        tags = [{tag} for tag in tags if isinstance(tag, int)
               ] + [set(tag) for tag in tags if not isinstance(tag, int)]
        pars = {
            i: par
            for i, par in pars.items()
            if all([not par.tags.isdisjoint(tag) for tag in tags])
        }

    if num_sequential == 1:
        if paragraph_object:
            return list(pars.values())
        else:
            return [par.text(lowercase=lowercase) for par in pars.values()]
    elif num_sequential > 1:
        pars2 = []
        for par in pars.values():
            pp = [par]
            next_par = par
            flag = True
            for k in range(1, num_sequential):
                cur_par = next_par
                id = cur_par.next_id
                if id not in pars:
                    flag = False
                    break
                next_par = pars[id]
                pp.append(next_par)
            if flag:
                pars2.append(tuple(pp))
        if paragraph_object:
            return pars2
        else:
            return [
                tuple(par.text(lowercase=lowercase)
                      for par in pt)
                for pt in pars2
            ]
    else:
        raise ValueError("num_sequential most be positive")
