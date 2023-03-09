import re
import time
import os
import heapq
import math

action_codes = [
    [1, 0, 0],
    [-1, 0, 0],
    [0, 1, 0],
    [0, -1, 0],
    [0, 0, 1],
    [0, 0, -1],
    [1, 1, 0],
    [1, -1, 0],
    [-1, 1, 0],
    [-1, -1, 0],
    [1, 0, 1],
    [1, 0, -1],
    [-1, 0, 1],
    [-1, 0, -1],
    [0, 1, 1],
    [0, 1, -1],
    [0, -1, 1],
    [0, -1, -1],
]

def getPathCostByAction(action):
    if action < 7:
        return 10
    else:
        return 14

class ProblemDetails:
    def __init__(self):
        pass

    def set_values(self, algorithm, max_vertex, start_vertex, end_vertex, input_size):
        self.algorithm = algorithm
        self.max_vertex = max_vertex
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.input_size = input_size

class PriorityQueueElement():
    def __init__(self, nodekey, cost):
        self.nodekey = nodekey
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost

class Vertex:
    def __init__(self, x_value, y_value, z_value):
        self.x = int(x_value)
        self.y = int(y_value)
        self.z = int(z_value)

    def getVertexKey(self):
        return str(self.x) + "-" + str(self.y) + "-" + str(self.z)

def formVertexKey(vertices):
    return "-".join(str(x) for x in vertices)

def getVertexNodeFromKey(key):
    vertices = key.split("-")
    return Vertex(vertices[0], vertices[1], vertices[2])

def isVertexInBoundary(x, y, z, max_vertex):
    if(x < 0 or y < 0 or z < 0 or x > (max_vertex.x-1) or y > (max_vertex.y-1) or z > (max_vertex.z-1)):
        return False
    else:
        return True

def getFilePatternMatchingValue(key):
    vertex = getVertexNodeFromKey(key)
    return str(vertex.x) + " " + str(vertex.y) + " " + str(vertex.z) + " "

def performAction(vertex, actions, max_vertex):
    adjacent_nodes = {}
    for act in actions:
        act = int(act)
        x = vertex.x
        y = vertex.y
        z = vertex.z
        x = x + action_codes[act-1][0]
        y = y + action_codes[act-1][1]
        z = z + action_codes[act-1][2]
        if(isVertexInBoundary(x, y, z, max_vertex)):
            adjacent_nodes[formVertexKey([x ,y, z])] = getPathCostByAction(act)
    return adjacent_nodes

def writeSuccessOutputFile(parent, goal_node_key, root_node_key, heapdictelements, individualPathCost):
    outputfilename = "output.txt"
    totalcost = heapdictelements[goal_node_key]
    steps = []
    steps.append(goal_node_key)
    while(goal_node_key != root_node_key):
        steps.append(parent[goal_node_key])
        goal_node_key = parent[goal_node_key]
    steps.reverse()
    with open(outputfilename, 'w') as ouputfile:
        ouputfile.write(str(totalcost))
        ouputfile.write("\n")
        ouputfile.write(str(len(steps)))
        ouputfile.write("\n")
        for step in steps:
            stepkey = getVertexNodeFromKey(step)
            ouputfile.write(str(stepkey.x) + " " + str(stepkey.y) + " " + str(stepkey.z) + " " + str(individualPathCost[step]))
            ouputfile.write("\n")

def writeFailureOutputFile():
    outputfilename = "output.txt"
    with open(outputfilename, 'w') as ouputfile:
        ouputfile.write("FAIL")

def getHeuristicFutureCostValue(vertex_akey, goal_nodekey):
    vertex_a = getVertexNodeFromKey(vertex_akey)
    goal_node = getVertexNodeFromKey(goal_nodekey)
    dx = abs(vertex_a.x - goal_node.x)
    dy = abs(vertex_a.y - goal_node.y)
    dz = abs(vertex_a.z - goal_node.z)
    distance = math.sqrt((dx*dx) + (dy*dy) + (dz*dz))
    return distance

def AStarImplementation(inputData, problemDetails):
    source_nodekey = problemDetails.start_vertex.getVertexKey()
    source_heap = []
    heapq.heappush(source_heap, PriorityQueueElement(source_nodekey, 0 + getHeuristicFutureCostValue(source_nodekey, problemDetails.end_vertex.getVertexKey())))
    source_heapDictElementsHeuristicTotal = {}
    source_heapDictElementsActualTotal = {}
    source_individualPathCost = {}
    source_heapDictElementsHeuristicTotal[source_nodekey] = 0 + getHeuristicFutureCostValue(source_nodekey, problemDetails.end_vertex.getVertexKey())
    source_heapDictElementsActualTotal[source_nodekey] = 0
    source_individualPathCost[source_nodekey] = 0
    source_visited = {}
    source_visited["5-2-3"] = 1000000
    source_parent = {}
    source_parent[source_nodekey] = -1

    while(len(source_heap) != 0):
        current_node = heapq.heappop(source_heap)
        current_node_key = current_node.nodekey
        current_pathcost = source_heapDictElementsActualTotal[current_node_key]
        if(current_node_key == problemDetails.end_vertex.getVertexKey()):
            print("GOAL FOUND")
            writeSuccessOutputFile(source_parent, current_node_key, source_nodekey, source_heapDictElementsActualTotal, source_individualPathCost)
            return
        source_visited[current_node_key] = current_pathcost
        source_actions_for_current_node = inputData[current_node_key]
        source_child_nodes = performAction(getVertexNodeFromKey(current_node_key), source_actions_for_current_node, problemDetails.max_vertex)
        for child, childcost in source_child_nodes.items():
            childHeuristic = getHeuristicFutureCostValue(child, problemDetails.end_vertex.getVertexKey())
            if not child in source_visited and not child in source_heapDictElementsHeuristicTotal:
                source_parent[child] = current_node_key
                source_heapDictElementsHeuristicTotal[child] = current_pathcost + childcost + childHeuristic
                heapq.heappush(source_heap,PriorityQueueElement(child, source_heapDictElementsHeuristicTotal[child]))
                source_heapDictElementsActualTotal[child] = current_pathcost + childcost
                source_individualPathCost[child] = childcost
            elif child in source_heapDictElementsHeuristicTotal and source_heapDictElementsHeuristicTotal[child] > (current_pathcost + childcost + childHeuristic):
                for element in source_heap:
                    if element.nodekey == child and element.cost == source_heapDictElementsHeuristicTotal[child]:
                        source_heap.remove(element)
                heapq.heapify(source_heap)
                heapq.heappush(source_heap, PriorityQueueElement(child, current_pathcost + childcost))
                source_heapDictElementsHeuristicTotal[child] = current_pathcost + childcost + childHeuristic
                source_heapDictElementsActualTotal[child] = current_pathcost + childcost
                source_individualPathCost[child] = childcost
                source_parent[child] = current_node_key
            elif child in source_visited and source_visited[child] > (current_pathcost + childcost):
                print("here")
                print(child)
                heapq.heappush(source_heap, PriorityQueueElement(child, current_pathcost + childcost))
                source_heapDictElementsHeuristicTotal[child] = current_pathcost + childcost + childHeuristic
                source_heapDictElementsActualTotal[child] = current_pathcost + childcost
                source_individualPathCost[child] = childcost
                source_parent[child] = current_node_key
                source_visited.pop(child)
    writeFailureOutputFile()
    return
