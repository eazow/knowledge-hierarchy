
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'


class Token(object):

    def __init__(self, type, value):
        # token type: INTEGER | PLUS | EOF
        self.type = type
        self.value = value

    def __str__(self):
        """
        Examples:
            Token(INTEGER, 6)
        :return:
        """
        return "Token({type}, {value})".format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        if self.position > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.position]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.position += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.position += 1
            return token

        self.error()

