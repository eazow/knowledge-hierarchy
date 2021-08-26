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
    Param,
)
from tokens import (
    INTEGER,
    LPAREN,
    RPAREN,
    PLUS,
    MINUS,
    MUL,
    DIV,
    EOF,
    DOT,
    BEGIN,
    END,
    ID,
    ASSIGN,
    SEMI,
    VAR,
    COMMA,
    COLON,
    REAL,
    PROGRAM,
    FLOAT_DIV,
    INTEGER_DIV,
    INTEGER_CONST,
    REAL_CONST,
    PROCEDURE,
)


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

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
        if token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type in [PLUS, MINUS]:
            self.eat(token.type)
            return UnaryOp(token, self.factor())
        elif token.type == ID:
            node = self.variable()
            return node

        self.error()

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in [MUL, INTEGER_DIV, FLOAT_DIV]:
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

        while self.current_token.type in [PLUS, MINUS]:
            op = self.current_token
            self.eat(op.type)

            node = BinOp(left=node, op=op, right=self.term())

        return node

    def parse(self):
        # return self.expr()
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node

    def program(self):
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)

        block_node = self.block()
        program_node = Program(prog_name, block_node)
        # node = self.compound_statement()
        self.eat(DOT)
        return program_node

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        root.children = nodes
        return root

    def statement_list(self):
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assign_statement()
        else:
            node = self.empty()
        return node

    def assign_statement(self):
        left = self.variable()
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return Assign(left, op, right)

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
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
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)

        while self.current_token.type == PROCEDURE:
            self.eat(PROCEDURE)
            proc_name = self.current_token.value
            self.eat(ID)
            params = []

            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                params = self.formal_params_list()
                self.eat(RPAREN)

            self.eat(SEMI)
            block_node = self.block()
            proc_decl = ProcedureDecl(proc_name, params, block_node)
            declarations.append(proc_decl)
            self.eat(SEMI)

        return declarations

    def variable_declaration(self):
        """variable_declaration : ID (, ID)* : type_spec"""
        var_nodes = [Var(self.current_token)]
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)

        self.eat(COLON)

        type_node = self.type_spec()
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return var_declarations

    def type_spec(self):
        """type_spec : INTEGER | REAL"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        return Type(token)

    def formal_params_list(self):
        """formal_params_list: formal_params | formal_params SEMI formal_params"""
        if self.current_token.type != ID:
            return []

        param_nodes = self.formal_params()

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            param_nodes.extend(self.formal_params())

        return param_nodes

    def formal_params(self):
        """formal_params: ID (, ID)* : type_spec"""
        param_tokens = [self.current_token]
        self.eat(ID)

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            param_tokens.append(self.current_token)
            self.eat(ID)

        self.eat(COLON)
        type_node = self.type_spec()

        return [Param(Var(t), type_node) for t in param_tokens]