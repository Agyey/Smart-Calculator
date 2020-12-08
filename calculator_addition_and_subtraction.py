def process(operations):
    total = 0
    operation = '+'
    for operand in operations:
        try:
            operand = int(operand)
            total = perform(total, operand, operation)
        except:
            if operand.count('+') >= 0 and operand.count('-') % 2 == 0:
                operation = '+'
            else:
                operation = '-'
    return total


def perform(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b


while True:
    command = input().strip()
    if command == '/exit':
        print('Bye!')
        break
    elif command == '/help':
        print('This Program prints the sum of numbers.')
        print('Separate the numbers with a space.')
        print('Press /exit to stop using the program.')
        continue
    elif command != '':
        operations = command.split()
        result = process(operations)
        print(result)
