# src/obfuscator_visitor.py

from minic_parser.MiniCParser import MiniCParser
from ast_visitor import CodeReconstructionVisitor # Base class for reconstruction
import random 

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {} # original_name -> new_name
        self.prefix_counters = {} 

    def declare(self, original_name, prefix="v_"):
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
        return original_name

class ObfuscatorVisitor(CodeReconstructionVisitor):
    def __init__(self, active_techniques):
        super().__init__()
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        
        self.global_rename_counters = {"f": 0, "mf": 0}
        self.var_name_counter_for_dead_code = 0
        
        self.active_techniques = active_techniques
        self.is_in_cff_target_block = False 
        self.generated_meaningless_funcs_code = []
        self.uses_stdio = False
        self.uses_stdbool = False # <<< Ensure this is initialized

    def _get_renamed_globally(self, original_name, prefix_char_key):
        count = self.global_rename_counters.get(prefix_char_key, 0)
        new_name = f"{prefix_char_key}_{count}"
        self.global_rename_counters[prefix_char_key] = count + 1
        self.global_scope.symbols[original_name] = new_name
        return new_name

    def _create_meaningless_recursive_function(self):
        func_base_name = f"__mrf_sem_base_{len(self.generated_meaningless_funcs_code)}"
        func_name = func_base_name
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            func_name = self._get_renamed_globally(func_base_name, "mf")
        elif func_base_name not in self.global_scope.symbols:
             self.global_scope.symbols[func_base_name] = func_name
        
        param_orig_name = f"depth_param_mrf_{len(self.generated_meaningless_funcs_code)}"
        param_renamed = param_orig_name
        mrf_param_scope = Scope() 
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            param_renamed = mrf_param_scope.declare(param_orig_name, prefix="pm_")

        indent1, indent2 = "    ", "        "
        func_code = f"int {func_name}(int {param_renamed}) {{\n"
        func_code += f"{indent1}if ({param_renamed} <= {random.randint(0,1)}) {{\n"
        func_code += f"{indent2}return {param_renamed} + {random.randint(0,5)};\n"
        func_code += f"{indent1}}}\n"
        func_code += f"{indent1}int temp_val = ({param_renamed} * {random.randint(1,3)}) - ({param_renamed} / {random.randint(2,4) +1});\n"
        func_code += f"{indent1}return {func_name}({param_renamed} - {random.randint(1,2)}) + (temp_val % {random.randint(3,7) +1});\n"
        func_code += "}\n"
        self.generated_meaningless_funcs_code.append(func_code)
        return func_name

    def _generate_call_to_meaningless_func(self):
        if not self.generated_meaningless_funcs_code: return ""
        mrf_names = [f_code.split('(')[0].split()[-1] for f_code in self.generated_meaningless_funcs_code if '(' in f_code and ' ' in f_code.split('(')[0]]
        if not mrf_names: return ""

        chosen_func_name = random.choice(mrf_names)
        depth = random.randint(2, 5)
        dummy_var_orig_name = f"__mrf_ret_val_sem_{random.randint(1000,9999)}"
        dummy_var_renamed = dummy_var_orig_name
        if "rename" in self.active_techniques and self.active_techniques["rename"]:
            dummy_var_renamed = self.current_scope.declare(dummy_var_orig_name, prefix="drv_")
        else: 
             if dummy_var_orig_name not in self.current_scope.symbols:
                self.current_scope.symbols[dummy_var_orig_name] = dummy_var_orig_name
        return f"{self.get_indent()}int {dummy_var_renamed} = {chosen_func_name}({depth});"

    def generate_dead_code_statement(self):
        if "meaningless_funcs" in self.active_techniques and self.active_techniques["meaningless_funcs"] and \
           self.generated_meaningless_funcs_code and random.random() < 0.4:
            call_stmt = self._generate_call_to_meaningless_func()
            if call_stmt: return call_stmt
        dead_var_name_ugly = f"dead_v_{self.var_name_counter_for_dead_code}"
        self.var_name_counter_for_dead_code += 1
        value = random.randint(1000, 9999)
        return f"{self.get_indent()}int {dead_var_name_ugly} = {value};"

    def visitProgram(self, ctx:MiniCParser.ProgramContext):
        self.generated_meaningless_funcs_code = [] 
        self.uses_stdio = False
        self.uses_stdbool = False # Reset for each program
        if "meaningless_funcs" in self.active_techniques and self.active_techniques["meaningless_funcs"]:
            for _ in range(random.randint(1, 2)):
                self._create_meaningless_recursive_function()
        original_program_code_parts = [self.visit(decl_ctx) for decl_ctx in ctx.declaration()] if ctx.declaration() else []
        final_code_segments = list(self.generated_meaningless_funcs_code) + list(filter(None, original_program_code_parts))
        return "\n\n".join(final_code_segments)

    def visitBlock(self, ctx:MiniCParser.BlockContext):
        is_cff_active = self.is_in_cff_target_block and \
                        ("flatten_control_flow" in self.active_techniques and self.active_techniques["flatten_control_flow"])

        if not is_cff_active:
            # ... (standard block processing - this part should be okay) ...
            self.indent_level += 1
            block_stmts = []
            if "dead_code" in self.active_techniques and self.active_techniques["dead_code"]:
                for _ in range(random.randint(1,2)): block_stmts.append(self.generate_dead_code_statement())
            if ctx.statement():
                for stmt_ctx in ctx.statement(): block_stmts.append(self.visit(stmt_ctx))
            all_stmts_str = "\n".join(filter(None, block_stmts))
            self.indent_level -= 1
            return f"{{\n{all_stmts_str}\n{self.get_indent()}}}" if all_stmts_str.strip() else f"{{\n{self.get_indent()}}}"
        else: # CFF Path
            # print("DEBUG: Block - CFF path is active for this block.")
            self.indent_level += 1 # For the content of the block '{' '}'
            
            declarations, stmts_to_flatten = [], []
            if ctx.statement():
                for stmt_ctx in ctx.statement():
                    if stmt_ctx.variableDeclaration(): declarations.append(self.visit(stmt_ctx))
                    else: stmts_to_flatten.append(self.visit(stmt_ctx).strip())
            
            cff_code = list(declarations)
            if stmts_to_flatten:
                state_var_sem = "__cff_state_semantic__"
                state_var_name = self.current_scope.declare(state_var_sem, "st_") if \
                                 ("rename" in self.active_techniques and self.active_techniques["rename"]) else \
                                 f"cff_ctrl_{self.current_scope.prefix_counters.get('st_', 0) if 'st_' in self.current_scope.prefix_counters else random.randint(0,9)}" # Fallback

                cff_code.append(f"{self.get_indent()}int {state_var_name} = 1;")
                if "dead_code" in self.active_techniques and self.active_techniques["dead_code"]:
                    cff_code.append(self.generate_dead_code_statement())
                
                cff_code.append(f"{self.get_indent()}while ({state_var_name} > 0) {{")
                self.indent_level += 1 # For content of 'while'
                cff_code.append(f"{self.get_indent()}switch ({state_var_name}) {{")
                
                # The case labels and default label should be at the switch's indentation level
                # The content *inside* each case/default should be one level deeper.
                
                for i, stmt_str in enumerate(stmts_to_flatten):
                    cff_code.append(f"{self.get_indent()}case {i+1}:") # Case label at current indent
                    self.indent_level += 1 # Deeper for case content
                    cff_code.append(f"{self.get_indent()}{stmt_str}")
                    cff_code.append(f"{self.get_indent()}{state_var_name} = {i+2 if i < len(stmts_to_flatten)-1 else 0};")
                    cff_code.append(f"{self.get_indent()}break;")
                    self.indent_level -= 1 # Back to switch indent level for next case label
                
                cff_code.append(f"{self.get_indent()}default:") # Default label at current indent
                self.indent_level += 1 # Deeper for default content
                cff_code.append(f"{self.get_indent()}{state_var_name} = 0;")
                cff_code.append(f"{self.get_indent()}break;")
                self.indent_level -= 1 # Back to switch indent level
                
                self.indent_level -=1 # Back from switch content to while content level
                cff_code.append(f"{self.get_indent()}}}") # end switch
                self.indent_level -=1 # Back from while content to block's main content level
                cff_code.append(f"{self.get_indent()}}}") # end while
            
            self.indent_level -= 1 # Back from block content to original level before this visitBlock call
            final_content = "\n".join(filter(None, cff_code))
            return f"{{\n{final_content}\n{self.get_indent()}}}" if final_content.strip() else f"{{\n{self.get_indent()}}}"
    def visitAdditiveExpression(self, ctx:MiniCParser.AdditiveExpressionContext):
        if ("transform_expressions" not in self.active_techniques or \
            not self.active_techniques["transform_expressions"]) or \
            ctx.getChildCount() <= 1: 
            return super().visitAdditiveExpression(ctx)
        result = self.visit(ctx.multiplicativeExpression(0))
        idx = 1
        while idx < ctx.getChildCount():
            op, right_op_node = ctx.getChild(idx).getText(), ctx.getChild(idx+1)
            right_op_text = self.visit(right_op_node)
            result += f" - (0 - ({right_op_text}))" if op == '+' else f" + (0 - ({right_op_text}))"
            idx += 2
        return result

    def visitFunctionDeclaration(self, ctx:MiniCParser.FunctionDeclarationContext):
        orig_name = ctx.IDENTIFIER().getText()
        self.is_in_cff_target_block = ("flatten_control_flow" in self.active_techniques and \
                                      self.active_techniques["flatten_control_flow"] and orig_name == "main")
        
        type_spec = self.visit(ctx.typeSpecifier()) # Will set uses_stdbool if type is bool
        new_name = orig_name
        
        outer_scope = self.current_scope
        if orig_name not in ["main", "printf", "scanf"] and \
           "rename" in self.active_techniques and self.active_techniques["rename"]:
            new_name = self._get_renamed_globally(orig_name, "f")
        elif orig_name not in self.global_scope.symbols:
            self.global_scope.symbols[orig_name] = orig_name

        self.current_scope = Scope(parent=self.global_scope)
        
        params_str = ""
        if ctx.parameters():
            param_strs = []
            for p_ctx in ctx.parameters().parameter():
                # Visit type specifier for parameter, which also checks for bool usage
                p_type_str = self.visit(p_ctx.typeSpecifier()) 
                p_orig = p_ctx.IDENTIFIER().getText()
                p_new = p_orig
                if "rename" in self.active_techniques and self.active_techniques["rename"]:
                    p_new = self.current_scope.declare(p_orig, prefix="p_")
                else: self.current_scope.symbols[p_orig] = p_orig
                param_strs.append(f"{p_type_str} {p_new}")
            params_str = ", ".join(param_strs)
            
        body_str = self.visit(ctx.block())
        self.current_scope = outer_scope
        return f"{type_spec} {new_name}({params_str}) {body_str}"

    def visitVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        type_spec = self.visit(ctx.typeSpecifier()) # Will set uses_stdbool if type is bool
        orig_name = ctx.IDENTIFIER().getText()
        new_name = orig_name
        
        is_param = orig_name in self.current_scope.symbols and self.current_scope.parent == self.global_scope

        if not is_param and "rename" in self.active_techniques and self.active_techniques["rename"]:
            new_name = self.current_scope.declare(orig_name, prefix="v_")
        elif not is_param and orig_name not in self.current_scope.symbols:
            self.current_scope.symbols[orig_name] = orig_name
        elif is_param : 
            new_name = self.current_scope.symbols[orig_name]
            
        init_expr = f" = {self.visit(ctx.expression())}" if ctx.expression() else ""
        return f"{self.get_indent()}{type_spec} {new_name}{init_expr};"

    def visitPrimaryExpression(self, ctx:MiniCParser.PrimaryExpressionContext):
        if ctx.IDENTIFIER(): return self.current_scope.lookup(ctx.IDENTIFIER().getText())
        if ctx.constant(): return self.visit(ctx.constant()) # Will set uses_stdbool if bool literal
        if ctx.LPAREN(): return f"({self.visit(ctx.expression())})"
        if ctx.functionCall(): return self.visit(ctx.functionCall())
        return super().visitPrimaryExpression(ctx)

    def visitFunctionCall(self, ctx:MiniCParser.FunctionCallContext):
        orig_name = ctx.IDENTIFIER().getText()
        if orig_name in ["printf", "scanf"]: self.uses_stdio = True
        renamed_name = self.global_scope.lookup(orig_name)
        args = self.visit(ctx.arguments()) if ctx.arguments() else ""
        return f"{renamed_name}({args})"

    # visitTypeSpecifier and visitConstant are crucial for setting uses_stdbool
    def visitTypeSpecifier(self, ctx:MiniCParser.TypeSpecifierContext):
        if ctx.BOOL(): # If the actual token matched is BOOL
            self.uses_stdbool = True
        return ctx.getText() 

    def visitConstant(self, ctx:MiniCParser.ConstantContext):
        if ctx.BOOL_LITERAL(): # If a boolean literal 'true' or 'false' is parsed
            self.uses_stdbool = True
        return ctx.getText()

    def visitArguments(self, ctx:MiniCParser.ArgumentsContext): # From CodeReconstructionVisitor
        return ", ".join(self.visit(expr) for expr in ctx.expression())

    # Make sure get_indent in CodeReconstructionVisitor (ast_visitor.py) does NOT take an argument.
    # If you need a different indent level temporarily, manage self.indent_level before/after calling get_indent().
    # Example: get_indent(self, offset=0): return " " * (self.indent_level + offset) * 4
    # The error was from calling self.get_indent(1)
    # Fixed in visitBlock's CFF path by adjusting self.indent_level around calls to self.get_indent()
    # The get_indent in ast_visitor.py should be:
    # def get_indent(self): return "    " * self.indent_level