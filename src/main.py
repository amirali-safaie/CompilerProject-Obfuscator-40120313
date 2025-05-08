import sys
import os # For path manipulation
from antlr4 import FileStream, CommonTokenStream
from minic_parser.MiniCLexer import MiniCLexer
from minic_parser.MiniCParser import MiniCParser
from ast_visitor import CodeReconstructionVisitor # Assuming ast_visitor.py is in src/

from obfuscator_visitor import ObfuscatorVisitor # New visitor

def main(argv):
    # ... (arg parsing similar to before)
    if len(argv) < 2:
        print("Usage: python src/main.py <input_file.mc> [output_file.mc]")
        sys.exit(1)

    input_filepath = argv[1]
    output_filepath = None
    if len(argv) > 2:
        output_filepath = argv[2]
    else:
        base, ext = os.path.splitext(os.path.basename(input_filepath))
        output_filepath = os.path.join("output", f"{base}_obfuscated{ext}") # Changed name
        os.makedirs("output", exist_ok=True)

    input_stream = FileStream(input_filepath, encoding='utf-8')
    lexer = MiniCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniCParser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"Syntax errors found in {input_filepath}. Aborting.")
        sys.exit(1)
    else:
        print(f"Parsing {input_filepath} successful.")
        
        # --- Select Obfuscation Techniques ---
        # For now, just enable renaming. Later, this could come from CLI args.
        active_techniques = {
            "rename": True,
            "dead_code": True,
            "flatten_control_flow": True,  # Enable CFF
            "transform_expressions": True
        }
        print(f"Applying obfuscation with techniques: {active_techniques}")

        obfuscator = ObfuscatorVisitor(active_techniques)
        obfuscated_code = obfuscator.visit(tree)

        print(f"Obfuscated code will be saved to: {output_filepath}")
        with open(output_filepath, "w", encoding='utf-8') as f:
            f.write(obfuscated_code)
        print("--- Obfuscated Code ---")
        print(obfuscated_code)
        print("-------------------------")

if __name__ == '__main__':
    main(sys.argv)