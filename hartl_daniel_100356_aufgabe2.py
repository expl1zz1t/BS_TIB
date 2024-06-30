import matplotlib.pyplot as plt
import graphviz as gv
import numpy as np

class EVENT:
    def __init__(self, name, l):
        self.name = name
        self.fail = l
        self.nodes = []
        
    def add(self, node):
        self.nodes.append(node)
        return
    
    def failure_probability(self):        
        return self.fail
    
       
class NOTNODE:
    def __init__(self,name):
        self.name = name
        self.nodes = []
        
    def add(self, node):
        self.nodes.append(node)
        return
    
    def failure_probability(self):
        self.fail = 1       
        for node in self.nodes:
            self.fail *= node.failure_probability()                       
        return (1-self.fail)


class ORNODE:
    def __init__(self,name):
        self.name = name
        self.nodes = []
        
    def add(self, node):
        self.nodes.append(node)
        return
    
    def failure_probability(self):
        self.fail = 1       
        for node in self.nodes:
            self.fail *= (1-node.failure_probability())                     
        return 1-self.fail
        

class ANDNODE:
    def __init__(self,name):
        self.name = name
        self.nodes = []        
        
    def add(self, node):
        self.nodes.append(node)
        return
    
    def failure_probability(self):
        self.fail = 1       
        for node in self.nodes:
            self.fail *= node.failure_probability()                       
        return self.fail
    

class GraphPrint:
    def __init__(self,name):
        self.name = name       
        
    def create(self,root):
        self.dot = gv.Digraph(self.name, format="png")
        
        def recurse(root):        
            for node in root.nodes:
                self.dot.node(node.name)
                self.dot.edge(root.name, node.name) 
                recurse(node)
                
        for node in root.nodes:
            self.dot.node(node.name)
            self.dot.edge(root.name, node.name) 
            recurse(node)     

    def view(self):
        return self.dot.render() 
     
# Init TOP Nodes   
TOP = ANDNODE("TOP")
A = ORNODE("A")
E1 = EVENT("1",0.1)
E2 = EVENT("2",0.1)
E3 = EVENT("3",0.1)
# Create Graphtree
TOP.add(A)
TOP.add(E1)
A.add(E2)
A.add(E3) 

# Aufgabe b Beispiel)
print ("Ausfallwahrscheinlichkeit an TOP: " +  str(TOP.failure_probability()))

# Init K1 Nodes
K1 = ANDNODE("K1")
K2 = ANDNODE("K2")
K3 = ORNODE("K3")
K4 = ANDNODE("K4")
K5 = ORNODE("K5")
NOT = NOTNODE("NOT")
G = EVENT("G", 0.1)
F = EVENT("F", 0.01)
D = EVENT("D", 0.01)
E = EVENT("E", 0.01)
C = EVENT("C", 0.001)
B = EVENT("B", 0.1)
A = EVENT("A", 0.01)

# Aufgabe a) Create Graphtree
K1.add(K2)
K1.add(NOT)
NOT.add(K3)
K2.add(D)
K2.add(E)
K3.add(F)
K3.add(G)
K2.add(K4)
K4.add(K5)
K4.add(C)
K5.add(A)
K5.add(B)

# Aufgabe b Bild1)
print ("Ausfallwahrscheinlichkeit an K1: " +  str(K1.failure_probability()))

# Aufgabe c)
print("Create TOP Graph")
test = GraphPrint("Test TOP Graph")
test.create(TOP)
test.view()

print("Create K1 Graph")
a2 = GraphPrint("K1 Graph")
a2.create(K1)
a2.view()

# Aufgabe d)
n = 1000
mean = [0.01, 0.1, 0.001, 0.01, 0.01, 0.01, 0.1]
sigma = [0.002, 0.02, 0.002, 0.002, 0.002, 0.002, 0.02]
K1_fail = np.zeros(n)

def pos_prob(mean, sigma):
    prop = np.random.normal(mean, sigma)
    while(prop < 0):
        prop = np.random.normal(mean, sigma)            
    return prop 

def createGraph():
    K1 = ANDNODE("K1")
    K2 = ANDNODE("K2")
    K3 = ORNODE("K3")
    K4 = ANDNODE("K4")
    K5 = ORNODE("K5")
    NOT = NOTNODE("NOT")
    A = EVENT("A", pos_prob(mean[0], sigma[0]))
    B = EVENT("B", pos_prob(mean[1], sigma[1]))
    C = EVENT("C", pos_prob(mean[2], sigma[2]))
    E = EVENT("E", pos_prob(mean[3], sigma[3]))
    D = EVENT("D", pos_prob(mean[4], sigma[4]))
    F = EVENT("F", pos_prob(mean[5], sigma[5]))
    G = EVENT("G", pos_prob(mean[6], sigma[6]))

    # Aufgabe a) Create Graphtree
    K1.add(K2)
    K1.add(NOT)
    NOT.add(K3)
    K2.add(D)
    K2.add(E)
    K3.add(F)
    K3.add(G)
    K2.add(K4)
    K4.add(K5)
    K4.add(C)
    K5.add(A)
    K5.add(B)
    return K1

for n in range(n):
    K1 = createGraph()
      
    #print ("Ausfallwahrscheinlichkeit an K1: " +  str(K1.failure_probability()))
    K1_fail[n] = K1.failure_probability()
    
# Histogramm der Fehlerwahrscheinlichkeiten anzeigen
plt.hist(K1_fail, bins=30, edgecolor='black')
plt.xlabel('Fehlerwahrscheinlichkeit')
plt.ylabel('Anzahl der Versuche')
plt.title('Histogramm der Fehlerwahrscheinlichkeiten')
plt.grid(True)
plt.show()