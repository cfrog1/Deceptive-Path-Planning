# Deceptive-Path-Planning
Visualisation of a deceptive path planning algorithm (pi d3) as outlined in [Masters and Sardina](https://pdfs.semanticscholar.org/1b3e/73a4396c460ce05577b5e0dfa651f978720e.pdf).
The deceptive agent has a true goal and one or more 'fake' goals. The agent plans a path intended to keep an observer uncertain as to whether it is trying to reach its true goal or one of its fake goals.

The environment was built from scratch using PyGame.

The agent uses Breadth First Search to determine the node 'n', the point at which the observer would know which goal the agent is going for. A path to 'n' is then found using Iterative Deepening A* search, using Manhattan Distance as the heuristic.
The key difference is that when a node is evaluated, if the Manhattan distance to the goal is less than the Manhattan distance to the fake goal, the Manhattan distance to 'n' is disincentivised by multiplying it by a constant 'alpha'. Thus the agent finds a path towards 'n', prioritising 'untruthful steps'. Once 'n' is reached, Breadth First Search is used to find an optimal path to the real goal. 


