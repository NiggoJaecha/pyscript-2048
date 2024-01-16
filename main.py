from pyweb import pydom
from js import document
from pyscript import window
import random

LEFT=37
RIGHT=39
UP=38
DOWN=40

DID_MOVE = False
SCORE = 0

Colors = {
    2: "eee4da",
    4: "eee1c9",
    8: "f3b27a",
    16: "f69664",
    32: "f77c5f",
    64: "f75f3b",
    128: "edd073",
    256: "edcc62",
    512: "90ee90",
    1024: "008000",
    2048: "ffc0cb"
}

FontSize = {
    2: 80,
    4: 75,
    8: 70,
    16: 65,
    32: 60,
    64: 55,
    128: 50,
    256: 40,
    512: 40,
    1024: 30,
    2048: 30
}

Tiles = {
    0:{0:None,1:None,2:None,3:None},
    1:{0:None,1:None,2:None,3:None},
    2:{0:None,1:None,2:None,3:None},
    3:{0:None,1:None,2:None,3:None}
    }

def getTranform(x, y):
    return f"translate({x}00%,{y}00%)"

def moveTileTo(fromX, fromY, toX, toY):
    global DID_MOVE
    #window.console.log(f"Move ({fromX}|{fromY}) to ({toX}|{toY})")
    Tile = Tiles[fromX][fromY]
    Tile[0].style["transform"] = getTranform(toX,toY)
    Tiles[toX][toY] = Tile
    Tiles[fromX][fromY] = None
    DID_MOVE = True


container = pydom['#game'][0]
container.html = ""

def spawnTile():
    freePos = []
    for x in range(4):
        for y in range(4):
            if Tiles[x][y] is None:
                freePos.append((x,y))
    rnd = random.randrange(-1, len(freePos)-1)
    newX = freePos[rnd][0]
    newY = freePos[rnd][1]

    newTile = None
    newTile = container.create("div", classes=["tile-container"])
    label = newTile.create("div", classes=["tile-label", "spawn-animation"], html="2")
    label.style["background-color"] = f"#{Colors[2]}"
    label.style["font-size"] = f"{FontSize[2]}px"
    label.style["color"] = "#776e65"
    newTile.style["transform"] = getTranform(newX, newY)
    Tiles[newX][newY] = [newTile, 2, False]

def deleteTile(x,y):
    Tile = Tiles[x][y]
    Tile[0].id = "remove"
    document.getElementById("remove").classList.add("to-delete")
    Tile[0].id = ""
    Tiles[x][y] = None

def doubleTile(x,y):
    global SCORE
    Tile = Tiles[x][y]
    Tile[2] = True
    Tile[1] = Tile[1] * 2
    Label = Tile[0].children[0]
    if Tile[1] <= 2048:
        Label.style["background-color"] = f"#{Colors[Tile[1]]}"
        Label.style["font-size"] = f"{FontSize[Tile[1]]}px"
    else:
        Label.style["background-color"] = "#776e65"
        Label.style["font-size"] = "30px"
    if Tile[1] == 8:
        Label.style["color"] = "#f9f6f2"
    Label.html = Tile[1]
    SCORE += Tile[1]
    pydom["#score"][0].html = f"Score: {SCORE}"

def moveUp():
    for x in range(4):
        for row in range(4):
            y = row # form top to bottom
            tileMoveUp(x,y)

def tileMoveUp(x,y):
    Tile = Tiles[x][y]
    if Tile is None: # empty Tile
        return
    if y == 0: # upper most tile can't go up
        return
    LookAtTile = Tiles[x][y-1]
    if (LookAtTile is None): # LookAtTile empty, move there
        moveTileTo(x,y,x,y-1)
    # if LookAtTile has same value and has not merged this round
    elif (LookAtTile[1] == Tile[1] and not (LookAtTile[2] or Tile[2])):
        deleteTile(x, y-1)
        doubleTile(x,y) # double self
        moveTileTo(x,y,x,y-1) # move self
    tileMoveUp(x, y-1) # keep on movin'

def moveDown():
    for x in range(4):
        for row in range(4):
            y = 3-row # form bottom to top
            tileMoveDown(x,y)

def tileMoveDown(x,y):
    Tile = Tiles[x][y]
    if Tile is None: # empty Tile
        return
    if y == 3: # lower most tile can't go dwon
        return
    LookAtTile = Tiles[x][y+1]
    if (LookAtTile is None): # LookAtTile empty, move there
        moveTileTo(x,y,x,y+1)
    # if LookAtTile has same value and has not merged this round
    elif (LookAtTile[1] == Tile[1] and not (LookAtTile[2] or Tile[2])):
        deleteTile(x,y+1)
        doubleTile(x,y) # double self
        moveTileTo(x,y,x,y+1) # move self
    tileMoveDown(x, y+1) # keep on movin'

def moveLeft():
    for y in range(4):
        for column in range(4):
            x = column # from left to right
            tileMoveLeft(x,y)

def tileMoveLeft(x,y):
    Tile = Tiles[x][y]
    if Tile is None: # empty Tile
        return
    if x == 0: # left most tile can't go left
        return
    LookAtTile = Tiles[x-1][y]
    if (LookAtTile is None): # LookAtTile empty, move there
        moveTileTo(x,y,x-1,y)
    # if LookAtTile has same value and has not merged this round
    elif (LookAtTile[1] == Tile[1] and not (LookAtTile[2] or Tile[2])):
        deleteTile(x-1,y)
        doubleTile(x,y) # double self
        moveTileTo(x,y,x-1,y) # move self
    tileMoveLeft(x-1, y) # keep on movin'

def moveRight():
    for y in range(4):
        for column in range(4):
            x = 3-column # from right to left
            tileMoveRight(x,y)

def tileMoveRight(x,y):
    Tile = Tiles[x][y]
    if Tile is None: # empty Tile
        return
    if x == 3: # right most tile can't go right
        return
    LookAtTile = Tiles[x+1][y]
    if (LookAtTile is None): # LookAtTile empty, move there
        moveTileTo(x,y,x+1,y)
    # if LookAtTile has same value and has not merged this round
    elif (LookAtTile[1] == Tile[1] and not (LookAtTile[2] or Tile[2])):
        deleteTile(x+1,y)
        doubleTile(x,y) # double self
        moveTileTo(x,y,x+1,y) # move self
    tileMoveRight(x+1, y) # keep on movin'

def LogTiles():
    window.console.log(f"{Tiles[0][0]}|{Tiles[1][0]}|{Tiles[2][0]}|{Tiles[3][0]}")
    window.console.log(f"{Tiles[0][1]}|{Tiles[1][1]}|{Tiles[2][1]}|{Tiles[3][1]}")
    window.console.log(f"{Tiles[0][2]}|{Tiles[1][2]}|{Tiles[2][2]}|{Tiles[3][2]}")
    window.console.log(f"{Tiles[0][3]}|{Tiles[1][3]}|{Tiles[2][3]}|{Tiles[3][3]}")

def keypress(e):
    global DID_MOVE
    kc = e.keyCode
    if kc not in [LEFT,RIGHT,UP,DOWN]:
        return
    DID_MOVE = False
    # Set all Tiles has merged to False
    for x in range(4):
        for y in range(4):
            if Tiles[x][y] is not None:
                Tiles[x][y][2] = False

    for element in document.getElementsByClassName("to-delete"):
        element.remove()

    if kc == LEFT:
        #window.console.log("Left")
        moveLeft()
    if kc == RIGHT:
        #window.console.log("Right")
        moveRight()
    if kc == UP:
        #window.console.log("Up")
        moveUp()
    if kc == DOWN:
        #window.console.log("Down")
        moveDown()
    if DID_MOVE:
        spawnTile()

window.console.log("Game Start")
spawnTile()