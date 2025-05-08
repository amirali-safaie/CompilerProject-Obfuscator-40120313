from minic_parser.MiniCParser import MiniCParser
from ast_visitor import CodeReconstructionVisitor # Reuse for base structure

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {} # original_name -> new_name
        self.name_counter = 0

    def declare(self, original_name, prefix="v_"):
        # Generate a new, unique ugly name
        new_name = f"{prefix}{self.name_counter}"
        self.name_counter += 1
        self.symbols[original_name] = new_name
        return new_name

    def lookup(self, original_name):
        if original_name in self.symbols:
            return self.symbols[original_name]
        if self.parent:
            return self.parent.lookup(original_name)
        # If not found, it might be a built-in like printf or an error
        # For now, return original name if not found (e.g. printf, scanf)
        # A more robust solution would pre-populate global scope with known functions
        if original_name in ["printf", "scanf"]: # Don't rename built-ins
             return original_name
        return f"UNKNOWN_{original_name}" # Or raise error

class ObfuscatorVisitor(CodeReconstructionVisitor): # Inherit for structure
    def __init__(self, active_techniques):
        super().__init__()
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.function_name_counter = 0
        self.active_techniques = active_techniques # Dict like {"rename": True, ...}

        # Pre-define known functions that shouldn't be renamed by default
        # Or handle them in lookup. For simplicity, let's assume they are not user-defined with these names.
        # self.global_scope.symbols["printf"] = "printf"
        # self.global_scope.symbols["scanf"] = "scanf"

    def generate_new_func_name(self):
        name = f"func_{self.function_name_counter}"
        self.function_name_counter += 1
        return name

    # --- Overridden methods for Renaming ---
    def visitFunctionDeclaration(self, ctx:MiniCParser.FunctionDeclarationContext):
        if "rename" not in self.active_techniques or not self.active_techniques["rename"]:
            return super().visitFunctionDeclaration(ctx)

        type_spec = self.visit(ctx.typeSpecifier())
        original_func_name = ctx.IDENTIFIER().getText()
        
        # Don't rename main, or specific built-ins if they were parsed as general IDs
        if original_func_name == "main" or original_func_name in ["printf", "scanf"]:
             new_func_name = original_func_name
             self.global_scope.symbols[original_func_name] = new_func_name # Still record it
        else:
            new_func_name = self.global_scope.declare(original_func_name, prefix="f_")


        self.current_scope = Scope(parent=self.global_scope) # New scope for function
        
        params_str = ""
        if ctx.parameters():
            # Process parameters within the new function scope
            param_nodes = ctx.parameters().parameter()
            param_strs = []
            for p_ctx in param_nodes:
                p_type = self.visit(p_ctx.typeSpecifier())
                p_orig_name = p_ctx.IDENTIFIER().getText()
                p_new_name = self.current_scope.declare(p_orig_name, prefix="p_")
                param_strs.append(f"{p_type} {p_new_name}")
            params_str = ", ".join(param_strs)

        # Visit block within the function's scope
        body_str = self.visit(ctx.block()) # Block will use current_scope

        self.current_scope = self.global_scope # Pop scope
        return f"{type_spec} {new_func_name}({params_str}) {body_str}"

    def visitVariableDeclaration(self, ctx:MiniCParser.VariableDeclarationContext):
        # Renaming logic
        if "rename" not in self.active_techniques or not self.active_techniques["rename"]:
            return super().visitVariableDeclaration(ctx)

        type_spec = self.visit(ctx.typeSpecifier())
        original_name = ctx.IDENTIFIER().getText()
        new_name = self.current_scope.declare(original_name, prefix="v_")
        
        init_expr_str = ""
        if ctx.expression():
            init_expr_str = f" = {self.visit(ctx.expression())}" # Expression will lookup renamed vars

        return f"{self.get_indent()}{type_spec} {new_name}{init_expr_str};"

    def visitPrimaryExpression(self, ctx:MiniCParser.PrimaryExpressionContext):
        if "rename" not in self.active_techniques or not self.active_techniques["rename"]:
             return super().visitPrimaryExpression(ctx)

        if ctx.IDENTIFIER():
            original_name = ctx.IDENTIFIER().getText()
            new_name = self.current_scope.lookup(original_name)
            return new_name
        # Delegate to super for constants, parenthesized expressions, and function calls
        # Function calls are handled separately by visitFunctionCall
        if ctx.constant(): return self.visit(ctx.constant())
        if ctx.LPAREN(): return f"({self.visit(ctx.expression())})"
        if ctx.functionCall(): return self.visit(ctx.functionCall())
        return super().visitPrimaryExpression(ctx) # Fallback

    def visitFunctionCall(self, ctx:MiniCParser.FunctionCallContext):
        if "rename" not in self.active_techniques or not self.active_techniques["rename"]:
            return super().visitFunctionCall(ctx)

        original_func_name = ctx.IDENTIFIER().getText()
        # Functions are typically in global scope for Mini-C
        new_func_name = self.global_scope.lookup(original_func_name) 
                                            # If it was a local func pointer (not in MiniC)
                                            # it would be current_scope.lookup

        args_str = ""
        if ctx.arguments():
            args_str = self.visit(ctx.arguments()) # Arguments are expressions, will use renaming
        return f"{new_func_name}({args_str})"
    
    def visitBlock(self, ctx:MiniCParser.BlockContext):
        # For renaming, ensure block statements are processed in a new scope if it's a standalone block
        # not directly part of a function (though MiniC grammar implies blocks are mainly for func/if/while/for)
        # Our current logic: functionDeclaration creates new scope, block reuses it.
        # If a block could declare variables and create a new scope:
        # previous_scope = self.current_scope
        # self.current_scope = Scope(parent=previous_scope)
        # ... visit statements ...
        # self.current_scope = previous_scope
        # For now, standard block doesn't create its own *new* scope for renaming beyond what its parent (func, if, etc.) provides.
        # CodeReconstructionVisitor's visitBlock is fine for structure.
        # Obfuscation techniques might want to inject code *into* the block.

        # This method will be important for dead code insertion and CFF.
        # For now, let's just use the inherited one and see how renaming fares.
        return super().visitBlock(ctx)


# In main.py, you'd instantiate this:
# techniques = {"rename": True}
# obfuscator = ObfuscatorVisitor(techniques)
# obfuscated_code = obfuscator.visit(tree)