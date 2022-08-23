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

import math
import time
import webbrowser

# config so things work gud-ly
from kivy.config import Config

# disable simulated multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# window size
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'minimum_width', '400')
Config.set('graphics', 'minimum_height', '400')

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
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

# file to load up on start
landing_file = 'kivy/character_view.kv'

# load fileB
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

class ButtonStack(ButtonBehavior, StackLayout):
	pass
# integer only input box
class IntInput(TextInput):
	def insert_text(self, substring, from_undo=False):
		try:
			s = str(int(substring))
		except:
			s = ''
		return super().insert_text(s, from_undo=from_undo)

# character viewer page 
class CharacterView(Screen):
	pass

	# global ids
	global_widgets = {}
	def register_widget(self, widget_object):
		if widget_object.gid not in self.global_widgets:
			print(widget_object.gid)
			self.global_widgets[widget_object.gid] = widget_object


	def get_widget(self, widget_gid):
		if widget_gid in self.global_widgets:
			return self.global_widgets[widget_gid]
		else:
			return None


	##### ERROR when sidebar is hidden and window is resized verticaly the (hidden) sizebar apears to have width set to 250 rather than 0 as it should while all other attributes apear to be consistant. Suspicios of either hide_widget or size_items methods

	# hides a widget
	def hide_widget(self, wid, dohide=True):
		if hasattr(wid, 'saved_attrs'):
			if not dohide:
				wid.height, wid.size_hint_y, wid.opacity, wid.disabled, wid.size_hint_x, wid.width = wid.saved_attrs
				del wid.saved_attrs
		elif dohide:
			wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled, wid.size_hint_x, wid.width
			wid.height, wid.size_hint_y, wid.opacity, wid.disabled, wid.size_hint_x, wid.width = 0, None, 0, True, None, 0


	# resize the contents to fit nicely in window
	def size_items(self):
		GAP = 7
		SIDE_BAR = 250
		MIN_SIDE = 240

		# calculations for minimum sizes for different layouts
		ITEM_CLASSES = {
			SIDE_BAR + (4 * (MIN_SIDE + GAP) + GAP): (4, 1),
			SIDE_BAR + (3 * (MIN_SIDE + GAP) + GAP): (3, 1),
			3 * (MIN_SIDE + GAP) + GAP: (3, 0),
			2 * (MIN_SIDE + GAP) + GAP: (2, 0),
			0: (1, 0)
		}

		# get calculation number
		SIZE_KEYS = ITEM_CLASSES.keys()

		# get widgets to resize
		items = [
			self.get_widget("stat_block"),
			self.get_widget("stat_block2"),
			self.get_widget("stat_block3"),
			self.get_widget("stat_block4")
		]

		# window width
		width = Window.width - 1

		# find best fitting size
		for key in SIZE_KEYS:
			if width > key:
				# size variables
				cols, side_toggle = ITEM_CLASSES[key]

				# item size calculation
				item_width = math.floor((width - ((cols * GAP) + GAP + (SIDE_BAR * side_toggle))) / cols)

				for item in items:
				# set all items
					item.width = item_width

				# show or hide sidebar and sidebar button when minimized
				self.hide_widget(self.get_widget("sidebar"), not side_toggle)
				self.hide_widget(self.get_widget("side_bar_btn"), side_toggle)

				# hide temporary grid
				self.hide_widget(self.get_widget("remove"), 1)
				
				break


	# show 
	def sidebar_btn(self):
		self.hide_widget(self.global_widgets["sidebar"])


	# send user to github repo
	def view_source(self):
		webbrowser.open("https://github.com/SpicedSage/Leaf-Character-Gen")

# program class
class MainApp(App):
	def build(self):
		# init screen manager
		sm = ScreenManager()

		# add screens
		sm.add_widget(CharacterView(name='char_view'))

		# update on resize
		def resize(window, width, height):
			# print('Window was resized!')
			sm.screens[0].size_items()

			time.sleep(0.01)

			# print(sm.screens)

		Window.bind(on_resize=resize)

		self.title = 'Leaf Character View'
		self.icon = "Images/Logo/Leaf-Logo_large.png"


		return sm

# main
if __name__ == '__main__':
	ma = MainApp()
	ma.run()
