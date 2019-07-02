# 
# most of the code for the gunner class was modeled after the tank from this git:
# https://github.com/Mekire/pygame-samples/blob/master/tank_turret/turret_gamepad.py

import pygame
import os
import math
import sys

CAPTION = "TWIN STICK" 
SCREEN_SIZE = (800, 600)
BACKGROUND_COLOR = (50,50,50)
COLOR_KEY = (255, 0, 255) 

# character class
class Gunner(object):
	'''twin stick shooter'''
	def __init__(self, controller, location):
		'''location is (x,y) coord pair.'''
		
		# setup controller
		self.controller = controller 
		self.id = controller.get_id()
	
		# setup location and angle
		self.angle = 0
		self.location = location
	
		# setup gunner sprite. Has gunner and feet. top is gunner, bottom is feet.
		# create og gunner, then rotate and animate a copy of the og each frame
		self.original_gunner = GUNNER.subsurface((0,0,150,150)) # GUNNER will be a png with sprite assets. 
		self.gunner = self.original_gunner.copy()
		self.original_feet = GUNNER.subsurface((300,0,150,150))
		self.feet = self.original_feet.copy()
		self.gunner_rect = self.gunner.get_rect(center=location)
		self.feet_rect = self.feet.get_rect(center=location)
		self.gunner_angle=0
		self.feet_angle=0
		
	def set_angle(self, deadzone=0.1):
		'''
		get the current angle of the passed sticks 
		and set the according sprites.
		'''
	
		leftx,lefty = self.controller.get_axis(0), self.controller.get_axis(1)
		rightx,righty = self.controller.get_axis(3), -self.controller.get_axis(4)
		
		if abs(leftx) > deadzone or abs(lefty) > deadzone:
			# set the angle
			if leftx == 0.0: leftx += 0.0001
			self.feet_angle = 225.0 -math.degrees(math.atan2(float(lefty), float(leftx)))
			self.feet = pygame.transform.rotate(self.original_feet, self.feet_angle)
			self.feet_rect = self.feet.get_rect(center=self.feet_rect.center)
			# move the feet and gunner
			'''
			if abs(leftx) > deadzone:
				x += speed * axis0 # move horiz
			if abs(lefty) > deadzone:
				y += speed * axis1 # move vert
				self.gunner.transform.()
				self.feet.transform()'''
			'''
			movement control:
			# control movement
				if abs(axis0) > deadzone:
					x += speed * axis0
				
				if abs(axis1) > deadzone:
					y += speed * axis1
			'''
				
		# change the logic to just set the self.angle and self.x and self.y
		if abs(rightx) > deadzone or abs(righty) > deadzone:
			if rightx == 0.0: rightx += 0.0001
			self.gunner_angle = 45.0 -math.degrees(math.atan2(float(righty), float(rightx)))
			self.gunner = pygame.transform.rotate(self.original_gunner, self.gunner_angle)
			self.gunner_rect = self.gunner.get_rect(center=self.gunner_rect.center)
			
	def position(self):
		# self.angle
		# self.location
		pass
			
		
	def get_event(self, event, objects):
		'''catch and process gamepad events.'''
		if event.type == pygame.JOYBUTTONDOWN:
			if event.joy == self.id and event.button == 5:	# FIXME set fire button 
				objects.add(Bullet(self.gunner_rect.center, self.gunner_angle))
		if event.type == pygame.JOYAXISMOTION:
			if event.joy == self.id:
				self.set_angle()
	
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
		self.original_bullet = GUNNER.subsurface((150,0,150,150)) # FIXME bullet from sprite image
		self.angle = -math.radians(angle-135)
		self.image = pygame.transform.rotate(self.original_bullet, angle)
		self.rect = self.image.get_rect(center=location)
		self.pos = [self.rect.x, self.rect.y]
		self.speed = 9
		self.velocity = (self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
		self.done = False 
		
	
	def update(self, screen_rect):
		'''update the bullet each frame'''
		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]
		self.rect.topleft = self.pos 
		self.remove(screen_rect)
		
	def remove(self, screen_rect):
		'''remove the bullet if it has left the screen'''
		if not self.rect.colliderect(screen_rect):
			self.kill()
	
class Control(object):
	'''main control class'''
	def __init__(self):
		'''create a gunner and create a group for bullets '''
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.joys = initialize_all_gamepads()
		self.done = False
		self.clock = pygame.time.Clock()
		self.fps = 30
		self.keys = pygame.key.get_pressed()
		self.player = Gunner(self.joys[0], self.screen_rect.center)# FIXME May have to replace center with (x,y)
		self.bullets = pygame.sprite.Group()
		
	def event_loop(self):
		''' events are passed to appropriate object'''
		for event in pygame.event.get():
			self.keys = pygame.key.get_pressed()
			if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
				self.done = True 
			self.player.get_event(event, self.bullets)
			
	def update(self):
		''' update all bullets '''
		self.bullets.update(self.screen_rect)
		
	def draw(self):
		'''draw all elements to the display surface'''
		self.screen.fill(BACKGROUND_COLOR)
		self.player.draw(self.screen)
		self.bullets.draw(self.screen)
		
	def display_fps(self):
		'''show the program's FPS in the window handle'''
		caption = '{} - FPS: {:.2f}'.format(CAPTION, self.clock.get_fps())
		pygame.display.set_caption(caption)
		
	def main_loop(self):
		'''main loop'''
		while not self.done:
			self.event_loop()
			self.update()
			self.draw()
			pygame.display.flip()
			self.clock.tick(self.fps)
			self.display_fps()
			
def initialize_all_gamepads():
	'''checks for gamepads and returns an intialized list of them if found'''
	joysticks = []
	for joy_id in range(pygame.joystick.get_count()):
		joysticks.append(pygame.joystick.Joystick(joy_id))
		joysticks[joy_id].init()
	return joysticks

	
def main():
	'''prepare display, load sprite image, and start program'''
	global GUNNER 
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	# pygame window setup 
	pygame.init()
	pygame.display.set_caption(CAPTION)
	pygame.display.set_mode(SCREEN_SIZE)
	# load sprite images
	GUNNER = pygame.image.load("gunner.png").convert()
	GUNNER.set_colorkey(COLOR_KEY)
	
	Control().main_loop()
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	