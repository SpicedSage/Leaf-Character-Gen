# import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

Builder.load_file('test.kv')


class ButtonGrid(ButtonBehavior, GridLayout):
	pass

	def set_bgcolor(self,r,b,g,o,*args):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(r/255.0,g/255.0,b/255.0,o/100)
			Rectangle(pos=self.pos,size=self.size)


class LandingScreen(Screen):
	pass

class SettingsScreen(Screen):
	pass

class PizzaScreen(Screen):
	pass

class TestingProgram(Screen):
	pass

class Test(App):

	def build(self):
		sm = ScreenManager()
		sm.add_widget(LandingScreen(name='landing_s'))
		sm.add_widget(SettingsScreen(name='settings_s'))
		sm.add_widget(PizzaScreen(name='pizza_s'))
		sm.add_widget(TestingProgram(name='program_s'))

		return sm

	class settings_f:
		def alert():
			print("Settings")

	class landing_f:
		def close():
			print("closing safely")
			exit()

	class pizza_f:
		name = ObjectProperty(None)
		pizza = ObjectProperty(None)
		color = ObjectProperty(None)

		def submit(root):
			name = root.inputname.text
			pizza = root.pizza.text
			color = root.color.text

			print(f"your name is {name} and you like the color {color} and {pizza} pizza!")

			root.inputname.text = ""
			root.pizza.text = ""
			root.color.text = ""

def main():
	print("running")

	Test().run()

	print("if you are seeing this then something realy fucked up- just restart it and dont do that again, im sorry")

if __name__ == '__main__':
	main()