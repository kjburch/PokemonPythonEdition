import turtle
import mapHandler

screen = turtle.Screen()

# this assures that the size of the screen will always be 400x400 ...
screen.setup(400, 400)

# ... which is the same size as our image
# now set the background to our space image
backgroundGrid = mapHandler.buildMapGrid(0)
backgroundImage = mapHandler.buildMapImage()

screen.addshape("mapData/route2.gif")
background = turtle.Turtle()
background.shape("mapData/route2.gif")

# Or, set the shape of a turtle
screen.addshape("Images/Sprites/Player/playerDown.gif")
screen.addshape("Images/Sprites/Player/playerLeft.gif")
screen.addshape("Images/Sprites/Player/playerRight.gif")
screen.addshape("Images/Sprites/Player/playerUp.gif")
player = turtle.Turtle()
player.setx(8)
player.sety(8)
player.shape("Images/Sprites/Player/playerDown.gif")
background.penup()
move_speed = 16


# these defs control the movement of our "turtle"
def up():
    background.sety(background.ycor()-move_speed)
    player.shape("Images/Sprites/Player/playerUp.gif")


def down():
    background.sety(background.ycor()+move_speed)
    player.shape("Images/Sprites/Player/playerDown.gif")


def left():
    background.setx(background.xcor()+move_speed)
    player.shape("Images/Sprites/Player/playerLeft.gif")


def right():
    background.setx(background.xcor()-move_speed)
    player.shape("Images/Sprites/Player/playerRight.gif")


# now associate the defs from above with certain keyboard events
screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")
screen.listen()

screen.mainloop()