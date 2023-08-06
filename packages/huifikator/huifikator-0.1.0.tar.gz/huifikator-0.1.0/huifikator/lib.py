import re

HUIFY_TABLE = {
    'е': 'е',
    'о': 'е',
    'и': 'и',
    'а': 'я',
    'ы': 'и',
    'у': 'ю',
    'і': 'ї',
    'ё': 'е',

    'ю': 'ю',
    'я': 'я'
}

RUSSIAN = re.compile(r'[А-я]+|[їіё]+')


def reduplicate_text(text: str, include_original=True):
    result = []

    for line in text.split("\n"):
        if len(result) > 0:
            result.append("\n")

        for word in line.split(" "):
            if len(word) <= 1:
                result.append(word)
                continue

            idx = next((idx for idx, ch in enumerate(word) if ch.lower() in HUIFY_TABLE), None)

            if idx is None or word[idx].lower() not in HUIFY_TABLE:
                result.append(word)
                continue

            diphthong = HUIFY_TABLE[word[idx].lower()]
            plain_word = "".join(RUSSIAN.findall(word))

            appendix = f"ху{diphthong + word[idx + 1:]}"
            if word.isupper():
                appendix = appendix.upper()

            if include_original:
                result.append(plain_word + "-" + appendix)
            else:
                result.append(appendix)

    return " ".join(result)
