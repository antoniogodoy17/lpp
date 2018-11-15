from lexLpp import LexicalAnalyzer
from sinLpp import SyntacticAnalyzer
from semLpp import SemanticAnalyzer
import finder

def main():
    sourceCode = finder.search()

    #Lexical Analysis
    l = LexicalAnalyzer()
    l.analyze(sourceCode)
    tokens = l.tokens

    #Syntactic Analysis
    s = SyntacticAnalyzer(tokens)
    s.analyze(sourceCode)

    syntacticOutput = s.output
    syntacticVars = s.vars
    syntacticTree = s.tree

    #Semanti Analysis
    semantic = SemanticAnalyzer()
    semantic.analyze(syntacticTree.start)

    #Print tree
    print(syntacticTree)

    #Print labels
    for label in semantic.labels:
        print(label)

if __name__ == '__main__':
    main()