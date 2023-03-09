from collections import deque
import re
import time
import os

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

class ProblemDetails:
    def __init__(self):
        pass

    def set_values(self, algorithm, max_vertex, start_vertex, end_vertex, input_size):
        self.algorithm = algorithm
        self.max_vertex = max_vertex
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.input_size = input_size

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

def performAction(vertex, actions, max_vertex):
    adjacent_nodes = []
    for act in actions:
        act = int(act)
        x = vertex.x
        y = vertex.y
        z = vertex.z
        x = x + action_codes[act-1][0]
        y = y + action_codes[act-1][1]
        z = z + action_codes[act-1][2]
        if(isVertexInBoundary(x, y, z, max_vertex)):
            adjacent_nodes.append(formVertexKey([x ,y, z]))
    return adjacent_nodes

def writeSuccessOutputFile(parent, goal_node_key, root_node_key):
    outputfilename = "output.txt"
    steps = []
    steps.append(goal_node_key)
    while(goal_node_key != root_node_key):
        steps.append(parent[goal_node_key])
        goal_node_key = parent[goal_node_key]
    steps.reverse()
    with open(outputfilename, 'w') as ouputfile:
        ouputfile.write(str(len(steps) - 1))
        ouputfile.write("\n")
        ouputfile.write(str(len(steps)))
        ouputfile.write("\n")
        count = 0
        for step in steps:
            stepkey = getVertexNodeFromKey(step)
            ouputfile.write(str(stepkey.x) + " " + str(stepkey.y) + " " + str(stepkey.z) + " " + str(count))
            ouputfile.write("\n")
            if(count == 0):
                 count = 1

def writeFailureOutputFile():
    outputfilename = "output.txt"
    with open(outputfilename, 'w') as ouputfile:
        ouputfile.write("FAIL")

def BFSImplementation(inputData, problemDetails):
    rootnodekey = problemDetails.start_vertex.getVertexKey()
    queueSetElements = set()
    queue = deque(maxlen = problemDetails.input_size)
    visited = set()
    visited.add(rootnodekey)
    queue.append(rootnodekey)
    queueSetElements.add(rootnodekey)
    parent = {}
    parent[rootnodekey] = -1
    while(len(queue) != 0):
        current_node_key = queue.popleft()
        queueSetElements.remove(current_node_key)
        if(current_node_key == problemDetails.end_vertex.getVertexKey()):
            writeSuccessOutputFile(parent, current_node_key, rootnodekey)
            return
        actions_for_current_node = inputData[current_node_key]
        child_node_keys = performAction(getVertexNodeFromKey(current_node_key), actions_for_current_node, problemDetails.max_vertex)
        for child in child_node_keys:
            if not child in visited and not child in queueSetElements:
                parent[child] = current_node_key
                if(child == problemDetails.end_vertex.getVertexKey()):
                    writeSuccessOutputFile(parent, child, rootnodekey)
                    return
                queue.append(child)
                queueSetElements.add(child)
                visited.add(child)
    writeFailureOutputFile()
    return
