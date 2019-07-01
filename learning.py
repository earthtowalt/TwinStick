import pygame

pygame.init()
# setup joysticks

# setup joystick controller.
control = None
while not control:
	pygame.joystick.init()
	print(pygame.joystick.get_count())
	if pygame.joystick.get_count() > 0:
		control = pygame.joystick.Joystick(0)
	else:
		print("no controller found")
		pygame.joystick.quit()
	pygame.time.wait(2000)
	
control.init()
print(control)

# setup window
screen = pygame.display.set_mode((400,300))

# setup clock
clock = pygame.time.Clock()

# setup character
x = 30
y = 30
direction = 0
color = (0, 128, 255)

# deadzone
deadzone = 0.3

done = False 
while not done: 
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		print(event)
		
	
	# pygame.joystick.get_axis()
	axis0 = control.get_axis(0)
	axis1 = control.get_axis(1)
	
	# control movement
	if abs(axis0) > deadzone:
		if axis0 > 0:
			x += 3
		else:
			x -= 3
	
	if abs(axis1) > deadzone:
		if axis1 > 0:
			y += 3
		else:
			y -= 3
	
	# control direction.
	# calculate direction based on axis 3,4
	
	# point in right direction
	
			
	# axis
	#       movement
	# 0: left, right
	# 1: up, down
	
	#       aim
	# 3: down, up
	# 4: left, right
	
	screen.fill((0,0,0))
	pygame.draw.rect(screen, color, 
					 pygame.Rect(x, y, 60, 80))
    
	
	pygame.display.flip()
	
	
	
	
	
	
	
print('exit')
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	