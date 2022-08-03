def Test(desc, method, input, expected):
    print('Running test: ' + desc)
    result = method(input)
    if (result == expected):
        print(f'Passed test: {result} == {expected}')
    else:
        print(f'Failed test: {result} != {expected}')