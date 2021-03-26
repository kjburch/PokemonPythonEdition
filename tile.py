from PIL import Image


class Tile:
    def __init__(self, tileSetCoordinate=(0, 0), animation=[], walk=True, surf=False, slide=False, walkSpeed=1.0,
                 footprint=False, interactable=False, encounter=False, route=False):
        self.tileSetCoordinate = tileSetCoordinate
        self.animation = animation
        self.walk = walk
        self.surf = surf
        self.slide = slide
        self.walkSpeed = walkSpeed
        self.footprint = footprint
        self.interactable = interactable
        self.encounter = encounter
        self.route = route

    # Returns the appropriate image for the requested tile
    def getImage(self):
        tileMap = Image.open(r"Images/TileSet/tempMap.gif")
        tileImage = tileMap.crop(
            (self.tileSetCoordinate[0] * 16, self.tileSetCoordinate[1] * 16, self.tileSetCoordinate[0] * 16+16,
             self.tileSetCoordinate[1] * 16+16))
        tileMap.close()
        return tileImage
