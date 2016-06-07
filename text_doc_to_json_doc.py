#!/usr/bin/env python

import docopt
import json
import multiprocessing
import nltk
import re
import sys



# functions

def tokenize_document(document):
  return [nltk.tokenize.word_tokenize(sentence)
          for sentence in nltk.tokenize.sent_tokenize(remove_tags(document))]


def tokenize_documents(documents):
  return multiprocessing.Pool().map(tokenize_document, documents)


def remove_tags(string):
  return re.sub(r"<\s*br\s*/?\s*>", r" ", string)



# main routine

def main(args):
  """
  Usage:
    doc2json [<document_filename>]

  Options:
    -h --help Show help.
  """

  if args["<document_filename>"] is not None:
    with open(args["<document_filename>"]) as file:
      documents = file.readlines()
  else:
    documents = sys.stdin.readlines()

  print(json.dumps(tokenize_documents(documents)))


if __name__ == "__main__":
  main(docopt.docopt(main.__doc__))
