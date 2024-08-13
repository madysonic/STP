### Define Variable Types ###
 
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

# Strings can be declared using double or single quotes
name = "MC" 

print(type(x))
print(type(y))
print(type(z))
print(type(name))

'''
Rules for Variable names

A variable name must start with a letter or the underscore character
A variable name cannot start with a number
A variable name can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )
Variable names are case-sensitive (age, Age and AGE are three different variables)
A variable name cannot be any of the Python keywords.


For multiple words, use either camelCase PascalCase or snake_case

'''

### Assign Multple Variables At Once ###

# x, y, z = "Orange", "Banana", "Cherry"

fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

# Output variables
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)


### Global vs Local Variables ###

# The below will print both Python is fantastic and Python is awesome.
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)


# As the keyword Global has been used, the below will print Python is fantastic outside of the function
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)