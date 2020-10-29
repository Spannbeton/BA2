from sympy import sympify

class OpticalElementData:
    #initialize
    def __init__(self):
        pass
    #Variables
    oe_transmissionfunction=1#"sin(x)*sin(y)/(x*y)"
    #Coordinates of Optical Element
    oe_coordinates=[0,0,0.5]
    #Area that should be sampled (geometry) Default only x,y values needed, z for further upgrades
    oe_samplingarea=[[-0.000005,0.000005],[-0.000005,0.000005],[0,0]]
    def calculate(self):
        self.oe_transmissionfunction_sympify=sympify(self.oe_transmissionfunction)



