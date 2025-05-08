from minic_parser.MiniCParser import MiniCParser
from ast_visitor import CodeReconstructionVisitor # Reuse for base structure
import random 

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {} # original_name -> new_name
        self.name_counter = 0

    def declare(self, original_name, prefix="v_"):
        new_name = f"{prefix}{self.name_counter}"
        self.name_counter += 1
        self.symbols[original_name] = new_name
        return new_name

    def lookup(self, original_name):
        if original_name in self.symbols:
            return self.symbols[original_name]
        if self.parent:
            return self.parent.lookup(original_name)
        if original_name in ["printf", "scanf"]:
             return original_name
        # For debugging, let's be clear if something is not found and not a built-in
        # print(f"Warning: Identifier '{original_name}' not found in any scope, returning as is (or could be an error).")
        return original_name # Return original if not found and not special (could be an error in a strict checker)

class ObfuscatorVisitor(CodeReconstructionVisitor):
    def __init__(self, active_techniques):
        super().__init__()
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.function_name_counter = 0
        self.var_name_counter_for_dead_code = 0
        self.active_techniques = active_techniques
        print(f"DEBUG: ObfuscatorVisitor initialized with techniques: {self.active_techniques}")
        self.is_in_cff_target_block = False # Initialize CFF flag

    # In ObfuscatorVisitor class:

    def generate_dead_code_statement(self):
        dead_var_name = f"dead_v_{self.var_name_counter_for_dead_code}"
        self.var_name_counter_for_dead_code += 1
        value = random.randint(1000, 9999)
        # statement = f"{self.get_indent()}int {dead_var_name} = {value}; // Dead code" # Old version
        statement = f"{self.get_indent()}int {dead_var_name} = {value};" # New version without comment
        print(f"DEBUG: Generated dead code: {statement.strip()}")
        return statement

    # --- THIS IS THE CORRECT visitBlock METHOD TO KEEP ---
    def visitBlock(self, ctx:MiniCParser.BlockContext):
        print(f"DEBUG: Visiting Block. Current indent: {self.indent_level}. is_cff_target_block: {self.is_in_cff_target_block}")
        
        # Determine if CFF is active for this specific block invocation
        # This flag should be set appropriately before visitBlock is called (e.g., in visitFunctionDeclaration)
        is_cff_active_for_this_block = self.is_in_cff_target_block and \
                                       ("flatten_control_flow" in self.active_techniques and \
                                        self.active_techniques["flatten_control_flow"])

        if not is_cff_active_for_this_block:
            print("DEBUG: Block - Standard path (no CFF or CFF disabled for this block)")
            self.indent_level += 1
            
            dead_code_stmts_list = []
            if "dead_code" in self.active_techniques and self.active_techniques["dead_code"]:
                print("DEBUG: Block - Dead code is active. Generating...")
                num_dead_stmts = random.randint(1,2) # Insert 1 or 2 dead lines
                print(f"DEBUG: Block - Will attempt to generate {num_dead_stmts} dead statements.")
                for i in range(num_dead_stmts):
                    # print(f"DEBUG: Block - Generating dead statement #{i+1}") # Redundant with print in generate_dead_code_statement
                    dead_code_stmts_list.append(self.generate_dead_code_statement())
            else:
                print("DEBUG: Block - Dead code is NOT active for this block (based on active_techniques).")
            
            original_statements_strs = []
            # ANTLR context objects for children are usually attributes, not direct iterables unless it's a list of terminals.
            # ctx.statement() should return a list of StatementContext objects.
            if ctx.statement(): # Check if there are any statement children
                for stmt_ctx in ctx.statement():
                    original_statements_strs.append(self.visit(stmt_ctx))
            
            # Ensure proper joining, especially if one list is empty
            all_statements_components = dead_code_stmts_list + original_statements_strs
            all_statements_str = "\n".join(filter(None, all_statements_components)) # Filter out potential None or empty strings

            self.indent_level -= 1
            
            if not all_statements_str.strip():
                print("DEBUG: Block - Resulting block content is empty.")
                return f"{{\n{self.get_indent()}}}" # Correctly handles indentation for empty block
            # print(f"DEBUG: Block - Final content before returning:\n{{\n{all_statements_str}\n{self.get_indent()}}}\n---")
            return f"{{\n{all_statements_str}\n{self.get_indent()}}}"
        
        else: # CFF Block Logic Path
            print("DEBUG: Block - CFF path. Implement CFF logic here.")
            # ... (Your CFF logic would go here) ...
            # For now, if CFF is active but not implemented, it might call super or do something basic.
            # Make sure this path also correctly handles indentation and returns a valid block string.
            # Example: For now, let's just reconstruct it simply if CFF is active but not fully coded.
            self.indent_level += 1
            cff_placeholder_statements = []
            if ctx.statement():
                for stmt_ctx in ctx.statement():
                    cff_placeholder_statements.append(self.visit(stmt_ctx))
            cff_block_content = "\n".join(filter(None, cff_placeholder_statements))
            self.indent_level -=1
            if not cff_block_content.strip():
                 return f"{{\n{self.get_indent()}}}"
            return f"{{\n{self.get_indent()}// CFF Active - Placeholder\n{cff_block_content}\n{self.get_indent()}}}"


    def generate_new_func_name(self): # This seems unused, function renaming is in visitFunctionDeclaration
        name = f"func_{self.function_name_counter}"
        self.function_name_counter += 1
        return name

    def visitFunctionDeclaration(self, ctx:MiniCParser.FunctionDeclarationContext):
        original_func_name = ctx.IDENTIFIER().getText()
        print(f"DEBUG: Visiting function: {original_func_name}")

        # Determine and set CFF flag state for the upcoming block visit
        self.is_in_cff_target_block = False # Default for each function
        if "flatten_control_flow" in self.active_techniques and \
           self.active_techniques["flatten_control_flow"] and \
           original_func_name == "main": # Example: Target only main for CFF
            self.is_in_cff_target_block = True
        print(f"DEBUG: For function {original_func_name}, is_in_cff_target_block set to: {self.is_in_cff_target_block}")

        # Renaming logic for function
        type_spec = self.visit(ctx.typeSpecifier())
        new_func_name = original_func_name # Default if renaming is off

        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            if original_func_name == "main" or original_func_name in ["printf", "scanf"]:
                 new_func_name = original_func_name
                 # Even if not renaming, add to global scope so lookups for calls find it
                 self.global_scope.symbols[original_func_name] = new_func_name
            else:
                new_func_name = self.global_scope.declare(original_func_name, prefix="f_")
        elif original_func_name not in self.global_scope.symbols: # If not renaming, still ensure it's in global scope for calls
            self.global_scope.symbols[original_func_name] = original_func_name


        # Handle scope for parameters and function body
        previous_scope = self.current_scope # Save outer scope (likely global)
        self.current_scope = Scope(parent=self.global_scope) # New scope for this function
        
        params_str = ""
        if ctx.parameters():
            param_nodes = ctx.parameters().parameter()
            param_strs = []
            for p_ctx in param_nodes:
                p_type = self.visit(p_ctx.typeSpecifier())
                p_orig_name = p_ctx.IDENTIFIER().getText()
                p_new_name = p_orig_name # Default if renaming is off
                if "rename" in self.active_techniques and self.active_techniques["rename"]:
                    p_new_name = self.current_scope.declare(p_orig_name, prefix="p_")
                else: # If not renaming, still declare in current scope for local var shadowing checks if any
                    self.current_scope.symbols[p_orig_name] = p_orig_name
                param_strs.append(f"{p_type} {p_new_name}")
            params_str = ", ".join(param_strs)

        body_str = self.visit(ctx.block()) # << This will call the one defined visitBlock

        self.current_scope = previous_scope # Restore outer scope

        return f"{type_spec} {new_func_name}({params_str}) {body_str}"

    def visitVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        type_spec = self.visit(ctx.typeSpecifier())
        original_name = ctx.IDENTIFIER().getText()
        new_name = original_name # Default if renaming is off
        
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            new_name = self.current_scope.declare(original_name, prefix="v_")
        else: # If not renaming, still declare in current scope
            self.current_scope.symbols[original_name] = original_name
            
        init_expr_str = ""
        if ctx.expression():
            init_expr_str = f" = {self.visit(ctx.expression())}"

        return f"{self.get_indent()}{type_spec} {new_name}{init_expr_str};"

    def visitPrimaryExpression(self, ctx:MiniCParser.PrimaryExpressionContext):
        if ctx.IDENTIFIER():
            original_name = ctx.IDENTIFIER().getText()
            # Lookup always happens, renaming just changes what is returned by lookup
            new_name = self.current_scope.lookup(original_name)
            return new_name
        
        # Delegate to super for other primary expression types or implement them directly
        if ctx.constant(): return self.visit(ctx.constant()) # Or super().visitConstant(ctx.constant())
        if ctx.LPAREN(): return f"({self.visit(ctx.expression())})" # Or super().visitParenExpression(...)
        if ctx.functionCall(): return self.visit(ctx.functionCall()) # Or super().visitFunctionCall(ctx.functionCall())
        
        # Fallback if none of the above (should not happen with a complete grammar/visitor)
        return super().visitPrimaryExpression(ctx) 

    def visitFunctionCall(self, ctx:MiniCParser.FunctionCallContext):
        original_func_name = ctx.IDENTIFIER().getText()
        # Function names are looked up in global scope for this simple C subset
        new_func_name = self.global_scope.lookup(original_func_name) 
                                            
        args_str = ""
        if ctx.arguments():
            args_str = self.visit(ctx.arguments()) 
        return f"{new_func_name}({args_str})"

    # REMOVE THE REDUNDANT visitBlock METHOD THAT WAS HERE:
    # def visitBlock(self, ctx:MiniCParser.BlockContext): 
    #     return super().visitBlock(ctx) # THIS WAS THE PROBLEM