import re
import time
import os
import heapq
from ucs_implementation import UCSImplementation
from bfs_implementation import BFSImplementation
from astar_implementation import AStarImplementation

def new_cmp_lt(self,a,b):
    return a.cost < b.cost

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

def processInputFile(filename):
    inputdata = {}
    with open(filename) as inputFile:
        problemDetails = ProblemDetails()
        line = inputFile.readline()
        count = 1
        while line:
            line = line.strip()
            if(count == 1):
                problemDetails.algorithm = line;
            elif(count == 2):
                vertices = line.split(' ')
                problemDetails.max_vertex = Vertex(vertices[0], vertices[1], vertices[2])
            elif(count == 3):
                vertices = line.split(' ')
                problemDetails.start_vertex = Vertex(vertices[0], vertices[1], vertices[2])
            elif(count == 4):
                vertices = line.split(' ')
                problemDetails.end_vertex = Vertex(vertices[0], vertices[1], vertices[2])
            elif(count == 5):
                problemDetails.input_size = int(line)
            elif(count == 6):
                while line:
                    line = line.strip()
                    data = line.split(' ')
                    vertex = Vertex(data[0], data[1], data[2])
                    actions = data[3:]
                    vertexkey = vertex.getVertexKey()
                    if(vertexkey in inputdata):
                        inputdata.get(vertexkey).append(actions)
                    else:
                        inputdata[vertexkey] = actions

                    line = inputFile.readline()
                    count = count + 1
            line = inputFile.readline()
            count = count + 1
    if(problemDetails.algorithm == "BFS"):
        BFSImplementation(inputdata, problemDetails)
    elif(problemDetails.algorithm == "UCS"):
        heapq.cmp_lt=new_cmp_lt
        UCSImplementation(inputdata, problemDetails)
    elif(problemDetails.algorithm == "A*"):
        heapq.cmp_lt=new_cmp_lt
        AStarImplementation(inputdata, problemDetails)

processInputFile("input8.txt")
