a=(1) #not a tuple, considered as int
print(type(a))

b=(1, ) # way to create single element tuple
c=() # empty tuple
d=(1, 2, 5, 6)
print(type(c))
print(d.count(6))
print(d.index(6))