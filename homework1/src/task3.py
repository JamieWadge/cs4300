#Gets a number and returns sign in str
def number_sign(num):

    if num > 0:
        return "positive"
    
    elif num < 0:
        return "negative"
    
    else:
        return "zero"

#Puts the first ten prime numbers in list
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

#Gets the sum of 1 to 100                    
def sum_100():
    sum = 0
    count = 1

    while count <= 100:
        sum += count
        count += 1

    return sum

print("Ten is:", number_sign(10))
print("Negative Ten is:", number_sign(-10))
print("Zero is:", number_sign(0))
print("First ten primes are:", ten_prime())
print("Sum is:", sum_100())