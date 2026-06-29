# about string slicing
name="Percy"
nameslice= name[0:3] # or name[:3] 
print(nameslice)
# name[0:] assumes length of string as second argument i.e. 5 here

#negative slicing: change to corresponding positive counter parts
nslice = name[-5:-2]  # same as name[0:3]
print(nslice)

name_ = "annabeth chase"
n= name_[0:9:3] # slicing with skip value
print(n)

#extra funcns
char= name[1]
print(char)

print(name.endswith("cy"))
print(name_.startswith("anna"))
print(name_.capitalize())

#if you wish to print " then 
print("\"hello\" ") #similarly for single quote
#similarly use \n for ending and moving to next line
#these are called as escape sequence characters

#f strings
print(f"Hello! I like \"{name}\" and \"{name_.capitalize()}\"")

#find func: it returns -1 if string not found, else it returns the starting place of character
text = "Python is awesome"
print(text.find("is"))

#in funcn 
print('the' in 'feed the dog and the cat')

# replace func
name_2 = name_.replace("annabeth", "magnus")
print(name_2)

#count, index  
string = 'feed the dog and the cat'
print(string.count('the'))
print(string.index('the'))