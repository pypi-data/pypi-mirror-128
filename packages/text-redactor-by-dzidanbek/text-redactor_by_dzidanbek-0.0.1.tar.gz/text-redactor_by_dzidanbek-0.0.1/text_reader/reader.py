def read_file(file):
   text = open(file).read()
   return text


def word_search(file, word):
    text = open(file).read()
    for line in text:
        for key in line.split():
            if (word) in (key):
                print("Success)")
            else:
                print("Word is missing(")


def text_data(text: str) -> dict:
    words_count = len(text.split())
    symbol_count = len(text)
    symbol_count_without_w = len(text.replace(" ", ""))
    sentences_list = text.split(".")
    sentences_count = len(text.split("."))
    if sentences_list[-1] == '':
        sentences_count -= 1
    return {
        "words_count": words_count,
        "symbol_count": symbol_count,
        "without_whitespace": symbol_count_without_w,
        "sentences_count": sentences_count
    }


# text = read_file("example.TXT")
# data = text_data(text)

# print(data)

