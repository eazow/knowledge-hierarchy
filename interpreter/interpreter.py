
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
        
