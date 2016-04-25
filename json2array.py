#!/usr/bin/env python

import docopt
import json
import multiprocessing
import numpy
import sys



# constants

NULL_CHAR = '\x00'
UNKNOWN_CHAR = '\x01'

NULL_WORD = NULL_CHAR
UNKNOWN_WORD = UNKNOWN_CHAR


# functions

## utils

def array(sequence):
  return numpy.array(list(sequence), dtype=numpy.int32)


## word indices

def create_word_indices(documents):
  words = {word
           for document in documents
           for sentence in document
           for word in sentence} \
          | {NULL_WORD, UNKNOWN_WORD}

  return {word : index for index, word in enumerate(sorted(words))}


## word array

def create_word_array(word_indices, word_length):
  word_array = numpy.zeros((len(word_indices), word_length))

  for word, index in word_indices.items():
    word_array[index] = word_to_array(word, word_length)

  return word_array


def word_to_array(word, word_length):
  return array(ord(char) for char in format_word(word, word_length))


def format_word(word, word_length):
  return word[:word_length] if len(word) >= word_length else \
         word + NULL_CHAR * (word_length - len(word))


## document array

def create_document_array(documents,
                          word_indices,
                          sentence_length,
                          document_length):
  return array(format_int_list(
    [[[word_to_index(word, word_indices)
       for word in sentence]
      for sentence in document]
     for document in documents],
    {
      1 : sentence_length,
      2 : document_length,
      3 : None,
    },
    word_indices[NULL_WORD],
  ))


def word_to_index(word, word_indices):
  return word_indices[word] if word in word_indices else \
         word_indices[UNKNOWN_WORD]


## int list

def format_int_list(the_list, lengths, null_int):
  assert all(isinstance(hier, int) and hier > 0 for hier in lengths.keys())

  if not isinstance(the_list, list):
    return the_list

  formated_sub_lists = [format_int_list(sub_list, lengths, null_int)
                        for sub_list in the_list]

  hier = hierarchy(the_list)
  length = lengths[hier]

  if length is None:
    return formated_sub_lists

  return formated_sub_lists[:length] \
         if len(the_list) >= length else \
         formated_sub_lists + [dummy(hier - 1, lengths, null_int)] \
                              * (length - len(the_list))


def dummy(hier, lengths, null_int):
  return null_int if hier == 0 else \
         [dummy(hier - 1, lengths, null_int)] * lengths[hier]


def hierarchy(the_list):
  if not isinstance(the_list, list):
    return 0

  assert all(hierarchy(elem) == hierarchy(the_list[0]) for elem in the_list)
  return hierarchy(the_list[0]) + 1



# main routine

def main(args):
  """
  Usage:
    json2array -w <length> -s <length> -d <length>
               --word-array-file <file>
               --document-array-file <file>
               [<json_document_file>]

  Options:
    -w --word-length <length>
    -s --sentence-length <length>
    -d --document-length <length>
    -h --help
  """

  if args["<json_document_file>"] is not None:
    with open(args["<json_document_file>"]) as file:
      json_documents = file.read()
  else:
    json_documents = sys.stdin.read()

  documents = json.loads(json_documents)

  word_indices = create_word_indices(documents)

  create_word_array(
    word_indices,
    word_length=int(args["--word-length"]),
  ).dump(args["--word-array-file"])

  create_document_array(
    documents,
    word_indices,
    sentence_length=int(args["--sentence-length"]),
    document_length=int(args["--document-length"]),
  ).dump(args["--document-array-file"])


if __name__ == "__main__":
  main(docopt.docopt(main.__doc__))
