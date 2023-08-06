from os import read


def read_file(f):
    file_text = open(f).read()
    return file_text


def read_data(text):
    # Переделывает строку в массив(split)
    word_count = len(text.split())
    sen_list = text.split('.')
    sentence_count = len(text.split('.'))
    if sen_list[-1] == '':
        sentence_count = - 1
    return {
        "word_count": word_count,
        "sentence_count": sentence_count
    }


def del_superfluou(text):
    superfluou_list = ['.', ',', ':', ';', '(', ')']
    for i in superfluou_list:
        text = text.replace(i, "")
    return text


def word_finding(text: str, word: str) -> dict:
    result_text = del_superfluou(text).split()
    words_count = result_text.count(word)
    index_list = [index for index, item_word in enumerate(
        result_text) if word == item_word]

    return {
        "count": words_count,
        "words_indexes": index_list
    }
