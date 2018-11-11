from lexLpp import tokens
from sinLpp import tree, r, vars
from ast import Tree, Node
import finder

for key in vars.keys():
    print(f'{key}: {vars[key]}')

print(tree)