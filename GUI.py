from Calculation import Calculation
from SourceData import SourceData
from OpticalElementData import OpticalElementData
from Settings import Settings
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class GUI:
    def __init__(self):
        # initiate
        sd = SourceData()
        oe = OpticalElementData()
        se = Settings()
        self.calc = Calculation(sd, oe, se)

        # GUI Definition
        self.root = tk.Tk()
        self.root.title("Simulation")
        self.root.geometry("500x300")
        # define Tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab1.geometry = self.root.geometry
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        # Add Tabs
        self.tabControl.add(self.tab1, text='Calculation')
        self.tabControl.add(self.tab2, text='Settings')
        self.tabControl.add(self.tab3, text='Optical Element')
        self.tabControl.add(self.tab4, text='Source')
        self.tabControl.pack(expand=1, fill="both")
        # Calculation Page
        # Design and hook each Window
        ttk.Label(self.tab1, text="Folders").grid(column=0, row=0, padx=10, pady=10)
        ttk.Label(self.tab1, text="Beam Propagation", borderwidth=1).grid(column=1, row=0, padx=10, pady=10)
        ttk.Button(self.tab1, text="Read Data").grid(column=0, row=3, padx=10, pady=10)
        ttk.Button(self.tab1, text="Select").grid(column=1, row=3, padx=10, pady=10)

        # Progressbar
        # Farbe und text vom Status abhängig machen,länge relativ
        self.progressbar_text = ttk.Label(self.tab1, text="Progressbartext")
        self.progressbar_text.grid(column=0, row=5, columnspan=2)
        self.progressbar = ttk.Progressbar(self.tab1, mode="determinate")
        self.progressbar.grid(column=0, row=6, columnspan=2)

        # Settings Page
        ttk.Label(self.tab2, text="Save & Plot:", font=('Arial', 20)).grid(column=0, row=0, pady=5,columnspan=2)
        ttk.Label(self.tab2, text="Directory", font=('Arial'), anchor='w').grid(column=0, row=1, pady=5)
        self.parentdir = tk.StringVar()
        self.parentdir.set(self.calc.Settings.parentdir)
        ttk.Label(self.tab2, textvariable=self.parentdir, font=('Arial', 8)).grid(column=1, row=1, padx=5, pady=5,columnspan=2)
        ttk.Button(self.tab2, text="Change", command=lambda: self.browseFiles()).grid(column=3, row=1, padx=5, pady=5)
        ttk.Label(self.tab2, text="Plotting angles (topdown: 90,90)", font=('Arial'), anchor='w').grid(column=0, row=2, pady=5,columnspan=3)
        ttk.Label(self.tab2,text="Elevation angle:").grid(column=0, row=3, pady=5)
        self.elev=tk.IntVar()
        self.elev.set(self.calc.Settings.plotting_angles[0])
        self.azimuth=tk.IntVar()
        self.azimuth.set(self.calc.Settings.plotting_angles[1])
        ttk.Entry(self.tab2,textvariable=self.elev).grid(column=1, row=3, pady=5)
        ttk.Label(self.tab2, text="Azimuth:").grid(column=2, row=3, pady=5)
        ttk.Entry(self.tab2, textvariable=self.azimuth).grid(column=3, row=3, pady=5)
        ttk.Label(self.tab2, text="Sampling:", font=('Arial', 20)).grid(column=0, row=4, pady=5, columnspan=2)
        #Combobox Which plane
        #FFT Sampling 2^x, 2^y with Entry
        #Lambdasampling with Entry
        #Samplingarea with Entry
        #z-koordinate with entry


        #main loop
        self.root.mainloop()

    def browseFiles(self):
        self.parentdir.set(filedialog.askdirectory(initialdir=self.calc.Settings.parentdir, title="Select a File"))
        print(self.parentdir.get())

    def ApplyChanges_Settings(self):
        self.calc.Settings.parentdir=self.parentdir.get()
        self.calc.Settings.plotting_angles[0]=self.elev.get()
        self.calc.Settings.plotting_angles[1]=self.azimuth.get()

