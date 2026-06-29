#reading a file
f = open("file.txt") #open("file.txt", "r") by default
data=f.read()
print(data)
f.close()
#alternate way in which you do not need to mention separately to close file
with open("file.txt", "r") as f: #if just written open("file.txt") then also it works because by default it is read
    print(f.read())

# writing in file
str= "Thank You"
f1 =open("myfile.txt", "w")
f1.write(str)
f1.close
#write function does not append, hence if a file of that name already existed it will erase the previous content and write new
#for append we use "a" and append instead of "w" and write 