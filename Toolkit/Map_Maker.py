from tkinter import *
from tkinter.ttk import Frame, Button, Label, Style
from PIL import ImageTk, Image, ImageDraw

tileSetImage = Image.open("tilesets/tempMap.gif")
tileSize = 16
tileSetX = 0
tileSetY = 0


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # App Window
        self.master.title("Map Maker")
        self.pack(fill=BOTH, expand=True)

        # Current Map Label
        tileLabel = Label(self, text="Map")
        tileLabel.grid(row=1, column=3)

        # Current Map
        levelMap = Label(self, borderwidth=10, relief="ridge")
        levelMap.grid(row=2, column=1, columnspan=7)
        img = Image.new('RGB', (400, 400), (255, 255, 255))
        img = img.resize((400, 400))

        draw = ImageDraw.Draw(img)
        for i in range(0, img.size[0], tileSize):
            draw.line(((i, 0), (i, img.size[1])), fill=128)
            draw.line(((0, i), (img.size[0], i)), fill=128)

        img = ImageTk.PhotoImage(img)
        levelMap.img = img  # keep a reference so it's not garbage collected
        levelMap['image'] = img

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
            x, y = event.x, event.y
            print("Location Clicked:",'{}, {}'.format(x, y))

            tileX = 0
            tileY = 0

            tempImage = tileSetImage.copy()
            tempDraw = ImageDraw.Draw(tempImage)

            for i in range(0, tempImage.size[0]+tileSize, tileSize):
                for j in range(0, tempImage.size[1]+tileSize, tileSize):
                    if i < x / 400 * tempImage.size[0] < i+tileSize and j < y / 400 * tempImage.size[1] < j+tileSize:
                        tempDraw.rectangle(((i-1, j-1), (i+tileSize, j+tileSize)), width=1, outline=10)
                        tileX = int(i/tileSize+1)
                        tileY = int(j/tileSize+1)
                        i = tempImage.size[0]+tileSize
                        j = tempImage.size[1]+tileSize

            tempImage = tempImage.resize((400, 400))
            tempImage = ImageTk.PhotoImage(tempImage)
            tileset.img = tempImage  # keep a reference so it's not garbage collected
            tileset['image'] = tempImage

            print("Chosen Tile:",(tileX, tileY))

        tileset.bind('<Button-1>', chooseActiveTile)

        # ----------------------------------------------------------------------------------------------------------

        # Tile Size Label
        sizeLabel = Label(self, text="Tile Size: ")
        sizeLabel.grid(row=3, column=1)
        # Tile Size textbox
        size = Text(self, height=1, width=7)
        size.grid(row=3, column=2)

        # Level Name
        nameLabel = Label(self, text="Level name: ")
        nameLabel.grid(row=3, column=3)
        # Level Name Textbox
        name = Text(self, height=1, width=7)
        name.grid(row=3, column=4)


def main():
    root = Tk()
    root.geometry("900x600+200+200")
    app = Example()

    root.mainloop()


if __name__ == '__main__':
    main()
