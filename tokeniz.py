#!/usr/bin/env python

import argparse
import json
import multiprocessing
import nltk
import re
import sys



def tokenize_document(document):
  return [nltk.tokenize.word_tokenize(sentence)
          for sentence in nltk.tokenize.sent_tokenize(document)]


def tokenize_documents(documents):
  return multiprocessing.Pool().map(tokenize_document, documents)


def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("document_file",
                          type=argparse.FileType(),
                          default=sys.stdin)
  return arg_parser.parse_args()


def main():
  args = get_args()
  print(json.dumps(tokenize_documents(args.document_file.readlines()),
                   indent="\t"))


if __name__ == "__main__":
  main()
