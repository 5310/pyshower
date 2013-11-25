import pyglet
import os
from random import shuffle

interval = 1

window = pyglet.window.Window(resizable = True)
window.set_mouse_visible(False)
window.set_caption("Navyshower")
background = (0.2,0.2,0.2,1)
pyglet.gl.glClearColor(*background)


class Show():
    def __init__(self):
	self.interval = interval
	self.stretch = False
	self.state = 1	#0 = pause; 1 = running
	self.showtimer = False
	self.scan_images()	
	self.tick(0)
	pyglet.clock.schedule_interval(self.tick, self.interval)
	
	
    def scan_images(self):
	self.files = filter(os.path.isfile, os.listdir('.'))
	self.imagequeue = []
	for item in self.files:
		if item[-3:].lower() in ("png", "jpg"):
			self.imagequeue.append(item)
	shuffle(self.imagequeue)
	self.position = 0
	if not self.imagequeue: self.state = -1

    def load_image(self):
	#loading and anchoring the actual image and sprite
	imagename = self.imagequeue[self.position]
	try:
	    self.image = pyglet.image.load(imagename)
	    self.image.anchor_x = self.image.width/2
	    self.image.anchor_y = self.image.height/2
	    self.sprite = pyglet.sprite.Sprite(self.image)
	    window.set_caption(imagename+" - Navyshower")
	except:
	    print "whahappon?"
	    self.imagequeue.remove(imagename)
	    self.load_image()
	    if not self.imagequeue: self.scan_images()
	
    
    def draw(self):
	if self.state == -1:
	    #show something when there is nothing
	    pass
	else:
	    self.fit()
	    self.sprite.draw()
	
    def fit(self, window=window):
	if self.sprite.width > window.width or self.sprite.height > window.height or self.stretch:
	    if self.sprite.width/float(self.sprite.height) > window.width/float(window.height):
		self.sprite.scale = window.width/float(self.sprite.width)*self.sprite.scale
	    else:
		self.sprite.scale = window.height/float(self.sprite.height)*self.sprite.scale
	self.sprite.set_position(window.width/2, window.height/2)
	    
    def backward(self):
	self.position = len(self.imagequeue)-1 if self.position == 0 else self.position-1
	self.load_image()
	self.pause()
	print "backward"
	
    def forward(self):
	if len(self.imagequeue) > 1: 
	    self.position += 1
	    self.position %= len(self.imagequeue)-1
	self.load_image()
	print "forward"
	
    def pause(self):
	self.state = 0
	print "pause"
	
    def unpause(self):
	self.state = 1
	print "unpause"
	
    def toggle_pause(self):
	self.state = 0 if self.state == 1 else 1
	print "toggle pause"
	
    def slower(self):
	self.interval += 1
	shower.unpause()
	pyglet.clock.unschedule(self.tick)
	pyglet.clock.schedule_interval(self.tick, self.interval)
	print "slower/t interval %d seconds" % (self.interval)
	
    def faster(self):
	if self.interval > 1:
	    self.interval -= 1
	shower.unpause()
	pyglet.clock.unschedule(self.tick)
	pyglet.clock.schedule_interval(self.tick, self.interval)
	print "faster/t interval %d seconds" % (self.interval)
	
    def toggle_stretch(self):
	self.stretch = not self.stretch
	
    def tick(self, dt):
	if self.state == -1:
	    self.scan_images()
	if self.state == 1:
	    self.forward()
	
shower = Show()


@window.event
def on_draw():
    window.clear()
    shower.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        shower.forward()
	
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.F11:
	window.set_fullscreen(not window.fullscreen)
	
    elif symbol == pyglet.window.key.LEFT:
	shower.backward()
	shower.pause()
    elif symbol == pyglet.window.key.RIGHT:
	shower.forward()
	
    elif symbol == pyglet.window.key.SPACE:
	shower.toggle_pause()
	
    elif symbol == pyglet.window.key.PLUS or symbol == pyglet.window.key.EQUAL or symbol == pyglet.window.key.NUM_ADD:
	shower.faster()
    elif symbol == pyglet.window.key.MINUS or symbol == pyglet.window.key.NUM_SUBTRACT:
	shower.slower()
	
    elif symbol == pyglet.window.key.F4:
	shower.toggle_stretch()
	
    

pyglet.app.run()

