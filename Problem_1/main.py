def give_remainder_dict(dividend, divisor, number_of_digits):
    # result = round((dividend / divisor), number_of_digits)
    result = format((dividend / divisor), f'.{number_of_digits}f')  # get the required digits after .
    b = list(result.split(".")[1])  # converted that digits to a list after the .
    x = [int(i) for i in b]  # converted the elements into integer
    output_result = dict()  # final output
    for i in range(1, 10):
        output_result[i] = x.count(i)  # stores the result into dictionary
    output_result[0] = x.count(0)
    return output_result  # final dictionary


test_cases = int(input("Enter No. of Test Cases  "))
for i in range(test_cases):
    dividend = int(input("Enter dividend  "))
    divisor = int(input("Enter divisor  "))
    number_of_digits = int(input("Enter number of digits  "))
    print(f"test case {i + 1}: \n--", give_remainder_dict(dividend, divisor, number_of_digits))
