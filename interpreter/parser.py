from nodes import BinOp, UnaryOp, Num, Compound, Assign, Var, NoOp
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
        """factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN  | variable"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
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
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in [MUL, DIV]:
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
        node = self.compound_statement()
        self.eat(DOT)
        return node

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
