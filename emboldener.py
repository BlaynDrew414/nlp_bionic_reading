import spacy

nlp = spacy.load("en_core_web_sm")

def calculate_bold_level(word):
    length = sum(1 for char in word if char.isalpha())
    
    if length <= 3:
        return 1
    elif length <= 5:
        return 2
    elif length == 6:
        return 3
    elif length <= 9:
        return 4
    else:
        return 5

def embolden_based_on_length(text):
    doc = nlp(text)
    emboldened_words = []

    for token in doc:
        if token.is_alpha:
            bold_level = calculate_bold_level(token.text)
            emboldened_word = token.text[:bold_level].upper() + token.text[bold_level:]
            emboldened_words.append(emboldened_word)
        else:
            emboldened_words.append(token.text)

    emboldened_text = ' '.join(emboldened_words)
    return emboldened_text