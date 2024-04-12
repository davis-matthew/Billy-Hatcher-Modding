from tkinter import * # Using TKinter popups for user input
import os.path as osp
from binascii import hexlify
import struct, json, bpy, bmesh

currentWorld = ""
currentLevel = ""

controls = Tk()

# Adjust size 
controls.geometry("600x200")
  
# Change the label text 
def show():
    currentWorld = worldSelection.get()
    currentLevel = levelSelection.get() 
  
worlds = [
    "[Choose World]"
    "Forest", 
    "Pirate", 
    "Dino", 
    "Blizzard", 
    "Circus", 
    "Sand", 
    "Palace"
]

levels = [
    "[Choose Level]"
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "boss",
    "boss2",
    "all"
]
  
worldSelection = StringVar()
worldSelection.set("[Choose World]")

levelSelection = StringVar()
levelSelection.set("[Choose Level]")
  
worldDropdown = OptionMenu(controls, worldSelection, *worlds)
worldDropdown.pack()
levelDropdown = OptionMenu(controls, levelSelection, *levels) 
levelDropdown.pack()
  
# Create button, it will change label text 
button = Button( controls , text = "click Me" , command = show ).pack() 
  
# Create Label 
label = Label( controls , text = " ") 
label.pack() 
  
# Execute tkinter 
controls.mainloop() 