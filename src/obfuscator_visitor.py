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
        return original_name

class ObfuscatorVisitor(CodeReconstructionVisitor):
    def __init__(self, active_techniques):
        super().__init__()
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.function_name_counter = 0
        self.var_name_counter_for_dead_code = 0
        self.cff_state_var_counter = 0 # Added for CFF
        self.active_techniques = active_techniques
        print(f"DEBUG: ObfuscatorVisitor initialized with techniques: {self.active_techniques}")
        self.is_in_cff_target_block = False # Flag for CFF targeting specific blocks

    def get_cff_state_var_name(self): # Added for CFF
        name = f"cff_state_{self.cff_state_var_counter}"
        self.cff_state_var_counter +=1
        # If renaming is active, this name could also be obfuscated if desired
        # by declaring it in the current scope. For simplicity, using a fixed prefix.
        # Example: if "rename" in self.active_techniques and self.active_techniques["rename"]:
        #    return self.current_scope.declare(f"__cff_state_orig_{self.cff_state_var_counter}", prefix="ugly_state_")
        return name

    def generate_dead_code_statement(self):
        dead_var_name = f"dead_v_{self.var_name_counter_for_dead_code}"
        self.var_name_counter_for_dead_code += 1
        value = random.randint(1000, 9999)
        statement = f"{self.get_indent()}int {dead_var_name} = {value};"
        print(f"DEBUG: Generated dead code: {statement.strip()}")
        return statement

    def visitBlock(self, ctx:MiniCParser.BlockContext):
        print(f"DEBUG: Visiting Block. Current indent: {self.indent_level}. is_cff_target_block (from func): {self.is_in_cff_target_block}")
        
        is_cff_active_for_this_block = self.is_in_cff_target_block and \
                                       ("flatten_control_flow" in self.active_techniques and \
                                        self.active_techniques["flatten_control_flow"])
        
        print(f"DEBUG: Block - CFF active for this specific block call: {is_cff_active_for_this_block}")

        if not is_cff_active_for_this_block:
            # --- Standard Block Processing (No CFF for this block) ---
            print("DEBUG: Block - Standard path (no CFF or CFF disabled for this block)")
            self.indent_level += 1
            
            dead_code_stmts_list = []
            if "dead_code" in self.active_techniques and self.active_techniques["dead_code"]:
                print("DEBUG: Block - Dead code is active. Generating...")
                num_dead_stmts = random.randint(1,2)
                print(f"DEBUG: Block - Will attempt to generate {num_dead_stmts} dead statements.")
                for _ in range(num_dead_stmts):
                    dead_code_stmts_list.append(self.generate_dead_code_statement())
            
            original_statements_strs = []
            if ctx.statement():
                for stmt_ctx in ctx.statement():
                    original_statements_strs.append(self.visit(stmt_ctx))
            
            all_statements_components = dead_code_stmts_list + original_statements_strs
            all_statements_str = "\n".join(filter(None, all_statements_components))

            self.indent_level -= 1
            
            if not all_statements_str.strip():
                return f"{{\n{self.get_indent()}}}"
            return f"{{\n{all_statements_str}\n{self.get_indent()}}}"
        
        else: 
            # --- CFF Logic for this targeted block ---
            print("DEBUG: Block - CFF path is active for this block.")
            self.indent_level += 1
            
            declarations = []
            statements_to_flatten_details = [] # Store tuples of (original_text_for_debug, visited_text)
            
            # Separate declarations from other statements
            # This assumes variable declarations appear before other statements that would be flattened.
            # More complex C allows interspersed declarations, but MiniC is simpler.
            if ctx.statement():
                for stmt_ctx in ctx.statement():
                    if stmt_ctx.variableDeclaration():
                        declarations.append(self.visit(stmt_ctx))
                    else:
                        # For statements to flatten, we need their string representation.
                        # The .strip() is important if self.visit(stmt_ctx) adds its own indents/newlines.
                        statements_to_flatten_details.append(self.visit(stmt_ctx).strip()) 
            
            print(f"DEBUG: CFF - Declarations found: {len(declarations)}")
            print(f"DEBUG: CFF - Statements to flatten: {len(statements_to_flatten_details)}")

            cff_output_lines = []
            cff_output_lines.extend(declarations) 

            if statements_to_flatten_details:
                state_var_original_name = f"__cff_state_var_{self.get_cff_state_var_name()}" # A unique internal name
                state_var_obfuscated = state_var_original_name # Default if no renaming
                
                # If renaming is on, declare and get the obfuscated name for the state variable
                # It needs to be declared in the *current function's scope*.
                if "rename" in self.active_techniques and self.active_techniques["rename"]:
                     # We need to ensure current_scope is the function's scope, not global, when declaring this.
                     # This is tricky because visitBlock is generic. Assuming current_scope is set by visitFunctionDeclaration.
                    state_var_obfuscated = self.current_scope.declare(state_var_original_name, prefix="st_")
                else: # If not renaming, still add to scope so it's "known"
                    self.current_scope.symbols[state_var_original_name] = state_var_obfuscated


                cff_output_lines.append(f"{self.get_indent()}int {state_var_obfuscated} = 1; // CFF state")

                # Optional: Add dead code *inside* the CFF structure, before the loop
                if "dead_code" in self.active_techniques and self.active_techniques["dead_code"]:
                    for _ in range(random.randint(1,1)): 
                         cff_output_lines.append(self.generate_dead_code_statement())

                cff_output_lines.append(f"{self.get_indent()}while ({state_var_obfuscated} > 0) {{")
                self.indent_level += 1
                cff_output_lines.append(f"{self.get_indent()}switch ({state_var_obfuscated}) {{")
                
                self.indent_level += 1
                for i, stmt_str in enumerate(statements_to_flatten_details):
                    current_case_num = i + 1
                    next_case_num = i + 2 if i < len(statements_to_flatten_details) - 1 else 0 # 0 to exit loop

                    cff_output_lines.append(f"{self.get_indent()}case {current_case_num}:")
                    self.indent_level += 1
                    # stmt_str is already processed (visited) and stripped.
                    cff_output_lines.append(f"{self.get_indent()}{stmt_str}") 
                    cff_output_lines.append(f"{self.get_indent()}{state_var_obfuscated} = {next_case_num};")
                    cff_output_lines.append(f"{self.get_indent()}break;")
                    self.indent_level -= 1
                
                # Add a default case for robustness, though ideally not hit with this simple CFF
                cff_output_lines.append(f"{self.get_indent()}default:")
                self.indent_level += 1
                cff_output_lines.append(f"{self.get_indent()}{state_var_obfuscated} = 0; // Exit on unknown state")
                cff_output_lines.append(f"{self.get_indent()}break;")
                self.indent_level -= 1

                self.indent_level -= 1
                cff_output_lines.append(f"{self.get_indent()}}}") # end switch
                self.indent_level -= 1
                cff_output_lines.append(f"{self.get_indent()}}}") # end while
            
            self.indent_level -= 1 # Outer block indent adjustment
            
            final_block_content = "\n".join(filter(None, cff_output_lines))
            if not final_block_content.strip():
                 return f"{{\n{self.get_indent()}}}"
            return f"{{\n{final_block_content}\n{self.get_indent()}}}"

    def visitAdditiveExpression(self, ctx:MiniCParser.AdditiveExpressionContext):
        if ("transform_expressions" not in self.active_techniques or \
            not self.active_techniques["transform_expressions"]) or \
            ctx.getChildCount() <= 1: # Check if it's more than just one multExpr
            return super().visitAdditiveExpression(ctx)

        print(f"DEBUG: Transforming AdditiveExpression: {ctx.getText()}")
        result = self.visit(ctx.multiplicativeExpression(0))
        child_idx = 1
        while child_idx < ctx.getChildCount():
            op_node = ctx.getChild(child_idx)
            op_text = op_node.getText()
            child_idx += 1
            if child_idx >= ctx.getChildCount(): break
            right_operand_node = ctx.getChild(child_idx)
            right_operand_text = self.visit(right_operand_node)
            child_idx += 1

            if op_text == '+':
                result += f" - (0 - ({right_operand_text}))"
            elif op_text == '-':
                result += f" + (0 - ({right_operand_text}))"
            else: 
                result += f" {op_text} {right_operand_text}"
        return result    

    def visitFunctionDeclaration(self, ctx:MiniCParser.FunctionDeclarationContext):
        original_func_name = ctx.IDENTIFIER().getText()
        print(f"DEBUG: Visiting function: {original_func_name}")

        # Set the CFF target flag *before* visiting the block
        # This flag is instance-wide but effectively acts per-function call to visitBlock
        self.is_in_cff_target_block = False 
        if "flatten_control_flow" in self.active_techniques and \
           self.active_techniques["flatten_control_flow"] and \
           original_func_name == "main": # Target CFF only for 'main' function
            self.is_in_cff_target_block = True
        print(f"DEBUG: For function {original_func_name}, is_in_cff_target_block set to: {self.is_in_cff_target_block}")

        type_spec = self.visit(ctx.typeSpecifier())
        new_func_name = original_func_name 

        # Scope setup for the function (parameters and local variables)
        # Must happen before declaring CFF state var if it's to be renamed.
        previous_scope = self.current_scope 
        self.current_scope = Scope(parent=self.global_scope) # New scope for this function

        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            if original_func_name == "main" or original_func_name in ["printf", "scanf"]:
                 new_func_name = original_func_name
                 self.global_scope.symbols[original_func_name] = new_func_name # Record in global
            else:
                new_func_name = self.global_scope.declare(original_func_name, prefix="f_")
        elif original_func_name not in self.global_scope.symbols: 
            self.global_scope.symbols[original_func_name] = original_func_name
        
        params_str = ""
        if ctx.parameters():
            param_nodes = ctx.parameters().parameter()
            param_strs = []
            for p_ctx in param_nodes:
                p_type = self.visit(p_ctx.typeSpecifier())
                p_orig_name = p_ctx.IDENTIFIER().getText()
                p_new_name = p_orig_name 
                if "rename" in self.active_techniques and self.active_techniques["rename"]:
                    p_new_name = self.current_scope.declare(p_orig_name, prefix="p_") # Declare in func scope
                else: 
                    self.current_scope.symbols[p_orig_name] = p_orig_name # Declare in func scope
                param_strs.append(f"{p_type} {p_new_name}")
            params_str = ", ".join(param_strs)

        # Now that current_scope is the function's scope, CFF state var can be declared/renamed correctly if CFF path is taken in visitBlock.
        body_str = self.visit(ctx.block()) 

        self.current_scope = previous_scope # Restore outer scope
        # self.is_in_cff_target_block = False # Reset flag after processing the function's block if needed for visitor reuse.
                                           # For a single pass, setting it at start of func visit is often enough.
        return f"{type_spec} {new_func_name}({params_str}) {body_str}"

    def visitVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        type_spec = self.visit(ctx.typeSpecifier())
        original_name = ctx.IDENTIFIER().getText()
        new_name = original_name 
        
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            new_name = self.current_scope.declare(original_name, prefix="v_")
        else: 
            if original_name not in self.current_scope.symbols:
                self.current_scope.symbols[original_name] = original_name
            
        init_expr_str = ""
        if ctx.expression():
            init_expr_str = f" = {self.visit(ctx.expression())}"
        return f"{self.get_indent()}{type_spec} {new_name}{init_expr_str};"

    def visitPrimaryExpression(self, ctx:MiniCParser.PrimaryExpressionContext):
        if ctx.IDENTIFIER():
            original_name = ctx.IDENTIFIER().getText()
            new_name = self.current_scope.lookup(original_name)
            return new_name
        if ctx.constant(): return self.visit(ctx.constant()) 
        if ctx.LPAREN(): return f"({self.visit(ctx.expression())})" 
        if ctx.functionCall(): return self.visit(ctx.functionCall()) 
        return super().visitPrimaryExpression(ctx) 

    def visitFunctionCall(self, ctx:MiniCParser.FunctionCallContext):
        original_func_name = ctx.IDENTIFIER().getText()
        new_func_name = self.global_scope.lookup(original_func_name)                             
        args_str = ""
        if ctx.arguments():
            args_str = self.visit(ctx.arguments()) 
        return f"{new_func_name}({args_str})"