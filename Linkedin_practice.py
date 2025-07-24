print("Hello", "Karl", "Ade", sep="-")
print("World")

name = input("Enter Your Name:")
print("Hello", name)

# Chapter 2 - Control Flow: Conditional blocks and Loops


price = input("What is the price?: $")
price = float(price)
if price > 0:
    print("The price is", "$ ", price)
    total_price = price + 100
    print("Price after tax:", total_price)
else:
    if price < 0:
        print("Invalid Price")
    if price == 0:
        print("You did not enter a price")

count = 0
while count < 20:
    print(count)
    count += 1

print("Loop end"
      "")

word = "banana"
for character in word:
    if character != "a":
        print(character, end="")
    print(".")

total_price = 0
for number in range(1, 6):
    price = input("Type the price" + " " + str(number) + ": $")
    # print(price)
    total_price += float(price)

print("Total price is: $", total_price)

total = 0
while input("Continue? (Y/N) ") == "Y":
    qty = float(input("Enter the quantity: "))
    if qty < 0:
        break
    total += qty
print("Total quantity", total)

endOfProgram = False
while not endOfProgram:
    name = input("Please enter your name: ")
    if len(name) < 2:
        endOfProgram = True
        continue
    else:
        age = int(input("Age: "))
        if age > 15:
            children = int(input("How many children: "))
            if (children > 0):
                for c in range(children):
                    child_name = input("Child name: ")
        else:
            mother_name = input("Mother's name: ")

print("End.")

# Chapter 3 - Data Collections: Lists, Tuples, Dictionaries

countries = [
    "USA",
    "Philippines",
    "Denmark"
]
countries.append("Canada")
countries.insert(1, "Spain")
Denmark = countries.pop(3)

countries.sort(reverse=False)
print(countries)


list = [1, 2, 3, 4, 5]
print(list[:4])


# Chapter 4 - Functions adn Exceptions

def my_function():
    print("I am a function")
    print("I am still a function")
    return "I am done"


message = my_function()
print("The output of the function is:", message)


def area_of_rectangle():
    rect_length = 10
    rect_width = 5

    rect_area = rect_length * rect_width
    print("Area of the rectangle is: ", rect_area)


area_of_rectangle()


def area_of_circle():
    circle_radius = 12
    pi = 3.14159

    circle_area = pi * (circle_radius**2)
    print("Area of the circle is: ", circle_area)


area_of_circle()

# (item_name, price_per_item, quantity)
items = [
    ("apple", 0.5, 20),
    ("banana", 0.25, 2),
    ("grape", 0, 75, 3)
]

total = 0
for item in items:
    total += item[1] * item[2]

if total > 10:
    discount = 0.1
    total_with_discount = total * (1-discount)
else:
    total_with_discount = total

print("Total: $", total)
print("Total after possible discount: $", total_with_discount)


def printName():
    global name
    name = name + "!"
    print(name)


name = input("input your name here: ")
printName()
