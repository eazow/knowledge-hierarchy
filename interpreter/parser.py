from errors import ParserError, ErrorCode
from nodes import (
    BinOp,
    UnaryOp,
    Num,
    Compound,
    Assign,
    Var,
    NoOp,
    Block,
    VarDecl,
    Type,
    Program,
    ProcedureDecl,
    Param, ProcedureCall,
)
from tokens import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, error_code=None, token=None):
        raise ParserError(
            error_code=error_code, token=token, message=f"{error_code.value} -> {token}"
        )

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(error_code=ErrorCode.UNEXPECTED_TOKEN, token=self.current_token)

    def factor(self):
        """
        factor : PLUS factor
               | MINUS factor
               | INTEGER_CONST
               | REAL_CONST
               | LPAREN expr RPAREN
               | variable
        """
        token = self.current_token
        if token.type == TokenType.INTEGER_CONST:
            self.eat(TokenType.INTEGER_CONST)
            return Num(token)
        elif token.type == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        elif token.type in [TokenType.PLUS, TokenType.MINUS]:
            self.eat(token.type)
            return UnaryOp(token, self.factor())
        elif token.type == TokenType.ID:
            node = self.variable()
            return node

        self.error(error_code=ErrorCode.INVALID_SYNTAX, token=token)

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in [TokenType.MUL, TokenType.INTEGER_DIV, TokenType.FLOAT_DIV]:
            op = self.current_token
            self.eat(op.type)

            node = BinOp(left=node, op=op, right=self.factor())

        return node

    def expr(self):
        """Arithmetic expression parser / interpreter.
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        node = self.term()

        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token
            self.eat(op.type)

            node = BinOp(left=node, op=op, right=self.term())

        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error()

        return node

    def program(self):
        self.eat(TokenType.PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(TokenType.SEMI)

        block_node = self.block()
        program_node = Program(prog_name, block_node)
        # node = self.compound_statement()
        self.eat(TokenType.DOT)
        return program_node

    def compound_statement(self):
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        root.children = nodes
        return root

    def statement_list(self):
        node = self.statement()

        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        if self.current_token.type == TokenType.ID:
            self.error()

        return results

    def statement(self):
        """
        statement : compound_statement
                  | proccall_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.ID:
            if self.lexer.current_char == TokenType.LPAREN.value:
                node = self.proccall_statement()
            else:
                node = self.assign_statement()
        else:
            node = self.empty()
        return node

    def assign_statement(self):
        left = self.variable()
        op = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        return Assign(left, op, right)

    def variable(self):
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    @staticmethod
    def empty():
        return NoOp()

    def block(self):
        """block : declarations compound_statement"""
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node

    def declarations(self):
        """declarations : (VAR (variable_declaration SEMI)+)*
        | (PROCEDURE ID (LPAREN formal_parameter_list RPAREN)? SEMI block SEMI)*
        | empty
        """
        declarations = []
        if self.current_token.type == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.type == TokenType.ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(TokenType.SEMI)

        while self.current_token.type == TokenType.PROCEDURE:
            proc_decl = self.procedure_declaration()
            declarations.append(proc_decl)

        return declarations

    def procedure_declaration(self):
        self.eat(TokenType.PROCEDURE)
        proc_name = self.current_token.value
        self.eat(TokenType.ID)
        params = []
        if self.current_token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            params = self.formal_params_list()
            self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMI)
        block_node = self.block()
        proc_decl = ProcedureDecl(proc_name, params, block_node)
        self.eat(TokenType.SEMI)
        return proc_decl

    def variable_declaration(self):
        """variable_declaration : ID (, ID)* : type_spec"""
        var_nodes = [Var(self.current_token)]
        self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)

        type_node = self.type_spec()
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return var_declarations

    def type_spec(self):
        """type_spec : INTEGER | REAL"""
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
        else:
            self.eat(TokenType.REAL)
        return Type(token)

    def formal_params_list(self):
        """formal_params_list: formal_params | formal_params SEMI formal_params"""
        if self.current_token.type != TokenType.ID:
            return []

        param_nodes = self.formal_params()

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            param_nodes.extend(self.formal_params())

        return param_nodes

    def formal_params(self):
        """formal_params: ID (, ID)* : type_spec"""
        param_tokens = [self.current_token]
        self.eat(TokenType.ID)

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            param_tokens.append(self.current_token)
            self.eat(TokenType.ID)

        self.eat(TokenType.COLON)
        type_node = self.type_spec()

        return [Param(Var(t), type_node) for t in param_tokens]

    def proccall_statement(self):
        """proccall_statement: ID LPAREN (expr (COMMA expr)*)? RPAREN"""
        token = self.current_token

        proc_name = token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)

        actual_params = []

        if self.current_token.type != TokenType.RPAREN:
            actual_params.append(self.expr())

        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            actual_params.append(self.expr())

        self.eat(TokenType.RPAREN)

        return ProcedureCall(proc_name, actual_params, token)
