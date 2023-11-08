import tkinter
from tkinter import *
from tkinter import filedialog
import PyPDF2
import pyttsx3
# python -m pip install PyPDF2 pyttsx3

'''
Sample PDF Reader
=================
import PyPDF2

fileobject=open("dummy.pdf", "rb")
pdffilereader=PyPDF2.PdfReader(fileobject)

extract_text=""

for pageNum in range( len(pdffilereader.pages)):
	pdfpageObj = pdffilereader.pages[pageNum]
	extract_text += pdfpageObj.extract_text()


fileobject.close()
print(extract_text)

Sample PDF Reader
=================
import pyttsx3

engine_object=pyttsx3.init()
engine_object.setProperty('rate', 200)
engine_object.setProperty('voice', 'f1')
engine_object.say("hello world")
engine_object.say(extract_text)

engine_object.runAndWait()
'''
def extract_text():
	file = filedialog.askopenfile(parent=root, mode="rb", title="Choose a PDF file")
	if file:
		pdffilereader=PyPDF2.PdfReader(file)

		global extract_pdf_text

		for pageNum in range( len(pdffilereader.pages)):
			pdfpageObj = pdffilereader.pages[pageNum]
			extract_pdf_text += pdfpageObj.extract_text()
		file.close()

def speak_text():
	global rate, male, female
	r=int(rate.get())
	m=int(male.get())
	f=int(female.get())

	engine.setProperty('rate', r)
	all_voices=engine.getProperty('voices')
	maleVoice=all_voices[0].id
	femaleVoice=all_voices[1].id
	if (m == 0 and f == 1):
		engine.setProperty('voice', femaleVoice)
	else: #(m == 0 and f == 0) or (m == 1 and f == 1) or (m == 1 and f == 0):
		engine.setProperty('voice', maleVoice)

	engine.say(extract_pdf_text)

	engine.runAndWait()


def  stop_speaking():
	engine.stop()

def Application(root):
	root.geometry(f"{700}x{600}")
	root.resizable(width=False, height=False)
	root.title("PDF Reader")
	root.configure(background="light grey")

	global rate, male, female

	frame1=Frame(root, width=500,height=200, bg="indigo")
	frame2=Frame(root, width=500,height=450, bg="light grey")
	frame1.grid()#side=TOP,expand=NO,fill=NONE)
	frame2.grid()#side=TOP,expand=NO,fill=NONE)
	name1=Label(frame1, text="PDF to AUDIO",fg="black",bg="blue")
	name1.pack()
	name2=Label(frame1,text="Listen your PDF file", fg="red",bg="indigo",font="Calibri 25 bold")
	name2.pack()

	btn=Button(frame2, text="Select PDF file", activeforeground="red", command=extract_text,
			   padx="7", pady="10", fg="white",bg="black", font="Arial 12")
	btn.grid(row=0,pady=20,columnspan=2)

	rate_text=Label(frame2, text="Enter rate of speech", fg="black",bg="aqua",
		font="Arial 12")
	rate_text.grid(row=1,column=0,pady=15,sticky=W)
	default_rate=IntVar()
	default_rate.set(200)
	rate=Entry(frame2, textvariable=default_rate, fg="black", bg="white",font="Arieal 12")
	rate.grid(row=1, column=1, padx=30,pady=15, sticky=W)


	voice_text=Label(frame2, text="Select voice:", fg="black", bg="aqua", font="Arial 12")
	voice_text.grid(row=2, column=0,pady=15,padx=0,sticky=E)
	male=IntVar()
	maleOpt=Checkbutton(frame2, text="Male", bg="pink",variable=male,onvalue=1,offvalue=0 )
	maleOpt.grid(row=2,column=1,pady=0,padx=30,sticky=W)
	female=IntVar()
	female.set(1)
	femaleOpt=Checkbutton(frame2, text="Female", bg="pink",variable=female,onvalue=1,offvalue=0 )
	femaleOpt.grid(row=3,column=1,pady=0,padx=30,sticky=W)

	submitbtn=Button(frame2, text="Play PDF file", command=speak_text,
		activeforeground="red", padx="60", pady="10", fg="white", bg="black",
		font="Arial 12")
	submitbtn.grid(row=4, column=0,pady=65)

	stopbtn=Button(frame2, text="Stop Playing", command=stop_speaking,
		activeforeground="red", padx="60", pady="10", fg="white", bg="black",
		font="Arial 12")
	stopbtn.grid(row=4, column=1,pady=65)


if __name__=="__main__":
	extract_pdf_text, rate, male, female = "",100, 0, 0
	engine = pyttsx3.init()
	root = Tk()
	Application(root)
	root.mainloop()
