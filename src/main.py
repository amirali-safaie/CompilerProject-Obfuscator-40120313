# src/main.py

import sys
import os
import argparse
import time
import subprocess # To call external compiler and run programs
import tempfile   # To create temporary .c files

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

def compile_and_time(source_code_str, source_name_for_log, include_stdio_header=False, compiler="gcc", temp_dir_base=None):
    """
    Compiles a C source string, times its execution, and returns runtime.
    Returns (runtime_seconds, executable_path_for_debug) or (None, None) on failure.
    The executable is created in a temporary directory.
    """
    print(f"\n--- Processing for Runtime: {source_name_for_log} ---")
    
    # Use a persistent temporary directory for the session if provided, else create one per call
    # This is mainly for debugging if you want to inspect the .c and .exe files.
    # For normal operation, tempfile.TemporaryDirectory() is fine.
    # If temp_dir_base is None, it means this function controls its temp dir lifecycle.

    context_manager = tempfile.TemporaryDirectory(dir=temp_dir_base) if temp_dir_base else tempfile.TemporaryDirectory()

    with context_manager as temp_dir:
        source_file_name = f"{source_name_for_log}.c"
        exe_file_name = f"{source_name_for_log}_exe" # Add .exe for Windows if compiler does it automatically
        if os.name == 'nt' and not exe_file_name.endswith(".exe"):
            exe_file_name += ".exe"


        source_file_path = os.path.join(temp_dir, source_file_name)
        exe_path = os.path.join(temp_dir, exe_file_name)

        code_to_compile = source_code_str
        if include_stdio_header:
            code_to_compile = "#include <stdio.h>\n\n" + code_to_compile
        
        with open(source_file_path, "w", encoding='utf-8') as f:
            f.write(code_to_compile)

        compile_command = [compiler, source_file_path, "-o", exe_path]
        if compiler == "gcc" or compiler == "clang": # Common flags
            compile_command.extend(["-w"]) # Suppress warnings for cleaner output, optional

        print(f"Compiling with: {' '.join(compile_command)}")
        try:
            compile_proc = subprocess.run(compile_command, capture_output=True, text=True, check=False, timeout=15)
        except FileNotFoundError:
            print(f"ERROR: Compiler '{compiler}' not found. Make sure it's in your system PATH.")
            return None, None
        except subprocess.TimeoutExpired:
            print(f"ERROR: Compilation timed out for {source_name_for_log}.")
            return None, None


        if compile_proc.returncode != 0:
            print(f"ERROR: Compilation failed for {source_name_for_log}.")
            print("Compiler errors/warnings:")
            if compile_proc.stdout: print("STDOUT:\n" + compile_proc.stdout)
            if compile_proc.stderr: print("STDERR:\n" + compile_proc.stderr)
            return None, None

        # print(f"Compilation successful: {exe_path}") # exe_path is temporary

        print(f"Running compiled program for {source_name_for_log}...")
        exec_start_time = time.perf_counter()
        try:
            run_proc = subprocess.run([exe_path], capture_output=True, text=True, timeout=10) # 10s timeout for execution
        except subprocess.TimeoutExpired:
            print(f"ERROR: Program execution timed out for {source_name_for_log}.")
            return None, exe_path # Return path for potential cleanup if needed
        exec_end_time = time.perf_counter()
        
        execution_time = exec_end_time - exec_start_time
        
        print(f"Output of {source_name_for_log}:")
        print(run_proc.stdout.strip() if run_proc.stdout else "<no stdout>")
        if run_proc.stderr and run_proc.stderr.strip():
             print(f"Runtime Errors/Warnings from {source_name_for_log}:")
             print(run_proc.stderr.strip())
        print(f"Execution time for {source_name_for_log}: {execution_time:.6f} seconds")
        
        # Return execution time and the path (though path is in temp dir that will be cleaned)
        return execution_time, exe_path 
    # Temp directory is cleaned up here

def main_cli():
    parser = argparse.ArgumentParser(
        description="Obfuscate Mini-C code. By default, if no technique flags are specified, you will be prompted interactively.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Path to the input Mini-C file (.mc)")
    parser.add_argument("-o", "--output_file", 
                        help="Path to save the obfuscated code. Default: output/<input_file_base>_obfuscated.mc")
    
    parser.add_argument("--rename", action="store_true", help="Enable variable/function renaming.")
    parser.add_argument("--dead-code", action="store_true", help="Enable dead code insertion.")
    parser.add_argument("--flatten", action="store_true", dest="flatten_control_flow",
                        help="Enable control flow flattening for 'main'.")
    parser.add_argument("--expr-transform", action="store_true", dest="transform_expressions",
                        help="Enable expression transformation.")
    parser.add_argument("--meaningless-funcs", action="store_true",
                        help="Enable adding meaningless recursive functions.")
    
    parser.add_argument("--all", action="store_true", help="Enable all defined obfuscation techniques.")
    parser.add_argument("--interactive", action="store_true", 
                        help="Force interactive prompt for techniques.")
    parser.add_argument("--compare-runtime", action="store_true",
                        help="Compile and compare runtime of original and obfuscated code (requires GCC/Clang in PATH).")
    parser.add_argument("--compiler", default="gcc", choices=["gcc", "clang"],
                        help="C compiler to use for runtime comparison (default: gcc).")

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
        "rename": False, "dead_code": False, "flatten_control_flow": False,
        "transform_expressions": False, "meaningless_funcs": False
    }
    all_technique_keys = list(active_techniques.keys())


    any_technique_flag_set = args.rename or args.dead_code or args.flatten_control_flow or \
                             args.transform_expressions or args.meaningless_funcs

    if args.interactive:
        print("\n--- Interactive Obfuscation Technique Selection ---")
        active_techniques["rename"] = ask_yes_no("Enable Identifier Renaming?")
        active_techniques["dead_code"] = ask_yes_no("Enable Dead Code Insertion?")
        active_techniques["flatten_control_flow"] = ask_yes_no("Enable Control Flow Flattening (for main)?")
        active_techniques["transform_expressions"] = ask_yes_no("Enable Expression Transformation?")
        active_techniques["meaningless_funcs"] = ask_yes_no("Enable Adding Meaningless Recursive Functions?")
    elif args.all:
        print("\n--- Enabling all obfuscation techniques ---")
        active_techniques = {key: True for key in all_technique_keys}
    elif any_technique_flag_set:
        print("\n--- Using specified command-line techniques ---")
        active_techniques["rename"] = args.rename
        active_techniques["dead_code"] = args.dead_code
        active_techniques["flatten_control_flow"] = args.flatten_control_flow
        active_techniques["transform_expressions"] = args.transform_expressions
        active_techniques["meaningless_funcs"] = args.meaningless_funcs
    else:
        print("\nNo specific techniques selected via command line. Defaulting to interactive prompt...")
        print("--- Interactive Obfuscation Technique Selection ---")
        active_techniques["rename"] = ask_yes_no("Enable Identifier Renaming?")
        active_techniques["dead_code"] = ask_yes_no("Enable Dead Code Insertion?")
        active_techniques["flatten_control_flow"] = ask_yes_no("Enable Control Flow Flattening (for main)?")
        active_techniques["transform_expressions"] = ask_yes_no("Enable Expression Transformation?")
        active_techniques["meaningless_funcs"] = ask_yes_no("Enable Adding Meaningless Recursive Functions?")


    print(f"\nInput file: {input_filepath}")
    print(f"Output file: {output_filepath}")
    print(f"Active obfuscation techniques: {active_techniques}")
    print("-" * 40)

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            original_code_content = f.read()
        
        input_stream = FileStream(input_filepath, encoding='utf-8')
        lexer = MiniCLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = MiniCParser(stream)
        tree = parser.program()

        if parser.getNumberOfSyntaxErrors() > 0:
            print(f"Syntax errors found in {input_filepath}. Obfuscation aborted.")
            sys.exit(1)

        print(f"Parsing {input_filepath} successful.")
        print("Applying obfuscation...")
        obfuscator = ObfuscatorVisitor(active_techniques)
        obfuscated_code_raw = obfuscator.visit(tree)

        final_obfuscated_code_to_write = obfuscated_code_raw # Base obfuscated code
        # The obfuscator.visitProgram now prepends MRFs.
        # We only add stdio.h here if needed for compilation by GCC/Clang.
        
        print(f"Obfuscated code (raw, before potential stdio.h) will be saved to: {output_filepath}")
        with open(output_filepath, "w", encoding='utf-8') as f:
            # Write the version that has stdio.h if needed, for easier direct compilation
            # For runtime comparison, compile_and_time handles adding stdio.h separately
            temp_obf_code_for_file = obfuscated_code_raw
            if obfuscator.uses_stdio:
                 temp_obf_code_for_file = "#include <stdio.h>\n\n" + obfuscated_code_raw
            f.write(temp_obf_code_for_file)
        
        print("Obfuscation complete.")

        if args.compare_runtime:
            print("\n--- Runtime Comparison ---")
            with tempfile.TemporaryDirectory(prefix="minic_obf_runtime_") as session_temp_dir:
                print(f"Using temporary directory for compilation: {session_temp_dir}")

                # --- SWAPPED ORDER STARTS HERE ---

                # 1. Compile and Time OBFUSCATED Code First
                # For obfuscated code, use the uses_stdio flag set by the visitor
                print("\n=> Processing OBFUSCATED code first...")
                obfuscated_runtime, _ = compile_and_time(
                    obfuscated_code_raw, 
                    "obfuscated", 
                    include_stdio_header=obfuscator.uses_stdio, # Assuming 'obfuscator' instance is available
                    compiler=args.compiler, 
                    temp_dir_base=session_temp_dir
                )

                # 2. Compile and Time ORIGINAL Code Second
                # Check if original code itself used stdio (heuristically or assume yes for printf/scanf)
                print("\n=> Processing ORIGINAL code second...")
                original_uses_stdio_heuristic = "printf" in original_code_content or "scanf" in original_code_content
                original_runtime, _ = compile_and_time(
                    original_code_content, 
                    "original", 
                    include_stdio_header=original_uses_stdio_heuristic, 
                    compiler=args.compiler, 
                    temp_dir_base=session_temp_dir
                )
                
                # --- SWAPPED ORDER ENDS HERE ---


                if original_runtime is not None and obfuscated_runtime is not None:
                    print("\n--- Summary of Runtimes ---")
                    # Print original first for consistent reporting, even if run second
                    print(f"Original code execution time:   {original_runtime:.6f} seconds")
                    print(f"Obfuscated code execution time: {obfuscated_runtime:.6f} seconds")
                    if original_runtime > 1e-9 : 
                        overhead = ((obfuscated_runtime - original_runtime) / original_runtime) * 100 
                        print(f"Runtime overhead: {overhead:.2f}%")
                    else:
                        print("Runtime overhead: N/A (original runtime was zero or too small)")
                else:
                    print("Could not compare runtimes due to compilation or execution errors.")
            print("Temporary compilation files have been removed.")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filepath}' not found.")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("ERROR: A subprocess (compilation or execution) timed out.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main_cli()