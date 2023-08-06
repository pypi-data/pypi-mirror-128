

def read_file(file):
    file_text = open(file).read()
    return file_text


def read_data(text: str):
    words_count = len(text.split())
    symbol_count = len(text)
    without_whitespace = len(text.replace(" ", ""))
    sentence_count = len(text.split(".")[:-1])
    return {
        "words_count": words_count,
        "symbol_count": symbol_count,
        "without_whitespace": without_whitespace,
        "sentence_count": sentence_count,
    }


def change_text(text: str) -> list:
    changes_list = [",", ".", ";", ":"]
    for i in changes_list:
        text = text.replace(i, "")
    return text.split()


def words_counter(text: str, word) -> dict:
    result_text = change_text(text)
    words_counter = result_text.count(word)
    index_list = []
    for index, item in enumerate(result_text):
        if word == item:
            index_list.append(index)
    return {
        "count": words_counter,
        "indexes": index_list
    }


text = read_file("text.txt")
data = read_data(text)
words = words_counter(text, "text")
print(data)
print(words)
