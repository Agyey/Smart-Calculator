import re
from collections import OrderedDict


class Calculator:

    def __init__(self, variables=None):
        if variables is None:
            variables = dict()
        self.run: bool = True
        self.error: bool = False
        self.variables: dict = variables
        self.expression: str = ''
        self.results: OrderedDict = OrderedDict()
        self.infix: list = list()
        self.postfix: list = list()
        self.stack: list = list()
        self.operand = ''
        self.result = None

    def is_running(self) -> bool:
        return self.run

    def is_command(self) -> bool:
        return self.expression.startswith('/')

    def is_assignment(self) -> bool:
        return '=' in self.expression

    def is_binary(self) -> bool:
        return bool(re.match(r"^([+-]+|[*/])$", self.operand))

    def is_operator(self) -> bool:
        return bool(re.match(r"^([+*/^-]+|\(+|\)+)$", self.operand))

    def is_variable(self) -> bool:
        return bool(re.match(r"^[a-zA-Z_$][a-zA-Z_$]*$", self.operand))

    def is_numeric(self) -> bool:
        return isinstance(self.operand, int) or self.operand.isnumeric()

    def is_operand(self) -> bool:
        return self.is_numeric() or self.is_variable() or self.is_operator()

    @staticmethod
    def is_higher_precedence(x, y) -> bool:
        precedence = "^/*+-"
        precedence = {
            '^': 0,
            '/': 1,
            '*': 1,
            '+': 2,
            '-': 2,
        }
        if y in precedence:
            if x in precedence:
                return precedence[y] <= precedence[x]
            else:
                return True
        else:
            return False

    def operate(self, x, y, operator):
        try:
            x = int(x)
            y = int(y)
            if operator == '+':
                self.result = x + y
            elif operator == '-':
                self.result = x - y
            elif operator == '/':
                self.result = x / y
            elif operator == '*':
                self.result = x * y
            elif operator == '^':
                self.result = x ** y
        except:
            self.report_error('Invalid expression')

    def report_error(self, message: str):
        self.result = message
        self.error = True

    def clear(self):
        self.expression = ''
        self.infix = list()
        self.postfix = list()
        self.stack = list()
        self.operand = ''
        self.result = None
        self.error = False

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        value = self.stack[-1]
        self.stack = self.stack[:-1]
        return value

    def simplify_operator(self):
        if re.match('^[+-]+$', self.operand):
            plus_count = self.operand.count('+')
            minus_count = self.operand.count('-') % 2
            self.operand = '+' if plus_count >= 0 and minus_count == 0 else '-'
        else:
            if len(self.operand) != 1:
                self.report_error('Invalid expression')

    def process_command(self):
        if self.expression == '/exit':
            self.run = False
            self.result = 'Bye!'
        elif self.expression == '/help':
            self.result = "Hi, I'm a calculator!\n" \
                          "Type /history to see All calculations\n" \
                          "Type /clear to reset history\n" \
                          "Type /exit to stay bye!\n"
        elif self.expression == '/history':
            for expression, result in self.results.items():
                print(expression, result)
            self.result = "Type /clear to reset history"
        elif self.expression == '/clear':
            self.results = OrderedDict()
            self.clear()
            self.result = "Type /exit to stay bye!"
        else:
            self.report_error('Unknown command')

    def process_assignment(self):
        if self.expression.count('=') == 1:
            var, expression = map(lambda x: str(x).strip(), self.expression.split('='))
            self.operand = var
            if self.is_variable():
                sub_calculator = Calculator(self.variables)
                self.operand = sub_calculator.calculate(expression)
                if self.is_numeric():
                    self.variables[var] = self.operand
                    self.result = 'store'
                else:
                    self.report_error('Invalid assignment')
            else:
                self.report_error('Invalid assignment')
        else:
            self.report_error('Invalid assignment')

    def add_to_infix(self, ):
        if self.is_variable():
            if self.operand in self.variables:
                self.infix.append(str(self.variables[self.operand]))
            else:
                self.report_error('Unknown Variable')
        else:
            if self.is_operator():
                self.simplify_operator()
            if not self.error:
                self.infix.append(self.operand)

    def expression_to_infix(self):
        for char in self.expression:
            self.operand += char.strip()
            if not self.is_operand():
                self.operand = self.operand[:-1]
                self.add_to_infix()
                if self.error:
                    break
                self.operand = char
        if not self.error:
            self.add_to_infix()

    def infix_to_postfix(self):
        self.push('#')
        last_operand = ''
        for operand in self.infix:
            if operand.isalnum():
                self.postfix.append(operand)
            elif operand == '(':
                self.push('(')
            elif operand == '^':
                self.push('^')
            elif operand == ')':
                while self.stack[-1] != '#' and self.stack[-1] != '(':
                    self.postfix.append(self.pop())
                self.pop()
            else:
                while self.stack[-1] != '#' and self.is_higher_precedence(operand, self.stack[-1]):
                    self.postfix.append(self.pop())
                self.push(operand)
        while self.stack[-1] != '#':
            self.postfix.append(self.pop())

    def process_postfix(self):
        self.stack = []
        for operand in self.postfix:
            self.operand = operand
            if self.is_operator():
                y = self.pop()
                x = self.pop()
                self.operate(x, y, operand)
                self.push(self.result)
            else:
                self.push(operand)
        self.result = self.pop()

    def process_expression(self):
        if self.expression.count('(') != self.expression.count(')'):
            self.report_error('Invalid expression')
        operations = [
            'expression_to_infix',
            'infix_to_postfix',
            'process_postfix'
        ]
        operation = 0
        while not self.error and operation < 3:
            getattr(self, operations[operation])()
            operation += 1

    def calculate(self, expression: str):
        self.clear()
        if expression:
            self.expression = expression
            if self.is_command():
                self.process_command()
            elif self.is_assignment():
                self.process_assignment()
            else:
                self.process_expression()
            self.results[expression] = self.result
        return self.result


calculator = Calculator()
while calculator.is_running():
    result = calculator.calculate(input().strip())
    if result not in ('store', None):
        print(result)
