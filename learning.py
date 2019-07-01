# 
# most of the code for the gunner class was modeled after the tank from this git:
# https://github.com/Mekire/pygame-samples/blob/master/tank_turret/turret_gamepad.py

import pygame

deadzone = 0.1

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
screen = pygame.display.set_mode((1200, 800))

# setup clock
clock = pygame.time.Clock()

# setup character
x = 30
y = 30
direction = 0
color = (0, 128, 255)
speed = 5

# character class
class Gunner(object):
	'''twin stick shooter'''
	def __init__(self, controller, location):
		'''location is (x,y) coord pair.'''
		
		# setup controller
		self.controller = controller 
		self.id = controller.get_id()
	
		# setup gunner sprite. Has gunner and feet. top is gunner, bottom is feet.
		# create og gunner, then rotate and animate a copy of the og each frame
		self.original_gunner = GUNNER.subsurface((0,0,150,150)) # GUNNER will be a png with sprite assets. 
		self.gunner = self.original_gunner.copy()
		self.original_feet = GUNNER.subsurface((0,0,10,10))
		self.feet = self.original_feet.copy()
		self.gunner_rect = self.gunner.get_rect(center=location)
		self.feet_rect = self.rect.copy()
		self.angle=0
		
	def get_angle(self, stick, deadzone=0.1):
		''' get the current angle of the passed stick'''
		if stick == 'left':
			x,y = self.controller.get_axis(0), self.controller.get_axis(1)
		elif stick == 'right':
			x,y = self.controller.get_axis(3), -1 * self.controller.get_axis(4)
		
		if abs(x) > deadzone or abs(y) > deadzone:
			if (x == 0.0): x += 0.0001
			# arctan(y/x)
			self.angle += 5 #FIXME: actually get angle
			self.barrel = pygame.transform.rotate(self.original_barrel, self.angle)
			self.barrel_rect = self.barrel.get_rect(center=self.rect.center)
		
	def get_event(self, event, objects):
		''' catch and process gamepad events.'''
		if event.type == pygame.JOYBUTTONDOWN:
			if event.joy == self.id and event.button == 0:	# FIXME set fire button 
				objects.add(Bullet(self.rect.center, self.angle))
			elif event.type == pygame.JOYAXISMOTION:
				if event.joy == self.id:
					if event.joy.get_axis() in (0,1): # FIXME this probably wont work
						self.get_angle('left')
					elif event.joy.axis() in (3,4): 
						self.get_angle('right')
	
	def draw(self, surface):
		'''draw gunner and feet to the target surface'''
		surface.blit(self.feet, self.feet_rect)
		surface.blit(self.gunner, self.gunner_rect)

class Bullet(pygame.sprite.Sprite):
	'''a class for the bullet sprites.'''
	def __init__(self, location, angle):
		'''
		takes in a coordinate pair and angle in degrees. 
		These are passed in by the gunner class when the projectile is created
		'''
		pygame.sprite.Sprite.__init__(self)
		self.original_bullet = GUNNER.subsurface((0,0,10,10)) # FIXME bullet from sprite image
		self.angle = angle # FIXME, may have to change this
		self.image = pygame.transform.rotate(self.original_laser, angle)
		self.rect = self.image.get_rect(center=location)
		self.pos = [self.rect.x, self.rect.y] # what does this do???
		self.speed = 9
		self.velocity = (self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
		self.done = False 
	
	def update(self, screen_rect):
		''' update the bullet each frame'''
		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]
		self.rect.topleft = self.pos 
		self.remove(screen_rect)
		
	def remove(self, screen_rect):
		'''remove the bullet if it has left the screen'''
		if not self.rect.colliderect(screen.rect):
			self.kill()
	
class Control(object):
	'''main control class'''
	def __init__(self):
		''' create a gunner and create a group for bullets '''
		

done = False 
while not done: 
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		print(event)
		
	
	# get the left stick positions
	axis0 = control.get_axis(0)
	axis1 = control.get_axis(1)
	
	# control movement
	if abs(axis0) > deadzone:
		x += speed * axis0
	
	if abs(axis1) > deadzone:
		y += speed * axis1
	
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	