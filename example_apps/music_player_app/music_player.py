import tkinter 
from tkinter import *
from pygame import mixer
from tkinter import filedialog
from PIL import Image, ImageTk

# python -m pip install pygame Pillow

window=Tk()

window.geometry("300x300")
window.title("Python Music Player")

def browse_file():
	global filename
	filename=filedialog.askopenfilename()

def help_me():
	tkinter.messagebox.showinfo("help", "Version 1.0")

def play_music():
	try:
		paused
	except:
		try:
			mixer.music.load(filename)
			mixer.music.play()

			statusbar['text']='Music is playing'
		except Exception as ex:
			print(f" file {ex} not found")
			tkinter.messagebox.showerror("File Error", "File Not found")
	else:
		mixer.music.unpause()
		statusbar['text']='Music is resumed'

def stop_music():
	mixer.music.stop()
	statusbar['text']='Music is stopped'

def set_volume(value):
	try:
		mixer.music.set_volume(int(value)/100)
	except Exception as ex:
		print(f"{ex}")
		tkinter.messagebox.showerror("mixer error") 

def pause_music():
	global paused
	paused=True
	mixer.music.pause()
	statusbar['text']='Music is paused'

def rewind_music():
	play_music()
	statusbar['text']='Music is rewinded'

def image_load(filename, x=70, y=70):
	image = Image.open(filename)
	# Resize the image using resize() method
	resize_image = image.resize((x, y))
	# Resize the image using resize() method
	img = ImageTk.PhotoImage(resize_image)
	return img

menubar=Menu(window)
submenu=Menu(menubar,tearoff=0)
window.config(menu=menubar)

menubar.add_cascade(label="File",menu=submenu)
submenu.add_cascade(label="Open", command=browse_file)
submenu.add_cascade(label="Exit", command=window.destroy)

submenu=Menu(menubar,tearoff=0)
menubar.add_cascade(label="About Us",menu=submenu)
submenu.add_cascade(label="Help", command=help_me)


textLabel=Label(window, text="This is  a Play button")
textLabel.pack()


try:
	mixer.init()
except Exception as ex:
	print(f"{ex}")
	tkinter.messagebox.showerror("mixer error") 

frame=Frame(window)
frame.pack(padx=10, pady=10)

playphoto=image_load('play.png')
#playphoto = PhotoImage(file='play.png')
playButton=Button(frame, image=playphoto, command=play_music)
playButton.grid(row=0, column=0, padx=10)

stopphoto=image_load('stop.png')
stopButton=Button(frame, image=stopphoto, command=stop_music)
stopButton.grid(row=0, column=1, padx=10)

pausephoto=image_load('pause.png')
pauseButton=Button(frame, image=pausephoto, command=pause_music)
pauseButton.grid(row=0, column=2, padx=10)


bottomframe=Frame(window)
bottomframe.pack(padx=1, pady=10)

rewindphoto=image_load('rewind.png', x=15, y=15)
rewindButton=Button(bottomframe, image=rewindphoto, command=rewind_music)
rewindButton.grid(row=0, column=0, padx=10)

scale=Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_volume)
scale.set(70)
scale.grid(row=0, column=1, padx=2,pady=10)

statusbar=Label(window, text="Keep enjoying the music", relief=SUNKEN,anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

window.mainloop()
