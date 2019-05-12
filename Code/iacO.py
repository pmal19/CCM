class Person():
    graph = {
        "instance": [],
        "name": [],
        "gang": [],
        "age": [],
        "edu": [],
        "mar": [],
        "occ": []
    }

    def __init__(self, attributes):
        # Assuming name attribute of the instance is unique
        self.value = attributes['name']
        self.kind = "instance"
        self.activation = REST
        self.netInput = 0
        self.attachedTo = []
        for attribute in attributes:
            prop = None
            # Check if property already exists
            for node in Person.graph[attribute]:
                if node.value == attributes[attribute]:
                    prop = node
                    break

            # If property do not exist, create it
            if prop is None:
                prop = Property(attribute, attributes[attribute])
                Person.graph[attribute].append(prop)

            # Create connections
            prop.attachedTo.append(self)
            self.attachedTo.append(prop)

        # Attach a reference of oneself to access it later
        Person.graph["instance"].append(self)

    def __str__(self):
        return "%s %s %s" % (self.kind, self.value, self.activation)#, map(lambda x: x.value, self.attachedTo))



class Property():
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value
        self.attachedTo = []
        self.activation = REST
        self.netInput = 0

    def __str__(self):
        return "%s %s %s" % (self.kind, self.value, self.activation)#, ' '.join(map(str, self.attachedTo)))

data = [
    {'name': 'Art',   'gang': 'Jets', 'age': '40s', 'edu': 'JH', 'mar': 'single',   'occ': 'pusher'},
    {'name': 'Al',    'gang': 'Jets', 'age': '30s', 'edu': 'JH', 'mar': 'married',  'occ': 'burglar'},
    {'name': 'Sam',   'gang': 'Jets', 'age': '20s', 'edu': 'COL', 'mar': 'single',  'occ': 'bookie'},
    {'name': 'Clyde', 'gang': 'Jets', 'age': '40s', 'edu': 'JH', 'mar': 'single',   'occ': 'bookie'},
    {'name': 'Mike',  'gang': 'Jets', 'age': '30s', 'edu': 'JH', 'mar': 'single',   'occ': 'bookie'},
    {'name': 'Jim',   'gang': 'Jets', 'age': '20s', 'edu': 'JH', 'mar': 'divorced', 'occ': 'burglar'},
    {'name': 'Greg',  'gang': 'Jets', 'age': '20s', 'edu': 'HS', 'mar': 'married',  'occ': 'pusher'},
    {'name': 'John',  'gang': 'Jets', 'age': '20s', 'edu': 'JH', 'mar': 'married',  'occ': 'burglar'},
    {'name': 'Doug',  'gang': 'Jets', 'age': '30s', 'edu': 'HS', 'mar': 'single',   'occ': 'bookie'},
    {'name': 'Lance', 'gang': 'Jets', 'age': '20s', 'edu': 'JS', 'mar': 'married',  'occ': 'burglar'},
    {'name': 'George','gang': 'Jets', 'age': '20s', 'edu': 'JH', 'mar': 'divorced', 'occ': 'burglar'},
    {'name': 'Pete',  'gang': 'Jets', 'age': '20s', 'edu': 'HS', 'mar': 'single',   'occ': 'bookie'},
    {'name': 'Fred',  'gang': 'Jets', 'age': '20s', 'edu': 'HS', 'mar': 'single',   'occ': 'pusher'},
    {'name': 'Gene',  'gang': 'Jets', 'age': '20s', 'edu': 'COL', 'mar': 'single',  'occ': 'pusher'},
    {'name': 'Ralph', 'gang': 'Jets', 'age': '30s', 'edu': 'JH',  'mar': 'single',  'occ': 'pusher'},
    {'name': 'Phil', 'gang': 'Sharks', 'age': '30s', 'edu': 'COL', 'mar': 'married',  'occ': 'pusher'},
    {'name': 'Ike',  'gang': 'Sharks', 'age': '30s', 'edu': 'JH',  'mar': 'single',   'occ': 'bookie'},
    {'name': 'Nick', 'gang': 'Sharks', 'age': '30s', 'edu': 'HS',  'mar': 'single',   'occ': 'pusher'},
    {'name': 'Don',  'gang': 'Sharks', 'age': '30s', 'edu': 'COL', 'mar': 'married',  'occ': 'burglar'},
    {'name': 'Ned',  'gang': 'Sharks', 'age': '30s', 'edu': 'COL', 'mar': 'married',  'occ': 'bookie'},
    {'name': 'Karl', 'gang': 'Sharks', 'age': '40s', 'edu': 'HS',  'mar': 'married',  'occ': 'bookie'},
    {'name': 'Ken',  'gang': 'Sharks', 'age': '20s', 'edu': 'HS',  'mar': 'single',   'occ': 'burglar'},
    {'name': 'Earl', 'gang': 'Sharks', 'age': '40s', 'edu': 'HS',  'mar': 'married',  'occ': 'burglar'},
    {'name': 'Rick', 'gang': 'Sharks', 'age': '30s', 'edu': 'HS',  'mar': 'divorced', 'occ': 'burglar'},
    {'name': 'Ol',   'gang': 'Sharks', 'age': '30s', 'edu': 'COL', 'mar': 'married',  'occ': 'pusher'},
    {'name': 'Neal', 'gang': 'Sharks', 'age': '30s', 'edu': 'HS',  'mar': 'single',   'occ': 'bookie'},
    {'name': 'Dave', 'gang': 'Sharks', 'age': '30s', 'edu': 'HS',  'mar': 'divorced', 'occ': 'pusher'}
]

MAX = 1.0
MIN = -0.2
REST = -0.1
DECAY = 0.1
ESTR = 0.4
ALPHA = 0.1
GAMMA = 0.1

def find_node(type, value):
    for node in Person.graph[type]:
        if node.value == value:
            return node

def constructGraph():
    for row in data:
        Person(row)

def reset():
    for attribute in Person.graph:
        for node in Person.graph[attribute]:
            node.activation = REST

def get_net(probes):
    for attribute in Person.graph:
        for node in Person.graph[attribute]:
            inhibitory = 0
            excitatory = 0

            for neighbour in node.attachedTo:
                if neighbour.activation > 0:
                    excitatory += neighbour.activation

            for neighbour in Person.graph[node.kind]:
                if neighbour.value == node.value:
                    continue
                if neighbour.activation > 0:
                    inhibitory += neighbour.activation

            excitatory *= ALPHA
            inhibitory *= GAMMA
            node.netInput = excitatory - inhibitory
            if (node.kind, node.value) in probes:
                node.netInput += ESTR * probes[(node.kind, node.value)]

def update():
    for attribute in Person.graph:
        for node in Person.graph[attribute]:

            if node.netInput > 0:
                node.activation += (MAX - node.activation) * node.netInput - DECAY * (node.activation - REST)
            else:
                node.activation += (node.activation - MIN) * node.netInput - DECAY * (node.activation - REST)


            if node.activation > MAX:
                node.activation = MAX
            if node.activation < MIN:
                node.activation = MIN

def show_graph_state():
    for attribute in Person.graph:
        for node in Person.graph[attribute]:
            print node.kind, node.value, node.activation

def cycle(nTimes, probes):
    for i in xrange(nTimes):
        get_net(probes)
        update()

    show_graph_state()

# constructGraph()
# cycle(100, {('name', 'Ken'): 1})