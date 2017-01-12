#!/usr/bin/env python

import argparse
import json
import multiprocessing
import sys


def tokenize_documents(documents, language):
    return multiprocessing.Pool().map(DocumentTokenizer(language).tokenize,
                                      documents)


def print_as_json(obj):
    print(json.dumps(obj, ensure_ascii=False, indent="\t"))


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("document_file",
                            type=argparse.FileType(),
                            default=sys.stdin)
    arg_parser.add_argument("-l", "--language", default="english")
    return arg_parser.parse_args()


def main():
    args = get_args()
    print_as_json(tokenize_documents(args.document_file.readlines(),
                                     language=args.language))


if __name__ == "__main__":
    main()
