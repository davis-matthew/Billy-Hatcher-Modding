import tkinter as tk

VERSION=0.1

# SHOULD MOD PATH BE DOCS/BillyMODS OR something?
# Or just store within the billy folder and selectively take the files out and replace them?
# How does this work with GCN iso archive nonsense?
# Call C#?


#######################################
# Setup global unchanging frame content

frame = tk.Tk()
frame.wm_title(f"Billy Hatcher Mod Loader - v{VERSION}")
frame.geometry("400x300")

refreshIcon = tk.PhotoImage(file="Tools/refresh.png")
openIcon = tk.PhotoImage(file="Tools/open.png")
saveIcon = tk.PhotoImage(file="Tools/save.png")

enabledMod = None
#######################################

class Mod:
    def __init__(self):
        # TODO: actually read in this data
        self.name = "mod name"
        self.author = "author"
        self.version = "version"
        self.currentlyEnabled = False
        self.canvas = None

    def draw(self):

        #clear out data
        if self.canvas is not None:
            self.canvas.destroy()

        modCanvas = tk.Canvas(frame, width = frame.winfo_width(), height = 32, bd=1,relief='solid')
        modCanvas.pack()
        self.canvas = modCanvas

        if self.currentlyEnabled:
            modTitle = tk.Label(frame, text=self.name, font=("Arial",16))
            modCanvas.create_window(10, 16, window=modTitle, anchor='w')

            modAuthor = tk.Label(frame, text=self.author, font=("Arial",12))
            modCanvas.create_window(150, 16, window=modAuthor, anchor='w')

            modVersion = tk.Label(frame, text=self.version, font=("Arial",12))
            modCanvas.create_window(frame.winfo_width() - 42, 32, window=modVersion, anchor='se')

            saveModButton = tk.Button(frame, text="Save", image=saveIcon, command=self.save, width=32, height=32)
            modCanvas.create_window(frame.winfo_width() - 32, 0, window=saveModButton, anchor='nw')
            
        else:
            loadModButton = tk.Button(frame, text="Open", image=openIcon, command=self.enable, width=32, height=32)
            modCanvas.create_window(0, 0, window=loadModButton, anchor='nw')
                     
            modTitle = tk.Label(frame, text=self.name, font=("Arial",16))
            modCanvas.create_window(40, 16, window=modTitle, anchor='w')

            modAuthor = tk.Label(frame, text=self.author, font=("Arial",12))
            modCanvas.create_window(180, 16, window=modAuthor, anchor='w')

            modVersion = tk.Label(frame, text=self.version, font=("Arial",12))
            modCanvas.create_window(frame.winfo_width() - 10, 32, window=modVersion, anchor='se')

    def toggleEnabled(self):
        if self.currentlyEnabled:
            self.disable()
        else:
            self.enable()

    def enable(self):
        global enabledMod
        enabledMod = self
        self.currentlyEnabled = True
        refreshModList()

    def disable(self):
        global enabledMod
        if enabledMod == self:
            enabledMod = None
        self.currentlyEnabled = False
        refreshModList()

    def save(self):
        #TODO: dump the mod in the Billy folder into a mod package folder, overwrite if exists?
        pass

def refreshModList():
    # TODO: parse out mod folders and add to mods list

    for mod in mods:
        mod.draw()

def clear():
    for component in frame.children:
        component.destroy()

def draw():

    refreshModList()





# if no path provided, then prompt?

# option to set billy path
menubar = tk.Menu(frame)
configmenu = tk.Menu(menubar, tearoff=0)
configmenu.add_command(label='Change Billy Directory', command=frame.quit)
menubar.add_cascade(label="Config", menu=configmenu)
frame.config(menu=menubar)

label = tk.Label(frame, text="Current Mod:")
label.pack()


refreshModsButton = tk.Button(frame, text="Refresh", image=refreshIcon, command=refreshModList, width=32, height=32)
refreshModsButton.pack()

mods = []
mods.append(Mod())



frame.mainloop()