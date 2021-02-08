import itertools as it
import sys

def sum_digits(digit):
    if digit < 10:
        return digit
    else:
        sum = (digit % 10) + (digit // 10)
        return sum

def validate(cc_num):
    # reverse the credit card number
    cc_num = cc_num[::-1]
    # convert to integer list
    cc_num = [int(x) for x in cc_num]
    # double every second digit
    doubled_second_digit_list = list()
    digits = list(enumerate(cc_num, start=1))
    for index, digit in digits:
        if index % 2 == 0:
            doubled_second_digit_list.append(digit * 2)
        else:
            doubled_second_digit_list.append(digit)

    # add the digits if any number is more than 9
    doubled_second_digit_list = [sum_digits(x) for x in doubled_second_digit_list]
    # sum all digits
    sum_of_digits = sum(doubled_second_digit_list)
    # return True or False
    return sum_of_digits % 10 == 0

if __name__ == "__main__":
    # target = 543******5251849
    
    digits = "0123456789"
    # combos = it.permutations(digits, 6)

    # for i in combos:
    for i in range(999999):
        # num = "543" + ''.join(i) + "5251849"
        num = '543' + '{:0>6}'.format(str(i)) + '5251849'
        sys.stdout.write('\r> ' + num)
        if validate(num) and int(num)%53451==0:

            print("\nFound: " + num)
            # break

"""
: 5434511245251849
> 5435045755251849
Found: 5435045755251849
> 5439999985251849
"""