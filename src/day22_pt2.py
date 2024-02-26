import networkx as nx
import numpy as np


def parse_input(input_raw: str):
    bricks = {}
    for idx, line in enumerate(input_raw.split('\n')):
        x1, y1, z1, x2, y2, z2 = map(int, line.replace('~', ',').split(','))
        brick_id = idx + 1  
        cube_coords = np.array(
            np.meshgrid(
                np.arange(x1, x2+1), 
                np.arange(y1, y2+1), 
                np.arange(z1, z2+1)
        )).T.reshape(-1, 3)

        cubes = []
        for coords in cube_coords:
            cubes.append(tuple(coords))
        bricks[brick_id] = cubes

    return bricks




test_input_raw = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""

with open('inputs/day22.txt', 'r') as f:
    input_raw = f.read()

#bricks = parse_input(test_input_raw)
bricks = parse_input(input_raw)

# we'll create a 3d numpy array to represent the grid
max_x = max([x for coords in bricks.values() for x,_,_ in coords])
max_y = max([y for coords in bricks.values() for _,y,_ in coords])
max_z = max([z for coords in bricks.values() for _,_,z in coords])

# we'll add 1 to each dimension so indexes match the brick positions
brick_array = np.zeros((max_x+1, max_y+1, max_z+1), dtype=int)
for brick_id, cubes in bricks.items():
    for (x, y, z) in cubes:
        brick_array[x, y, z] = brick_id 

# mark the floor
brick_array[:, :, 0] = -1

# we'll iterate through the bricks and check if they can fall
finished = False
while not finished:
    falling_brick_count = 0
    for brick_id, cubes in bricks.items():

        # cubes beneath the brick's cubes that are not part of the brick
        beneath = [(x, y, z-1) 
                   for (x,y,z) in cubes
                   if brick_array[(x, y, z-1)] != brick_id]

        x_beneath, y_beneath, z_beneath = zip(*beneath)

        # if the area beneath is all empty, the brick falls
        if np.all(brick_array[x_beneath, y_beneath, z_beneath] == 0):
            #print(f"Brick {brick_id} fell")
            new_cubes = [(x, y, z-1) for (x,y,z) in cubes]
            x_new, y_new, z_new = zip(*new_cubes)
            x_old, y_old, z_old = zip(*cubes)

            # update the array
            brick_array[x_old, y_old, z_old] = 0
            brick_array[x_new, y_new, z_new] = brick_id

            # update the brick
            bricks[brick_id] = new_cubes

            falling_brick_count += 1

    if falling_brick_count == 0:
        finished = True 
    
# which bricks support which other bricks?
supported_by = {}
for brick_id, cubes in bricks.items():
    
    # different from part 1: we also consider the floor as a support
    beneath = [(x, y, z-1) 
               for (x,y,z) in cubes
               if brick_array[(x, y, z-1)] != brick_id]

    below_x_indices, below_y_indices, below_z_indices = zip(*beneath)
    cubes_below = brick_array[below_x_indices, below_y_indices, below_z_indices]
    bricks_below = set([b_id for b_id in cubes_below if b_id not in [0, brick_id]])
    supported_by[brick_id] = bricks_below

# create a directed graph
g = nx.DiGraph(supported_by).reverse()

# let's say I remove a node from the graph -- for which nodes does the graph become disconnected?
# the falling bricks are the size of the connected components that do not contain the floor
falling_bricks = {}
for node in g.nodes():

    # don't consider removing the floor 
    if node == -1:
        continue
    
    g2 = g.copy()
    g2.remove_node(node)

    # falling bricks are ones that have now become unreachable from the floor
    connected_to_floor_before_deletion = set(nx.descendants(g, -1))
    connected_to_floor_after_deletion = set(nx.descendants(g2, -1))


    # fallings bricks are the difference between the two sets, if we remember to remove the node itself
    falling_bricks[node] = connected_to_floor_before_deletion - connected_to_floor_after_deletion - {node}


result = sum([len(v) for k, v in falling_bricks.items()])

# 60963
print(f"Part 2: {result} bricks will fall.")