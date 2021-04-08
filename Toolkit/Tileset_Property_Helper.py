from tkinter import *
from tkinter.ttk import Frame, Button, Label, Style
from PIL import ImageTk, Image

tileSet = Image.open("tilesets/tempMap.gif")
tileSize = 16
tileSetX = 0
tileSetY = 0


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # List of preexisting templates
        existingTemplates = ["Default", "Grass", "Sand", "Water", "Sign"]
        variable = StringVar(self)
        variable.set(existingTemplates[0])  # default value

        # Variables tracked
        walkable = IntVar()
        surfable = IntVar()
        slippery = IntVar()
        footprints = IntVar()
        interactable = IntVar()

        # Applies the chosen template to the current tile
        def applyTemplate():
            print("Template is: "+variable.get())

        # App Window Title
        self.master.title("Tileset Property Helper")
        self.pack(fill=BOTH, expand=True)

        # Tile Label
        tileLabel = Label(self, text="Current Tile")
        tileLabel.grid(column=1, pady=10)

        # Current Tile Image
        area = Label(self)
        area.grid(row=1, column=0, columnspan=2, rowspan=14, padx=5, sticky=E+W+S+N)
        img = tileSet.crop((0 * tileSize, 0 * tileSize, (0+1) * tileSize, (0+1) * tileSize))
        img = ImageTk.PhotoImage(img.resize((400, 400)))
        area.img = img  # keep a reference so it's not garbage collected
        area['image'] = img

        # Find the next Tile
        def nextTile():
            global tileSetX, tileSetY

            # Iterate to the next tile in the Tile Set
            if tileSetX >= int(tileSet.size[0] / tileSize)-1:
                tileSetX = 0
                tileSetY = tileSetY+1
            else:
                tileSetX += 1

            if tileSetY >= int(tileSet.size[1] / tileSize):
                tileSetY = 0
                tileSetX = 0

            # load the image and display it
            tile = tileSet.crop(
                (tileSetX * tileSize, tileSetY * tileSize, (tileSetX+1) * tileSize, (tileSetY+1) * tileSize))
            tile = ImageTk.PhotoImage(tile.resize((400, 400)))
            area.tile = tile  # keep a reference so it's not garbage collected
            area['image'] = tile

        # Template Label
        templateLabel = Label(self, text="Existing Templates:")
        templateLabel.grid(row=1, column=3)
        # Lists Available Templates
        templateList = OptionMenu(self, variable, *existingTemplates)
        templateList.grid(row=1, column=4)
        # Applies the chosen Template
        applyTemplateButton = Button(self, text="Apply Chosen Template", command=applyTemplate)
        applyTemplateButton.grid(row=2, column=3, columnspan=2)

        # Walk Speed Label
        templateLabel = Label(self, text="Walk Speed: ")
        templateLabel.grid(row=3, column=3, padx=0)
        # Sets walk speed
        walkSpeed = Text(self, height=1, width=7)
        walkSpeed.grid(row=3, column=4, padx=0)

        # Walkable Label
        walkableLabel = Label(self, text="Walkable: ")
        walkableLabel.grid(row=4, column=3, padx=0)
        # Check Walkable
        walkableCheckbox = Checkbutton(self, variable=walkable, onvalue=1, offvalue=0)
        walkableCheckbox.grid(row=4, column=4, padx=0)

        # Surfable Label
        surfableLabel = Label(self, text="Surfable: ")
        surfableLabel.grid(row=5, column=3, padx=0)
        # Check Surfable
        surfableCheckbox = Checkbutton(self, variable=surfable, onvalue=1, offvalue=0)
        surfableCheckbox.grid(row=5, column=4, padx=0)

        # Slippery Label
        slipperyLabel = Label(self, text="Slippery: ")
        slipperyLabel.grid(row=6, column=3, padx=0)
        # Check Slippery
        slipperyCheckbox = Checkbutton(self, variable=slippery, onvalue=1, offvalue=0)
        slipperyCheckbox.grid(row=6, column=4, padx=0)

        # Footprints Label
        footprintsLabel = Label(self, text="Footprints: ")
        footprintsLabel.grid(row=7, column=3, padx=0)
        # Footprints Slippery
        footprintsCheckbox = Checkbutton(self, variable=footprints, onvalue=1, offvalue=0)
        footprintsCheckbox.grid(row=7, column=4, padx=0)

        # Footprints Label
        interactableLabel = Label(self, text="Interactable: ")
        interactableLabel.grid(row=8, column=3, padx=0)
        # Footprints Slippery
        interactableCheckbox = Checkbutton(self, variable=interactable, onvalue=1, offvalue=0)
        interactableCheckbox.grid(row=8, column=4, padx=0)

        # Interaction Label
        interactionTextLabel = Label(self, text="Interaction Text")
        interactionTextLabel.grid(row=9, column=3, padx=0)
        # Interaction Text
        interactionText = Text(self, height=5, width=20)
        interactionText.grid(row=10, column=3, padx=0, columnspan=2)

        # Goes to the next tile
        nextTileButton = Button(self, text="Next Tile", command=nextTile)
        nextTileButton.grid(row=15, column=1, padx=0)


def main():
    root = Tk()
    root.geometry("600x600+200+200")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()
