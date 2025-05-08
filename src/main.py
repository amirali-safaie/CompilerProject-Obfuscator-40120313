import sys
import os # For path manipulation
from antlr4 import FileStream, CommonTokenStream
from minic_parser.MiniCLexer import MiniCLexer
from minic_parser.MiniCParser import MiniCParser
from ast_visitor import CodeReconstructionVisitor # Assuming ast_visitor.py is in src/

def main(argv):
    if len(argv) < 2:
        print("Usage: python src/main.py <input_file.mc> [output_file.mc]")
        sys.exit(1)

    input_filepath = argv[1]
    output_filepath = None
    if len(argv) > 2:
        output_filepath = argv[2]
    else:
        # Default output path
        base, ext = os.path.splitext(os.path.basename(input_filepath))
        output_filepath = os.path.join("output", f"{base}_reconstructed{ext}")
        os.makedirs("output", exist_ok=True)


    input_stream = FileStream(input_filepath, encoding='utf-8')
    lexer = MiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniCParser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"Syntax errors found in {input_filepath}. Aborting.")
        # ANTLR's default error listener prints to stderr.
        # You can add a custom error listener for more control if needed.
        sys.exit(1)
    else:
        print(f"Parsing {input_filepath} successful.")
        
        print("Reconstructing code...")
        reconstructor = CodeReconstructionVisitor()
        reconstructed_code = reconstructor.visit(tree)

        print(f"Reconstructed code will be saved to: {output_filepath}")
        with open(output_filepath, "w", encoding='utf-8') as f:
            f.write(reconstructed_code)
        print("--- Reconstructed Code ---")
        print(reconstructed_code)
        print("-------------------------")


if __name__ == '__main__':
    main(sys.argv)