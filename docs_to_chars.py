#!/usr/bin/env python

import argparse
import json
import sys

from lib import print_as_json, \
                create_elem_list, \
                documents_to_chars, \
                NULL_CHAR, \
                UNKNOWN_CHAR



def create_char_list(documents, min_freq):
  return create_elem_list(documents_to_chars(documents),
                          min_freq=min_freq,
                          kept_elems={NULL_CHAR, UNKNOWN_CHAR})


def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("--min-freq", type=int, default=1)
  arg_parser.add_argument("json_document_file",
                          type=argparse.FileType(),
                          nargs="?",
                          default=sys.stdin)
  return arg_parser.parse_args()


def main():
  args = get_args()
  print_as_json(create_char_list(json.load(args.json_document_file),
                                 min_freq=args.min_freq))


if __name__ == "__main__":
  main()
