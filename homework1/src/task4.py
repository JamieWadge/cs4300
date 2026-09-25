#Calculates discount given price and discount amount
def calculate_discount(price, discount):
    return price - (price * discount / 100)

print("10 percent of 90 is:", calculate_discount(100, 10))
print("33.3 percent of 100 is:", calculate_discount(100, 33.3))
print("10 percent of 50.5 is:", calculate_discount(50.5, 10))
print("33.3 percent of 50.5 is:", calculate_discount(50.5, 33.3))