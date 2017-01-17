import iso639
import langdetect
import nltk
import MeCab


__all__ = ['tokenize']


def tokenize(document, language=None):
    if language is not None and not iso639.is_valid639_1(language):
        raise ValueError('"{}" is not a valid ISO 639-1 code.'
                         .format(language))

    return {
        'en': tokenize_english,
        'ja': tokenize_japanese,
    }[language or langdetect.detect(document)](document)


def tokenize_english(document):
    return [nltk.tokenize.word_tokenize(sentence.strip())
            for sentence in nltk.tokenize.sent_tokenize(document.strip())]


def tokenize_japanese(document):
    sentence_tokenizer = nltk.RegexpTokenizer(
        '[^{0}]+(?:[{0}]+|$)'.format('!?.！？。．'))

    return [list(sentence_to_words_in_japanese(sentence.strip()))
            for sentence
            in sentence_tokenizer.tokenize(document.strip())]


def sentence_to_words_in_japanese(sentence):
    tagger = MeCab.Tagger()
    tagger.parse('')  # prevent UnicodeDecodeError

    node = tagger.parseToNode(sentence)

    while node != None:
        if node.surface != '':
            yield node.surface

        node = node.next

    raise StopIteration()  # Need to be done manually somehow
