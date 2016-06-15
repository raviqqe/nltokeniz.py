#!/usr/bin/env python

import argparse
import json
import multiprocessing
import nltk
import re
import sys
import MeCab



japanese_tagger = MeCab.Tagger()
japanese_tagger.parse("") # prevent UnicodeDecodeError
japanese_sentence_tokenizer \
    = nltk.RegexpTokenizer("[^{0}]+[{0}]+".format("!?.！？。．"))



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
      "english" : self._tokenize_in_english,
      "japanese": self._tokenize_in_japanese,
    }[self._language](document)

  def _tokenize_in_english(self, document):
    return [nltk.tokenize.word_tokenize(sentence)
            for sentence in nltk.tokenize.sent_tokenize(document)]

  def _tokenize_in_japanese(self, document):
    return [list(sentence_to_words_in_japanese(sentence))
            for sentence in japanese_sentence_tokenizer.tokenize(document)]


def tokenize_documents(documents, language):
  return multiprocessing.Pool().map(DocumentTokenizer(language).tokenize,
                                    documents)


def print_as_json(obj):
  print(json.dumps(obj, indent="\t"))


def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("document_file",
                          type=argparse.FileType(),
                          default=sys.stdin)
  arg_parser.add_argument("-l", "--language", default="english")
  return arg_parser.parse_args()


def main():
  args = get_args()
  print_as_json(tokenize_documents(args.document_file.readlines(),
                                   language=args.language))


if __name__ == "__main__":
  main()
