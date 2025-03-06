print("--------------------------------CALCULATOR---------------------------------------")
print("\n\n")
num1 =float(input("Please enter the first number: "))
num2 = float(input("Please enter the second number: "))
operartion = input ("Please enter the operation")
result = 0.0

if operartion == '+':
    result = num1 + num2
elif operartion == "-":
    result = num1 - num2
elif operartion == "*":
    result = num1 * num2
elif operartion == "/":
    result = num1 / num2

print(f"{num1} {operartion} {num2} = {result}")

