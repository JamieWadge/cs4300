#Gets the word count of file
def word_count(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

        #Removes , and . since they were being counted as words due to spaces in text
        removed_punctuation = text.replace(",", "").replace(".", "")
        return len(removed_punctuation.split())

print("Word count is:", word_count("task6_read_me.txt"))