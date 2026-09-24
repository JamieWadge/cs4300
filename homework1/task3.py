def number_sign():
    num = int(input("Enter a number: "))

    if num > 0:
        return "positive"
    
    elif num < 0:
        return "negative"
    
    else:
        return "zero"

def ten_prime():
    primes = []

    

def test_sign():
    sign = number_sign()

    if sign == "positive":
        assert sign == "positive"
    
    elif sign == "negative":
        assert sign == "negative"
    
    else:
        assert sign == "zero"