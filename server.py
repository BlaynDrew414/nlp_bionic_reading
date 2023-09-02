import spacy
from flask import Flask, render_template, jsonify, request

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# Sample text data
sample_text = """
== Example 1: Improved Reading ==
Bionic Reading redefines reading by highlighting the initial letters of words, accelerating comprehension and speed. This visual method leverages your brain's innate ability to automatically complete familiar words. As you read, each word's start illuminates, guiding your eyes seamlessly and enhancing speed. Particularly beneficial for individuals with neurodivergencies like ADHD, this technique aids concentration. Bionic Reading revolutionizes reading, tapping into visual innovations to elevate comprehension and address unique needs.

== Example 2: From "Pride and Prejudice" by Jane Austen ==
"It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.

However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters.

"My dear Mr. Bennet," said his lady to him one day, "have you heard that Netherfield Park is let at last?"

Mr. Bennet replied that he had not.

"But it is," returned she; "for Mrs. Long has just been here, and she told me all about it."

Mr. Bennet made no answer.

"Do you not want to know who has taken it?" cried his wife impatiently.

"You want to tell me, and I have no objection to hearing it."

This was invitation enough.

"Why, my dear, you must know, Mrs. Long says that Netherfield is taken by a young man of large fortune from the north of England; that he came down on Monday in a chaise and four to see the place, and was so much delighted with it that he agreed with Mr. Morris immediately; that he is to take possession before Michaelmas, and some of his servants are to be in the house by the end of next week."
"""

# Parse the sample text into examples
def parse_example_text(content):
    examples = content.split('== Example')
    exampleTexts = {}

    for i in range(1, len(examples)):
        exampleParts = examples[i].split('==')
        exampleNumber = exampleParts[0].strip()
        exampleText = exampleParts[1].strip()
        exampleTexts[exampleNumber] = exampleText

    return exampleTexts

# Parse the sample text
exampleTexts = parse_example_text(sample_text)

def bionic_reading_logic(text):
    doc = nlp(text)
    emboldened_words = []

    for token in doc:
        if token.is_alpha:
            length = len(token.text)  # Use spaCy to check word length

            if length <= 3:
                emboldened_word = f'<span style="font-weight: bold;">{token.text}</span>'
            else:
                emboldened_word = token.text

            emboldened_words.append(emboldened_word)
        else:
            emboldened_words.append(token.text)

    emboldened_text = ' '.join(emboldened_words)
    return emboldened_text

@app.route('/')
def index():
    initial_example = "Example 1"
    initial_example_text = exampleTexts.get(initial_example, "")
    initial_example_text_bionic = bionic_reading_logic(initial_example_text)
    return render_template('index.html', exampleTexts=exampleTexts, sampleText=initial_example_text, emboldenedText=initial_example_text_bionic)

def embolden_text_logic(input_text):
    doc = nlp(input_text)
    emboldened_words = []

    for token in doc:
        if token.is_alpha:
            length = sum(1 for char in token.text if char.isalpha())

            if length <= 3:
                emboldened_word = "<b>" + token.text[0] + "</b>" + token.text[1:]
            elif length <= 5:
                emboldened_word = "<b>" + token.text[:2] + "</b>" + token.text[2:]
            elif length <= 7:
                emboldened_word = "<b>" + token.text[:3] + "</b>" + token.text[3:]
            elif length <= 9:
                emboldened_word = "<b>" + token.text[:4] + "</b>" + token.text[4:]
            else:
                emboldened_word = "<b>" + token.text[:5] + "</b>" + token.text[5:]

            emboldened_words.append(emboldened_word)
        else:
            emboldened_words.append(token.text)

    emboldened_text = ' '.join(emboldened_words)
    return emboldened_text

@app.route('/embolden-text', methods=['POST'])
def embolden_text():
    input_text = request.json.get('inputText', '')
    emboldened_text = embolden_text_logic(input_text)
    
    return jsonify({"inputText": input_text, "emboldenedText": emboldened_text})

@app.route('/embolden/<example_number>')
def embolden_example(example_number):
    example_text = exampleTexts.get(example_number, "")
    emboldened_text = embolden_text_logic(example_text)
    
    return jsonify({"sampleText": example_text, "emboldenedText": emboldened_text})

if __name__ == '__main__':
    app.run(debug=True)
