# importing the pyttsx library 
import pyttsx3 

# initialisation 
engine = pyttsx3.init() 

myText = open("./vision_output.txt", "r")
string1 = myText.read()
myText.close()

# testing 
engine.say("My first code on text-to-speech") 
engine.say("Thank you, Geeksforgeeks")
engine.say(string1)
engine.runAndWait() 
