import spacy

from emboldener import embolden_based_on_length

def main():
    with open('data/sample_text.txt', 'r') as file:
        content = file.read()

    examples = content.split('== Example')[1:]

    for i, example in enumerate(examples, start=1):
        print(f"Example {i}:")
        emboldened_text = embolden_based_on_length(example.strip())
        print(emboldened_text)
        print()

if __name__ == "__main__":
    main()
