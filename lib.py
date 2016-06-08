import collections
import json
import multiprocessing
import numpy



# constants

NULL_CHAR = '\x00'
UNKNOWN_CHAR = '\x01'

NULL_WORD = NULL_CHAR
UNKNOWN_WORD = UNKNOWN_CHAR



# functions

def print_as_json(obj):
  print(json.dumps(obj, indent="\t"))


def array(sequence):
  return numpy.array(list(sequence), dtype=numpy.int32)


def documents_to_words(documents):
  return [word
          for document in documents
          for sentence in document
          for word in sentence]


def documents_to_chars(documents):
  return [char for word in documents_to_words(documents) for char in word]


def list_to_index(list_):
  assert len(list_) == len(set(list_))
  return {elem : index for index, elem in enumerate(list_)}


def parallel_map(func, sequence):
  return multiprocessing.Pool().map(func, sequence)


def filter_by_freq(elems, min_freq):
  return {elem for elem, freq in collections.Counter(list(elems)).items()
          if freq >= min_freq}


def create_elem_list(elems, *, min_freq, kept_elems):
  return sorted(filter_by_freq(elems, min_freq) | kept_elems)



## classes

class ListAligner:
  def __init__(self, lengths, bottom_dummy, centerize):
    assert all(isinstance(hier, int) and hier > 0 for hier in lengths.keys())

    self._lengths = lengths # hier -> length
    self._dummies = {0 : bottom_dummy} # hier -> dummy
    self._centerize = centerize

  def _dummy(self, hier):
    if hier in self._dummies:
      return self._dummies[hier]

    assert hier != 0
    self._dummies[hier] = [self._dummy(hier - 1)] * self._lengths[hier]
    return self._dummies[hier]

  def align(self, list_):
    if not isinstance(list_, list):
      return list_

    aligned_sub_lists = [self.align(sub_list) for sub_list in list_]

    hier = self._hier(list_)
    length = self._lengths[hier]

    if length is None:
      return aligned_sub_lists

    return self._align_list_of_aligned_sub_lists(aligned_sub_lists)

  def _align_list_of_aligned_sub_lists(self, list_):
    hier = self._hier(list_)
    length = self._lengths[hier]
    dummy_head, dummy_tail \
        = self._split_in_half(self._dummy(hier)[:max(length - len(list_), 0)])
    return dummy_head + list_[:length] + dummy_tail \
           if self._centerize else \
           list_[:length] + dummy_head + dummy_tail

  def _hier(self, list_):
    if not isinstance(list_, list):
      return 0

    assert all(self._hier(elem) == self._hier(list_[0]) for elem in list_)
    return self._hier(list_[0]) + 1

  @staticmethod
  def _split_in_half(list_):
    half_length = len(list_) // 2
    return list_[:half_length], list_[half_length:]
