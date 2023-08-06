from tkinter import *
from tkinter import filedialog
from .misc_util import *
from .tune_freq import tune_cols

def main():

    root=Tk()
    root.title("CTSF's SWX Tuner")

    notes=['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    selectorOptions=["Scale","Notes"]

    intervalVar = StringVar()
    fileVar = StringVar()

    scaleVar = IntVar()
    showVar = IntVar()

    noteVars = [IntVar() for _ in range(len(notes))]

    def limitIntervalLen(*args):
        interval_in = intervalVar.get()
        if len(interval_in)>2 or (len(interval_in) >0 and not interval_in[-1].isdigit()):
            intervalVar.set(interval_in[:-1])

    intervalVar.trace('w',limitIntervalLen)

    def showsel():
        if showVar.get():
            scaleRadioFrame.pack_forget()
            noteButtonsFrame.pack(side='right')
        else:
            noteButtonsFrame.pack_forget()
            scaleRadioFrame.pack(side='right')

    def getFile():
        file =  filedialog.askopenfilename(
            title="Select File to Tune",
            filetypes=[("SWX Files","*.swx")]
            )
        
        fileName.config(text=f'File: {file[file.rfind("/")+1:]}')
        fileVar.set(file) 

    def tuneWithData():
        filepath = fileVar.get()
        interval = int(intervalVar.get())

        tuneType = showVar.get()        # 0: scale, 1: notes
        if tuneType == 0:
            scale = construct_default_scale(scaleVar.get(), 'maj_scale')
        else:
            scale = [i+1 for i in range(len(noteButtons)) if noteVars[i].get()]

        can_proceed = (filepath and interval and scale)

        if can_proceed:
            tune_cols(filepath, interval, scale)

    optionsFrame = Frame(root, borderwidth=10)
    optionsFrame.pack(side='left', anchor=N)


    # File Input
    fileFrame = Frame(optionsFrame, borderwidth=5)
    fileFrame.pack(side='top', anchor=W)

    fileLabel = Label(fileFrame, text="Select File to Tune:")
    fileLabel.pack(side='top', anchor=W)

    fileInput = Button(fileFrame, text="Browse Files...", command=getFile)
    fileInput.pack(side='left')

    fileName = Label(fileFrame)
    fileName.pack(side='right')


    # Interval Input
    intervalFrame = Frame(optionsFrame, borderwidth=3)
    intervalFrame.pack(side='top', anchor=W)

    intervalInputLabel = Label(intervalFrame, text="Tuning interval (x10ms): ")
    intervalInputLabel.pack(side='left')

    intervalInput = Entry(intervalFrame, width=2, textvariable=intervalVar)
    intervalInput.pack(side='right')


    # Submit Button

    submitButton = Button(optionsFrame, text="Tune File", command=tuneWithData, borderwidth=15)
    submitButton.pack(side='bottom',anchor=SW)

    # Selector Radios
    selectorFrame = Frame(optionsFrame, borderwidth=3)
    selectorFrame.pack(side='top', anchor=W)

    selectorLabel = Label(selectorFrame, text="Tune File By: ")
    selectorLabel.pack(anchor=W)

    selectorButtons = [Radiobutton(selectorFrame,text=n, variable=showVar, command=showsel, value=i) for i,n in enumerate(selectorOptions)]
    for n in selectorButtons: n.pack(anchor=W)


    # Scale radiobuttons
    scaleRadioFrame = Frame(root, borderwidth=10)
    scaleRadioFrame.pack(side='right')

    scaleRadioLabel = Label(scaleRadioFrame, text="Select scale to tune to: ")
    scaleRadioLabel.pack(anchor=W)

    scaleRadios = [Radiobutton(scaleRadioFrame, text=f'{n} Maj. scale',variable=scaleVar, value=i+1) for i,n in enumerate(notes)]
    for r in scaleRadios: r.pack(anchor=W)


    # Note checkbuttons
    noteButtonsFrame = Frame(root, borderwidth=10)

    noteButtonsLabel = Label(noteButtonsFrame, text="Select note(s) to tune to: ")
    noteButtonsLabel.pack(anchor=W)

    noteButtons = [Checkbutton(noteButtonsFrame, text=n, variable=noteVars[i], onvalue=1, offvalue=0) for i,n in enumerate(notes)]
    for n in noteButtons: n.pack(anchor=W)

    root.mainloop()

if __name__ == "__main__": main()
