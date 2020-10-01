from Calculation import Calculation
from SourceData import SourceData
from OpticalElementData import OpticalElementData
from Settings import Settings
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from GUI import GUI
g=GUI()
'''
def browseFiles():
    calc.Settings.parentdir = filedialog.askdirectory(initialdir=calc.Settings.parentdir,title="Select a File")

    print(calc.Settings.parentdir)
    parentdir.set(calc.Settings.parentdir)
    root.update()


#initiate
sd=SourceData()
sd.source_samplingarea=[400e-9,720e-9] #400 to 720 nm
oe=OpticalElementData()
se=Settings()
calc=Calculation(sd,oe,se)

#GUI Definition
root = tk.Tk()
root.title("Simulation")
root.geometry("500x300")
#define Tabs
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab1.geometry = root.geometry
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
#Add Tabs
tabControl.add(tab1, text='Calculation')
tabControl.add(tab2, text='Settings')
tabControl.add(tab3, text='Optical Element')
tabControl.add(tab4, text='Source')
tabControl.pack(expand=1, fill="both")
#Calculation Page
#Design and hook each Window
ttk.Label(tab1,text="Folders").grid(column=0,row=0,padx=10,pady=10)
ttk.Label(tab1,text="Beam Propagation",borderwidth=1).grid(column=1,row=0,padx=10,pady=10)
ttk.Button(tab1,text="Read Data").grid(column=0,row=3,padx=10,pady=10)
ttk.Button(tab1,text="Select").grid(column=1,row=3,padx=10,pady=10)


#Progressbar
#Farbe und text vom Status abhängig machen,länge relativ
progressbar_text=ttk.Label(tab1,text="Progressbartext")
progressbar_text.grid(column=0,row=5,columnspan=2)
progressbar=ttk.Progressbar(tab1,mode="determinate")
progressbar.grid(column=0,row=6,columnspan=2)

#Settings Page
ttk.Label(tab2,text="Save & Plot:", font = ('Arial',20)).grid(column=0,row=0,pady=5)
ttk.Label(tab2,text="Directory", font = ('Arial'), anchor='w').grid(column=0,row=1,pady=5)
parentdir=tk.StringVar()
parentdir.set(calc.Settings.parentdir)
ttk.Label(tab2,text=parentdir.get(), font = ('Arial',8)).grid(column=1,row=1,padx=5,pady=5)
ttk.Button(tab2,text="Change",command=lambda:browseFiles()).grid(column=2,row=1,padx=5,pady=5)


root.mainloop()





sd=SourceData()
sd.source_samplingarea=[400e-9,720e-9] #400 to 720 nm
oe=OpticalElementData()
se=Settings()
calc=Calculation(sd,oe,se)
calc.Calculation()
calc.Plot_All_SaveAll()
'''