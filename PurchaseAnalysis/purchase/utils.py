import random
from datetime import timedelta


def get_random_date(start_date, end_date):
    delta = end_date - start_date
    diff_seconds = delta.total_seconds()
    random_second = random.randrange(diff_seconds)
    return start_date + timedelta(seconds=random_second)


def chunk_array(input_list, num_chunks):
    if not input_list:
        return input_list
    input_list_length = len(input_list)
    chunk_size = int(input_list_length / num_chunks)
    last_chunkable_item_index = input_list_length - input_list_length % num_chunks
    chunks_array = []
    for i in range(0, last_chunkable_item_index, chunk_size):
        start_index = i
        end_index = i + chunk_size
        chunks_array.append(input_list[start_index: end_index])
    chunks_array[-1].extend(input_list[last_chunkable_item_index:])
    return chunks_array


def generate_fixed_avg_list(start, end, average, num_elements):

    # Out of range
    if (average < start or average > end):
        raise ValueError(
            f"Average Number {average} out of range ({start}, {end})"
        )

    if average == start or average == end:
        result = [average] * num_elements
        return result

    final_sum_required = average * num_elements
    result = [start] * num_elements
    current_sum = sum(result)
    increment_indices = list(range(0, len(result)))
    while current_sum < final_sum_required:
        random_index = random.choice(increment_indices)
        random_increment = random.randint(
            1, min(
                end - result[random_index],
                final_sum_required - current_sum,
            )
        )
        result[random_index] += random_increment
        current_sum += random_increment
        if result[random_index] == end:
            increment_indices.remove(random_index)
    return result


def get_same_average_indices(items_lists):
    averages = []
    for index, item_list in enumerate(items_lists):
        current_average = round(sum(item_list) / len(item_list), 2)
        if current_average in averages:
            return averages.index(current_average), index
        averages.append(current_average)
    return


def rectify_same_average_by_shifting(list_1, list_2):
    if not list_1 or not list_2:
        raise ValueError("Input list cannot be empty")
    try:
        avg_list_1 = round(sum(list_1) / len(list_1), 2)
        avg_list_2 = round(sum(list_2) / len(list_2), 2)
        while(avg_list_1 == avg_list_2):
            list_1.append(list_2.pop())
            avg_list_1 = round(sum(list_1) / len(list_1), 2)
            avg_list_2 = round(sum(list_2) / len(list_2), 2)
        return list_1, list_2
    except ZeroDivisionError:
        raise ValueError(
            "Average of the input lists cannot be rectified by shifting"
        )


# def generate_fixed_avg_list(start, end, average, num_elements):
#     """
#         In the list ranging between (start, end), if no item on the left of
#         average can have a corresponding item on the right of average, the
#         only way the resulting list can be formed is with n average items.

#         From an item between (start, average) find a corresponding couple item
#         between (average, end) such that avg(item, couple item) = average
#     """

#     result = []

#     # Out of range
#     if (average < start or average > end):
#         raise ValueError(
#             f"Average Number {average} out of range ({start}, {end})"
#         )

#     if average == start or average == end:
#         result = [average] * num_elements
#         return result

#     num_items_before_avg = average - start
#     num_items_after_avg = end - average
#     if num_items_after_avg < num_items_before_avg:
#         start = average - num_items_after_avg
#     if num_items_before_avg < num_items_after_avg:
#         end = average + num_items_before_avg

#     items_universe = list(range(start, average + 1))
#     if num_elements % 2 == 1:
#         result.append(average)

#     while(len(result) < num_elements):
#         item = random.choice(items_universe)
#         couple_item = average * 2 - item
#         result.insert(random.randint(0, len(result)), item)
#         result.insert(random.randint(0, len(result)), couple_item)
#         # result.extend([item, couple_item])
#     return result


# def generate_fixed_avg_list(start, end, average, num_elements):

#     # Out of range
#     if (average < start or average > end):
#         raise ValueError(
#             f"Average Number {average} out of range ({start}, {end})"
#         )

#     if average == start or average == end:
#         result = [average] * num_elements
#         return result

#     final_sum_required = average * num_elements
#     result = [start] * num_elements
#     current_sum = sum(result)
#     increment_indices = list(range(0, len(result)))
#     for _ in range(0, final_sum_required - current_sum):
#         random_index = random.choice(increment_indices)
#         result[random_index] += 1
#         if result[random_index] == end:
#             increment_indices.remove(random_index)
#     return result
