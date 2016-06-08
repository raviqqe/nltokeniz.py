#!/usr/bin/env python

import argparse
import json
import numpy
import sys



def get_args():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("json_char_file",
                          nargs="?",
                          type=argparse.FileType(),
                          default=sys.stdin)
  arg_parser.add_argument("numpy_char_file")
  return arg_parser.parse_args()


def main():
  args = get_args()
  numpy.save(args.numpy_char_file, numpy.array(
      [ord(char) for char in json.load(args.json_char_file)],
      dtype=numpy.uint32))


if __name__ == "__main__":
  main()
