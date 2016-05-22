#!/usr/bin/env python

import docopt
import json



# functions

def read_json_file(filename):
  with open(filename) as file_:
    return json.load(file_)


def get_documents(filename):
  return read_json_file(filename)


def get_sentences(documents):
  return [sentence for document in documents for sentence in document]


def get_words(sentences):
  return [word for sentence in sentences for word in sentence]


def group_by_length(sequences):
  lengths = set(len(sequence) for sequence in sequences)
  return {length : filter_by_length(sequences, length) for length in lengths}


def filter_by_length(sequences, length):
  return list(filter(lambda x: len(x) == length, sequences))


def stat_lengths(sequences, about):
  total_num = len(sequences)
  print("Total number of {} is:".format(about), total_num)

  sum_of_nums = 0
  for length, sequences in sorted(group_by_length(sequences).items()):
    sum_of_nums += len(sequences)
    print("Number of {} of length {:4} is:".format(about, length),
          "{:8}".format(len(sequences)),
          "(ratio: {})".format(sum_of_nums / total_num),
          sep="\t")



# main routine

def main():
  """
  Usage:
    stat_json <filename>
  """

  args = docopt.docopt(main.__doc__)

  documents = get_documents(args["<filename>"])
  stat_lengths(documents, "documents")

  sentences = get_sentences(documents)
  print()
  stat_lengths(sentences, "sentences")

  words = get_words(sentences)
  print()
  stat_lengths(words, "words")


if __name__ == "__main__":
  main()
