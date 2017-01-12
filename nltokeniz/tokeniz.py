import nltk
import MeCab


__all__ = ["tokenize"]


def tokenize(document, language="english"):
    tokenizers = {
        "english": tokenize_in_english,
        "japanese": tokenize_in_japanese,
    }

    if language not in tokenizers:
        raise ValueError("The language, {} is not supported.".format(language))

    return tokenizers[language](document)


def tokenize_in_english(document):
    return [nltk.tokenize.word_tokenize(sentence.strip())
            for sentence in nltk.tokenize.sent_tokenize(document.strip())]


def tokenize_in_japanese(document):
    sentence_tokenizer = nltk.RegexpTokenizer(
        "[^{0}]+(?:[{0}]+|$)".format("!?.！？。．"))

    return [list(sentence_to_words_in_japanese(sentence.strip()))
            for sentence
            in sentence_tokenizer.tokenize(document.strip())]


def sentence_to_words_in_japanese(sentence):
    tagger = MeCab.Tagger()
    tagger.parse('')  # prevent UnicodeDecodeError

    node = tagger.parseToNode(sentence)

    while node != None:
        if node.surface != "":
            yield node.surface

        node = node.next

    raise StopIteration()  # Need to be done manually somehow
