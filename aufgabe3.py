import matplotlib.pyplot as plt
import graphviz as gv
import numpy as np

class STATE:
    def __init__(self, name, num):
        self.name = name
        self.num = num
        return

class TRANSITION:
    def __init__(self, source, destination, name, rate):
        self.source = source
        self.destination = destination
        self.name = name
        self.rate = rate
        return
    
class MARKOV:
    def __init__(self, name, dt=1.0):
        self.nodes = []
        self.transitions = []
        self.name = name
        self.transition_matrix = None
        return
    
    def state(self, node):
        self.nodes.append(node)
        return
    
    def transition(self, edge):
        self.transitions.append(edge)
        return
    
    def build_transition_matrix(self):
        n = len(self.nodes)
        P = np.zeros((n, n))
        for t in self.transitions:
            i = t.source.num
            j = t.destination.num
            P[i, j] = t.rate
        for i in range(n):
            P[i, i] = 1 - np.sum(P[i])
        self.transition_matrix = P
        np.set_printoptions(precision=3)
        print(P)
        return P

    def probability(self, hours, state):
        self.build_transition_matrix()
        prob_state = np.zeros(len(self.nodes))
        prob_state[0] = 1
        for _ in range(hours):
            prob_state = np.dot(prob_state, self.transition_matrix)
        return prob_state[state-1]
    
    def plot(self):
        self.dot = gv.Digraph(self.name, format="png")
        # Set the graph to left-to-right layout
        self.dot.attr(rankdir='LR')
               
        for node in self.nodes:
            self.dot.node(node.name, shape="circle")
                
        for node in self.transitions:
            self.dot.edge(node.source.name, node.destination.name, label=node.name)
        
        return self.dot.render()    
     
  
#Beispiel    
B = MARKOV("Beispiel")
B_S1 = STATE('S1',0)
B_S2 = STATE('S2',1)
B.state(B_S1)
B.state(B_S2)
B.transition(TRANSITION(B_S1, B_S2, 'l12', 1000))
prob_days = B.probability(1 * 24, 1)
print(f"Verfügbarkeit nach 1 Tagen: {prob_days:.6f}\n")
B.plot()

#Aufgabe 3
M = MARKOV("Markov Graph")
S1 = STATE('S1\nNormal',0)
S2 = STATE('S2\nDD\nEine SPS',1)
S3 = STATE('S3\nDD\nBeide SPS',2)
S4 = STATE('S4\nDD\nEingang',3)
S5 = STATE('S5\nDD\nAusgang',4)
S6 = STATE('S6\nSicher',5)

#Berechnung von lamda und mü
lam = 3000 / 10e9
mu  = 1 / 8

print(lam)

M.state(S1)
M.state(S2)
M.state(S3)
M.state(S4)
M.state(S5)
M.state(S6)

M.transition(TRANSITION(S1, S2, '2λ12', 2*lam))
M.transition(TRANSITION(S1, S3, 'λ13', lam))
M.transition(TRANSITION(S1, S4, 'λ14', lam))
M.transition(TRANSITION(S1, S5, 'λ15', lam))
M.transition(TRANSITION(S1, S6, '2λ16', 2*lam))
M.transition(TRANSITION(S2, S3, 'λ23', lam))
M.transition(TRANSITION(S2, S4, 'λ24', lam))
M.transition(TRANSITION(S2, S5, 'λ25', lam))
M.transition(TRANSITION(S2, S6, 'μ26', mu))
M.transition(TRANSITION(S3, S4, 'λ34', lam))
M.transition(TRANSITION(S3, S5, 'λ35', lam))
M.transition(TRANSITION(S3, S6, 'μ26', mu))
M.transition(TRANSITION(S4, S6, 'μ46', mu))
M.transition(TRANSITION(S5, S6, 'μ56', mu))

# Simulation
prob_days = M.probability(40 * 24, 1)
print(f"Verfügbarkeit nach 40 Tagen: {prob_days:.6f}\n")

prob_days = M.probability(6 * 30 * 24, 1)
print(f"Verfügbarkeit nach 6 Monaten: {prob_days:.6f}\n")

prob_days = M.probability(12 * 365 * 24, 1)
print(f"Verfügbarkeit nach 12 Jahren: {prob_days:.6f}\n")

print("Plot Markov Graph ... ")
M.plot()
