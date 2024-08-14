# List items are ordered, changeable, and allow duplicate values.
# List items are indexed, the first item has index [0], the second item has index [1] etc.
# Tupless are similar to lists. These are defined with single brackets (). Tuples are ordered and unchangeable.

### Create lists ###

# Create list using [] or using the list(()) constructor with double brackets.
thislist = ["apple", "banana", "cherry"]
print(len(thislist))
print(type(thislist))

thislist = list(("apple", "banana", "cherry",  "kiwi", "melon", "mango")) 
print(type(thislist))

# Lists can be any data type.
list1 = ["abc", 34, True, 40, "male"]

### Indexing ###

print(thislist[1]) # second item as indexing starts at 0
print(thislist[-1]) # last item
print(thislist[2:5]) # items 3,4 and 5.
print(thislist[:4]) # items from the begining up to but not including the 5th item (indexing starts at 0)

# Check if item exists
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")

### Modify lists ###

thislist[1] = "blackcurrant"
print(thislist)

# Modify a range
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)

# Insert as third item
thislist.insert(2, "watermelon")
print(thislist)

# Insert items at the end using append
thislist.append("orange")

# Extend a list
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)

# Remove specific item ( this will remove the first occurence only)
thislist.remove("banana")
print(thislist)

#Remove via index using pop (if index not specified, last item in list is removed)
thislist.pop(1)
print(thislist)

# Remove using del
del thislist[0]
print(thislist)


### Loop through lists ### 

# Several methods - note indentation
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)
# OR
[print(x) for x in thislist]


for i in range(len(thislist)):
  print(thislist[i])

i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1

#This will print apple, banana and mango as they contain the letter a
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []

for x in fruits:
  if "a" in x:
    newlist.append(x)

print(newlist)

# Short hand version
newlist = [x for x in fruits if "a" in x]


### Wrangle lists ###

# Sort alphabetically or numerically
thislist.sort()
print(thislist)
thislist.sort(key = str.lower) # ignore case

# sort descending
thislist.sort(reverse = True)

# Custom function sorts list based on closeness to 50
def myfunc(n):
  return abs(n - 50)

thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)


