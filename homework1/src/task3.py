def number_sign(num):

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
            prime.append(number)

        if len(prime) == 10:
            break
    
    return prime
                    
def sum_100():
    sum = 0
    count = 1

    while count <= 100:
        sum += count
        count += 1

    return sum