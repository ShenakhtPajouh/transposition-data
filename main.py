from utils import get_paragraph_words
from utils import make_transposition_pair_dataset
from utils import write_tsv

if __name__ == '__main__':
    paragraphs = get_paragraph_words(500, 20, 60, 3, tags=[[0, 1, 2]])
    train_data, validation_data = make_transposition_pair_dataset(
        paragraphs, 128)

    write_tsv(train_data, 'train.tsv')
    write_tsv(validation_data, 'dev.tsv')
