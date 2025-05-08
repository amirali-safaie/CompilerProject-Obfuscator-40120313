import sys
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from minic_parser.MiniCLexer import MiniCLexer
from minic_parser.MiniCParser import MiniCParser
# from minic_parser.MiniCListener import MiniCListener # If you were to use Listener
from minic_parser.MiniCVisitor import MiniCVisitor # We will use Visitor

# A simple visitor to print node types (for demonstration)
class PrintVisitor(MiniCVisitor):
    def visitChildren(self, node):
        print(f"Visiting: {type(node).__name__} with text: '{node.getText()[:30]}...'") # Print type and some text
        return super().visitChildren(node)

def main(argv):
    if len(argv) > 1:
        input_filepath = argv[1]
    else:
        print("Usage: python src/main.py <input_file.mc>")
        # Create a dummy test file for now
        dummy_file = "tests/input/dummy.mc"
        with open(dummy_file, "w") as f:
            f.write("int main() { int x = 10; return x; }")
        input_filepath = dummy_file
        print(f"Using dummy file: {input_filepath}")

    input_stream = FileStream(input_filepath)
    lexer = MiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniCParser(stream)
    tree = parser.program() # Start rule

    if parser.getNumberOfSyntaxErrors() > 0:
        print("Syntax errors found!")
        # ANTLR's default error listener prints to stderr.
        # You can add a custom error listener for more control.
    else:
        print("Parsing successful. AST root:", type(tree).__name__)
        # Example of using our simple visitor
        # print("\n--- AST Traversal (PrintVisitor) ---")
        # visitor = PrintVisitor()
        # visitor.visit(tree)

if __name__ == '__main__':
    main(sys.argv)