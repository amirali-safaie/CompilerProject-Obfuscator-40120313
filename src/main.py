# src/main.py

import sys
import os
import argparse
import time
import subprocess
import tempfile

from antlr4 import FileStream, CommonTokenStream 
from minic_parser.MiniCLexer import MiniCLexer
from minic_parser.MiniCParser import MiniCParser
from obfuscator_visitor import ObfuscatorVisitor

def ask_yes_no(prompt_message):
    while True:
        choice = input(f"{prompt_message} (y/n): ").lower().strip()
        if choice in ['y', 'yes']: return True
        if choice in ['n', 'no']: return False
        print("Invalid input. Please enter 'y' or 'n'.")

def compile_and_run(source_code_str, source_name_for_log, 
                    include_stdio_header=False, include_stdbool_header=False,
                    compiler="gcc", temp_dir_base=None, verbose_output=False): # Added verbose_output
    """
    Compiles C source string and runs it, returning execution time, stdout, stderr.
    """
    if verbose_output:
        print(f"\n--- Processing for Execution: {source_name_for_log} ---")
    
    context_manager = tempfile.TemporaryDirectory(dir=temp_dir_base, prefix=f"{source_name_for_log}_exec_") if temp_dir_base else tempfile.TemporaryDirectory(prefix=f"{source_name_for_log}_exec_")

    with context_manager as temp_dir:
        source_file_name = f"{source_name_for_log}_temp_src.c"
        exe_file_name = f"{source_name_for_log}_temp_exe"
        if os.name == 'nt' and not exe_file_name.endswith(".exe"): exe_file_name += ".exe"
        source_file_path = os.path.join(temp_dir, source_file_name)
        exe_path = os.path.join(temp_dir, exe_file_name)

        headers_to_add = []
        if include_stdio_header: headers_to_add.append("#include <stdio.h>")
        if include_stdbool_header: headers_to_add.append("#include <stdbool.h>")
        
        code_to_compile = source_code_str
        if headers_to_add:
            code_to_compile = "\n".join(headers_to_add) + "\n\n" + source_code_str
        
        with open(source_file_path, "w", encoding='utf-8') as f: f.write(code_to_compile)

        compile_command = [compiler, source_file_path, "-o", exe_path]
        if compiler in ["gcc", "clang"]: compile_command.extend(["-w"]) 

        if verbose_output:
            print(f"Compiling ({source_name_for_log}) with: {' '.join(compile_command)}")
        try:
            compile_proc = subprocess.run(compile_command, capture_output=True, text=True, check=False, timeout=20)
        except FileNotFoundError:
            if verbose_output: print(f"ERROR: Compiler '{compiler}' not found for {source_name_for_log}. Ensure it's in PATH.")
            return None, None, f"Compiler '{compiler}' not found"
        except subprocess.TimeoutExpired:
            if verbose_output: print(f"ERROR: Compilation timed out for {source_name_for_log}.")
            return None, None, "Compilation timed out"

        if compile_proc.returncode != 0:
            if verbose_output:
                print(f"ERROR: Compilation failed for {source_name_for_log}.")
                err_details = "Compilation STDERR:\n" + (compile_proc.stderr or "<no stderr>")
                if compile_proc.stdout: err_details += "\nCompilation STDOUT:\n" + compile_proc.stdout
                print(err_details)
            return None, None, (compile_proc.stderr or "Compilation failed without stderr")
            
        if verbose_output:
            print(f"Running compiled program for {source_name_for_log}...")
        exec_start_time = time.perf_counter()
        try:
            run_proc = subprocess.run([exe_path], capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired:
            if verbose_output: print(f"ERROR: Program execution timed out for {source_name_for_log}.")
            return None, None, "Execution timed out"
        exec_end_time = time.perf_counter()
        
        execution_time = exec_end_time - exec_start_time
        
        if verbose_output: # Only print these if verbose_output is True
            print(f"Output of {source_name_for_log}:")
            print(run_proc.stdout.strip() if run_proc.stdout else "<no stdout>")
            if run_proc.stderr and run_proc.stderr.strip():
                 print(f"Runtime Errors/Warnings from {source_name_for_log}:")
                 print(run_proc.stderr.strip())
            print(f"Execution time for {source_name_for_log}: {execution_time:.6f} seconds") # Still useful here
        
        return execution_time, run_proc.stdout, run_proc.stderr

def main_cli():
    parser = argparse.ArgumentParser(
        description="Obfuscate Mini-C code.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # ... (all argparse arguments remain the same) ...
    parser.add_argument("input_file", help="Path to the input Mini-C file (.mc)")
    parser.add_argument("-o", "--output_file", 
                        help="Path to save the obfuscated code. Default: output/<input_file_base>_obfuscated.mc")
    
    parser.add_argument("--rename", action="store_true", help="Enable variable/function renaming.")
    parser.add_argument("--dead-code", action="store_true", help="Enable dead code insertion.")
    parser.add_argument("--flatten", action="store_true", dest="flatten_control_flow", help="Enable control flow flattening for 'main'.")
    parser.add_argument("--expr-transform", action="store_true", dest="transform_expressions", help="Enable expression transformation.")
    parser.add_argument("--meaningless-funcs", action="store_true", help="Enable adding meaningless recursive functions.")
    
    parser.add_argument("--all", action="store_true", help="Enable all defined obfuscation techniques.")
    parser.add_argument("--interactive", action="store_true", help="Force interactive prompt for techniques.")
    parser.add_argument("--compare-runtime", action="store_true", help="Compile and compare EXECUTION time of original and obfuscated code.")
    parser.add_argument("--compiler", default="gcc", choices=["gcc", "clang"], help="C compiler to use (default: gcc).")
    parser.add_argument("--verbose-runtime", action="store_true", help="Show detailed stdout/stderr during runtime comparison.")


    args = parser.parse_args()
    # ... (input/output filepath logic remains same) ...
    input_filepath = args.input_file
    output_filepath = args.output_file

    if not os.path.exists(input_filepath):
        print(f"Error: Input file not found: {input_filepath}"); sys.exit(1)

    if not output_filepath:
        base, ext = os.path.splitext(os.path.basename(input_filepath))
        output_dir = "output"; os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, f"{base}_obfuscated{ext if ext else '.mc'}")

    active_techniques = {
        "rename": False, "dead_code": False, "flatten_control_flow": False,
        "transform_expressions": False, "meaningless_funcs": False
    }
    all_technique_keys = list(active_techniques.keys())
    # Correctly check if any technique flag specifically provided by user is True
    any_technique_flag_set = any(getattr(args, key, False) for key in all_technique_keys if hasattr(args, key) and isinstance(getattr(args, key), bool) and getattr(args, key) is True)


    if args.interactive:
        print("\n--- Interactive Obfuscation Technique Selection ---")
        for key in all_technique_keys:
            active_techniques[key] = ask_yes_no(f"Enable {key.replace('_', ' ').title()}?")
    elif args.all:
        print("\n--- Enabling all obfuscation techniques ---")
        active_techniques = {key: True for key in all_technique_keys}
    elif any_technique_flag_set: # If specific flags were set (and not --all or --interactive prior)
        print("\n--- Using specified command-line techniques ---")
        for key in all_technique_keys: 
            if hasattr(args, key): active_techniques[key] = getattr(args, key)
    else: # Default to interactive if no flags given
        print("\nNo specific techniques selected. Defaulting to interactive prompt...")
        print("--- Interactive Obfuscation Technique Selection ---")
        for key in all_technique_keys:
            active_techniques[key] = ask_yes_no(f"Enable {key.replace('_', ' ').title()}?")

    # ... (Print input/output/active_techniques) ...
    print(f"\nInput file: {input_filepath}")
    print(f"Output file: {output_filepath}")
    print(f"Active obfuscation techniques: {active_techniques}")
    print("-" * 40)


    try:
        with open(input_filepath, 'r', encoding='utf-8') as f: original_code_content = f.read()
        
        input_stream = FileStream(input_filepath, encoding='utf-8')
        # ... (ANTLR parsing logic) ...
        lexer = MiniCLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = MiniCParser(stream)
        tree = parser.program()

        if parser.getNumberOfSyntaxErrors() > 0:
            print(f"Syntax errors found in {input_filepath}. Obfuscation aborted."); sys.exit(1)
        
        print(f"Parsing {input_filepath} successful.")
        print("Applying obfuscation...")
        obfuscator = ObfuscatorVisitor(active_techniques)
        obfuscated_code_raw = obfuscator.visit(tree)
        
        final_obfuscated_code_for_disk = obfuscated_code_raw
        disk_headers = []
        if obfuscator.uses_stdio: disk_headers.append("#include <stdio.h>")
        if obfuscator.uses_stdbool: disk_headers.append("#include <stdbool.h>")
        if disk_headers:
            final_obfuscated_code_for_disk = "\n".join(disk_headers) + "\n\n" + obfuscated_code_raw
        
        print(f"Obfuscated code will be saved to: {output_filepath}")
        with open(output_filepath, "w", encoding='utf-8') as f: f.write(final_obfuscated_code_for_disk)
        print("Obfuscation complete.")


        if args.compare_runtime:
            print("\n--- Runtime Comparison ---")
            # Create a single temporary directory for this session's compilations
            with tempfile.TemporaryDirectory(prefix="minic_obf_rtcomp_") as session_temp_dir:
                if args.verbose_runtime:
                    print(f"Using temporary directory for compilation: {session_temp_dir}")

                # Determine includes for original code (heuristic)
                orig_needs_stdio = "printf" in original_code_content or "scanf" in original_code_content
                orig_needs_stdbool = "bool" in original_code_content or \
                                     "true" in original_code_content or \
                                     "false" in original_code_content
                
                # Run OBFUSCATED first
                if args.verbose_runtime: print("\n=> Processing OBFUSCATED code for runtime test...")
                obfuscated_exec_time, obf_stdout, obf_stderr = compile_and_run(
                    obfuscated_code_raw, "obfuscated", 
                    include_stdio_header=obfuscator.uses_stdio, 
                    include_stdbool_header=obfuscator.uses_stdbool,
                    compiler=args.compiler, temp_dir_base=session_temp_dir,
                    verbose_output=args.verbose_runtime # Pass verbose flag
                )
                if args.verbose_runtime and obfuscated_exec_time is not None:
                    print(f"Obfuscated STDOUT:\n{obf_stdout.strip() if obf_stdout else '<no stdout>'}")
                    if obf_stderr and obf_stderr.strip(): print(f"Obfuscated STDERR:\n{obf_stderr.strip()}")
                
                # Run ORIGINAL second
                if args.verbose_runtime: print("\n=> Processing ORIGINAL code for runtime test...")
                original_exec_time, orig_stdout, orig_stderr = compile_and_run(
                    original_code_content, "original", 
                    include_stdio_header=orig_needs_stdio, 
                    include_stdbool_header=orig_needs_stdbool,
                    compiler=args.compiler, temp_dir_base=session_temp_dir,
                    verbose_output=args.verbose_runtime # Pass verbose flag
                )
                if args.verbose_runtime and original_exec_time is not None:
                    print(f"Original STDOUT:\n{orig_stdout.strip() if orig_stdout else '<no stdout>'}")
                    if orig_stderr and orig_stderr.strip(): print(f"Original STDERR:\n{orig_stderr.strip()}")

                # --- Summary focusing on Execution Time ---
                if original_exec_time is not None and obfuscated_exec_time is not None:
                    print("\n--- Summary of Execution Times ---")
                    print(f"Original Program Execution Time:   {original_exec_time:.6f} seconds")
                    print(f"Obfuscated Program Execution Time: {obfuscated_exec_time:.6f} seconds")
                    if original_exec_time > 1e-9 : 
                        overhead = ((obfuscated_exec_time - original_exec_time) / original_exec_time) * 100 
                        print(f"Execution Time Overhead (Obfuscated vs Original): {overhead:.2f}%")
                    else:
                        print("Execution Time Overhead: N/A (original runtime too small to measure reliably)")
                else:
                    print("Could not complete runtime comparison due to errors in compiling/running one or both versions.")
            if not args.verbose_runtime and args.compare_runtime: # To indicate temp dir removal if not verbose
                 print("Temporary compilation files have been removed (run with --verbose-runtime to see details).")


    except FileNotFoundError: print(f"Error: Input file '{input_filepath}' not found."); sys.exit(1)
    except subprocess.TimeoutExpired: print("ERROR: A critical subprocess timed out."); sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}"); import traceback; traceback.print_exc(); sys.exit(1)

if __name__ == '__main__':
    main_cli()