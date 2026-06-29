s ={1, 2, 3, 4}
print(len(s))
s.remove(3)
print(s)
print(s.pop()) #removes an arbitary element and returns it
print(s)
#s.union({9,10})
#print(s)
print(s.union({9,10}))
print(s.intersection({2,1,10}))
s.clear()
print(s)

d={} # empty dictionary
e=set() # empty set
f={1,3,5,3,1}
f.add(7)
print(f) #repeating elements ignored in set

#you cannot have list as an element in set