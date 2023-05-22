import math
import turtle as trtl
wn = trtl.Screen()
wn.setup(width=800, height=800) # set dimensions of the window

"""
Default target and cannon images are in the same directory, 
and the angled cannon images are in a nested directory called 'Images'
"""

image_angle = 0
while image_angle < 9:  # add all 9 cannon images of different angles
  image_angle += 1
  wn.addshape('Images/Cannon_{}0.gif'.format(str(image_angle)))
wn.addshape('Images/Cannon_45.gif') # add the 45 degree cannon

background = trtl.Turtle()
background.pencolor('green')
background.pensize(200)
background.speed(0)
background.penup()
y = -500
x = 900
while y < 300:    # draw grass and sky
  y += 100
  if y > 100:
    background.pencolor('lightblue')
  background.goto(x, y)
  x = -x
  background.pendown()
  background.goto(x, y)

background.penup()  # draw sun
background.goto(400, 400)
background.shape('circle')
background.color('yellow')
background.shapesize(20)
background.stamp()

y = -400
x = -400
height = 550
background.pensize(20)
background.hideturtle()
background.pencolor('brown')
background.goto(x, y)
while background.xcor() < -200:
  background.pendown()
  background.goto(x, y)
  background.goto(x, y + height)
  x += 20
  y += 5


# creat a turtle with a cannon image as its shape
cannon_image = 'cannon.gif'
wn.addshape(cannon_image)
cannon = trtl.Turtle(shape=cannon_image)
cannon.hideturtle()
cannon.penup()
cannon.speed(0)
# creat a turtle with the target image as its shape and move it to its position
target_image = 'Target.gif'
wn.addshape(target_image)
target = trtl.Turtle(shape=target_image)
target.color('white')
target.penup()
target.speed(0)
target.goto(-300, 0)
target.shapesize(20)
target.stamp()
# create a turtle that will be the projectile
cannon_ball = trtl.Turtle(shape='circle')
cannon_ball.hideturtle()
cannon_ball.color('red')
cannon_ball.penup()
cannon_ball.speed(0)
cannon_ball.shapesize(0.5)

start_x = 300
start_y = -300

cannon.goto(start_x, start_y)
cannon.showturtle()

scores = []       # empty list of for all scores

repeat_input = ''
print('\nEnter the angle to fire the cannon!')
while repeat_input != 'n':
  angle_input = input('Angle: ')

  viable = False
  while viable == False:      # check if the input is between 10 and 90 and an integer
    try:
      if float(angle_input) > 90 or float(angle_input) < 10:
        angle_input = input('Invalid Input: (Angle must be between 10 and 90 degrees)\nAngle: ')
      else:
        viable = True
    except ValueError:
      angle_input = input('Invalid Input: (Angle must be an float between 10 and 90)\nAngle: ')

  angle = float(angle_input)  
  if angle == 45:             # change the angle of the cannon to be the closest match with the input angle
    cannon.shape('Images/Cannon_45.gif')
  else:
    if int(angle_input[1]) >= 5:
      degree_tens_place = int(angle_input[0]) + 1
    else:
      degree_tens_place = int(angle_input[0])
    cannon.shape('Images/Cannon_{}0.gif'.format(str(degree_tens_place)))

  grav_accel = -1             # constants and varialbles for projectile motion simulation
  mag_velocity = 60
  time = 0

  cannon_ball.goto(start_x, start_y)
  cannon_ball.speed(50)

  target_center = target.xcor() + 20    # apriximate center of the target in x-cordinate values

  # fire the cannon
  over_the_target = False
  x_end = -900
  while cannon_ball.xcor() > x_end and cannon_ball.ycor() > cannon.ycor() - 50: # loop will continue until the projectile passes the target or hits the ground
    time += 0.3   # only prpresents how far apart different points are - likely should not exeed 1

    y_velocity = mag_velocity * (math.sin(angle * (math.pi / 180)))   # calculate the y-component of the velocity vector
    y = (grav_accel * (time ** 2)) + (y_velocity * time) + start_y    # calculate y-position from the gravitational constant, y-component of the velocity vector, and starting position

    x_velocity = mag_velocity * (math.cos(angle * (math.pi / 180)))   # calculate the x-component of the velocity vector
    x = (x_velocity * time) - start_x                                 # calculate x-position from the x-component of the velocity vector and starting position


    acuracy = 0
    if -x < target_center and over_the_target == False:  # keeps projectile from going past the target and makes them all end in the same spot
      if cannon_ball.ycor() < 200:  # stop the projectile if it hits the target or backboard, if not it will stop off screen
        x = -target_center
        time_to_target = (-target_center + start_x) / x_velocity        # just a rearranged equation solved for time given the know value of x
        y = (grav_accel * (time_to_target ** 2)) + (y_velocity * time_to_target) + start_y  # plug in to get the ending y-position
        x_end = 0
      else:
        over_the_target = True

      acuracy = 200 - abs(cannon_ball.ycor() + target.ycor()) # distance from perfect bullseye (200 is aproximately the 'radius' of the target)
      

    cannon_ball.goto(-x, y)

    if ((start_x - cannon_ball.xcor()) ** 2) + ((start_y - cannon_ball.ycor()) ** 2) > (40 ** 2): # hide all traces of the projectile until it 'leaves' the cannon
      cannon_ball.showturtle()
      cannon_ball.pendown()

  if acuracy < 0: # if the projectile did not hit the target at all the score will be zero
    acuracy = 0
  score = acuracy * 5 # scale up scores to where a perfect score is 1000
  scores.append(score)
  print('Score: ' + str(score)[0:5])

  cannon_ball.stamp()
  cannon_ball.penup()
  repeat_input = input('Would you like to try again? (y/n): ')
  viable = False
  while viable == False:  # verify input
    if repeat_input != 'y' and repeat_input != 'n':
      repeat_input = input('Invalid Input: (Type \'y\' or \'n\'): ')
    else:
      viable = True
# find highest score
highest_score = 0
for score in scores:
  if score > highest_score:
    highest_score = score

# display the score to the user
print('Your highscore: ' + str(highest_score)[0:5] + ' out of 1000.')
if highest_score > 750:
  print('Great Job!')
