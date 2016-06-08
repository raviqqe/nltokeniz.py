#!/usr/bin/env python

import argparse
import json
import numpy
import sys

from lib import list_to_index, array, parallel_map, ListAligner, NULL_CHAR



def create_word_array(words, *, word_length, chars, centerize):
  char_index = list_to_index(chars)

  aligner = ListAligner({1 : word_length, 2 : None},
                        char_index[NULL_CHAR],
                        centerize)

  return array(parallel_map(
      aligner.align,
      [[char_to_index(char, char_index) for char in word] for word in words]))


def char_to_index(char, char_index):
  return char_index[char] if char in char_index else \
         char_index[UNKNOWN_CHAR]


def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("-c", "--centerize", action="store_true")
  arg_parser.add_argument("-l", "--word-length", type=int, required=True)
  arg_parser.add_argument("--json-char-file",
                          type=argparse.FileType(),
                          required=True)
  arg_parser.add_argument("json_word_file",
                          nargs="?",
                          type=argparse.FileType(),
                          default=sys.stdin)
  arg_parser.add_argument("numpy_word_file")
  return arg_parser.parse_args()


def main():
  args = get_args()
  numpy.save(args.numpy_word_file,
             create_word_array(
                 json.load(args.json_word_file),
                 word_length=args.word_length,
                 chars=json.load(args.json_char_file),
                 centerize=args.centerize))


if __name__ == "__main__":
  main()
