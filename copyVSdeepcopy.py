import copy

# Reference to the same object, not a new one
x = [1, 2, 3, 4]

y = x
y.append(5)
print(x)
print(y)
# Result x = y = [1, 2, 3, 4, 5]
del x, y


# Shallow Copy without reference type inside

x = [1, 2, 3, 4]
y = copy.copy(x)  # another way to create shallow copy is y = list(x) or y = x[:]
y.append(7)
x[0] = 0
y[0] = 50
print(x)
print(y)
del x, y

# Result x = [0, 2, 3, 4], y = [50, 2, 3, 4, 7]


# Shallow copy with reference type inside [9]

x = [1, 2, 3, [9]]

y = x[:]

x[0] = 0
y[0] = 50
print(x)
print(y)
# Result x = [0, 2, 3, 4], y = [50, 2, 3, 4, 7]

# But
y[3].append(999)
print("BUT:")
print(x)
print(y)
# Result x = [0, 2, 3, [9, 999]]], y = [50, 2, 3, [9, 999]]
del x, y


# DEEPCOPY

x = [1, 2, 3, [9]]
y = copy.deepcopy(x)

y[3].append(99999)
x[3].append(33333)

print(x)
print(y)
# Result x = [1, 2, 3, [9, 33333]], y = [1, 2, 3, [9, 99999]]
