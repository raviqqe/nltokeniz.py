#!/usr/bin/env python

import docopt
import json
import numpy
import sys



# constants

NULL_CHAR = 0


# functions

def word_list_to_int_list(word_list):
  return [word_list_to_int_list(elem) for elem in word_list] \
         if isinstance(word_list, list) else \
         [ord(char) for char in word_list]


def format_int_list(the_list, sizes):
  assert all(isinstance(hier, int) and hier > 0 for hier in sizes.keys())

  hier = hierarchy(the_list)
  size = sizes[hier]

  formated_sub_lists = [format_int_list(sub_list) for sub_list in the_list]

  if size is None:
    return formated_sub_lists

  return formated_sub_lists[:size] \
         if len(the_list) >= size else \
         formated_sub_lists + [dummy(hier - 1, sizes)] * (size - len(the_list))


def dummy(hier, sizes):
  return NULL_CHAR if hier == 0 else [dummy(hier - 1, sizes)] * sizes[hier]


def hierarchy(the_list):
  if not isinstance(the_list, list):
    return 0

  assert all(hierarchy(elem) == hierarchy(the_list[0]) for elem in the_list)
  return hierarchy(the_list[0]) + 1



# main routine

def main(args):
  """
  Usage:
    json2array [<json_document_filename>] <numpy_array_file>

  Options:
    -w --max-word-length <word_length>
    -s --max-sentence-length <sentence_length>
    -d --max-document-length <document_length>
    -h --help
  """

  if args["<json_document_filename>"] is not None:
    with open(args["<json_document_filename>"]) as file:
      json_documents = file.read()
  else:
    json_documents = sys.stdin.read()

  numpy.array(format_int_list(
    word_list_to_int_list(json.loads(json_documents)),
    {
      1 : int(args["--max-word-length"]),
      2 : int(args["--max-sentence-length"]),
      3 : int(args["--max-document-length"]),
      4 : None
    }
  )).dump(args["<numpy_array_file>"])


if __name__ == "__main__":
  main(docopt.docopt(main.__doc__))
