import multiplication
import addition

def main(a,b):
    print("Addition: ",addition.add(a,b))
    print("Multiplication: ",multiplication.multiply(a,b))
a=int(input("Enter a number: "))
b=int(input("Enter b number: "))
main(a,b)