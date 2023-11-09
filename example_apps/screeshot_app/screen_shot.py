from cefpython3 import cefpython as cef
import platform
import sys
import os
import subprocess
# pythoon -m pip install cefpython3-py3

try:
	from PIL import Image
except Exception as e:
	print("PIP is not install, Install using pip install PIL")
	# raise
	sys.exit(1)
else:
	pass
finally:
	pass

def main(url, w, h):
	global VIEWPORT_SIZE, PORT, SCREENSHOT_PATH
	URL=url
	VIEWPORT_SIZE =(w, h)
	SCREENSHOT_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)))

	check_versions()
	sys.excepthook=cef.ExceptHook()

	if os.path.exists(SCREENSHOT_PATH):
		print("Remove old Screenshot")
		os.remove(SCREENSHOT_PATH)

	command_line_arguments()

	settings={
		"windowless_rendering_enabled" : True,
	}
	switches = {
		"disable-gpu": "",
		"disable-gpu-compositing": "",
		"enable-begin-frame-scheduling": "",
		"disable-surfaces": "",
	}

	browser_settings = {
		"windowless_frame_rate": 30,
	}

	cef.initialize(settings=settings, switches=switches)
	create_browser(browser_settings)
	cef.MessageLoop()
	cef.Shutdown()
	print("Opening your screenshot with the default application")
	open_with_default_application(SCREENSHOT_PATH)

def check_versions():
	ver=cef.GetVersion()
	print(f"CEF Python {ver['version']}")
	print(f"Chromium {ver['chrome_version']}")
	print(f"CEF {ver['cef_version']}")
	print(f"Python {platform.python_version()} {platform.architecture()[0]}")

	assert cef.__version__ >= "57.0", "CEF Python v57.0+ required torun this"

def command_line_arguments():
	if len(sys.argv) == 4:
		url = sys.argv[1]
		width = sys.argv[2]
		height = sys.argv[3]

		if url.startswith("http://") or url.startswith("https://"):
			global URL
			URL = url
		else:
			print("Error: Invalid URL entered")
			sys.exit(1)

		if width > 0 and height > 0:
			global VIEWPORT_SIZE
			VIEWPORT_SIZE = (width, height)
		else:
			print("Error: Invalid Width and Height")
			sys.exit(1)
	elif len(sys.argv) > 1:
		print("Error: Expected arguments not received"
			"Expected argument are URL, width, height")
	else:
		pass


def create_browser(settings):
	global VIEWPORT_SIZE, URL
	parent_window_handle = 0
	window_info=cef.WindowInfo()
	window_info.SetAsOffscreen(parent_window_handle)
	print(f"VIEWPORT size: {str(VIEWPORT_SIZE)}")
	print(f"Loading URL: {URL}")
	browser = cef.CreateBrowserSync(window_info=window_info, settings=settings, url=URL)
	browser.SetClientHandler(loadHandler)
	browser.SetClientHandler(RenderHandler)
	browser.setFocusEvent(True)
	browser.WasResized()


def save_screenshot(browser):
	global SCREENSHOT_PATH
	buffer_string = browser.GetUserData("OnPaint.buffer, string")
	if not buffer_string:
		raise Exception("Buffer String was empty becasue onPaint wan never called")

	image = Image.frombytes("RGBA", VIEWPORT_SIZE, buffer_string, "raw", "RGBA", 0, 1)
	image.save(SCREENSHOT_PATH, "PNG")
	print(f"Saved screenshot to: {SCREENSHOT_PATH}")


def open_with_default_application(path):
	if sys.platform.startswith("darwin"): #mac
		subprocess.call(("open",path))
	elif os.name == "nt":
		os.startfile(path)
	elif os.name == "posix":
		subprocess.call(("open",path))
	else:
		pass

def exit_app(browser):
	print("Closing browser and exiting application")
	browser.CloseBrowser()
	cef.QuitMessageLoop()

class LoadHandle:
	def OnloadingStateChange(self, browser, is_loading, **_):
		if not is_loading:
			sys.stdout.write(os.linesep)
			print("website has been loaded")
			save_screenshot(browser)
			cef.PostTask(cef.TID_UI, exit_app, browser)

	def OnLoadError(self, browser, frame, error_code, faised_url, **_):
		if not frame.IsMain():
			return

		print(f"Failed to load URL: {faised_url}")
		print(f"Error code: {error_code}")
		cef.PostTask(cef.TID_UI, exit_app, browser)


class RenderHandler:
	def __init__(self):
		self.OnPaint_called = False

	def GerViewRect(self, rect_out, **_):
		rect_out.extend(0, 0, VIEWPORT_SIZE[0], VIEWPORT_SIZE[1])
		return True

	def OnPaint(self, browser, element_type, paint_buffer, **_):
		if self.OnPaint_called:
			sys.stdout.write(".")
			sys.stdout.flush()
		else:
			sys.stdout.write("OnPaint")
			self.OnPaint_called = True

		if element_type == cef.PET_VIEW():
			buffer_string= paint_buffer.GetBytes(mode="rgba", origin="top-left")
			browser.SetUserData("OnPaint.buffer_string", buffer_string)
		else:
			raise Exception("Unsupported element type in OnPaint")



import tkinter as tk

root=tk.Tk()
root.geometry("400x200")


class Widget:
	def __init__(self, labtext, set_variable):
		self.lab=tk.Label(root, text=labtext)
		self.lab.pack()
		self.v=tkStringVar()
		self.entry=Entry(root, textvariable=self.v)
		self.entry.pacck()
		self.v.set(set_variable)


	obj1=Widget("Enter website Name: ", "https:www.google.com")
	obj2=Widget("Enter width: ", "1024")
	obj3=Widget("Enter height: ", "2048")
	root.bind("<Return>", lambda x: main(obj1.v.get(), int(obj2.v.get())), int(obj3.v.get()))
	lab4=tk.Label(root, text="          ")
	lab4.pack()
	lab5=tk.Label(root, text="Press the Enter key to create Screenshot")
	lab5.pack()

	root.mainloop()
