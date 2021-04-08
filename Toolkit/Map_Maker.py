from math import floor
from operator import itemgetter
from tkinter import *
from tkinter.ttk import Frame, Button, Label
from tkinter.filedialog import askopenfilename, asksaveasfile
from PIL import ImageTk, Image, ImageDraw

tileSize = 16
brushSize = 1
tileSetImage = Image.new('RGB', (400, 400), (255, 255, 255))
currentTileCord = []
currentTileImg = []
mapImageBase = Image.new('RGB', (400, 400), (255, 255, 255))
draw = ImageDraw.Draw(mapImageBase)
for i in range(0, mapImageBase.size[0], tileSize):
    draw.line(((i, 0), (i, mapImageBase.size[1])), fill=128, width=1)
    draw.line(((0, i), (mapImageBase.size[0], i)), fill=128, width=1)
mapImage = mapImageBase.copy()
previousMaps = []
nextMaps = []
fileName = None


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        global mapImage, mapImageBase, tileSize, currentTileCord, currentTileImg, tileSetImage
        tileSizeText = IntVar()

        # App Window
        self.master.title("Map Maker")
        self.pack(fill=BOTH, expand=True)

        # Current Map Label
        tileLabel = Label(self, text="Map")
        tileLabel.grid(row=1, column=3)

        # Current Map
        levelMap = Label(self, borderwidth=10, relief="ridge")
        levelMap.grid(row=2, column=1, columnspan=7)

        img = ImageTk.PhotoImage(mapImage)
        levelMap.img = img  # keep a reference so it's not garbage collected
        levelMap['image'] = img

        def paintMap(event):
            global currentTileImg, nextMaps
            if len(currentTileImg) > 0:

                x, y = event.x, event.y
                print("Location Clicked:", '{}, {}'.format(x, y))

                tempImage = mapImage
                previousMaps.append(tempImage.copy())
                nextMaps = []

                if len(previousMaps) > 25:
                    previousMaps.pop(0)
                if len(nextMaps) > 25:
                    nextMaps.pop(0)

                tileX = floor(x / tileSize)
                tileY = floor(y / tileSize)

                print("Chosen Tile:", (tileX, tileY))

                minX = min(currentTileCord, key=itemgetter(0))[0]
                minY = min(currentTileCord, key=itemgetter(1))[1]
                maxX = max(currentTileCord, key=itemgetter(0))[0]
                maxY = max(currentTileCord, key=itemgetter(1))[1]

                for i in range(brushSize):
                    for j in range(brushSize):
                        for k in range(len(currentTileImg)):
                            tempImage.paste(currentTileImg[k],
                                            (((currentTileCord[k][0]-minX)+tileX+i * (maxX-minX+1)) * tileSize,
                                             ((currentTileCord[k][1]-minY)+tileY+j * (maxY-minY+1)) * tileSize))

                tempImage = ImageTk.PhotoImage(tempImage)
                levelMap.img = tempImage  # keep a reference so it's not garbage collected
                levelMap['image'] = tempImage
            else:
                print("No tile currently selected")

        levelMap.bind('<Button-1>', paintMap)

        # ----------------------------------------------------------------------------------------------------------

        # Current Tileset Label
        tileLabel = Label(self, text="Tileset")
        tileLabel.grid(row=1, column=11)

        # Current Tileset
        tileset = Label(self, borderwidth=10, relief="ridge")
        tileset.grid(row=2, column=8, columnspan=7)
        img = tileSetImage
        img = ImageTk.PhotoImage(img.resize((400, 400)))
        tileset.img = img  # keep a reference so it's not garbage collected
        tileset['image'] = img

        def chooseActiveTile(event):
            global currentTileCord, currentTileImg
            x, y = event.x, event.y
            print("Location Clicked:", '{}, {}'.format(x, y))

            tempImage = tileSetImage.copy()
            tempDraw = ImageDraw.Draw(tempImage)

            tileX = floor(x / 400 * tempImage.size[0] / tileSize)
            tileY = floor(y / 400 * tempImage.size[1] / tileSize)

            if (tileX, tileY) not in currentTileCord:
                currentTileCord.append((tileX, tileY))

                for tile in currentTileCord:
                    tempDraw.rectangle(
                        (
                            (tile[0] * tileSize-1, tile[1] * tileSize-1),
                            ((tile[0]+1) * tileSize, (tile[1]+1) * tileSize)),
                        width=1, outline=0)

                tempImage = tempImage.resize((400, 400))
                tempImage = ImageTk.PhotoImage(tempImage)

                tileset.img = tempImage  # keep a reference so it's not garbage collected
                tileset['image'] = tempImage

                currentTileImg.append(tileSetImage.crop((tileX * tileSize, tileY * tileSize,
                                                         (tileX+1) * tileSize,
                                                         (tileY+1) * tileSize)))
                print("Chosen Tile:", (tileX, tileY))
            else:
                print("Tile already selected")

        tileset.bind('<Button-1>', chooseActiveTile)

        # ----------------------------------------------------------------------------------------------------------
        # Tile Size Label
        sizeLabel = Label(self, text="Tile Size: ")
        sizeLabel.grid(row=3, column=1)
        # Tile Size textbox
        tileSizeText = Text(self, height=1, width=7)
        tileSizeText.grid(row=3, column=2)

        # Tile Size Setter
        def setTileSize():
            global tileSize
            try:
                temp = int(tileSizeText.get("1.0", END))
                if temp < 1:
                    raise ValueError
                print("Tile Size set to:", temp)
                tileSize = temp
            except ValueError:
                print("Not a valid tile size")

        # Sets the tile size
        sizeButton = Button(self, text="Set Tile Size", command=setTileSize)
        sizeButton.grid(row=3, column=3)

        # -------------------------------------------------------------------------------------------------------------
        # Brush Size Size Label
        brushLabel = Label(self, text="Brush Size: ")
        brushLabel.grid(row=4, column=1)
        # Brush Size textbox
        brushSizeText = Text(self, height=1, width=7)
        brushSizeText.grid(row=4, column=2)

        # Tile Size Setter
        def setBrushSize():
            global brushSize
            try:
                temp = int(brushSizeText.get("1.0", END))
                if temp < 1:
                    raise ValueError
                print("Tile Size set to:", temp)
                brushSize = temp
            except ValueError:
                print("Not a valid brush size")

        # Sets the tile siw
        brushButton = Button(self, text="Set Brush Size", command=setBrushSize)
        brushButton.grid(row=4, column=3)

        # ------------------------------------------------------------------------------------------------------------
        # Tile Size Setter
        def emptyBrush():
            global currentTileCord, currentTileImg
            currentTileImg = []
            currentTileCord = []
            tempImage = tileSetImage.copy()
            tempImage = tempImage.resize((400, 400))
            tempImage = ImageTk.PhotoImage(tempImage)

            tileset.img = tempImage  # keep a reference so it's not garbage collected
            tileset['image'] = tempImage
            print("Emptied Brush")

        # Sets the tile siw
        brushButton = Button(self, text="Empty Brush", command=emptyBrush)
        brushButton.grid(row=5, column=3)

        # --------------------------------------------------------------------------------------------------------------
        # Saves the Map
        def saveMap():
            global fileName
            if fileName is None:
                files = [('GIF Files', '*GIF')]
                fileName = asksaveasfile(filetypes=files, defaultextension=files).name
                mapImage.save(fileName)
            else:
                print("Saving to", fileName)
                mapImage.save(fileName)

        # Saves the Map
        saveButton = Button(self, text="Save Map", command=saveMap)
        saveButton.grid(row=4, column=7)

        # --------------------------------------------------------------------------------------------------------------
        # Saves the Map As a Certain Name
        def saveMapAs():
            global fileName
            files = [('GIF Files', '*GIF')]
            fileName = asksaveasfile(filetypes=files, defaultextension=files).name
            mapImage.save(fileName)

        # Saves the Map
        saveAsButton = Button(self, text="Save Map As", command=saveMapAs)
        saveAsButton.grid(row=3, column=7)

        # ---------------------------------------------------------------------------------------------------------------
        # Resets the Map
        def resetMap():
            global mapImage, mapImageBase
            print("Reset")
            mapImage = mapImageBase.copy()
            tempImage = ImageTk.PhotoImage(mapImageBase)
            levelMap.img = tempImage  # keep a reference so it's not garbage collected
            levelMap['image'] = tempImage

        # Rest map to blank
        resetButton = Button(self, text="Reset Map", command=resetMap)
        resetButton.grid(row=4, column=8)

        # --------------------------------------------------------------------------------------------------------------
        # Choose the Tileset File
        def chooseTileset():
            global tileSetImage
            tileSetFilename = askopenfilename()
            tileSetImage = Image.open(tileSetFilename)
            tileTempImage = ImageTk.PhotoImage(tileSetImage.resize((400, 400)))
            tileset.img = tileTempImage  # keep a reference so it's not garbage collected
            tileset['image'] = tileTempImage

        # Rest map to blank
        chooseTileSetButton = Button(self, text="Choose TileSet", command=chooseTileset)
        chooseTileSetButton.grid(row=3, column=11)

        # --------------------------------------------------------------------------------------------------------------
        # Choose a preexisting Map
        def chooseMap():
            global previousMaps, fileName, mapImageBase, mapImage
            fileName = askopenfilename()
            mapImage = Image.open(fileName).resize((400, 400))
            mapTempImage = ImageTk.PhotoImage(mapImage)
            levelMap.img = mapTempImage
            levelMap['image'] = mapTempImage
            previousMaps = [levelMap]

        # Rest map to blank
        chooseTileSetButton = Button(self, text="Choose Map", command=chooseMap)
        chooseTileSetButton.grid(row=4, column=11)

        # --------------------------------------------------------------------------------------------------------------
        # Undo's a change
        def undo():
            global mapImage
            if len(previousMaps) > 0:
                print("Undoing Action")
                nextMaps.append(mapImage)
                mapImage = previousMaps.pop()
                mapTempImage = ImageTk.PhotoImage(mapImage)
                levelMap.img = mapTempImage
                levelMap['image'] = mapTempImage
            else:
                print("Cannot Undo")

        # Saves the Map
        undoButton = Button(self, text="Undo", command=undo)
        undoButton.grid(row=5, column=7)

        # --------------------------------------------------------------------------------------------------------------
        # Redo  a change
        def redo():
            global mapImage
            if len(nextMaps) > 0:
                print("Redoing Action")
                previousMaps.append(mapImage)
                mapImage = nextMaps.pop()
                mapTempImage = ImageTk.PhotoImage(mapImage)
                levelMap.img = mapTempImage
                levelMap['image'] = mapTempImage
            else:
                print("Cannot Redo")

        # Saves the Map
        redoButton = Button(self, text="Redo", command=redo)
        redoButton.grid(row=5, column=8)


def main():
    root = Tk()
    root.geometry("900x600+200+200")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()
