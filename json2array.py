#!/usr/bin/env python

import argparse
import json
import numpy
import sys



# constants

NULL_CHAR = '\x00'
UNKNOWN_CHAR = '\x01'

NULL_WORD = NULL_CHAR
UNKNOWN_WORD = UNKNOWN_CHAR

CHAR_DATATYPE = numpy.int32



# functions

## utils

def array(sequence):
  return numpy.array(list(sequence), dtype=CHAR_DATATYPE)


def documents_to_words(documents):
  return {word
          for document in documents
          for sentence in document
          for word in sentence}


def documents_to_chars(documents):
  return {char for word in documents_to_words(documents) for char in word}


def index_elems_in_set(elems):
  return {elem : index for index, elem in enumerate(sorted(elems))}


## indices

def create_char_indices(documents):
  return index_elems_in_set(documents_to_chars(documents)
                            | {NULL_CHAR, UNKNOWN_CHAR})


def create_word_indices(documents):
  return index_elems_in_set(documents_to_words(documents)
                            | {NULL_WORD, UNKNOWN_WORD})


## word array

def create_word_array(word_indices, word_length, char_indices):
  word_array = numpy.zeros((len(word_indices), word_length),
                           dtype=CHAR_DATATYPE)

  for word, index in word_indices.items():
    word_array[index] = word_to_array(word, word_length, char_indices)

  return word_array


def word_to_array(word, word_length, char_indices):
  return array(char_indices[char] for char in format_word(word, word_length))


def format_word(word, word_length):
  return word[:word_length] if len(word) >= word_length else \
         word + NULL_CHAR * (word_length - len(word))


def save_word_array(filename, word_indices, *, word_length, char_indices):
  if filename is not None:
    create_word_array(word_indices,
                      word_length=word_length,
                      char_indices=char_indices).dump(filename)


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


def save_document_array(filename, *args, **kwargs):
  if filename is not None:
    create_document_array(*args, **kwargs).dump(filename)


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


def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("-w", "--word-length", type=int, required=True)
  arg_parser.add_argument("-s", "--sentence-length", type=int, required=True)
  arg_parser.add_argument("-d", "--document-length", type=int, required=True)
  arg_parser.add_argument("--word-array-file")
  arg_parser.add_argument("--document-array-file", required=True)
  arg_parser.add_argument("json_document_file", nargs="?")
  return arg_parser.parse_args()


# main routine

def main():
  args = get_args()

  if args.json_document_file is not None:
    with open(args.json_document_file) as file:
      json_documents = file.read()
  else:
    json_documents = sys.stdin.read()

  documents = json.loads(json_documents)

  char_indices = create_char_indices(documents)
  word_indices = create_word_indices(documents)

  save_word_array(args.word_array_file,
                  word_indices,
                  word_length=args.word_length,
                  char_indices=char_indices)

  save_document_array(args.document_array_file,
                      documents,
                      word_indices,
                      sentence_length=args.sentence_length,
                      document_length=args.document_length)


if __name__ == "__main__":
  main()
