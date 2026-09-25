def word_count(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

        removed_punctuation = text.replace(",", "").replace(".", "")
        return len(removed_punctuation.split())