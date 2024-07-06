import tkinter as tk
from enum import Enum

VERSION=0.1

# SHOULD MOD PATH BE DOCS/BillyMODS OR something?
# if no path provided, then prompt?
# Or just store within the billy folder and selectively take the files out and replace them?
# How does this work with GCN iso archive nonsense?
# Call C#?


#######################################
# Setup global unchanging frame content
class Screen(Enum):
    NO_BILLY_DIRECTORY = 0
    NO_MOD_LOADED = 1
    MOD_LOADED = 2

FRAME_WIDTH=400
FRAME_HEIGHT=300
frame = tk.Tk()
frame.wm_title(f"Billy Hatcher Mod Loader - v{VERSION}")
frame.geometry(f"{FRAME_WIDTH}x{FRAME_HEIGHT}")

refreshIcon = tk.PhotoImage(file="Tools/refresh.png")
openIcon = tk.PhotoImage(file="Tools/open.png")
disableIcon = tk.PhotoImage(file="Tools/disable.png")
saveIcon = tk.PhotoImage(file="Tools/save.png")

## menu option to set billy path
# menubar = tk.Menu(frame)
# configmenu = tk.Menu(menubar, tearoff=0)
# configmenu.add_command(label='Change Billy Directory', command=frame.quit)
# menubar.add_cascade(label="Config", menu=configmenu)
# frame.config(menu=menubar)

#######################################
# Program state
enabledMod = None
mods = []
currentScreen = Screen.NO_BILLY_DIRECTORY
billyDirectory = None
#######################################
class Mod:
    def __init__(self, directory):
        with open(directory/"modinfo.txt") as file:
            info = file.readlines()
        values = {}

        #Name: Name
        #Author: Author
        #Version: 1.0
        for line in info:
            split = line.split(": ")
            values[split[0].strip()] = split[1].strip()
        self.__init__(values["Name"], values["Author"], values["Version"])

    def __init__(self, name = "Unknown Mod Name", author = "Unknown Author", version = "1.0"):
        self.name = name
        self.author = author
        self.version = version
        self.canvas = None

    def clear(self):
        if self.canvas is not None:
            self.canvas.destroy()

    def draw(self):
        self.clear()

        modCanvas = tk.Canvas(frame, width = FRAME_WIDTH, height = 32, bd = 1, relief = 'solid')
        modCanvas.pack()
        self.canvas = modCanvas

        if self.isEnabled():
            modTitle = tk.Label(frame, text=self.name, font=("Arial",16))
            modCanvas.create_window(10, 16, window=modTitle, anchor='w')

            modAuthor = tk.Label(frame, text=self.author, font=("Arial",12))
            modCanvas.create_window(150, 16, window=modAuthor, anchor='w')

            modVersion = tk.Label(frame, text=self.version, font=("Arial",12))
            modCanvas.create_window(FRAME_WIDTH - 74, 32, window=modVersion, anchor='se')

            disableModButton = tk.Button(frame, text="Disable", image=disableIcon, command=self.disable, width=32, height = 32)
            modCanvas.create_window(FRAME_WIDTH - 64, 0, window=disableModButton, anchor='nw')

            saveModButton = tk.Button(frame, text="Save", image=saveIcon, command=self.save, width=32, height=32)
            modCanvas.create_window(FRAME_WIDTH - 32, 0, window=saveModButton, anchor='nw')
        else:
            loadModButton = tk.Button(frame, text="Open", image=openIcon, command=self.enable, width=32, height=32)
            modCanvas.create_window(0, 0, window=loadModButton, anchor='nw')
            
            modTitle = tk.Label(frame, text=self.name, font=("Arial",16))
            modCanvas.create_window(40, 16, window=modTitle, anchor='w')

            modAuthor = tk.Label(frame, text=self.author, font=("Arial",12))
            modCanvas.create_window(180, 16, window=modAuthor, anchor='w')

            modVersion = tk.Label(frame, text=self.version, font=("Arial",12))
            modCanvas.create_window(FRAME_WIDTH - 10, 32, window=modVersion, anchor='se')

    def enable(self):
        global enabledMod
        global currentScreen
        old = enabledMod
        enabledMod = self
        if old is not None:
            old.disable()
        currentScreen = Screen.MOD_LOADED
        refresh()

    def disable(self):
        global enabledMod
        global currentScreen
        if enabledMod == self:
            enabledMod = None
            currentScreen = Screen.NO_MOD_LOADED
        refresh()

    def isEnabled(self):
        return enabledMod == self
    
    def save(self):
        #TODO: dump the mod in the Billy folder into a mod package folder, overwrite if exists?
        pass

    def saveAs(self):
        #TODO:Open file chooser and pick where it is
        #Popup window to ask Name, Author, Version
        #Create modinfo.txt
        pass

    def __str__(self):
        return f"{self.name} by {self.author} v{self.version}"
    
    def __repr__(self):
        return self.__str__()

def setBillyDirectory():
    global currentScreen
    global billyDirectory
    try:
        billyDirectory = "" #fileChooser.chooseDirectory() # TODO: actually set dir
        currentScreen = Screen.NO_MOD_LOADED
        with open("modloaderconfig.txt") as file:
            file.write(billyDirectory)
    except:
        pass
    refresh()

def refreshModList(): 
    global enabledMod
    global mods
    
    # Deleting every time for 
    # - lexographic ordering
    # - "refresh" looking behavior
    # - in case mod info changed
    mods = []
    enabledMod = None

    loaded = None
    try:
        with open("BillyPC/mods/currentMod.txt") as file:
            loaded = file.read()
    except:
        pass

    # BillyPC/mods/
    try:
        for directory in billyDirectory/mods:
            mods.append(Mod(directory))
            if directory == loaded:
                mods[-1].enable()
    except:
        pass # There is no mods folder... Make one?

def clear():
    for component in frame.winfo_children():
        component.destroy()

def initialize():
    global billyDirectory
    global currentScreen
    try:
        with open("modloaderconfig.txt") as file:
            billyDirectory = file.read()
        currentScreen = Screen.NO_MOD_LOADED
    except:
        pass
    refresh()

def refresh():
    global currentScreen
    clear()

    if currentScreen == Screen.NO_BILLY_DIRECTORY:
        selectDirectoryButton = tk.Button(frame, text="Billy Directory not set. Click to set", command=setBillyDirectory, width=FRAME_WIDTH, height=FRAME_HEIGHT)
        selectDirectoryButton.pack()
        
    else:
        refreshModList()
        if currentScreen == Screen.MOD_LOADED:
            currentModLabel = tk.Label(frame, text="Current Mod:")
            currentModLabel.pack()

            enabledMod.draw()

        availableModCanvas = tk.Canvas(frame, width = FRAME_WIDTH, height = 32)
        availableModCanvas.pack()

        availableModLabel = tk.Label(frame, text="Available Mods:")
        availableModCanvas.create_window(FRAME_WIDTH / 2, 0, window=availableModLabel, anchor='n')
        
        refreshModsButton = tk.Button(frame, text="Refresh", image=refreshIcon, command=refreshModList, width=32, height=32)
        availableModCanvas.create_window(FRAME_WIDTH - 32, 0, window=refreshModsButton, anchor='nw')
        
        for mod in mods:
            if not mod.isEnabled():
                mod.draw()

################################################################################
initialize()
frame.mainloop()