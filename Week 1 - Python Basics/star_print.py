'''
for n=3
  *
 ***
*****
'''
n= int(input("Enter number : "))
for i in range(1, n+1):
    print(" "*(n-i), end="") #to not generate a new line and to print a thing multiple times
    print("*"*(2*i-1), end="")
    print("")
