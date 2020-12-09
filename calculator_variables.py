variables = {}

def process(operands):
    total = 0
    operation = '+'
    skip_operation = []
    for index, operand in enumerate(operands):
        if index in skip_operation:
            continue
        operand, operand_type = operand
        if operand_type == 'numeric':
            total = perform(total, int(operand), operation)
        elif operand_type == 'operation':
            operation = operand
        elif operand_type == 'variable':
            if index + 1 == len(operands):
                if operand in variables:
                    return perform(total, variables[operand], operation)
                else:
                    return 'Unknown variable'
            if operands[index+1][1] == 'operation':
                equate_count = operands[index+1][0].count('=')
                if equate_count == 1:
                    skip_operation.append(index+1)
                    sub_total = process(operands[index+2:])
                    if isinstance(sub_total, int):
                        variables[operand] = sub_total
                        return 'store'
                    else:
                        return 'Invalid assignment'
                if operand in variables:
                    if equate_count == 2:
                        skip_operation.append(index + 1)
                        sub_total = process(operands[index + 2:])
                        return variables[operand] == sub_total

                    elif equate_count > 2 or operand not in variables:
                        return 'Invalid expression'
                    else:
                        total = perform(total, variables[operand], operation)
                else:
                    return 'Unknown variable'
            else:
                return 'Invalid expression'
        else:
            return 'Invalid expression'
    return total


def perform(a, b, operation):
    if operation == '=':
        return 'Invalid assignment'
    elif operation.count('+') >= 0 and operation.count('-') % 2 == 0:
        return a + b
    elif operation.count('-') % 2:
        return a - b


def operations(command):
    operands = [(0, 'numeric'), ]
    operand = ''
    for ch in command:
        if ch == ' ':
            continue
        if operand and operand_type(operand) is not operand_type(ch):
            operands.append((operand, operand_type(operand)))
            operand = ch.strip()
        else:
            operand += ch
    operands.append((operand, operand_type(operand)))
    return operands


def operand_type(operand):
    unique_operands = list(set(operand))
    if operand.isnumeric():
        return 'numeric'
    elif len(unique_operands) == 1 and unique_operands[0] in '+-=/*^':
        return 'operation'
    else:
        return 'variable'


while True:
    command = input().strip()
    if command.startswith("/"):
        if command == '/exit':
            print('Bye!')
            break
        elif command == '/help':
            print('This Program prints the sum of numbers.')
            print('Separate the numbers with a space.')
            print('Press /exit to stop using the program.')
        else:
            print('Unknown command')
    elif command != '':
        operands = operations(command)
        result = process(operands)
        if result != 'store':
            print(result)
