'''
Project based heavily off of DiceCloud.
Their Web App can be found here: https://dicecloud.com
Thier GitHub Repository here:    https://github.com/ThaumRystra/DiceCloud
And thier Patreon here :         https://www.patreon.com/posts/53791769

Please check them out. The team over there is great, they put so much time and effort 
into what they do. Go show them some love, please!

Dice Cloud is the inpiration behind this project, however being DiceCloud is a Web App it
has its limitations and advantages, as does this project. Im producing this App which exsists 
to fix many of those issues, with the biggest two being speed and offline use.

I should mention, their point was to have a cloud based character manager. However, this project 
has no cloud access, everthing is stored directly on your computer. They exsist to fix different 
issues, and though they may share similar aethstetics, I am in no way affiliated with Dice Cloud 
or their Developement team.

Backup Files are not compatible between Dice Cloud and this Application or vice versa at the
current time.

Please note this is verry much a WIP and a passion project, so yes i know their are bugs they 
will be adressed eventualy and their may even be times, such as now, that it may be unusable. 
However i have an 8-5 job and am a solo developer, so please try to be patient, theres only so 
much one person can do.

Any questions or issues can be sent to me directly. Prefered contact method through discord 
at Sage#4244

Thank you for reading through this all, 
here if you got this far, you deserve a cookie, take it, its for you :) 🍪🥛

- Sage signing off
'''

# make text not blurry
import os
os.environ['KIVY_TEXT'] = 'sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_IMAGE'] = 'sdl2'

# config so things work gud-ly
from kivy.config import Config

# disable simulated multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# window size
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

# kivy module
import kivy

# restrict version
kivy.require('2.1.0')

# kivy things
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

# file to load up on start
landing_file = 'kivy\character_view.kv'

# load file
Builder.load_file(landing_file)

# works like a button, can be used like a grid, overall real nice
class ButtonGrid(ButtonBehavior, GridLayout):
	pass

	# easy background setter
	def set_bgcolor(self,r,b,g,o,*args):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(r/255.0,g/255.0,b/255.0,o/100)
			Rectangle(pos=self.pos,size=self.size)

# character viewer page 
class CharacterView(Screen):
	pass

	def hide_widget(wid, dohide=True):
		if hasattr(wid, 'saved_attrs'):
			if not dohide:
				wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
				del wid.saved_attrs
		elif dohide:
			wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
			wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True

	def resize(self):
		size = Window.width

		gap = 7
		side_bar = 250
		num = 0
		side_toggle = 1

		min_width = 240

		item_width = 0

		if size > ((1 * side_bar) + (4 * (min_width + gap) + gap)):
			num = 4
			side_toggle = 1
		elif size > ((1 * side_bar) + (3 * (min_width + gap) + gap)):
			num = 3
			side_toggle = 1
		elif size > ((0 * side_bar) + (3 * (min_width + gap) + gap)):
			num = 3
			side_toggle = 0
		elif size > ((0 * side_bar) + (2 * (min_width + gap) + gap)):
			num = 2
			side_toggle = 0
		else:
			num = 1
			side_toggle = 0

		item_width = (size - ((num * gap) + gap + (side_bar * side_toggle))) / num

		print(size)

		return item_width

# program class
class MainApp(App):
	def build(self):
		# init screen manager
		sm = ScreenManager()

		# add screens
		sm.add_widget(CharacterView(name='char_view'))

		return sm

# main
if __name__ == '__main__':
	MainApp().run()
