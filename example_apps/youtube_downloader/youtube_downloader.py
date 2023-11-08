from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import re
import threading


# python -m pip install --upgrade pytube

class Application:
	def __init__(self, root):
		self.root=root
		self.root.grid_rowconfigure(0, weight=2)
		self.root.grid_columnconfigure(0, weight=1)
		self.root.config(bg="#ffdddd")
		top_label=Label(self.root, text="Youtube download manager", fg="orange", font=("Type zero", 70))
		top_label.grid(pady=(0, 10))

		link_label=Label(self.root, text="Please paste Video URL below", fg="orange", font=("SnowPersons", 30))
		link_label.grid(pady=(0, 20))

		self.youtubeEntryVar = StringVar()
		self.youtubeEntryVar.set("https://www.youtube.com/watch?v=DkU9WFj8sYo")

		self.youtubeEntry=Entry(self.root, width=70,textvariable=self.youtubeEntryVar,font=('Agency Fb', 25))
		self.youtubeEntry.grid(pady=(0, 15), ipady=2)

		self.youtubeEntryError = Label(self.root, text="",font=("concert one", 20))
		self.youtubeEntryError.grid(pady=(0, 8))

		self.youtubeFileSaveLabel = Label(self.root, text="choose directory",font=("concert one", 30))
		self.youtubeFileSaveLabel.grid()

		self.youtubeFileDirectoryButton=Button(self.root, text="Directory", font=("Bell MT", 15), command=self.openDirectory)
		self.youtubeFileDirectoryButton.grid(pady=(10, 3))

		self.fileLocationLabel=Label(self.root,font=("Freestyle script", 25))
		self.fileLocationLabel.grid()

		self.youtubeChooseLable=Label(self.root, text="Choose the download Type", font=("Veriety", 25))
		self.youtubeChooseLable.grid()

		self.downaloadChoices=[("Audio MP3", 1), ("Video MP4", 2)]
		self.ChoicesVar=StringVar()
		self.ChoicesVar.set(1)

		for text, mode in self.downaloadChoices:
			self.youtubeChoices=Radiobutton(self.root,text=text,font=("Northwest old",15), variable=self.ChoicesVar, value=mode)
			self.youtubeChoices.grid()

		self.downloadButton=Button(self.root,text="Download",width=10,font=("Bell MT",15), command=self.checkyoutubelink)
		self.downloadButton.grid(pady=(30,5))


	def checkyoutubelink(self):
		self.matchyoutubelink=re.match("^https://www.youtube.com/.", self.youtubeEntryVar.get())
		if not self.matchyoutubelink:
			self.youtubeEntryError.config(text="Invalid youtube link", fg="red")
		elif not self.openDirectory:
			self.fileLocationLabel=config(text="please choose a Directory", fg="red")
		elif self.matchyoutubelink and self.openDirectory:
			self.downloadWindow()
		else:
			pass

	def downloadWindow(self):
		self.newWindow =Toplevel(self.root)
		self.root.withdraw()
		self.newWindow.state("zoomed")
		self.newWindow.grid_rowconfigure(0, weight=0)
		self.newWindow.grid_columnconfigure(0, weight=1)

		self.app=SecondApp(self.newWindow,self.youtubeEntryVar.get(), self.folderName,self.ChoicesVar.get())

	def openDirectory(self):
		self.folderName=filedialog.askdirectory()

		if len(self.folderName):
			self.fileLocationLabel.config(text=self.folderName,fg='green')
			return True
		else:
			return False

class SecondApp:
	def __init__(self, downloadwindow, youtubelink, foldername, choices):
		self.downloadWindow=downloadwindow
		self.youtubelink=youtubelink
		self.folderName=foldername
		self.choices=choices
		self.yt=YouTube(self.youtubelink, on_progress_callback=self.show_progress)

		if (choices == "1"):
			self.video_type=self.yt.streams.filter(only_audio=True).first()
			self.MaxFileSize=self.video_type.filesize
		else:
			self.video_type=self.yt.streams.first()
			self.MaxFileSize=self.video_type.filesize

		self.loadinglabel=Label(self.downloadWindow, text="Downloading in progress...", font=("Small Fonts", 40))
		self.loadinglabel.grid(pady=(100, 0))
		self.loadingPercent=Label(self.downloadWindow, text="0",fg="green",font=("Agency FB", 40))
		self.loadingPercent.grid(pady=(50, 0))
		self.progressBar=ttk.Progressbar(self.downloadWindow, length=500, orient='horizontal', mode='indeterminate')
		self.progressBar.grid(pady=(50, 0))
		self.progressBar.start()
		# TODO fix progress bar
		#threading.Thread(target=self.yt.register_on_progress_callback, args=(self.show_progress,)).start()
		threading.Thread(target=self.downloadFile).start()

	def downloadFile(self):
		try:
			if self.choices=="1":
				self.video_type.download(self.folderName)

			if self.choices=="2":
				self.video_type.download(self.folderName)
		except EOFError as err:
		    print(err)

		else:
		    print("\n====== Done - Check Download Dir =======")


	def show_progress(self, stream=None, chunk=None, bytes_remaining=None):
		print(f"bytes_remaining : {bytes_remaining}")
		self.percentCount = 0
		if bytes_remaining:
			self.percentCount=float("%0.2f"% (100-(100*(bytes_remaining/self.MaxFileSize))))
		if self.percentCount<100:
			self.loadingPercent.config(text=self.percentCount)
		else:
			self.progressBar.stop()
			self.loadinglabel.grid_forget()
			self.progressBar.grid_forget()

			self.downloadFinished = Label(self.downloadWindow, text="Download Completed", font=("Agency FB", 30))
			self.downloadFinished.grid(pady=(150, 0))
			self.downloadedFileName = Label(self.downloadWindow, text=self.yt.title, font=("Terminal", 30))
			self.downloadedFileName.grid(pady=(50, 0))
			MB=float("%0.2f"% (self.MaxFileSize/1000000))
			self.downloadedFileSize = Label(self.downloadWindow, text=str(MB), font=("Agency FB", 30))
			self.downloadedFileSize.grid(pady=(50, 0))


if __name__=="__main__":
	window = Tk()
	window.title("YouTube Download Manager")
	window.state("zoomed") # fullscreen

	app = Application(window)
	mainloop()
