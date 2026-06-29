def rem(l, word):
    n =[]
    for item in l:
        if not(item==word):
            n.append(item.strip(word)) #strip removes that segment from words starting and end if it exists
    return n

l = ["percy", "grover", "annabeth", "lucy", "cylecy"]
print(rem(l, "cy"))

#range functions
print(list(range(4)))
print(list(range(0,20,5))) #just like string slicing

#round function
#round(the input to be rounded, number to how many digit round after decimal)
print(round(12.567788, 1))

#lambda functions
#lambda arguments: expression