# Booleans are True and False

print(10 > 9) # will return True
print(10 == 9) # will return False
print(10 < 9) # will return False

# The below will print the second statment
a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

# Bool can be used to evaluate a variable
# Almost any value is evaluated to True if it has some sort of content, except empty strings/lists/dictionarys or the number 0.

# True
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

# False
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

# Use isinstance to confirm data type
x = 200
print(isinstance(x, int))