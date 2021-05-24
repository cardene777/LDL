import collections


def sorted_dict_by_key(unsorted_dict):
    # 辞書のキーでソートして返す
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d: d[0]))
