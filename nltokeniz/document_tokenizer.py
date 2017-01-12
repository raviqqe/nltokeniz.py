import nltk
import MeCab


__all__ = ["DocumentTokenizer"]


japanese_tagger = MeCab.Tagger()
japanese_tagger.parse("")  # prevent UnicodeDecodeError
japanese_sentence_tokenizer \
    = nltk.RegexpTokenizer("[^{0}]+(?:[{0}]+|$)".format("!?.！？。．"))


def sentence_to_words_in_japanese(sentence):
    node = japanese_tagger.parseToNode(sentence)
    while node != None:
        if node.surface != "":
            yield node.surface
        node = node.next


class DocumentTokenizer:

    def __init__(self, language):
        self._language = language

    def tokenize(self, document):
        return {
            "english": self._tokenize_in_english,
            "japanese": self._tokenize_in_japanese,
        }[self._language](document)

    def _tokenize_in_english(self, document):
        return [nltk.tokenize.word_tokenize(sentence.strip())
                for sentence in nltk.tokenize.sent_tokenize(document.strip())]

    def _tokenize_in_japanese(self, document):
        return [list(sentence_to_words_in_japanese(sentence.strip()))
                for sentence
                in japanese_sentence_tokenizer.tokenize(document.strip())]
