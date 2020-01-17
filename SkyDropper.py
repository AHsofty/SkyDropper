"""
Created by AHsoft
https://github.com/AHsofty
"""
import turtle
import random

# Define some variables
move = True
ongoing = True
MaxSpeed = 5
points = 0

enemy_amount = 15
coin_amount = 6


# Create the turtle screen
wn = turtle.Screen()
wn.bgcolor("Orange")
wn.title("falling skies")
wn.tracer(0)
wn.setup(height=800, width=600)
wn.addshape("bomb.gif")
wn.addshape("coin.gif")
wn.addshape("player.gif")
wn.delay(0)
wn.update()

'''
Draw lines for player to "walk on"
This was inspired by the game undertale (muffet fight)
'''

border_line = turtle.Turtle()
border_line.color("purple")
border_line.speed(0)
border_line.pensize(2)
border_line.hideturtle()
border_line.penup()
border_line.goto(-520 ,-315)
border_line.pendown()
border_line.goto(520, -315)
border_line.penup()
border_line.goto(-520, -255)
border_line.pendown()
border_line.goto(520, -255)
border_line.penup()
border_line.goto(-520, -195)
border_line.pendown()
border_line.goto(520, -195)
border_line.penup()
border_line.goto(-520, -375)
border_line.pendown()
border_line.goto(520, -375)


# Create the player
player = turtle.Turtle()
player.shape("player.gif")
player.speed(0)
player.penup()
player.goto(0 , -375)

"""
Creates a scoreboard
"""
board = turtle.Turtle()
board.speed(0)
board.color("white")
board.penup()
board.hideturtle()
board.goto(250, 350)
board.write(points, font=("courier", 24, "normal"))

"""
This is the class that does everything the enemies need to do
"""
class Enemies(turtle.Turtle):
	def __init__(self):
		# Creates the enemies
		turtle.Turtle.__init__(self)
		self.penup()
		self.color("red")
		self.speed(0)
		self.goto(random.randint(-200, 300), random.randint(100, 400))
		self.shape("bomb.gif")
		if self.xcor() == player.xcor():
			self.replace_enemy()
	
	def replace_enemy(self):
		# Replaces the enemies
		self.goto(random.randint(-270, 270), random.randint(200, 400))

"""
This creates a class that does everything with the coins/points
"""
class Create_coins(turtle.Turtle):
	def __init__(self):
		# Creates the coins
		turtle.Turtle.__init__(self)
		self.penup()
		self.color("red")
		self.speed(0)
		self.goto(random.randint(-200, 300), random.randint(100, 400))
		self.shape("coin.gif")
		if self.xcor() == player.xcor():
			self.replace_enemy()
	
	def replace_coin(self):
		# Replaces the coin
				
		self.goto(random.randint(-270, 270), random.randint(200, 400))

# Creates all of the coins
coins = []
for i in range(coin_amount):
	coins.append(Create_coins())

"""	
This allows us to create multiple enemies at the same time.
This also allows us to iterate through all the enemies and do things like moving them and checking for collisions etc
"""
enemies = []
for i in range(enemy_amount):
	enemies.append(Enemies())


"""
These direction functions allow the player to move in any direction
Note that it first checks if the player is allowed to move in that certain direction
For example: It checks if the player doesn't go down under the screen or get out of the lines 
"""
def left():
	if move == True and player.xcor() > -270:
		player.setheading(180) # Makes the player look in the 180 direction (Which is in this case left)
		player.forward(20) # Moves the player forward
		

def right():
	if move == True and player.xcor() < 270:
		player.setheading(0)
		player.forward(20)

def up():
	if move == True and player.ycor() <= -196:
		player.goto(player.xcor(), player.ycor()+60)

def down():
	if move == True and player.ycor() != -375:
		player.goto(player.xcor(), player.ycor()-60)
		if player.ycor() < -376:
			player.sety(-375)

def game_over():
	global move
	global ongoing
	move = False
	ongoing = False

def restart():
	"""
	This function will restart the game
	"""

	global player
	global enemies
	global points
	global move
	global ongoing
	global coins
	global coin

	# Resets the scorebaord and points
	points = 0
	board.clear()
	board.write(points, font=("courier", 24, "normal"))

	# Replaces the enemies
	for enem in enemies:
		enem.replace_enemy()
	# Replaces the coins
	for coin in coins:
		coin.replace_coin()

	# Reset the move and ongoing variable to enable movement and the while loop
	ongoing = True
	move = True

# Asign keyboard inputs
wn.listen()
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")
wn.onkeypress(left, "a")
wn.onkeypress(right, "d")
wn.onkeypress(up, "Up")
wn.onkeypress(down, "Down")
wn.onkeypress(up, "w")
wn.onkeypress(down, "s")
wn.onkeypress(restart, "space")


while True:
	wn.update()
	if ongoing:
		"""
		Right now we're going to iterate through all the enemies and make them do stuff
		Or make them check for stuff
		"""
		for enem in enemies:

			"""
			Makes the enemy fall from the sky. Note that the speed is randomised from 1 to 5
			You can read more about the random module here:
			https://docs.python.org/3/library/random.html
			"""
			enem.sety(enem.ycor()-random.randint(1, MaxSpeed)) # Replaces the enemy. enem.ycor() is the enemy's y coordinate before the fall, and we're reducing it by the enemy fall speed which is randomised.

			if enem.distance(player) < 20: # If any enemy's distance to the player is smaller than 20px, it'll run the game over function and basically stop all movement
				game_over()

			"""
			This bit checks if the enemy is out of the screen (under the screen)
			If this is the case' it'll call for the replace_enemies() function which is in the enemies class
			"""

			if enem.ycor() < -400:
				enem.replace_enemy() # calls the replace_enemy() function, this function will replace the enemy
				wn.update() # Updates the screen


		for coin in coins:
			"""
			Now we're going to iterate through all of the coins and do stuff with them
			"""
			coin.sety(coin.ycor()-random.randint(1, MaxSpeed)) # Just like the enemies, this makes the coins fall down

			"""
			checks for a collision with the coin, if this is the case we want to just replace the coin and add a point
			After adding the point it updates the scoreboard
			"""
			if coin.distance(player) < 20:
				points += 1
				board.clear()
				board.write(points, font=("courier", 24, "normal"))
				coin.replace_coin()

			"""
			Check if the coin is out of the screen
			If this is the case we just want to replace the coin
			"""
			if coin.ycor() < -400:
				coin.replace_coin()










