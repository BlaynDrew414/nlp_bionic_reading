
async function loadPyodideAndConvert() {
    await languagePluginLoader;

    const pythonCode = `
       

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
    `;

    const inputText = document.getElementById('inputText');
    const emboldenButton = document.getElementById('emboldenButton');
    const emboldenedText = document.getElementById('emboldenedText');

    const example1Button = document.getElementById('example1Button');
    const example2Button = document.getElementById('example2Button');

    example1Button.addEventListener('click', () => {
        inputText.value = "Bionic Reading redefines reading by highlighting the initial letters...";
    });

    example2Button.addEventListener('click', () => {
        inputText.value = "It is a truth universally acknowledged, that a single man...";
    });

    emboldenButton.addEventListener('click', () => {
        const input = inputText.value;
        const emboldened = emboldenText(input);
        emboldenedText.textContent = emboldened;
    });
}

loadPyodideAndConvert();