from collections import defaultdict, deque
from enum import Enum
from math import lcm 

def parse_input(input_str, pulse_queue):
    lines = input_str.split('\n')

    modules = {}
    for line in lines:
        identifier, destinations = line.split(" -> ")
        destinations = [d.strip() for d in destinations.split(",")]

        if identifier.startswith("%"):
            name = identifier[1:]
            modules[name] = Flipflop(name, destinations, pulse_queue)

        elif identifier.startswith("&"):
            name = identifier[1:]
            inputs = None # set below
            modules[name] = Conjunction(name, inputs, destinations, pulse_queue)

        elif identifier == "broadcaster":
            modules["broadcaster"] = Broadcaster(destinations, pulse_queue)

        elif identifier == "button":
            modules["button"] = Button(destinations, pulse_queue)

        else:
            raise ValueError(f"Invalid module identifier: {identifier}")

    # at this point, destinations are still strings, so we need to replace them with the actual objects
    terminal_modules = []
    for module in modules.values():
        # some modules only appear on the RHS
        for i, destination in enumerate(module.destinations):
            if destination in modules:
                module.destinations[i] = modules[destination]
            else:
                terminal_module = Terminal(destination)
                module.destinations[i] = terminal_module
                terminal_modules.append(terminal_module)

    for tm in terminal_modules:
        modules[tm.name] = tm

    # create the button
    modules["button"] = Button(modules["broadcaster"], pulse_queue)

    # set inputs for conjunction modules
    for module in modules.values():
        if isinstance(module, Conjunction):
            inputs = []
            for other_module in modules.values(): 
                if hasattr(other_module, "destinations") and module in other_module.destinations:
                    inputs.append(other_module.name)
            module.set_inputs(inputs)

    return modules
 
 
def pulse_counter(func):
    def wrapper(*args, **kwargs):
        
        global high_pulses_sent
        global low_pulses_sent

        sender = args[0]
        pulse = args[1]

        if pulse == Pulse.HIGH:
            high_pulses_sent += 1
        elif pulse == Pulse.LOW:
            low_pulses_sent += 1
        else:
            raise ValueError(f"Pulse must be either high or low. Received: {pulse}")

        return func(*args, **kwargs)
    
    return wrapper


def process_pulses(pulse_queue):
    while pulse_queue:
        sender, recipient, pulse = pulse_queue.popleft()  # FIFO
        recipient.receive_pulse(sender, pulse)


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class State(Enum):
    OFF = 0
    ON = 1


class Module():

    global record

    def __init__(self, name, destinations, pulse_queue):
        self.name = name
        self.destinations = destinations
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"Module '{self.name}'"

    def receive_pulse(self, sender, pulse):
        self.send_pulses(pulse)

    def send_pulses(self, pulse):
        for destination in self.destinations:
            self.send_pulse(pulse, destination)

    @pulse_counter
    def send_pulse(self, pulse, destination):
        #if destination.name in relevant_modules:
        if destination.name == 'nc' and pulse == Pulse.HIGH:
           #print(f"{self.name} -- {pulse} --> {destination}")
           record[self.name].append(i)
        self.pulse_queue.append((self.name, destination, pulse))


class Broadcaster(Module):

    """
    There is a single broadcast module (named broadcaster). 
    When it receives a pulse, it sends the same pulse to all of its destination modules
    """

    def __init__(self, destinations, pulse_queue):
        self.name = "broadcaster"
        self.destinations = destinations
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"Broadcaster '{self.name}'"


class Button(Module):
    """
    When you push the button, a single low pulse is sent directly to the broadcaster module.
    """ 

    def __init__(self, broadcaster, pulse_queue):
        self.name = "button"
        self.destinations = [broadcaster]
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"Button '{self.name}' with broadcaster {self.destinations}"

    def push(self):
        self.send_pulse(Pulse.LOW)

    @pulse_counter
    def send_pulse(self, pulse):
        #print(f"{self.name} -- {pulse} --> {self.destinations.name}")
        self.pulse_queue.append((self.name, self.destinations[0], pulse))
        

class Flipflop(Module):

    """ 
    Flip-flop modules (prefix %) are either on or off; they are initially off. 
    If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
    However, if a flip-flop module receives a low pulse, it flips between on and off. 
    If it was off, it turns on and sends a high pulse.
    If it was on, it turns off and sends a low pulse.
    """

    def __init__(self, name, destinations, pulse_queue):
        self.name = name
        self.state = State.OFF
        self.destinations = destinations
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"Flipflop '{self.name}' in state {self.state}"

    def flip(self):
        if self.state == State.OFF:
            self.state = State.ON
        else:
            self.state = State.OFF

    def receive_pulse(self, sender, pulse):
        #print(f"{self.name} received pulse {pulse} from {sender}")
        if pulse == Pulse.LOW:
            if self.state == State.OFF:
                self.flip()
                self.send_pulses(Pulse.HIGH)
            else:
                self.flip()
                self.send_pulses(Pulse.LOW)

        elif pulse == Pulse.HIGH:
            pass



class Conjunction(Module):

    """ 
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; 
    they initially default to remembering a low pulse for each input. 
    When a pulse is received, the conjunction module first updates its memory for that input. 
    Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    """

    def __init__(self, name, inputs, destinations, pulse_queue):
        self.name = name
        self.memory = {}
        self.destinations = destinations
        self.pulse_queue = pulse_queue

    def __repr__(self):
        return f"Conjunction '{self.name}'"

    def receive_pulse(self, sender, pulse):
        #print(f"{self.name} received pulse {pulse} from {sender}. Memory is: {self.memory}")
        self.memory[sender] = pulse
        if all([pulse == Pulse.HIGH for pulse in self.memory.values()]):
            self.send_pulses(Pulse.LOW)
        else:
            self.send_pulses(Pulse.HIGH)
        #print(f"Memory is now: {self.memory}")

    def set_inputs(self, inputs):
        self.memory = {_input: Pulse.LOW for _input in inputs}


class Terminal(Module):

    """A module that just receives a pulse.""" 

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Terminal '{self.name}'"

    def receive_pulse(self, sender, pulse):
        pass 

    def send_pulse(self, pulse):
        pass


test_input_raw_1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

test_input_raw_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""" 

with open("inputs/day20.txt") as f:
    input_raw = f.read()


high_pulses_sent = 0
low_pulses_sent = 0

pulse_queue = deque()
modules = parse_input(input_raw, pulse_queue)

# which modules connect directly to each other?
module_connections = defaultdict(set)
module_types = defaultdict(set)
for module in modules.values():

    # record the type of each module
    module_types[module.name].add(module.__class__.__name__)

    # record the connections between modules
    if hasattr(module, "destinations"):
        for destination in module.destinations:
            module_connections[module.name].add(destination.name)
    else:
        module_connections[module.name].add("None")


# modules that connect to nc -- if these are all high, a low pulse is sent to rx, so these are the ones we need to check
relevant_modules = []
for k,v in module_connections.items():
    if 'nc' in v:
        relevant_modules.append(k)

# run through a number of iterations and figure out the period of the modules that connect to nc
record = defaultdict(list)
input_str = input_raw
times = 10_000

pulse_queue = deque()
modules = parse_input(input_str, pulse_queue)

for i in range(times):
    modules['button'].push()
    process_pulses(pulse_queue)

periods = {}
for module, ns in record.items():
    period = ns[1] - ns[0]
    print(f"{module} has period {period}")  
    periods[module] = period

# the result is the least common multiple of the periods of the modules that connect to nc
# 238815727638557
result = lcm(*periods.values())
print("Part 2 result: ", result)



# visualization
# import networkx as nx
# import matplotlib.pyplot as plt

# # build up a graph of the connections between modules, showing each module's type 
# G = nx.DiGraph()
# for module in modules.values():
#     G.add_node(module.name, type=module.__class__.__name__)
#     if hasattr(module, "destinations"):
#         for destination in module.destinations:
#             G.add_edge(module.name, destination.name)


# type_colour_map = {
#     'Button': 'blue',
#     'Broadcaster': 'green',
#     'Flipflop': 'orange',
#     'Conjunction': 'yellow', 
#     'Terminal': 'red'
# }

# node_colours = [type_colour_map[G.nodes[n]['type']] for n in G.nodes]


# # plot the graph
# plt.figure(figsize=(20,20))
# pos = nx.spring_layout(G, k=0.5)
# nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colours)
# nx.draw_networkx_labels(G, pos)
# nx.draw_networkx_edges(G, pos, arrows=True, width=1.0, edge_color='black', alpha=0.1)
# plt.show()