import sys
from math import hypot

class Solution:
    def minimum_path_length(self, start_index, x_values, head_x, head_y):
        start_x = x_values[start_index - 1]
        left_x = min(x_values)
        right_x = max(x_values)
        points = [(left_x, 0), (right_x, 0), (head_x, head_y)]
        orders = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
        best_distance = None

        for order in orders:
            current_x = start_x
            current_y = 0
            total_distance = 0
            for point_index in order:
                next_x = points[point_index][0]
                next_y = points[point_index][1]
                total_distance += hypot(next_x - current_x, next_y - current_y)
                current_x = next_x
                current_y = next_y
            if best_distance is None or total_distance < best_distance:
                best_distance = total_distance

        return best_distance

def read_values(required_count):
    result_values = []
    while len(result_values) < required_count:
        input_line = sys.stdin.buffer.readline()
        if not input_line:
            break
        for value_text in input_line.split():
            result_values.append(int(value_text))
    return result_values

def main():
    first_values = read_values(2)
    if not first_values:
        return
    retailer_count = first_values[0]
    start_index = first_values[1]
    x_values = read_values(retailer_count)
    head_values = read_values(2)
    solution = Solution()
    answer = solution.minimum_path_length(start_index, x_values, head_values[0], head_values[1])
    print(f"{answer:.2f}")

if __name__ == "__main__":
    main()