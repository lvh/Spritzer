import Image
import imghdr
from sys import argv
import os

script, folder, save_path, spritename = argv

def get_starting_css(class_start, sprite):
	css = ("""
[class^="%s"] {
	display: inline-block;
	background: url('%s') no-repeat;
}""") % (class_start, sprite)
	return css

def get_current_icon_css(class_start, icon, icon_width, icon_height, icon_position_y):
	icon = class_start + "-" + icon[:-4].lower()
	css = """
.%s {
	width: %spx;
	height: %spx;
	background-position: 0 -%spx;
}
""" % (icon, icon_width, icon_height, icon_position_y)
	return css


def spritzer(folder, save_path, spritename, filename = folder):
	path = os.getcwd() + "\\" + folder + "\\"
	sprite = Image.new("RGBA", (0,0))

	# CSS:
	class_start = "spricik-icon"
	filename = folder + ".css"
	css_file = open(save_path + "mycss.css", 'w')
	# add starting css to the file
	css_file.write(get_starting_css(class_start, spritename + ".png"))

	for icon in os.listdir(path):
		icon_path = path+icon
		if( imghdr.what(icon_path) ): # skip non-image files

			# Icon setup
			icon_img    = Image.open(icon_path)
			icon_size   = icon_img.size
			icon_width  = icon_size[0]
			icon_height = icon_size[1]

			# Sprite setup
			sprite_size   = sprite.size
			sprite_width  = sprite_size[0]
			sprite_height = sprite_size[1]

			# add current sprite css
			css_file.write(get_current_icon_css(class_start, icon, icon_width, icon_height, sprite_height))

			# setup new dimensions
			new_height = sprite_height + icon_height
			new_width = sprite_width
			
			# all images are placed vertically so if a sprite 
			# is wider than current sprite width, we need to 
			# change sprite width so an icon can fit. Otherwise, we wanna leave it as it is
			if(icon_width > sprite_width):
				new_width  = icon_width - sprite_width

			#change sprites width & height using crop()
			sprite = sprite.crop((0,0,new_width, new_height))

			# we created empty place for our icon,
			# so we can just paste it at the end of previous values
			sprite.paste(icon_img, (0,sprite_height), icon_img)

	save_path_sprite = save_path + spritename + ".png"
	save_path_css = save_path
	# print save_path

	# save sprite
	sprite.save(save_path_sprite)
	# save CSS
	css_file.close()


spritzer(folder, save_path, spritename)