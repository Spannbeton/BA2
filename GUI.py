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
        self.root.geometry("1000x800")
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

        #Calculation
        ttk.Label(self.tab1, text="Calculation & Plotting:", font=('Arial', 20), anchor='w').grid(column=0, row=0, pady=20,columnspan=3)
        ttk.Button(self.tab1, text="Calculate", command=lambda:[self.calc.Calculation(),self.Plot_Button_enable()]).grid(column=0, row=1, padx=5, pady=5)
        # Progressbar Calculation
        ttk.Label(self.tab1, text="Progressbartext Calculation").grid(column=1, row=1)
        self.progressbar = ttk.Progressbar(self.tab1, mode="determinate")
        self.progressbar.grid(column=2, row=1, columnspan=2)

        #Plotting
        self.Plot_Button=ttk.Button(self.tab1, text="Plot", command=lambda:self.calc.Plot_All_SaveAll(),state=tk.DISABLED)
        self.Plot_Button.grid(column=0, row=2, padx=5, pady=5)
        # Progressbar Calculation
        ttk.Label(self.tab1, text="Progressbartext Plotting").grid(column=1, row=2)
        self.progressbar = ttk.Progressbar(self.tab1, mode="determinate")
        self.progressbar.grid(column=2, row=2, columnspan=2)

        # Settings Page
        ttk.Label(self.tab2, text="Save & Plot:", font=('Arial', 20), anchor='w').grid(column=0, row=0, pady=20,columnspan=3)
        ttk.Label(self.tab2, text="Directory", font=('Arial'), anchor='w').grid(column=0, row=1, pady=5)
        self.parentdir = tk.StringVar()
        self.parentdir.set(self.calc.Settings.parentdir)
        ttk.Label(self.tab2, textvariable=self.parentdir, font=('Arial', 8)).grid(column=1, row=1, padx=5, pady=5,columnspan=2)
        ttk.Button(self.tab2, text="Change", command=lambda: self.browseFiles()).grid(column=3, row=1, padx=5, pady=5)
        ttk.Label(self.tab2, text="Plotting angles (topdown: 90,90):", font=('Arial'), anchor='w').grid(column=0, row=2, pady=5,columnspan=3)
        ttk.Label(self.tab2,text="Elevation angle:").grid(column=0, row=3, pady=5)
        self.elev=tk.IntVar()
        self.elev.set(self.calc.Settings.plotting_angles[0])
        self.azimuth=tk.IntVar()
        self.azimuth.set(self.calc.Settings.plotting_angles[1])
        ttk.Entry(self.tab2,textvariable=self.elev).grid(column=1, row=3, pady=5)
        ttk.Label(self.tab2, text="Azimuth:").grid(column=2, row=3, pady=5)
        ttk.Entry(self.tab2, textvariable=self.azimuth).grid(column=3, row=3, pady=5)
        ttk.Label(self.tab2, text="Sampling:", font=('Arial', 20)).grid(column=0, row=4, pady=20, columnspan=2)
        ttk.Label(self.tab2, text="Which plane to sample:").grid(column=0, row=5, pady=5, columnspan=2) #Combobox Which plane
        self.Combobox_OptOrRes=ttk.Combobox(self.tab2,values=["result","optical"])
        self.Combobox_OptOrRes.grid(column=3,row=5,pady=5)
        self.Combobox_OptOrRes.current(int(self.calc.Settings.sampling_OptOrRes))
        # Samplingarea with Entry
        self.image_samplingarea_xstart=tk.DoubleVar()
        self.image_samplingarea_xend = tk.DoubleVar()
        self.image_samplingarea_ystart=tk.DoubleVar()
        self.image_samplingarea_yend = tk.DoubleVar()
        self.image_samplingarea_xstart.set(self.calc.Settings.image_samplingarea[0][0])
        self.image_samplingarea_xend.set(self.calc.Settings.image_samplingarea[0][1])
        self.image_samplingarea_ystart.set(self.calc.Settings.image_samplingarea[1][0])
        self.image_samplingarea_yend.set(self.calc.Settings.image_samplingarea[1][1])
        ttk.Label(self.tab2, text="Samplingarea resultplane:").grid(column=0, row=6, pady=5)
        ttk.Label(self.tab2, text="x from").grid(column=0, row=7, pady=5)
        ttk.Entry(self.tab2, textvariable=self.image_samplingarea_xstart).grid(column=1, row=7, pady=5)
        ttk.Label(self.tab2, text="to").grid(column=2, row=7, pady=5)
        ttk.Entry(self.tab2, textvariable=self.image_samplingarea_xend).grid(column=3, row=7, pady=5)
        ttk.Label(self.tab2, text="y from").grid(column=4, row=7, pady=5)
        ttk.Entry(self.tab2, textvariable=self.image_samplingarea_ystart).grid(column=5, row=7, pady=5)
        ttk.Label(self.tab2, text="to").grid(column=6, row=7, pady=5)
        ttk.Entry(self.tab2, textvariable=self.image_samplingarea_yend).grid(column=7, row=7, pady=5)
        # FFT Sampling 2^x, 2^y with Entry
        ttk.Label(self.tab2, text="Number of samplings (FFT conforming):").grid(column=0, row=8, pady=5, columnspan=2)
        self.FFT_Nx=tk.IntVar()
        self.FFT_Ny=tk.IntVar()
        self.FFT_Nx.set(self.calc.Settings.sampling_FFT_N[0])
        self.FFT_Ny.set(self.calc.Settings.sampling_FFT_N[1])
        ttk.Label(self.tab2, text="x=2^").grid(column=0, row=9, pady=5)
        ttk.Entry(self.tab2, textvariable=self.FFT_Nx).grid(column=1, row=9, pady=5)
        ttk.Label(self.tab2, text="y=2^").grid(column=3, row=9, pady=5)
        ttk.Entry(self.tab2, textvariable=self.FFT_Ny).grid(column=4, row=9, pady=5)
        #Lambdasampling with Entry
        self.sampling_lambda=tk.IntVar()
        self.sampling_lambda.set(self.calc.Settings.sampling_spectral_N)
        ttk.Label(self.tab2, text="Number of samplings for Wavelength:").grid(column=0, row=10, pady=5)
        ttk.Entry(self.tab2, textvariable=self.sampling_lambda).grid(column=1, row=10, pady=5)
        #z-koordinate with entry
        ttk.Label(self.tab2, text="z-coordinate of resultplane:").grid(column=0, row=11, pady=5)
        self.image_coordinates_z=tk.DoubleVar()
        self.image_coordinates_z.set(self.calc.Settings.image_coordinates[2])
        ttk.Entry(self.tab2, textvariable=self.image_coordinates_z).grid(column=1, row=11, pady=5)
        #apply button
        ttk.Button(self.tab2, text="Apply Settings", command=lambda: self.ApplyChanges_Settings()).grid( row=12, padx=5, pady=5,columnspan=7)

        #Optical Element Page
        #Sampling Area
        ttk.Label(self.tab3, text="Sampling:", font=('Arial', 20), anchor='w').grid(column=0, row=0, pady=20,columnspan=3)
        self.opt_samplingarea_xstart=tk.DoubleVar()
        self.opt_samplingarea_xend = tk.DoubleVar()
        self.opt_samplingarea_ystart=tk.DoubleVar()
        self.opt_samplingarea_yend = tk.DoubleVar()
        self.opt_samplingarea_xstart.set(self.calc.OpticalElementData.oe_samplingarea[0][0])
        self.opt_samplingarea_xend.set(self.calc.OpticalElementData.oe_samplingarea[0][1])
        self.opt_samplingarea_ystart.set(self.calc.OpticalElementData.oe_samplingarea[1][0])
        self.opt_samplingarea_yend.set(self.calc.OpticalElementData.oe_samplingarea[1][1])
        ttk.Label(self.tab3, text="Samplingarea optical plane:").grid(column=0, row=1, pady=5)
        ttk.Label(self.tab3, text="x from").grid(column=0, row=2, pady=5)
        ttk.Entry(self.tab3, textvariable=self.opt_samplingarea_xstart).grid(column=1, row=2, pady=5)
        ttk.Label(self.tab3, text="to").grid(column=2, row=2, pady=5)
        ttk.Entry(self.tab3, textvariable=self.opt_samplingarea_xend).grid(column=3, row=2, pady=5)
        ttk.Label(self.tab3, text="y from").grid(column=4, row=2, pady=5)
        ttk.Entry(self.tab3, textvariable=self.opt_samplingarea_ystart).grid(column=5, row=2, pady=5)
        ttk.Label(self.tab3, text="to").grid(column=6, row=2, pady=5)
        ttk.Entry(self.tab3, textvariable=self.opt_samplingarea_yend).grid(column=7, row=2, pady=5)
        #z-coordinate
        self.opt_coordinates_z=tk.DoubleVar()
        self.opt_coordinates_z.set(self.calc.OpticalElementData.oe_coordinates[2])
        ttk.Label(self.tab3, text="z-coordinate of optical plane:").grid(column=0, row=3, pady=5)
        ttk.Entry(self.tab3, textvariable=self.opt_coordinates_z).grid(column=1, row=4, pady=5)
        #Transmission
        ttk.Label(self.tab3, text="Transmission:", font=('Arial', 20), anchor='w').grid(column=0, row=5, pady=20,columnspan=3)
        ttk.Label(self.tab3, text="Transmissionfunction:").grid(column=0, row=6, pady=5)
        self.opt_transmission=tk.StringVar()
        self.opt_transmission.set(self.calc.OpticalElementData.oe_transmissionfunction)
        ttk.Entry(self.tab3, textvariable=self.opt_transmission,width=100).grid(column=1, row=7, pady=5,columnspan=7)
        #apply button
        ttk.Button(self.tab3, text="Apply Settings", command=lambda: self.ApplyChanges_OpticalElement()).grid( row=8, padx=5, pady=5,columnspan=7)

        #Source Page
        #Sampling
        #Sampling Area
        ttk.Label(self.tab4, text="Sampling:", font=('Arial', 20), anchor='w').grid(column=0, row=0, pady=20,columnspan=3)
        ttk.Label(self.tab4, text="Spectral function for wavelength as x:").grid(column=0, row=1, pady=5)
        self.source_spectralfunction=tk.StringVar()
        self.source_spectralfunction.set(self.calc.SourceData.source_spectrum)
        ttk.Entry(self.tab4, textvariable=self.source_spectralfunction, width=100).grid(column=1, row=2, pady=5, columnspan=7)
        ttk.Label(self.tab4, text="Sampling Interval from ").grid(column=0, row=3, pady=5)
        self.source_xstart=tk.DoubleVar()
        self.source_xend=tk.DoubleVar()
        self.source_xstart.set(self.calc.SourceData.source_samplingarea[0])
        self.source_xend.set(self.calc.SourceData.source_samplingarea[1])
        ttk.Entry(self.tab4, textvariable=self.source_xstart, width=10).grid(column=1, row=3, pady=5)
        ttk.Label(self.tab4, text="to").grid(column=2, row=3, pady=5)
        ttk.Entry(self.tab4, textvariable=self.source_xend, width=10).grid(column=3, row=3, pady=5)
        #Beam
        ttk.Label(self.tab4, text="Gaussian Beam", font=('Arial', 20), anchor='w').grid(column=0, row=4, pady=20,columnspan=3)
        self.source_Beam_radius=tk.DoubleVar()
        self.source_Beam_curveradius= tk.DoubleVar()
        self.source_Beam_radius.set(self.calc.SourceData.source_beam_radius)
        self.source_Beam_curveradius.set(self.calc.SourceData.source_curvature_radius)
        ttk.Label(self.tab4, text="Radius at Source (z=0):").grid(column=0, row=5, pady=5)
        ttk.Entry(self.tab4, textvariable=self.source_Beam_radius, width=10).grid(column=1, row=5, pady=5)
        ttk.Label(self.tab4, text="Curvature radius").grid(column=0, row=6, pady=5)
        ttk.Entry(self.tab4, textvariable=self.source_Beam_curveradius, width=10).grid(column=1, row=6, pady=5)
        #apply button
        ttk.Button(self.tab4, text="Apply Settings", command=lambda: self.ApplyChanges_Source()).grid( row=7, padx=5, pady=5,columnspan=7)



        #main loop
        self.root.mainloop()

    def browseFiles(self):
        self.parentdir.set(filedialog.askdirectory(initialdir=self.calc.Settings.parentdir, title="Select a File"))
        print(self.parentdir.get())

    def ApplyChanges_Settings(self):
        self.calc.Settings.parentdir=self.parentdir.get()
        self.calc.Settings.plotting_angles[0]=self.elev.get()
        self.calc.Settings.plotting_angles[1]=self.azimuth.get()
        self.calc.Settings.sampling_OptOrRes=False if self.Combobox_OptOrRes.get()=="result" else True
        self.calc.Settings.sampling_FFT_N[0]=self.FFT_Nx.get()
        self.calc.Settings.sampling_FFT_N[1]=self.FFT_Ny.get()
        self.calc.Settings.sampling_spectral_N=self.sampling_lambda.get()
        self.calc.Settings.image_samplingarea[0][0]=self.image_samplingarea_xstart.get()
        self.calc.Settings.image_samplingarea[0][1]=self.image_samplingarea_xend.get()
        self.calc.Settings.image_samplingarea[1][0]=self.image_samplingarea_ystart.get()
        self.calc.Settings.image_samplingarea[1][1]=self.image_samplingarea_yend.get()
        self.calc.Settings.image_coordinates[2]=self.image_coordinates_z.get()

    def ApplyChanges_OpticalElement(self):
        self.calc.OpticalElementData.oe_samplingarea[0][0]=self.opt_samplingarea_xstart.get()
        self.calc.OpticalElementData.oe_samplingarea[0][1]=self.opt_samplingarea_xend.get()
        self.calc.OpticalElementData.oe_samplingarea[1][0]=self.opt_samplingarea_ystart.get()
        self.calc.OpticalElementData.oe_samplingarea[1][1]=self.opt_samplingarea_yend.get()
        self.calc.OpticalElementData.oe_coordinates[2]=self.opt_coordinates_z
        self.calc.OpticalElementData.oe_transmissionfunction=self.opt_transmission.get()

    def ApplyChanges_Source(self):
        self.calc.SourceData.source_spectrum=self.source_spectralfunction.get()
        self.calc.SourceData.source_samplingarea[0]=self.source_xstart.get()
        self.calc.SourceData.source_samplingarea[1]=self.source_xend.get()
        self.calc.SourceData.source_beam_radius=self.source_Beam_radius.get()
        self.calc.SourceData.source_curvature_radius=self.source_Beam_curveradius.get()

    def Plot_Button_enable(self):
        self.Plot_Button['state'] = tk.NORMAL

