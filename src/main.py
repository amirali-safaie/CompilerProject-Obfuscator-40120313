# src/main.py

import sys
import os
import argparse # For command-line arguments
from antlr4 import FileStream, CommonTokenStream, InputStream
from minic_parser.MiniCLexer import MiniCLexer
from minic_parser.MiniCParser import MiniCParser
from obfuscator_visitor import ObfuscatorVisitor # Your obfuscator visitor
# from ast_visitor import CodeReconstructionVisitor # If you want to test reconstruction separately

def main_cli():
    parser = argparse.ArgumentParser(description="Obfuscate Mini-C code.")
    parser.add_argument("input_file", help="Path to the input Mini-C file (.mc)")
    parser.add_argument("-o", "--output_file", help="Path to save the obfuscated code. Default: output/<input_file_base>_obfuscated.mc")
    
    # Technique flags (default to enabled, use --no-<technique> to disable)
    parser.add_argument("--no-rename", action="store_false", dest="rename", default=True,
                        help="Disable variable/function renaming (Enabled by default)")
    parser.add_argument("--no-dead-code", action="store_false", dest="dead_code", default=True,
                        help="Disable dead code insertion (Enabled by default)")
    parser.add_argument("--no-flatten", action="store_false", dest="flatten_control_flow", default=True,
                        help="Disable control flow flattening for 'main' (Enabled by default)")
    parser.add_argument("--no-expr-transform", action="store_false", dest="transform_expressions", default=True,
                        help="Disable expression transformation (Enabled by default)")
    
    # Add more options for bonus features if implemented
    # parser.add_argument("--enable-bonus-feature", action="store_true", help="Enable a bonus feature")

    args = parser.parse_args()

    input_filepath = args.input_file
    output_filepath = args.output_file

    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found: {input_filepath}")
        sys.exit(1)

    if not output_filepath:
        base, ext = os.path.splitext(os.path.basename(input_filepath))
        # Ensure the "output" directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, f"{base}_obfuscated{ext if ext else '.mc'}")

    # Prepare active techniques dictionary from parsed arguments
    active_techniques = {
        "rename": args.rename,
        "dead_code": args.dead_code,
        "flatten_control_flow": args.flatten_control_flow,
        "transform_expressions": args.transform_expressions
        # "bonus_feature": args.enable_bonus_feature # Example for bonus
    }

    print(f"Input file: {input_filepath}")
    print(f"Output file: {output_filepath}")
    print(f"Active obfuscation techniques: {active_techniques}")

    try:
        # 1. Read input file
        # Using InputStream.fromPath for potentially better cross-platform encoding handling with ANTLR
        input_stream = FileStream(input_filepath, encoding='utf-8')
        # Or use FileStream if preferred:
        # input_stream = FileStream(input_filepath, encoding='utf-8')


        # 2. Lexing
        lexer = MiniCLexer(input_stream)
        stream = CommonTokenStream(lexer)

        # 3. Parsing
        parser = MiniCParser(stream)
        # Optional: Add a custom error listener for more control over syntax error reporting
        # from antlr4.error.ErrorListener import ErrorListener
        # class MyErrorListener(ErrorListener):
        #     def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        #         print(f"Syntax Error at line {line}:{column} - {msg}")
        #         # You might want to raise an exception here to stop processing
        # parser.removeErrorListeners() # Remove default console error listener
        # parser.addErrorListener(MyErrorListener())

        tree = parser.program() # Start parsing from the 'program' rule

        if parser.getNumberOfSyntaxErrors() > 0:
            print(f"Syntax errors found in {input_filepath}. Obfuscation aborted.")
            # The default error listener already prints to stderr.
            # If you added a custom listener, it would handle the output.
            sys.exit(1)
        else:
            print(f"Parsing {input_filepath} successful.")
            
            # 4. Obfuscation (AST Traversal and Transformation)
            print("Applying obfuscation...")
            obfuscator = ObfuscatorVisitor(active_techniques)
            obfuscated_code = obfuscator.visit(tree)

            # 5. Write output
            print(f"Obfuscated code will be saved to: {output_filepath}")
            with open(output_filepath, "w", encoding='utf-8') as f:
                f.write(obfuscated_code)
            
            print("-" * 30)
            print("Obfuscation complete.")
            print("First few lines of obfuscated code:")
            print("\n".join(obfuscated_code.splitlines()[:15])) # Print a preview
            print("-" * 30)


    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main_cli()