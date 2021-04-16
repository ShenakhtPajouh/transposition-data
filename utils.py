from gutenberg_API.API import get_paragraphs
from random import shuffle
import csv
from typing import List, Optional, Tuple


def filter(paragraphs: List[Tuple],
           max_len: int = 512,
           min_len: int = 10,
           max_sent: int = 60,
           min_sent: int = 3) -> List[Tuple]:
    """
    desc: removes tuples with at least one paragraph not satisfying following conditions:
          1. min_len <= words in the paragraph <= max_len
          2. min_sent <= sentences in the paragraph <= max_sent

    :param paragraphs: a list of tuples of consecutive paragraphs
    :param max_len: maximum number words in a paragraph
    :param min_len: minimum number of words in a paragraph
    :param max_sent: maximum number of sentences in a paragraph
    :param min_sent: minimum number of sentences in a paragraph

    :return: ret: list with tuples not satisfying the conditions removed
    """

    ret = []

    for tuple in paragraphs:
        flag = False
        for seq in tuple:
            world_len = len(seq.text(format="words"))
            sen_len = len(seq.text(format="sentences"))
            if world_len > max_len or world_len < min_len or sen_len > max_sent or sen_len < min_sent:
                flag = True

        if not flag:
            ret.append(tuple)

    return ret


def get_paragraph_words(max_len: int = 512,
                        min_len: int = 10,
                        max_sent: int = 60,
                        min_sent: int = 3,
                        paragraph_id: Optional[List] = None,
                        books: Optional[List] = None,
                        tags: Optional[List] = None,
                        num_sequential: int = 2,
                        shuffle: bool = True) -> List[List]:
    """
    :param max_len: (Optional) integer. maximum number of words in a paragraph
    :param min_len: (Optional) integer. minimum number of words in a paragraph
    :param max_sent: (Optional) integer. maximum number of sentences in a paragraph
    :param min_sent: (Optional) integer. minimum number of sentences in a paragraph
    :param paragraph_id: (Optional) a list of ints
    :param books: (Optional) a list of books id or GutenbergBooks
    :param tags: (Optional) a list of tags. if an element of list is a set,
                 list or ... it means the tag should be at least one of those tags. for instance tags = [3, [4, 5]]
                 means that paragraphs with tag 3 and 4 or 5
    :param num_sequential: (Optional) integer. the number of sequential paragraphs
    :param shuffle: (Optional) boolean. whether the output be shuffled or not

    :return: a list of lists of num_sequential consecutive paragraphs satisfying the conditions in which
             each paragraph is a list of words
    """

    paragraphs = get_paragraphs(paragraph_id=paragraph_id,
                                books=books,
                                tags=tags,
                                num_sequential=num_sequential)

    paragraphs = filter(paragraphs, max_len, min_len, max_sent, min_sent)

    ret = []
    for tuple in paragraphs:
        ret.append([p.text("words") for p in tuple])

    if shuffle:
        shuffle(ret)

    return ret


def make_transposition_pair_dataset(
        paragraphs: list[Tuple],
        num_tokens: Optional[int] = None,
        validation_split: float = 0.1) -> Tuple[List]:
    """
    desc: makes dataset of paragraphs in which each example is a list of :
            [label, first paragraph ID, second paragraph ID, first paragraph text, second paragraph text]

          here label indicates whether the first paragraph are in correct order or not: if it is 1, then the order
          is correct, otherwise it is 0. for each pair of paragraphs x and y in which x is before y, the dataset will
          (x , y) with label 1 and (y , x) with label 0.

          if paragraphs are too long for the task, we can have num_tokens tokens at the end of the first paragraph
          and num_tokens tokens at the beginning of the second paragraph


    :param paragraphs: list of tuples of two consecutive paragraphs in which each paragraph is a list of its words
    :param num_tokens: integer. number of tokens of each paragraph we want to be included. if its None, then all tokens of each
           paragraph will be included.
    :param validation_split:  float between 0,1. Fraction of the training data to be used as validation data.

    :return: train_data: a list containing strings. each string is a train example like what mentioned above.
             validation_data: a list containing strings. each string is a validation example like what mentioned above
    """

    all_pairs = []
    num = len(paragraphs)

    # here paragraph IDs for the first paragraphs will be index of their pair in the input paragraphs and
    # for the second paragraphs will be number of examples + index of their pair in the input paragraphs
    # paragraph IDs could also be their IDs in gutenberg API

    for i, (x, y) in enumerate(paragraphs):
        if (num_tokens is not None):
            all_pairs.append([
                "1",
                str(i),
                str(i + num), " ".join(x[max(0,
                                             len(x) - num_tokens):len(x)]),
                " ".join(y[:min(len(y), num_tokens)])
            ])

            all_pairs.append([
                "0",
                str(num + i),
                str(i), " ".join(y[max(0,
                                       len(y) - num_tokens):len(y)]),
                " ".join(x[:min(len(x), num_tokens)])
            ])
        else:
            all_pairs.append(
                ["1", str(i),
                 str(i + num), " ".join(x), " ".join(y)])
            all_pairs.append(
                ["0", str(num + i),
                 str(i), " ".join(y), " ".join(x)])

    shuffle(all_pairs)

    train_data = all_pairs[:int(len(all_pairs) * (1 - validation_split))]
    validation_data = all_pairs[int(len(all_pairs) * (1 - validation_split)):]

    return train_data, validation_data


def write_tsv(data, data_path: str):
    with open(data_path, 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        for example in data:
            writer.writerow(example)
