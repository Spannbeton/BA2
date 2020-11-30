from sympy import sympify

class OpticalElementData:
    #initialize
    def __init__(self):
        pass
    #Variables
    oe_transmissionfunction="exp(1j*sin(3e8*x/650e-9))"#"exp(-1j*3.14159*x*0.60/(l))"#
    #Coordinates of Optical Element
    oe_coordinates=[0,0,0.01]
    #Area that should be sampled (geometry) Default only x,y values needed, z for further upgrades
    oe_samplingarea=[[-0.01,0.01],[-0.01,0.01],[0,0]]
    def calculate(self):
        self.oe_transmissionfunction_sympify=sympify(self.oe_transmissionfunction)



