class Node():
    def __init__(self, value, level = 0):
        self.children = []
        self.value = value
        self.level = level

    def addChild(self, child):
        self.children.append(child)

    def __repr__(self):
        return f'Level: {self.level}, value: {self.value}'

class Tree():
    def __init__(self):
        self.start = None
        self.printedTree = ''

    def setStart(self, start):
        self.start = start

    def printNodes(self, node):
        tabs = '--'
        self.printedTree += f'[{node.level}]{tabs*node.level}{node.value}:\n'

        for child in node.children:
            self.printNodes(child)

        return self.printedTree

    def __repr__(self):
        if self.start:
            return self.printNodes(self.start)
        else:
            return 'There is not any nodes on this tree.'