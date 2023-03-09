Input file describes the maze configuration, the initial entrance grid location, the exit grid location, and characteristics of the agent. 

You should find the optimal path from the initial entrance grid location to that exit grid location. A path is composed of a sequence of legal moves. Each legal move consists of moving the agent from a point to one of its 18 neighbor points, using one of the elementary actions that are available at
the current location. Your agent must search through possible paths of movements and find the optimal path to travel from the entrance to the exit, and then output the results.

To find the solution you will use the following algorithms:
- Breadth-first search (BFS)
- Uniform-cost search (UCS)
- A* search (A*).

Input: The file input.txt in the current directory of your program will be formatted as follows:
● First line: Instruction of which algorithm to use, as a string: BFS, UCS or A*
● Second line: Three strictly positive 32-bit integers separated by one space
character, for the size of X, Y, and Z dimensions, respectively.
● Third line: Three non-negative 32-bit integers for the entrance grid location.
● Fourth line: Three non-negative 32-bit integers for the exit grid location.
● Fifth line: A strictly positive 32-bit integer N, indicating the number of grids in the
maze where there are actions available.
● Next N lines: Three non-negative 32-bit integers separated by one space character, for
the location of the grid, followed by a list of actions that are available at

Output: The file output.txt that your program creates in the current directory should be
formatted as follows:
● First line: A single integer C, indicating the total cost of your found solution. If no
solution was found (the exit grid location is unreachable from the given entrance, then
write the word “FAIL” (all capital) without any other lines following.
● Second line: A single integer N, indicating the total number of steps in your solution
including the starting position.
● N lines: Report the steps in your solution travelling from the entrance grid
location to the exit grid location as were given in the input.txt file. Write out one line per step with cost. Each line should contain a
tuple of four integers: X, Y, Z, Cost, separated by a space character,
specifying the grid location with the single step cost to visit that
grid location by your agent from its last grid during its traveling
from the entrance to the exit.
