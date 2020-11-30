from sympy import sympify

class SourceData:
    #initialize
    def __init__(self):
        pass
    #Variables
    #Spectral function
    source_spectrum="100/(2e-9*sqrt(6.28))*exp(-(1/2)*((x-975e-9)/5e-9)**2)*10**-8" #x means lambda
    #Coherence Length
    source_coherencelength=1e-2 #4e-6 is about that of an LED
    #Samplingarea of spectral function (interval)
    source_samplingarea=[965e-9,985e-9]
    #Beam Radius of source in m
    source_beam_radius=0.01
    #Radius of Curvature in m
    source_waistrad=0.009
    #coordinates (defaults to 0,0,0), needed for further upgrades
    source_coordinates=[0,0,0]

    def calculate(self):
        #String to calculatable function
        self.source_spectrum_sympify=sympify(self.source_spectrum)







