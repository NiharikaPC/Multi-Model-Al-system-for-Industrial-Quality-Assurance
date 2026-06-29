marks = {
    "percy" : 10,
    "annabeth" : 100,
    10 : "grover"
}
d={} # empty dictionary

print(marks.items())
print(marks.keys())
print(marks.values())

print(marks["percy"]) # generates error if key not present
print(marks.get("annabeth")) # returns none if key not present