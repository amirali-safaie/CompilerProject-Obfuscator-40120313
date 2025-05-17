# src/obfuscator_visitor.py

from minic_parser.MiniCParser import MiniCParser
from ast_visitor import CodeReconstructionVisitor # Base class for reconstruction
import random 

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {} # original_name -> new_name
        self.prefix_counters = {} # For v_0, p_0, f_0 etc. to be independent in *this specific scope*

    def declare(self, original_name, prefix="v_"):
        """Declares an identifier in this scope with a unique name for the given prefix."""
        if prefix not in self.prefix_counters:
            self.prefix_counters[prefix] = 0
        
        new_name = f"{prefix}{self.prefix_counters[prefix]}"
        self.prefix_counters[prefix] += 1
        
        self.symbols[original_name] = new_name
        return new_name

    def lookup(self, original_name):
        if original_name in self.symbols:
            return self.symbols[original_name]
        if self.parent:
            return self.parent.lookup(original_name)
        if original_name in ["printf", "scanf"]:
             return original_name
        # print(f"Warning: Identifier '{original_name}' not found in any scope, returning as is.")
        return original_name

class ObfuscatorVisitor(CodeReconstructionVisitor):
    def __init__(self, active_techniques):
        super().__init__()
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        
        # Global counters for renaming specific types of identifiers across the whole program run
        # These are used by the _get_renamed_globally helper
        self.global_rename_counters = {
            "f": 0,  # functions (excluding main, printf, scanf)
            "mf": 0, # meaningless functions
        }
        
        # Per-function counters for local/param names, reset for each function
        # These are used by the current_scope.declare method effectively
        
        self.var_name_counter_for_dead_code = 0 # For dead_v_N names
        
        self.active_techniques = active_techniques
        # print(f"DEBUG: ObfuscatorVisitor initialized with techniques: {self.active_techniques}")
        self.is_in_cff_target_block = False 
        self.generated_meaningless_funcs_code = [] # Stores code of generated MRFs
        self.uses_stdio = False # Flag to track if printf/scanf are used

    def _get_renamed_globally(self, original_name, prefix_char_key):
        """
        Declares and renames an identifier in the global_scope using visitor-level global counters.
        prefix_char_key: "f", "mf"
        """
        count = self.global_rename_counters.get(prefix_char_key, 0)
        new_name = f"{prefix_char_key}_{count}"
        self.global_rename_counters[prefix_char_key] = count + 1
        self.global_scope.symbols[original_name] = new_name # Store in global scope's symbol table
        return new_name

    def _create_meaningless_recursive_function(self):
        """Generates the C code string for a meaningless recursive function and its name."""
        # Use a semantic base name to make it unique before renaming
        func_base_name = f"__mrf_semantic_base_{len(self.generated_meaningless_funcs_code)}"
        func_name = func_base_name # Default if no renaming

        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            func_name = self._get_renamed_globally(func_base_name, "mf")
        else: # If not renaming, still add to global scope so it can be looked up
             self.global_scope.symbols[func_base_name] = func_name
        
        # Parameter name for the MRF
        param_orig_name = "depth_param"
        param_renamed = param_orig_name
        
        # Create a temporary scope for this MRF's parameter if renaming is on
        mrf_param_scope = Scope() # Not parented, just for this one param
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            param_renamed = mrf_param_scope.declare(param_orig_name, prefix="pm_") # "pm" for param_meaningless

        # Function Body
        # Indentation note: self.get_indent() is for current visitor indent level.
        # Here, we are generating standalone function code, so use fixed indents.
        indent1 = "    "
        indent2 = "        "
        func_code = f"int {func_name}(int {param_renamed}) {{\n"
        func_code += f"{indent1}if ({param_renamed} <= 0) {{\n"
        func_code += f"{indent2}return {param_renamed} + {random.randint(0,5)};\n" # Base case
        func_code += f"{indent1}}}\n"
        func_code += f"{indent1}int temp_val = ({param_renamed} * {random.randint(1,3)}) % {random.randint(5,10)};\n"
        func_code += f"{indent1}return {func_name}({param_renamed} - 1) + temp_val;\n" # Recursive call
        func_code += "}\n"
        
        self.generated_meaningless_funcs_code.append(func_code)
        return func_name # Return the (potentially renamed) name to be called

    def _generate_call_to_meaningless_func(self):
        """Generates a statement string that calls a random MRF."""
        if not self.generated_meaningless_funcs_code:
            return "" # No MRFs to call

        # Extract names of generated MRFs
        mrf_names = []
        for func_def_str in self.generated_meaningless_funcs_code:
            try:
                # Simple parsing: "int func_name(..."
                name = func_def_str.split('(')[0].split()[-1]
                mrf_names.append(name)
            except IndexError:
                continue # Should not happen if func_code is well-formed
        
        if not mrf_names: return ""

        chosen_func_name = random.choice(mrf_names)
        depth = random.randint(2, 5) # Small depth

        # Call and assign to a dummy variable (which itself might be dead code)
        dummy_var_orig_name = f"__mrf_ret_dummy_{random.randint(1000,9999)}"
        dummy_var_renamed = dummy_var_orig_name

        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            # This dummy var is local to the block where the call is inserted.
            # Use current_scope, which should be the function's local scope.
            dummy_var_renamed = self.current_scope.declare(dummy_var_orig_name, prefix="drv_") # dead_return_var

        return f"{self.get_indent()}int {dummy_var_renamed} = {chosen_func_name}({depth});"


    def generate_dead_code_statement(self):
        # Chance to call a meaningless function
        if "meaningless_funcs" in self.active_techniques and \
           self.active_techniques["meaningless_funcs"] and \
           self.generated_meaningless_funcs_code and \
           random.random() < 0.4: # 40% chance
            call_stmt = self._generate_call_to_meaningless_func()
            if call_stmt: # If a call was successfully generated
                # print(f"DEBUG: Generated dead code (MRF call): {call_stmt.strip()}")
                return call_stmt

        # Default to generating a dead variable
        dead_var_name_ugly = f"dead_v_{self.var_name_counter_for_dead_code}"
        self.var_name_counter_for_dead_code += 1
        value = random.randint(1000, 9999)
        statement = f"{self.get_indent()}int {dead_var_name_ugly} = {value};"
        # print(f"DEBUG: Generated dead code (var): {statement.strip()}")
        return statement

    # --- Program level ---
    def visitProgram(self, ctx:MiniCParser.ProgramContext):
        self.generated_meaningless_funcs_code = [] # Reset for each new program processing
        self.uses_stdio = False

        # 1. Create MRF definitions if technique is active
        if "meaningless_funcs" in self.active_techniques and self.active_techniques["meaningless_funcs"]:
            num_mrf_to_generate = random.randint(1, 2)
            for _ in range(num_mrf_to_generate):
                self._create_meaningless_recursive_function() # Appends to self.generated_meaningless_funcs_code

        # 2. Process original program declarations (functions, global vars if any)
        # This will call visitFunctionDeclaration, visitVariableDeclaration etc.
        # which will use self.current_scope (initially global).
        original_program_code_parts = []
        if ctx.declaration():
            for decl_ctx in ctx.declaration():
                original_program_code_parts.append(self.visit(decl_ctx))
        
        # 3. Assemble final code: MRFs first, then main program code
        final_code_segments = []
        if self.generated_meaningless_funcs_code:
            final_code_segments.extend(self.generated_meaningless_funcs_code)
        
        final_code_segments.extend(filter(None, original_program_code_parts))
        
        return "\n\n".join(final_code_segments) # Separate functions/declarations by double newline

    # --- Block and Statement Obfuscation ---
    def visitBlock(self, ctx:MiniCParser.BlockContext):
        is_cff_active_for_this_block = self.is_in_cff_target_block and \
                                       ("flatten_control_flow" in self.active_techniques and \
                                        self.active_techniques["flatten_control_flow"])

        if not is_cff_active_for_this_block: # Standard block processing
            self.indent_level += 1
            block_statements = []
            if "dead_code" in self.active_techniques and self.active_techniques["dead_code"]:
                num_dead = random.randint(1,2)
                for _ in range(num_dead):
                    block_statements.append(self.generate_dead_code_statement()) # Includes MRF calls chance
            
            if ctx.statement():
                for stmt_ctx in ctx.statement():
                    block_statements.append(self.visit(stmt_ctx))
            
            all_statements_str = "\n".join(filter(None, block_statements))
            self.indent_level -= 1
            if not all_statements_str.strip(): return f"{{\n{self.get_indent()}}}"
            return f"{{\n{all_statements_str}\n{self.get_indent()}}}"
        else: # CFF Logic
            # print("DEBUG: Block - CFF path is active for this block.")
            self.indent_level += 1
            declarations = []
            statements_to_flatten = []
            if ctx.statement():
                for stmt_ctx in ctx.statement():
                    if stmt_ctx.variableDeclaration(): declarations.append(self.visit(stmt_ctx))
                    else: statements_to_flatten.append(self.visit(stmt_ctx).strip()) 
            
            cff_code = []
            cff_code.extend(declarations) 
            if statements_to_flatten:
                state_var_name = self.current_scope.declare("__cff_state_sem__", "st_") if \
                                 ("rename" in self.active_techniques and self.active_techniques["rename"]) else \
                                 f"cff_state_{random.randint(0,99)}" # Fallback non-renamed

                cff_code.append(f"{self.get_indent()}int {state_var_name} = 1;")
                if "dead_code" in self.active_techniques and self.active_techniques["dead_code"]: # Dead code before loop
                    cff_code.append(self.generate_dead_code_statement())

                cff_code.append(f"{self.get_indent()}while ({state_var_name} > 0) {{")
                self.indent_level += 1
                cff_code.append(f"{self.get_indent()}switch ({state_var_name}) {{")
                self.indent_level += 1
                for i, stmt_str in enumerate(statements_to_flatten):
                    case_num = i + 1
                    next_state = i + 2 if i < len(statements_to_flatten) - 1 else 0
                    cff_code.append(f"{self.get_indent()}case {case_num}:")
                    self.indent_level += 1
                    cff_code.append(f"{self.get_indent()}{stmt_str}")
                    cff_code.append(f"{self.get_indent()}{state_var_name} = {next_state};")
                    cff_code.append(f"{self.get_indent()}break;")
                    self.indent_level -= 1
                cff_code.append(f"{self.get_indent()}default: {state_var_name} = 0; break;") # Default case
                self.indent_level -= 1; cff_code.append(f"{self.get_indent()}}}") # End switch
                self.indent_level -= 1; cff_code.append(f"{self.get_indent()}}}") # End while
            self.indent_level -= 1
            final_block_content = "\n".join(filter(None, cff_code))
            if not final_block_content.strip(): return f"{{\n{self.get_indent()}}}"
            return f"{{\n{final_block_content}\n{self.get_indent()}}}"

    # --- Expression Transformation ---
    def visitAdditiveExpression(self, ctx:MiniCParser.AdditiveExpressionContext):
        if ("transform_expressions" not in self.active_techniques or \
            not self.active_techniques["transform_expressions"]) or \
            ctx.getChildCount() <= 1: 
            return super().visitAdditiveExpression(ctx) # Use parent's reconstruction
        
        result = self.visit(ctx.multiplicativeExpression(0))
        child_idx = 1
        while child_idx < ctx.getChildCount():
            op_text = ctx.getChild(child_idx).getText() # Operator
            child_idx += 1
            if child_idx >= ctx.getChildCount(): break
            right_operand_text = self.visit(ctx.getChild(child_idx)) # Operand
            child_idx += 1
            if op_text == '+': result += f" - (0 - ({right_operand_text}))"
            elif op_text == '-': result += f" + (0 - ({right_operand_text}))"
            else: result += f" {op_text} {right_operand_text}" # Should not happen
        return result    

    # --- Renaming Logic for Declarations and Usages ---
    def visitFunctionDeclaration(self, ctx:MiniCParser.FunctionDeclarationContext):
        original_func_name = ctx.IDENTIFIER().getText()
        
        # Determine if CFF is active for THIS function's block
        self.is_in_cff_target_block = False 
        if "flatten_control_flow" in self.active_techniques and \
           self.active_techniques["flatten_control_flow"] and \
           original_func_name == "main": 
            self.is_in_cff_target_block = True

        type_spec = self.visit(ctx.typeSpecifier())
        new_func_name = original_func_name 

        # Renaming of function name (done in global scope)
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            if original_func_name not in ["main", "printf", "scanf"]:
                new_func_name = self._get_renamed_globally(original_func_name, "f")
            else: # Ensure main, printf, scanf are in global scope even if not "renamed" by us
                if original_func_name not in self.global_scope.symbols:
                    self.global_scope.symbols[original_func_name] = original_func_name
        elif original_func_name not in self.global_scope.symbols: # Not renaming, but ensure presence
             self.global_scope.symbols[original_func_name] = original_func_name
        
        # Create new scope for function's parameters and local variables
        outer_scope = self.current_scope
        self.current_scope = Scope(parent=self.global_scope) # Functions exist in global, locals in func scope

        params_str = ""
        if ctx.parameters():
            param_strs = []
            for p_ctx in ctx.parameters().parameter():
                p_type = self.visit(p_ctx.typeSpecifier())
                p_orig_name = p_ctx.IDENTIFIER().getText()
                p_new_name = p_orig_name
                if "rename" in self.active_techniques and self.active_techniques["rename"]:
                    p_new_name = self.current_scope.declare(p_orig_name, prefix="p_") # Params in func scope
                else:
                    self.current_scope.symbols[p_orig_name] = p_orig_name
                param_strs.append(f"{p_type} {p_new_name}")
            params_str = ", ".join(param_strs)

        body_str = self.visit(ctx.block()) # Process block within function's scope

        self.current_scope = outer_scope # Restore outer scope
        return f"{type_spec} {new_func_name}({params_str}) {body_str}"

    def visitVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        type_spec = self.visit(ctx.typeSpecifier())
        original_name = ctx.IDENTIFIER().getText()
        new_name = original_name
        
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            new_name = self.current_scope.declare(original_name, prefix="v_") # Local vars in current_scope
        else: 
            # If not renaming, still "declare" it in the current scope for correct lookup
            # and to handle cases where a local var might have same name as a param.
            if original_name not in self.current_scope.symbols:
                 self.current_scope.symbols[original_name] = original_name
            # If it is already in current_scope.symbols (e.g. it's a parameter), lookup will find that.
            # This simple model might not perfectly handle C's complex scoping/shadowing, but is ok for MiniC.

        init_expr_str = ""
        if ctx.expression():
            init_expr_str = f" = {self.visit(ctx.expression())}"
        return f"{self.get_indent()}{type_spec} {new_name}{init_expr_str};"

    def visitPrimaryExpression(self, ctx:MiniCParser.PrimaryExpressionContext):
        if ctx.IDENTIFIER():
            original_name = ctx.IDENTIFIER().getText()
            # Lookup starts from current_scope and goes up to global_scope
            renamed_name = self.current_scope.lookup(original_name)
            return renamed_name
        # For other primary expressions, delegate to parent or handle directly
        if ctx.constant(): return self.visit(ctx.constant()) 
        if ctx.LPAREN(): return f"({self.visit(ctx.expression())})" 
        if ctx.functionCall(): return self.visit(ctx.functionCall()) 
        return super().visitPrimaryExpression(ctx) # Fallback

    def visitFunctionCall(self, ctx:MiniCParser.FunctionCallContext):
        original_func_name = ctx.IDENTIFIER().getText()
        if original_func_name in ["printf", "scanf"]: # Track stdio usage
            self.uses_stdio = True
        
        # Function names are always looked up in the global scope for MiniC
        renamed_func_name = self.global_scope.lookup(original_func_name)                             
        
        args_str = ""
        if ctx.arguments():
            args_str = self.visit(ctx.arguments()) # Arguments are expressions, visited in current context
        return f"{renamed_func_name}({args_str})"