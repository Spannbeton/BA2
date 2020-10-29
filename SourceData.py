from sympy import sympify

class SourceData:
    #initialize
    def __init__(self):
        pass
    #Variables
    #Spectral function
    source_spectrum=4#"1/(2e-9*sqrt(6.28))*exp(-(1/2)*((x-650e-9)/2e-9)**2)*10**-8" #x means lambda

    #Samplingarea of spectral function (interval)
    source_samplingarea=[640e-9,660e-9]
    #Beam Radius of source in m
    source_beam_radius=0.001
    #Radius of Curvature in m
    source_curvature_radius=100
    #coordinates (defaults to 0,0,0), needed for further upgrades
    source_coordinates=[0,0,0]

    def calculate(self):
        #String to calculatable function
        self.source_spectrum_sympify=sympify(self.source_spectrum)







