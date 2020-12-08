while True:
    command = input().strip()
    if command == '/exit':
        print('Bye!')
        break
    elif command != '':
        command = command.split()
    try:
        nums = list(map(int, command))
    except:
        print('Only Numbers Can be Used')
        break
    if len(nums) == 2:
        print(sum(nums))
    elif len(nums) == 1:
        print(nums[0])
    else:
        continue
