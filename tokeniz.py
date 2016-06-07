#!/usr/bin/env python

import argparse
import multiprocessing
import nltk
import re
import sys

from lib import print_as_json



def tokenize_document(document):
  return [nltk.tokenize.word_tokenize(sentence)
          for sentence in nltk.tokenize.sent_tokenize(remove_tags(document))]


def tokenize_documents(documents):
  return multiprocessing.Pool().map(tokenize_document, documents)


def remove_tags(string):
  return re.sub(r"<\s*br\s*/?\s*>", r" ", string)


def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("document_file",
                          type=argparse.FileType(),
                          default=sys.stdin)
  return arg_parser.parse_args()


def main():
  args = get_args()
  print_as_json(tokenize_documents(args.document_file.readlines()))


if __name__ == "__main__":
  main()
