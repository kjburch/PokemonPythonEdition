import PIL
from Game import tile
import csv
import os

# pixel size of each tile
tileSize = 16
tileGrid = [[]]


# Creates the Tile Objects in a Grid that follows the tileSet
def buildTileGrid():
    global tileGrid
    # Determines the size of the tile grid based on the tileSet image
    im = PIL.Image.open(r"Images/TileSet/tempMap.gif")
    gridWidth = int(im.size[0] / tileSize)
    gridHeight = int(im.size[1] / tileSize)
    im.close()

    # Creates the empty Temp Grid and Tile Grid
    tempGrid = [[]]
    for i in range(gridWidth):
        for j in range(gridHeight):
            tileGrid[i].append([0])
            tempGrid[i].append([])
        if i != gridWidth-1:
            tileGrid.append([])
            tempGrid.append([])

    # adds csv info to the temp Grid so that the tile objects can be properly built
    for filename in os.listdir("Images/TileSet/csv"):
        with open("./Images/TileSet/csv/"+filename, encoding="UTF-8-sig") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            heightCount = 0
            for row in csv_reader:
                widthCount = 0
                for r in row:
                    tempGrid[widthCount][heightCount].append(r)
                    widthCount += 1
                heightCount += 1

    # Convert tempGrid to tiles and tileGrid
    for i in range(gridWidth):
        for j in range(gridHeight):
            tileGrid[i][j] = tile.Tile(tileSetCoordinate=(i, j), surf=tempGrid[i][j][0], walk=tempGrid[i][j][1])


# creates a 2D array of the tiles located as they would be on the map
def buildMapGrid(mapData):
    global tileGrid
    # Determines the size of the Map
    filename = "route1.csv"
    mapGrid = [[]]
    with open("./mapData/csv/"+filename, encoding="UTF-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:
            mapGrid.append([])
            j = 0
            for r in row:
                mapGrid[i].append([])
                point = list(map(int, r.split()))
                mapGrid[i][j] = tileGrid[point[0]-1][point[1]-1]
                j += 1
            i += 1
    mapGrid.pop()
    return mapGrid


# Creates a CSV that represents what Tile in the TileSet each Tile on the map is
# Allows map creator to make a map by picture rather than by CSV
def mapToCSV(mapName):
    tileSet = PIL.Image.open(r"Images/TileSet/tempMap.gif")
    map = PIL.Image.open(r"mapData/"+mapName+".gif")

    with open('mapData/csv/'+mapName+'.csv', 'w', newline='') as csvfile:
        csvWrite = csv.writer(csvfile, delimiter=',')

        for mapY in range(int(map.size[1] / tileSize)):
            row = []
            for mapX in range(int(map.size[0] / tileSize)):
                mapTile = map.crop((mapX * tileSize, mapY * tileSize, (mapX+1) * tileSize, (mapY+1) * tileSize))
                for tileSetY in range(int(tileSet.size[1] / tileSize)):
                    for tileSetX in range(int(tileSet.size[0] / tileSize)):
                        tileSetTile = tileSet.crop((tileSetX * tileSize, tileSetY * tileSize, (tileSetX+1) * tileSize,
                                                    (tileSetY+1) * tileSize))

                        if PIL.ImageChops.difference(tileSetTile.convert('RGB'),
                                                     mapTile.convert('RGB')).getbbox() is None:
                            row.append((tileSetX+1, tileSetY+1))

            csvWrite.writerow(row)


# Creates the .gif image of the current map using the map csv and tileSet grid
def buildMapImage():
    images = []
    mapGrid = buildMapGrid(1)

    # Create Rows of The Image
    for i in range(len(mapGrid)):
        rowImage = []
        for j in range(len(mapGrid[i])):
            rowImage.append(mapGrid[i][j].getImage())

        widths, heights = zip(*(i.size for i in rowImage))
        total_width = sum(widths)
        max_height = max(heights)

        new_im = PIL.Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in rowImage:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        images.append(new_im)

    # Combine Rows into one contiguous map image
    widths, heights = zip(*(i.size for i in images))
    total_width = max(widths)
    max_height = sum(heights)

    new_im = PIL.Image.new('RGB', (total_width, max_height))

    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    new_im.save('mapData/route2.gif')


def checkWalk(currentTile):
    return True


mapToCSV("route2")
