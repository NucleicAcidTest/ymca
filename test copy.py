import sys

class Solution:
    def maximum_possible_score(self, node_values, tree_edges):
        node_count = len(node_values)
        if node_count == 0:
            return 0
        if node_count == 1:
            return abs(node_values[0])
        if node_count == 2:
            return abs(node_values[0]) * abs(node_values[1])
        graph = []
        for _ in range(node_count):
            graph.append([])
        for tree_edge in tree_edges:
            first_node = tree_edge[0]
            second_node = tree_edge[1]
            graph[first_node].append(second_node)
            graph[second_node].append(first_node)
        root_node = 0
        for node_index in range(node_count):
            if len(graph[node_index]) > 1:
                root_node = node_index
                break
        parent_nodes = [-1] * node_count
        visit_order = [root_node]
        for node_index in visit_order:
            for next_node in graph[node_index]:
                if next_node == parent_nodes[node_index]:
                    continue
                parent_nodes[next_node] = node_index
                visit_order.append(next_node)
        down_scores = [0] * node_count
        best_score = 0
        for node_index in reversed(visit_order):
            best_down = 0
            second_down = 0
            child_count = 0
            for next_node in graph[node_index]:
                if next_node == parent_nodes[node_index]:
                    continue
                child_count += 1
                child_score = down_scores[next_node]
                if child_score > best_down:
                    second_down = best_down
                    best_down = child_score
                elif child_score > second_down:
                    second_down = child_score
            node_score = abs(node_values[node_index])
            if child_count == 0:
                down_scores[node_index] = node_score
            else:
                down_scores[node_index] = node_score * best_down
            if child_count >= 2:
                route_score = best_down * second_down * node_score
                if route_score > best_score:
                    best_score = route_score
        return best_score

def read_values(required_count):
    result_values = []
    while len(result_values) < required_count:
        input_line = sys.stdin.buffer.readline()
        if not input_line:
            break
        line_values = input_line.split()
        for value_text in line_values:
            result_values.append(int(value_text))
    return result_values

def main():
    first_values = read_values(1)
    if not first_values:
        return
    node_count = first_values[0]
    node_values = read_values(node_count)
    tree_edges = []
    edge_count = node_count - 1
    while len(tree_edges) < edge_count:
        input_line = sys.stdin.buffer.readline()
        if not input_line:
            break
        line_values = input_line.split()
        if len(line_values) < 2:
            continue
        first_node = int(line_values[0]) - 1
        second_node = int(line_values[1]) - 1
        tree_edges.append([first_node, second_node])
    solution = Solution()
    print(solution.maximum_possible_score(node_values, tree_edges))

if __name__ == "__main__":
    main()