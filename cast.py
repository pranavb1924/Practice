#integer
age = 26
#String
name = "Pranav"
#Float
gpa = 4.0
#Boolean
isStudent = True

print("Wecome\n")
print(f"Name: {name}")
print(f"Age: {age}")
print(f"GPA: {gpa}")
print(f"Currently Enrolled: {isStudent}")

print(f"Type of Variable age = {type(name)}")
print(f"Type of Variable age = {type(age)}")
print(f"Type of Variable age = {type(gpa)}")
print(f"Type of Variable age = {type(isStudent)}")

print(f"Casting from Int to Float: Int Value : {age} Float Value : {float(age)}")
print(f"Casting from Float to Int: Float Value : {gpa} Int Value : {int(gpa)}")
print(f"Casting from Int to String and Float to String and Boolean to String:\n Float Value : {gpa} String Value : {str(gpa)}\nInt Value : {age} String Value : {str(age)}\n Boolean Value: {isStudent} String Value: {str(isStudent)}")

