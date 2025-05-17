# src/main.py

import sys
import os
import argparse
from antlr4 import FileStream, CommonTokenStream # Use FileStream
from minic_parser.MiniCLexer import MiniCLexer
from minic_parser.MiniCParser import MiniCParser
from obfuscator_visitor import ObfuscatorVisitor

def ask_yes_no(prompt_message):
    """Helper function to ask a yes/no question."""
    while True:
        choice = input(f"{prompt_message} (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main_cli():
    parser = argparse.ArgumentParser(
        description="Obfuscate Mini-C code. By default, if no technique flags are specified, you will be prompted interactively.",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    parser.add_argument("input_file", help="Path to the input Mini-C file (.mc)")
    parser.add_argument("-o", "--output_file", 
                        help="Path to save the obfuscated code. Default: output/<input_file_base>_obfuscated.mc")
    
    # Technique flags - now they enable the technique if present
    parser.add_argument("--rename", action="store_true",
                        help="Enable variable/function renaming.")
    parser.add_argument("--dead-code", action="store_true",
                        help="Enable dead code insertion.")
    parser.add_argument("--flatten", action="store_true", dest="flatten_control_flow", # 'dest' to match dict key
                        help="Enable control flow flattening for 'main'.")
    parser.add_argument("--expr-transform", action="store_true", dest="transform_expressions", # 'dest'
                        help="Enable expression transformation.")
    
    parser.add_argument("--all", action="store_true", help="Enable all obfuscation techniques.")
    parser.add_argument("--interactive", action="store_true", 
                        help="Force interactive prompt for techniques even if other flags are set (overrides other technique flags).")


    args = parser.parse_args()

    input_filepath = args.input_file
    output_filepath = args.output_file

    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found: {input_filepath}")
        sys.exit(1)

    if not output_filepath:
        base, ext = os.path.splitext(os.path.basename(input_filepath))
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, f"{base}_obfuscated{ext if ext else '.mc'}")

    active_techniques = {
        "rename": False,
        "dead_code": False,
        "flatten_control_flow": False,
        "transform_expressions": False
    }

    # Determine if any specific technique flag was used
    any_technique_flag_set = args.rename or \
                             args.dead_code or \
                             args.flatten_control_flow or \
                             args.transform_expressions

    if args.interactive:
        print("\n--- Interactive Obfuscation Technique Selection ---")
        active_techniques["rename"] = ask_yes_no("Enable Identifier Renaming?")
        active_techniques["dead_code"] = ask_yes_no("Enable Dead Code Insertion?")
        active_techniques["flatten_control_flow"] = ask_yes_no("Enable Control Flow Flattening (for main)?")
        active_techniques["transform_expressions"] = ask_yes_no("Enable Expression Transformation?")
    elif args.all:
        print("\n--- Enabling all obfuscation techniques ---")
        active_techniques = {key: True for key in active_techniques}
    elif any_technique_flag_set:
        print("\n--- Using specified command-line techniques ---")
        active_techniques["rename"] = args.rename
        active_techniques["dead_code"] = args.dead_code
        active_techniques["flatten_control_flow"] = args.flatten_control_flow
        active_techniques["transform_expressions"] = args.transform_expressions
    else:
        # No specific technique flags, not --all, not --interactive: Prompt interactively
        print("\nNo specific techniques selected via command line. Prompting interactively...")
        print("--- Interactive Obfuscation Technique Selection ---")
        active_techniques["rename"] = ask_yes_no("Enable Identifier Renaming?")
        active_techniques["dead_code"] = ask_yes_no("Enable Dead Code Insertion?")
        active_techniques["flatten_control_flow"] = ask_yes_no("Enable Control Flow Flattening (for main)?")
        active_techniques["transform_expressions"] = ask_yes_no("Enable Expression Transformation?")

    print(f"\nInput file: {input_filepath}")
    print(f"Output file: {output_filepath}")
    print(f"Active obfuscation techniques: {active_techniques}")
    print("-" * 40)


    try:
        input_stream = FileStream(input_filepath, encoding='utf-8')
        lexer = MiniCLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = MiniCParser(stream)
        tree = parser.program()

        if parser.getNumberOfSyntaxErrors() > 0:
            print(f"Syntax errors found in {input_filepath}. Obfuscation aborted.")
            sys.exit(1)
        else:
            print(f"Parsing {input_filepath} successful.")
            
            print("Applying obfuscation...")
            obfuscator = ObfuscatorVisitor(active_techniques)
            obfuscated_code = obfuscator.visit(tree)

            print(f"Obfuscated code will be saved to: {output_filepath}")
            with open(output_filepath, "w", encoding='utf-8') as f:
                f.write(obfuscated_code)
            
            print("-" * 30)
            print("Obfuscation complete.")
            # print("First few lines of obfuscated code:")
            # print("\n".join(obfuscated_code.splitlines()[:15])) 
            # print("-" * 30)

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