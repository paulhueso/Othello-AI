import copy

class Node:
    
    def __init__(self, parents, position, children):
        self.parents = copy.deepcopy(parents)
        self.position = position
        self.children = copy.deepcopy(children)
        self.currentValue = 0

    def addChild(self, numChild, weight):
        self.children.append([numChild, weight])

    def addParent(self, numParent, weight):
        self.parents.append([numParent, weight])

    def save(self, file):
        file.write(str(len(self.parents)) + " ")
        file.write(str(self.position) + " ")
        file.write(str(len(self.children)) + " ")
        for parent in self.parents:
            file.write(str(parent[0]) + "," + str(parent[1]) + " ")
        for child in self.children:
            file.write(str(child[0]) + "," + str(child[1]) + " ")
