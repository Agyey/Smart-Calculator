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
        command = command.split()
    try:
        nums = list(map(int, command))
    except:
        print('Only Numbers Can be Used')
        print('This Program prints the sum of 2 or more numbers.')
        print("Type '/help' for help on how to use the program.")
        continue
    if len(nums) >= 2:
        print(sum(nums))
    elif len(nums) == 1:
        print(nums[0])
    else:
        continue
