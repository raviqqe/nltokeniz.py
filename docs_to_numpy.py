#!/usr/bin/env python

import argparse
import json
import sys

from lib import list_to_index, ListAligner, parallel_map, array, \
                UNKNOWN_WORD, NULL_WORD



def create_document_array(documents,
                          words,
                          *,
                          sentence_length,
                          document_length,
                          centerize):
  aligner = ListAligner(
    {
      1 : sentence_length,
      2 : document_length,
      3 : None,
    },
    words.index(NULL_WORD),
    centerize,
  )

  word_index = list_to_index(words)

  return array(parallel_map(
      aligner.align,
      [[[word_to_index(word, word_index) for word in sentence]
        for sentence in document]
       for document in documents]))


def word_to_index(word, word_index):
  return word_index[word] if word in word_index else word_index[UNKNOWN_WORD]


def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("--centerize", action="store_true")
  arg_parser.add_argument("-s", "--sentence-length", type=int, required=True)
  arg_parser.add_argument("-d", "--document-length", type=int, required=True)
  arg_parser.add_argument("--json-word-file",
                          required=True,
                          type=argparse.FileType())
  arg_parser.add_argument("json_document_file",
                          nargs="?",
                          type=argparse.FileType(),
                          default=sys.stdin)
  arg_parser.add_argument("numpy_document_file")
  return arg_parser.parse_args()


def main():
  args = get_args()

  create_document_array(
    json.load(args.json_document_file),
    json.load(args.json_word_file),
    sentence_length=args.sentence_length,
    document_length=args.document_length,
    centerize=args.centerize,
  ).dump(args.numpy_document_file)


if __name__ == "__main__":
  main()
