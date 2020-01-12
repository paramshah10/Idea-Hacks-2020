myText = open("./vision_output.txt", "r")
string1 = myText.read()
myText.close()

string1 = string1.replace(".\n", ". ZZZZ")

string1 = string1.replace("\n", " ")

string1 = string1.replace(". ZZZZ", ".\n")

print(string1)
