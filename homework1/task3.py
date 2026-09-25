def number_sign():
    num = int(input("Enter a number: "))

    if num > 0:
        return "positive"
    
    elif num < 0:
        return "negative"
    
    else:
        return "zero"

def ten_prime():
    prime = []

    for number in range(2, 100):
        is_prime = True

        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(number)

        if len(prime) == 10:
            number = 100
    
    return prime
                    
def sum_100():
    sum = 0
    count = 1

    while count <= 100:
        sum += count
        count += 1
    
    print(sum)

    return sum

def test_sign():
    sign = number_sign()

    if sign == "positive":
        assert sign == "positive"
    
    elif sign == "negative":
        assert sign == "negative"
    
    else:
        assert sign == "zero"

def test_prime():
    assert ten_prime == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_100():
    assert sum_100() == 5050