number = int(input("Enter a number: "))
fibonacci = [0, 1]
for i in range(2, number):
    fibonacci.append(fibonacci[i - 1] + fibonacci[i - 2])
print(fibonacci)
