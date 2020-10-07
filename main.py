from Calculation import Calculation
from SourceData import SourceData
from OpticalElementData import OpticalElementData
from Settings import Settings
from Calculation import Calculation
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from GUI import GUI
#g=GUI()

sd=SourceData()
sd.source_samplingarea=[400e-9,720e-9] #400 to 720 nm
oe=OpticalElementData()
se=Settings()
calc=Calculation(sd,oe,se)
calc.Calculation()
calc.Plot_All_SaveAll()
F=calc.calc_Eopt_lambda_xy[0,:,:]
print(F)