from antlr4.tree.Tree import TerminalNode
from minic_parser.MiniCParser import MiniCParser
from minic_parser.MiniCVisitor import MiniCVisitor


class CodeReconstructionVisitor(MiniCVisitor):
    def __init__(self):
        self.indent_level = 0
        self.code = []  # For building parts of code more easily

    def get_indent(self):
        return "    " * self.indent_level  # 4 spaces for indent

    # Helper to visit a list of nodes and join results
    def visit_node_list(self, nodes, separator=""):
        return separator.join([self.visit(node) for node in nodes if node is not None])

    def visitProgram(self, ctx: MiniCParser.ProgramContext):
        return self.visit_node_list(ctx.declaration(), "\n")

    def visitDeclaration(self, ctx: MiniCParser.DeclarationContext):
        if ctx.variableDeclaration():
            return self.visit(ctx.variableDeclaration())
        elif ctx.functionDeclaration():
            return self.visit(ctx.functionDeclaration())
        return ""  # Should not happen

    def visitVariableDeclaration(self, ctx: MiniCParser.VariableDeclarationContext):
        type_spec = self.visit(ctx.typeSpecifier())
        identifier = ctx.IDENTIFIER().getText()
        init_expr = ""
        if ctx.expression():
            init_expr = f" = {self.visit(ctx.expression())}"
        return f"{self.get_indent()}{type_spec} {identifier}{init_expr};"

    def visitTypeSpecifier(self, ctx: MiniCParser.TypeSpecifierContext):
        return ctx.getText()

    def visitFunctionDeclaration(self, ctx: MiniCParser.FunctionDeclarationContext):
        type_spec = self.visit(ctx.typeSpecifier())
        func_name = ctx.IDENTIFIER().getText()
        params = ""
        if ctx.parameters():
            params = self.visit(ctx.parameters())
        body = self.visit(ctx.block())
        return f"{type_spec} {func_name}({params}) {body}"

    def visitParameters(self, ctx: MiniCParser.ParametersContext):
        return self.visit_node_list(ctx.parameter(), ", ")

    def visitParameter(self, ctx: MiniCParser.ParameterContext):
        return f"{self.visit(ctx.typeSpecifier())} {ctx.IDENTIFIER().getText()}"

    def visitBlock(self, ctx: MiniCParser.BlockContext):
        self.indent_level += 1
        statements = "\n".join([self.visit(stmt) for stmt in ctx.statement()])
        self.indent_level -= 1
        # Handle empty blocks or blocks with only empty statements correctly
        if not statements.strip():  # if block is empty or only contains semicolons
            return f"{{\n{self.get_indent()}}}"  # Avoid extra newline for empty block
        return f"{{\n{statements}\n{self.get_indent()}}}"

    def visitStatement(self, ctx: MiniCParser.StatementContext):
        if ctx.variableDeclaration():
            return self.visit(ctx.variableDeclaration())
        elif ctx.expressionStatement():
            return self.visit(ctx.expressionStatement())
        elif ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        elif ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        elif ctx.forStatement():
            return self.visit(ctx.forStatement())
        elif ctx.returnStatement():
            return self.visit(ctx.returnStatement())
        elif ctx.block():  # Nested block
            # Need to ensure proper indentation if a block is a statement
            return self.get_indent() + self.visit(ctx.block())
        elif ctx.SEMI():  # Empty statement
            return f"{self.get_indent()};"
        return ""  # Should not happen

    def visitExpressionStatement(self, ctx: MiniCParser.ExpressionStatementContext):
        return f"{self.get_indent()}{self.visit(ctx.expression())};"

    def visitIfStatement(self, ctx: MiniCParser.IfStatementContext):
        condition = self.visit(ctx.expression())
        then_stmt = self.visit(ctx.statement(0))  # First statement is 'then'
        else_stmt_str = ""
        if ctx.ELSE():
            # The statement for 'else' might need its own indent if it's not a block
            # Our visitStatement should handle indenting itself
            else_stmt_str = f"\n{self.get_indent()}else {self.visit(ctx.statement(1))}"

        # Adjust formatting for single line statements vs blocks
        # This logic is tricky; a simple reconstruction might not perfectly match original spacing
        # but should be semantically correct.

        # Simplified if statement reconstruction (may need refinement for pretty printing)
        # If 'then_stmt' is a block, it already has newlines and indents
        # If it's a single statement, it needs to be on the same line or indented on next
        if not then_stmt.strip().startswith(self.get_indent() + "{"):  # If not a block
            then_stmt = (
                f"\n{self.get_indent()}{then_stmt.strip()}"
                if "\n" in then_stmt.strip()
                else f" {then_stmt.strip()}"
            )

        return f"{self.get_indent()}if ({condition}){then_stmt}{else_stmt_str}"

    def visitWhileStatement(self, ctx: MiniCParser.WhileStatementContext):
        condition = self.visit(ctx.expression())
        body_stmt = self.visit(ctx.statement())
        if not body_stmt.strip().startswith(self.get_indent() + "{"):
            body_stmt = (
                f"\n{self.get_indent()}{body_stmt.strip()}"
                if "\n" in body_stmt.strip()
                else f" {body_stmt.strip()}"
            )
        return f"{self.get_indent()}while ({condition}){body_stmt}"

    # In ast_visitor.py (inside CodeReconstructionVisitor class)

    def visitForStatement(self, ctx: MiniCParser.ForStatementContext):
        init_str = ""
        if ctx.init:  # ctx.init is now a ForInitializationContext
            init_str = self.visit(ctx.init)  # Visit the forInitialization rule

        condition_str = ""
        if ctx.cond:  # Accessing labeled 'cond' expression
            condition_str = self.visit(ctx.cond)

        update_str = ""
        if ctx.upd:  # Accessing labeled 'upd' expression
            update_str = self.visit(ctx.upd)

        body_stmt_str = self.visit(ctx.body)  # Accessing labeled 'body' statement

        current_indent_str = self.get_indent()
        # Adjust formatting for single-line body statements vs. blocks
        if (
            not body_stmt_str.strip().startswith(current_indent_str + "{")
            and "\n" not in body_stmt_str.strip()
            and body_stmt_str.strip() != ";"
        ):
            body_stmt_str = f"\n{current_indent_str}    {body_stmt_str.strip()}"
        elif body_stmt_str.strip() == ";":
            body_stmt_str = f"\n{current_indent_str}    ;"

        return f"{current_indent_str}for ({init_str}; {condition_str}; {update_str}){body_stmt_str}"

    def visitForInitialization(self, ctx: MiniCParser.ForInitializationContext):
        if ctx.varInit:  # Check for the labeled variableDeclaration
            # For variableDeclaration in 'for' init, reconstruct without its own trailing semicolon.
            var_decl_ctx = ctx.varInit  # This is VariableDeclarationContext
            type_spec = self.visit(var_decl_ctx.typeSpecifier())
            identifier = var_decl_ctx.IDENTIFIER().getText()
            init_expr_val = ""
            if var_decl_ctx.expression():  # Expression for the variable's initializer
                init_expr_val = f" = {self.visit(var_decl_ctx.expression())}"
            return f"{type_spec} {identifier}{init_expr_val}"
        elif ctx.exprInit:  # Check for the labeled expression
            return self.visit(ctx.exprInit)
        return ""  # Empty initialization

    def visitReturnStatement(self, ctx: MiniCParser.ReturnStatementContext):
        expr_str = ""
        if ctx.expression():
            expr_str = f" {self.visit(ctx.expression())}"
        return f"{self.get_indent()}return{expr_str};"

    # --- Expression Handling ---
    # For expressions, we generally want to reconstruct them as they appear,
    # including parentheses where the grammar implies them (e.g. primaryExpression).
    # The ANTLR tree already captures operator precedence.

    def visitExpression(self, ctx: MiniCParser.ExpressionContext):
        return self.visit(ctx.assignmentExpression())

    def visitAssignmentExpression(self, ctx: MiniCParser.AssignmentExpressionContext):
        if ctx.ASSIGN():
            left = self.visit(ctx.logicalOrExpression())  # The left side of assignment
            right = self.visit(
                ctx.assignmentExpression()
            )  # The right side (recursive for chained assignments)
            return f"{left} = {right}"
        return self.visit(
            ctx.logicalOrExpression()
        )  # Or just the logicalOrExpression if no assignment

    def visitLogicalOrExpression(self, ctx: MiniCParser.LogicalOrExpressionContext):
        if len(ctx.logicalAndExpression()) > 1:
            return f"{self.visit(ctx.logicalAndExpression(0))} || {self.visit(ctx.logicalOrExpression().logicalAndExpression(1))}"  # Simplified for binary
        # Correct for chain:
        result = self.visit(ctx.logicalAndExpression(0))
        for i in range(1, len(ctx.logicalAndExpression())):
            result += f" || {self.visit(ctx.logicalAndExpression(i))}"
        return result

    def visitLogicalAndExpression(self, ctx: MiniCParser.LogicalAndExpressionContext):
        result = self.visit(ctx.equalityExpression(0))
        for i in range(1, len(ctx.equalityExpression())):
            result += f" && {self.visit(ctx.equalityExpression(i))}"
        return result

    def visitEqualityExpression(self, ctx: MiniCParser.EqualityExpressionContext):
        result = self.visit(ctx.relationalExpression(0))
        if len(ctx.relationalExpression()) > 1:
            op = (
                "==" if ctx.EQ() else "!="
            )  # Assuming only one operator if multiple expressions
            # Correct way to handle multiple ops in the rule a (OP b (OP C ...))
            # The grammar is (relationalExpression ((EQ | NEQ) relationalExpression)*)
            # So we visit the first, then loop through operator and subsequent expressions
            idx = 1
            while idx < len(ctx.relationalExpression()):
                op_node = ctx.getChild(idx * 2 - 1)  # EQ or NEQ node
                op_text = op_node.getText()
                result += f" {op_text} {self.visit(ctx.relationalExpression(idx))}"
                idx += 1
        return result

    def visitRelationalExpression(self, ctx: MiniCParser.RelationalExpressionContext):
        result = self.visit(ctx.additiveExpression(0))
        idx = 1
        while idx < len(ctx.additiveExpression()):
            op_node = ctx.getChild(idx * 2 - 1)  # LT, LTE, GT, GTE node
            op_text = op_node.getText()
            result += f" {op_text} {self.visit(ctx.additiveExpression(idx))}"
            idx += 1
        return result

    def visitAdditiveExpression(self, ctx: MiniCParser.AdditiveExpressionContext):
        result = self.visit(ctx.multiplicativeExpression(0))
        idx = 1
        while idx < len(ctx.multiplicativeExpression()):
            op_node = ctx.getChild(idx * 2 - 1)  # PLUS or MINUS node
            op_text = op_node.getText()
            result += f" {op_text} {self.visit(ctx.multiplicativeExpression(idx))}"
            idx += 1
        return result

    def visitMultiplicativeExpression(
        self, ctx: MiniCParser.MultiplicativeExpressionContext
    ):
        result = self.visit(ctx.unaryExpression(0))
        idx = 1
        while idx < len(ctx.unaryExpression()):
            op_node = ctx.getChild(idx * 2 - 1)  # MUL, DIV, MOD node
            op_text = op_node.getText()
            result += f" {op_text} {self.visit(ctx.unaryExpression(idx))}"
            idx += 1
        return result

    def visitUnaryExpression(self, ctx: MiniCParser.UnaryExpressionContext):
        if ctx.PLUS():
            return f"+{self.visit(ctx.unaryExpression())}"
        if ctx.MINUS():
            return f"-{self.visit(ctx.unaryExpression())}"
        if ctx.NOT():
            return f"!{self.visit(ctx.unaryExpression())}"
        return self.visit(ctx.primaryExpression())

    def visitPrimaryExpression(self, ctx: MiniCParser.PrimaryExpressionContext):
        if ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        if ctx.constant():
            return self.visit(ctx.constant())
        if ctx.LPAREN():  # Parenthesized expression
            return f"({self.visit(ctx.expression())})"
        if ctx.functionCall():
            return self.visit(ctx.functionCall())
        return ""  # Should not happen

    def visitFunctionCall(self, ctx: MiniCParser.FunctionCallContext):
        func_name = ctx.IDENTIFIER().getText()
        args_str = ""
        if ctx.arguments():
            args_str = self.visit(ctx.arguments())
        return f"{func_name}({args_str})"

    def visitArguments(self, ctx: MiniCParser.ArgumentsContext):
        return self.visit_node_list(ctx.expression(), ", ")

    def visitConstant(self, ctx: MiniCParser.ConstantContext):
        return ctx.getText()  # INT_LITERAL, CHAR_LITERAL, BOOL_LITERAL, STRING_LITERAL
