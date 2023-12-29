import heapq
from dataclasses import dataclass
from collections import defaultdict, deque, namedtuple
from typing import Dict, List

@dataclass
class Node:
    location: tuple
    heat_loss: int
    direction_history: deque
    steps_in_current_direction: int = 0

    def __hash__(self):
        return hash((self.location, self.heat_loss) + tuple(self.direction_history))

    def __lt__(self, other):
        return shortest_known_distances[self] < shortest_known_distances[other]


def parse_input(input):
 
    grid = []
    for i, line in enumerate(input.splitlines()):
        grid_row = []
        for j, heat_loss in enumerate(line):
            grid_row.append(int(heat_loss))
        grid.append(grid_row)

    return grid


def plot_path(path, grid):

    grid_map = [[f'{".":<3}' for i in range(len(grid))] for j in range(len(grid[0]))]

    count = 1
    for node in path:
        i, j = node.location
        grid_map[i][j] = f"{count:<3}"
        count += 1

    for row in grid_map:
        print(''.join(row)) 


def get_neighbours(grid, node):

    neighbours = []
    for direction_name, (di, dj) in directions.items(): 

        ni, nj = node.location[0] + di, node.location[1] + dj

        # we can't go out of bounds
        if ni < 0 or nj < 0 or ni >= len(grid) or nj >= len(grid[0]):
            continue

        # we can't go back to the previous node
        if len(node.direction_history) > 1:
            if node.direction_history[-1] == 'UP' and direction_name == 'DOWN':
                continue
            elif node.direction_history[-1] == 'DOWN' and direction_name == 'UP':
                continue
            elif node.direction_history[-1] == 'LEFT' and direction_name == 'RIGHT':
                continue
            elif node.direction_history[-1] == 'RIGHT' and direction_name == 'LEFT':
                continue

        # we can't change direction if we haven't taken enough steps in the current direction
        change_of_direction = len(node.direction_history) > 1 and node.direction_history[-1] != direction_name
        if change_of_direction and node.steps_in_current_direction < MIN_CONSECUTIVE_STEPS: 
            continue

        # we can't take too many steps in the same direction
        if node.steps_in_current_direction == MAX_CONSECUTIVE_STEPS and not change_of_direction:
            continue

        # if the conditions are OK, create a new node and do various bits of incredibly messy bookkeeping
        neighbour_direction_history = node.direction_history.copy()
        neighbour_direction_history.append(direction_name)
        neighbour = Node(location=(ni, nj),
                    heat_loss=grid[ni][nj], 
                    direction_history = neighbour_direction_history)

        if change_of_direction:
            neighbour.steps_in_current_direction = 1
        else:
            neighbour.steps_in_current_direction = node.steps_in_current_direction + 1

        neighbour_distance_from_start = shortest_known_distances[node] + neighbour.heat_loss
        if neighbour in visited:
            if shortest_known_distances.get(neighbour, float('inf')) > neighbour_distance_from_start:
                shortest_known_distances[neighbour] = neighbour_distance_from_start
                predecessors[neighbour] = node
            else:
                continue
        else:
            visited.add(neighbour)
            shortest_known_distances[neighbour] = neighbour_distance_from_start
            heapq.heappush(priority_queue, neighbour)
            predecessors[neighbour] = node
            
        # finally, add the neighbour to the ones we're returning
        neighbours.append(neighbour)

    return neighbours


def reconstruct_path(node):
    current = node
    path = [current]
    print(path)
    while current.location != start_location: 
        prev = predecessors[current]
        path.append(prev)
        current = prev

    return path[::-1]



test_input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

with open('inputs/day17.txt') as f:
    input = f.read()

priority_queue = []
shortest_known_distances = {}
visited = set()
predecessors = {}

#grid = parse_input(test_input)
grid = parse_input(input)


# refs
MIN_CONSECUTIVE_STEPS = 4
MAX_CONSECUTIVE_STEPS = 10
directions = {'UP': (-1,0), 'DOWN': (1,0), 'LEFT': (0,-1), 'RIGHT': (0,1)}
start_location = (0,0)
end_location = (len(grid)-1, len(grid[0])-1)

current = Node(location=start_location, heat_loss=0, direction_history=deque(maxlen=MAX_CONSECUTIVE_STEPS+1), steps_in_current_direction=0)
shortest_known_distances[current] = 0

while current.location != end_location:

    neighbours = get_neighbours(grid, current)
    for neighbour in neighbours:
        if neighbour not in shortest_known_distances:
            shortest_known_distances[neighbour] = float('inf')

        if neighbour not in visited:
            heapq.heappush(priority_queue, neighbour)

    current = heapq.heappop(priority_queue)


path = reconstruct_path(current)

# don't include the start node in the score
result = sum([grid[node.location[0]][node.location[1]] for node in path[1:]])

# 1101
print(f"Part 2 result: {result}")

