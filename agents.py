from queue import Queue
import math

class DeceptiveAgent():
    def __init__(self):
        return

    def findPath(self, env):

        #Find a, b, c. calculate beta.
        a = len(self.bfs(env, env.agent, env.goal))
        b = len(self.bfs(env, env.agent, env.fakeGoal))
        c = len(self.bfs(env, env.goal, env.fakeGoal))
        beta = (c + a - b) * 0.5 * env.BLOCK_SIZE
        print(f'a b c: {a} {b} {c}')

        #Calculate vector from real goal to fake goal. Node t is at real goal + beta*unit vector
        vec = (env.fakeGoal[0] - env.goal[0], env.fakeGoal[1] - env.goal[1])
        vec_len = math.sqrt(math.pow(vec[0],2) + math.pow(vec[1],2))
        vec = (vec[0] / vec_len, vec[1] / vec_len) #Unit vector
        (t_x,t_y) = (int(env.goal[0] + (env.BLOCK_SIZE + beta)*vec[0]),  int(env.goal[1] + (env.BLOCK_SIZE + beta)*vec[1]))

        #Making sure t is at a valid location
        t = (t_x - (t_x % env.BLOCK_SIZE), t_y - (t_y % env.BLOCK_SIZE))
        if not env.valid(t):
            print("Improper positioning, try again")
            exit()

        print(f'agent loc: {env.agent}')
        print(f'goal loc: {env.goal}')
        print(f'fake loc: {env.fakeGoal}')
        print(f'beta: {beta}')
        print(f't: {t}')

        path_t = self.idaStar(env, t)
        path_goal = self.bfs(env, t, env.goal)
        return path_t + path_goal

    def bfs(self, env, start, goal):
        myq = Queue()
        startNode = (start, '', 0, []) #Node contains location, action taken, cost, path taken
        myq.put(startNode)
        visited = set() #Maintain set of visited nodes to prevent backtracking

        while myq:
            node = myq.get()
            state, action, cost, path = node

            if state not in visited :
                visited.add(state)
                if state == goal :
                    path = path + [(state, action)]
                    break

                succNodes = env.getSuccessors(state)
                for succNode in succNodes:
                    succState, succAction, succCost = succNode
                    newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                    myq.put(newNode)
        actions = [action[1] for action in path]
        del actions[0]
        return actions

    def idaStar(self, env, t):

        #Initialise node in s0 and threshold to h(s0)
        startNode = (env.agent, '', 0, [])
        threshold = self.manhattanDistance(env, env.agent, t)

        #Iterate search with increasing threshold until goal state is found
        node = startNode
        while True:
            state, action, _, path = node
            if state == t:
                break
            visited = set()
            node, threshold = self.newSearch(startNode, threshold, visited, env, t)
        
        #Add on action to get to final goal state, then return total list of actions 
        path = path + [(state, action)]
        actions = [action[1] for action in path]
        del actions[0]
        return actions

    def newSearch(self, startNode, threshold, visited, env, t):
        state, action, cost, path = startNode
        visited.add(state)

        #Additional manipulation to incentivise deceptive steps, alpha=2
        h_goal = self.manhattanDistance(env, state, env.goal)
        h_fake = self.manhattanDistance(env, state, env.fakeGoal)
        h_t = self.manhattanDistance(env, state, t)
        if h_goal < h_fake:
            h_t = 1.3*h_t
        f_score = cost + h_t
        #Return if f-score higher than threshold or it is the goal state
        if f_score > threshold:
            return startNode, f_score
        if state == t:
            return startNode, f_score

        #Otherwise, expand successor nodes
        min_f_score = float('Inf')
        min_node = startNode
        succNodes = env.getSuccessors(state)
        for succNode in succNodes:
            succState, succAction, succCost = succNode
            if succState not in visited:
                #Recursively calls newSearch until threshold is reached
                newNode = (succState, succAction, cost + succCost, path + [(state, action)])
                newNode, new_f_score = self.newSearch(newNode, threshold, visited, env, t)

                #If returned node is goal, return that node
                if newNode[0] == t:
                    return newNode, threshold

                #Minimum of threshold-reaching f-scores taken as new threshold
                if new_f_score < min_f_score:
                    min_f_score = new_f_score
                    min_node = newNode

        return min_node, min_f_score

    def manhattanDistance(self, env, xy1, xy2):
    #Returns the Manhattan distance between points xy1 and xy2
        return (abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])) / env.BLOCK_SIZE