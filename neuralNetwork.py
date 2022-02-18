import node
import random
import board

class NeuralNetwork:
    
    def __init__(self, inputLength = 0, layersLength = [], outputLength = 0):
        self.generate(inputLength, layersLength, outputLength)
        self.board = board.Board()

    def generate(self, inputLength = 0, layersLength = [], outputLength = 0):
        self.layers = [[node.Node([],0,[]) for _ in range(inputLength)]]
        for i in range(len(layersLength)):
            self.layers.append([node.Node([], i+1, []) for _ in range(layersLength[i])])
        self.layers.append([node.Node([],len(layersLength) + 1,[]) for _ in range(outputLength)])
        self.totalLayers = len(self.layers)

    def randomFullPopulate(self):
        for numLayer in range(self.totalLayers-1):
            for numNode in range(len(self.layers[numLayer])):
                node = self.layers[numLayer][numNode]
                for numChild in range(len(self.layers[numLayer + 1])):
                    node.addChild(numChild, random.random())
                    childNode = self.layers[numLayer + 1][numChild]
                    childNode.addParent(numNode, random.random())

    def mutate(self, mutationRatio = 0.01):
        for layer in self.layers:
            for node in layer:
                # ATTENTION ! IT IS A ONE WAY MODIFICATION
                for edge in node.children:
                    if(random.random() < mutationRatio):
                        edge[1] = random.random()
    
    def calculLayer(self, layer, posChild):
        total = 0
        for node in layer:
            for i in range(len(node.children)):
                if(node.children[i][0] == posChild):
                    total += node.currentValue*node.children[i][1]
        return total
    
    def initInput(self,board,color):
        if(color == self.board.player1):
            for j in range(len(board)):
                for i in range(len(board[j])):
                    if(board[j][i] == self.board.player1):
                        self.layers[0][i + j* 8].currentValue = 1
                    elif(board[j][i] == self.board.player2):
                        self.layers[0][i + j* 8].currentValue = 0
                    else:
                        self.layers[0][i + j* 8].currentValue = 0.5
        else:
            for j in range(len(board)):
                for i in range(len(board[j])):
                    if(board[j][i] == self.board.player1):
                        self.layers[0][i + j* 8].currentValue = 0
                    elif(board[j][i] == self.board.player2):
                        self.layers[0][i + j* 8].currentValue = 1
                    else:
                        self.layers[0][i + j* 8].currentValue = 0.5
    
    def choosePlay(self, board, color):
        self.initInput(board, color)
        for numLayer in range(1, len(self.layers)):
            for posChild in range(len(self.layers[numLayer])):
                total = self.calculLayer(self.layers[numLayer - 1], posChild)
                self.layers[numLayer][posChild].currentValue = total
        allPlay = [0 for _ in range(len(board[0])*len(board[1]))]
        for i in range(len(self.layers[-1])):
            allPlay[i] += self.layers[-1][i].currentValue
        return allPlay
    
    def chooseProposition(self, board, color):
        allMoves = self.choosePlay(board, color)
        slots = self.board.getAllSlotsAvailable(board, color)
        bestMove = (-1, -1000000)
        for numSlot in range(len(slots)):
            x,y = slots[numSlot]
            valueMove = allMoves[y * 8 + x]
            if(valueMove > bestMove[1]):
                bestMove = (numSlot, valueMove)
        return bestMove[0]

    def save(self, fileName = "best.txt"):
        print("Saving to " + fileName + "... ", end="")
        with open(fileName, "w") as f:
            for layer in self.layers:
                f.write(str(len(layer)) + " ")
            f.write("\n")
            for layer in self.layers:
                for node in layer:
                    node.save(f)
                    f.write("\n")
        print("DONE !")

    def loadNode(self, line, numNode):
        values = line.split(" ")
        values.remove("\n")
        position = int(values[1])
        parents = []
        children = []
        i = 0
        for i in range(3,int(values[0])+3):
            posParent, weight = values[i].split(",")
            parents.append([posParent, weight])
        for i in range(int(values[0]) + 3,len(values)):
            posChild, weight = values[i].split(",")
            children.append([posChild, weight])
        self.layers[position][numNode] = node.Node(parents, position, children)

    def load(self, fileName = "best.txt"):
        print("Loading from " + fileName + "... ", end="")
        try:
            with open(fileName, "r") as f:
                file = f.readlines()
            layersLength = file[0].split(" ")
            layersLength.remove("\n")
            self.layers = []
            i = 0
            for length in layersLength:
                self.layers.append([node.Node([], i, []) for _ in range(int(layersLength[i]))])
                i += 1
            numLine = 1
            numLayer = 0
            numNode = 0
            while(numLine < len(file)):
                if(numNode == int(layersLength[numLayer])):
                    numLayer += 1
                    numNode = 0
                self.loadNode(file[numLine], numNode)
                numNode += 1
                numLine += 1
            self.totalLayers = len(self.layers)
            print("DONE !")
        except(FileNotFoundError):
            print("FAILED !!!! GENERATING RANDOM AI !")
            self.generate(64, [16,16,16], 64)
