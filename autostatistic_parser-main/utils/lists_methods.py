import math


def merge_list_of_lists(lst):
    """Merging the list of lists.

    Args:
        lst (list): The list of lists.

    Returns:
        list: The merged list.
    """
    return [x for l in lst for x in l]


def slice_list(lst, size):
    """Slicing the list to chunks.

    Args:
        lst (list): The list to slice.
        size (int): The number of chunks.

    Returns:
        list: The list of lists.
    """

    sliced_lst = []
    max_list_size = math.ceil(len(lst) / size)
    temp_list = []
    temp_index = 1

    for item in lst:
        temp_list.append(item)
        temp_index += 1

        if temp_index > max_list_size:
            sliced_lst.append(temp_list)
            temp_list = []
            temp_index = 1

    if len(temp_list) > 0:
        sliced_lst.append(temp_list)

    return sliced_lst
