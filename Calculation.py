import sympy
import numpy
import os #operating system
#time
import time
from time import strftime
#plotting
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#threading
import threading
#my classes
from SourceData import SourceData
from OpticalElementData import OpticalElementData
from Settings import Settings
#saving data
import pickle


class Calculation:
    def __init__(self, SourceData, OpticalElementData, Settings):
        # initialise the instances
        SourceData.calculate()
        OpticalElementData.calculate()
        #Save the instances
        self.SourceData=SourceData
        self.OpticalElementData=OpticalElementData
        self.Settings=Settings
        #Lambda sampling step
        self.d_lambda_step=(SourceData.source_samplingarea[1]-SourceData.source_samplingarea[0])/(Settings.sampling_spectral_N-1)
        #x,y sampling step in accordance with FFT Restrictions in Resultplane
        self.d_x_step_RES=(self.Settings.image_samplingarea[0][1]-self.Settings.image_samplingarea[0][0])/(2**Settings.sampling_FFT_N[0]-1)
        self.d_y_step_RES=(self.Settings.image_samplingarea[1][1]-self.Settings.image_samplingarea[1][0])/(2**Settings.sampling_FFT_N[1]-1)
        self.d_x_step_OPT=(self.OpticalElementData.oe_samplingarea[0][1]-OpticalElementData.oe_samplingarea[0][0])/(2**Settings.sampling_FFT_N[0]-1)
        self.d_y_step_OPT=(self.OpticalElementData.oe_samplingarea[1][1]-self.OpticalElementData.oe_samplingarea[1][0])/(2**Settings.sampling_FFT_N[1]-1)
        #Initiate Arrays
        self.calc_sampling_lambda=[None]*self.Settings.sampling_spectral_N #Wavelengths sampled
        self.calc_sampling_offsets=[None]*self.Settings.sampling_spectral_N #Offsets
        self.calc_sampling_waistrad=[None]*self.Settings.sampling_spectral_N #Waistrads
        self.calc_sampling_E0=[None]*self.Settings.sampling_spectral_N #Field of Wavelength
        self.calc_Eopt_lambda_xy=numpy.zeros(([Settings.sampling_spectral_N, 2 ** Settings.sampling_FFT_N[0], 2 ** Settings.sampling_FFT_N[1]]), dtype=complex) #optical Field
        self.calc_transmission_lambda_xy=numpy.zeros(([Settings.sampling_spectral_N, 2 ** Settings.sampling_FFT_N[0], 2 ** Settings.sampling_FFT_N[1]]), dtype=complex)#transmission Matrix
        self.calc_Eres_lambda_xy=numpy.zeros(([Settings.sampling_spectral_N, 2 ** Settings.sampling_FFT_N[0], 2 ** Settings.sampling_FFT_N[1]]), dtype=complex) #result Field
        self.calc_CoordsOPT_lambda_xy=numpy.zeros(([Settings.sampling_spectral_N, 2 ** Settings.sampling_FFT_N[0], 2 ** Settings.sampling_FFT_N[1],2]), dtype=float)#coords optical
        self.calc_CoordsRES_lambda_xy = numpy.zeros(([Settings.sampling_spectral_N, 2 ** Settings.sampling_FFT_N[0], 2 ** Settings.sampling_FFT_N[1],2]),dtype=float)#coords res
        self.calc_IntensityResult=numpy.zeros([2 ** Settings.sampling_FFT_N[0], 2 ** Settings.sampling_FFT_N[1]]) #Resulting Intensity after coherence 0=Opt 1=Res
        self.calc_Data=[]



    def CreateFolder(self):
        "Create Folders to save data. Path defined in Settings"
        self.Directory=self.Settings.parentdir+'/'+strftime("%d_%m_%Y_%H%M")
        try:
            os.mkdir(self.Directory)
            os.mkdir(self.Directory +"/Intensity_OPT/")
            os.mkdir(self.Directory +"/Intensity_RES/")
            os.mkdir(self.Directory +"/Beam Propagation/")
            os.mkdir(self.Directory + "/Data/")
        except: #For the case that folder already exists
            print("Directory already exists")

    def Plot_Spectrum(self):
        "Plot the Spectrum in sampled Interval"
        fig=plt.figure()
        plt.title("Spectrum")
        plt.xlabel("Wavelength(m)")
        plt.ylabel("abs(Field)")
        absE=[abs(i) for i in self.calc_sampling_E0]
        plt.plot(self.calc_sampling_lambda,absE)
        try:
            plt.savefig(self.Directory+"/Spectrum.png")
        except:
            self.CreateFolder()
            plt.savefig(self.Directory)
        plt.close(fig)

    def Plot_Intensity(self,wavelength,OptOrRes):
        'Plots Intensity for a wavelength as iterator and opt=1/res=0 as bool'
        start=time.time()
        l=wavelength
        x=[]
        y=[]
        z=[]
        E=[]
        for m in range(0, 2 ** self.Settings.sampling_FFT_N[0]):
            # loop y
            for n in range(0, 2 ** self.Settings.sampling_FFT_N[1]):
                if OptOrRes:
                    x.append(self.calc_CoordsOPT_lambda_xy[l][m][n][0])
                    y.append(self.calc_CoordsOPT_lambda_xy[l][m][n][1])
                    F=self.calc_Eopt_lambda_xy[l][m][n]
                    E.append(F)
                    z.append(numpy.real(F*numpy.conjugate(F)))

                elif OptOrRes==False:
                    x.append(self.calc_CoordsRES_lambda_xy[l][m][n][0])
                    y.append(self.calc_CoordsRES_lambda_xy[l][m][n][1])
                    F=self.calc_Eres_lambda_xy[l][m][n]
                    E.append(F)
                    z.append(numpy.real(F * numpy.conjugate(F)))
        z=numpy.array(z)
        fig = plt.figure()
        ax = Axes3D(fig,elev=self.Settings.plotting_angles[0],azim=self.Settings.plotting_angles[1])
        ax.set_title("Intensity for Wavelenghth"+ str(l))
        ax.set_xlabel('x-axis (cm)', fontweight='bold')
        ax.set_ylabel('y-axis (cm)', fontweight='bold')
        ax.set_zlabel('Intensity', fontweight='bold')
        ax.plot_trisurf([xi*100 for xi in x],[yi*100 for yi in y],z,cmap=cm.jet)

        try:
            path = self.Directory + ("/Intensity_OPT/" if OptOrRes else "/Intensity_RES/") + str(self.calc_sampling_lambda[l] * 10 ** 9)
            plt.savefig(path+"nm.png")
        except:
            self.CreateFolder()
            path = self.Directory + ("/Intensity_OPT/" if OptOrRes else "/Intensity_RES/") + str(self.calc_sampling_lambda[l] * 10 ** 9)
            plt.savefig(path+"nm.png")
        plt.close(fig)
        #Also save Raw Data to file
        file = open(path+"nm.txt","w+")
        content = []
        content.append("Intensity Vectors for wavelength "+str(self.calc_sampling_lambda[l]*10**9)+"nm in "+("optical plane" if OptOrRes else "result plane"))
        content.append("\nVector Format [x,y,Field,Intensity]")
        for i in range(len(x)):
            content.append("\n"+str([x[i],5,y[i],round(E[i],2),round(z[i],2)]))
        file.writelines(content)
        file.close()
        end=time.time()
        print(end-start)

    def Plot_Beams(self,wavelength):
        "Plot beam propagation in profile"
        fig = plt.figure()
        axes= fig.add_axes([0.2,0.1,0.8,0.8]) #x is z axis, y is Radius
        zlim=[min(-0.1,self.SourceData.source_coordinates[2])*1.1,max(self.Settings.image_coordinates[2],self.OpticalElementData.oe_coordinates[2],0)*1.1]
        axes.set_xlim(zlim)
        plt.title("Beam Propagation for \u03BB="+str(round(self.calc_sampling_lambda[wavelength]*10**9,2))+" nm \n \u03C9_0="+str(round(self.calc_sampling_waistrad[wavelength]*1000,2))+"mm @z="+str(round(self.calc_sampling_offsets[wavelength][2]*100,2))+"cm")
        plt.xlabel("z-Axis (m)")
        plt.ylabel("Beam width (cm)")
        plt.axvline(self.SourceData.source_coordinates[2] ,label="Source",linewidth=4,color="Red")
        #plt.text(self.SourceData.source_coordinates[2],0,"Source")
        plt.axvline(self.calc_sampling_offsets[wavelength][2], label="Waist of Beam",linestyle=":",linewidth=2)
        #plt.text(self.calc_sampling_offsets[wavelength][2],0,"Waist")
        plt.axvline(self.OpticalElementData.oe_coordinates[2], label="Optical plane",linestyle="--")
        #plt.text(self.OpticalElementData.oe_coordinates[2], 0, "Optical plane")
        plt.axvline(self.Settings.image_coordinates[2], label="Result plane",linewidth=4)
        #plt.text(self.Settings.image_coordinates[2],0,"Result plane")
        #Add hyperbolic function for the beam
        z_1 = numpy.linspace(self.SourceData.source_coordinates[2], self.OpticalElementData.oe_coordinates[2],50) #50 from source to optical
        z_2 = numpy.linspace(self.OpticalElementData.oe_coordinates[2], self.Settings.image_coordinates[2],50) # 50 from optical to image
        Z_r = numpy.pi * self.calc_sampling_waistrad[wavelength] ** 2 / self.calc_sampling_lambda[wavelength]
        wz = lambda z: 100*self.calc_sampling_waistrad[wavelength]*(1+((z-self.calc_sampling_offsets[wavelength][2])/Z_r)**2)**0.5

        radii_1=[wz(k) for k in z_1]
        radii_2=[wz(k) for k in z_2]
        #to optical plane
        plt.plot(z_1,radii_1,color="Black",linewidth=2,label="Envelope")#upper
        plt.plot(z_1,[-k for k in radii_1],color="Black",linewidth=2)#lower
        #to resultplane
        plt.plot(z_2,radii_2,color="Black",linestyle="dashdot",linewidth=2,label="theor. envelope")#upper
        plt.plot(z_2,[-k for k in radii_2],color="Black",linestyle="dashdot",linewidth=2)#lower
        axes.legend()
        #save to Folder
        path=self.Directory +"/Beam Propagation/"+str(self.calc_sampling_lambda[wavelength]*10**9)+"nm.png"
        try:
            plt.savefig(path)
        except:
            self.CreateFolder()
            plt.savefig(path)
        plt.close(fig)

    def SaveInputData(self):
        "Save the input data to file"
        file=open(self.Directory+"/InputData.txt","w+")
        content=[]
        content.append("Source @z="+str(self.SourceData.source_coordinates[2])+" meters")
        content.append("\nSpectrum function: "+str(self.SourceData.source_spectrum))
        content.append("\nSampled Interval: "+str(self.SourceData.source_samplingarea)+" meters")
        content.append("\nwith "+str(self.Settings.sampling_spectral_N)+" equidistant Points and a step of "+str(self.d_lambda_step)+" meters")
        content.append("\n\nGaussian Beam:")
        content.append("\nBeam radius at Source: "+str(self.SourceData.source_beam_radius) +" meters")
        content.append("\nBeam curvature Radius: " +str(self.SourceData.source_curvature_radius) + " meters")
        content.append("\n\nOptical Element @z="+str(self.OpticalElementData.oe_coordinates[2])+ " meters")
        content.append("\nSampled in x Interval of "+str(self.OpticalElementData.oe_samplingarea[0])+" meters")
        content.append("\nwith "+str(2**self.Settings.sampling_FFT_N[0])+" equidistant Points and a step of "+ str(self.d_x_step_OPT)+" meters")
        content.append("\nSampled in y Interval of "+str(self.OpticalElementData.oe_samplingarea[1])+" meters")
        content.append("\nwith "+str(2 ** self.Settings.sampling_FFT_N[1])+" equidistant Points and a step of "+str(self.d_y_step_OPT)+" meters")
        content.append("\nTransmission function: "+str(self.OpticalElementData.oe_transmissionfunction))
        content.append(("\n\nResult plane @z="+str(self.Settings.image_coordinates[2])+" meters"))
        content.append("\nSampled in x Interval of "+str(self.OpticalElementData.oe_samplingarea[0])+" meters")
        content.append("\nwith "+str(2**self.Settings.sampling_FFT_N[0])+" equidistant Points and a step of "+ str(self.d_x_step_RES)+" meters")
        content.append("\nSampled in y Interval of "+str(self.OpticalElementData.oe_samplingarea[1])+" meters")
        content.append("\nwith "+str(2 ** self.Settings.sampling_FFT_N[1])+" equidistant Points and a step of "+str(self.d_y_step_RES)+" meters")
        file.writelines(content)
        file.close()

    def Calculate_z_offset(self,wavelength):#as iterator
        "wavelength as iterator"
        #get wavelength
        '''
        l=self.calc_sampling_lambda[wavelength]
        R=self.SourceData.source_curvature_radius
        W=self.SourceData.source_beam_radius
        res=R/((1+(numpy.pi*(W**2)/(l*R))**-2)**0.5)
        '''
        res=10
        return res

    def Calculate_Waistrad(self,wavelength):#as iterator
        "wavelength as iterator"
        #get wavelength
        '''
        l=self.calc_sampling_lambda[wavelength]
        R=self.SourceData.source_curvature_radius
        W=self.SourceData.source_beam_radius
        res=W/((1+(l*R/(numpy.pi*(W**2)))**-2)**0.5)
        '''
        res=0.01
        return res

    def Calculate_Field(self,wavelength,x,y):#wavelength as iterator, x,y as value
        "Calculate the Field in optical plane at x,y"
        l=self.calc_sampling_lambda[wavelength]
        E_0=self.calc_sampling_E0[wavelength]
        W_0=self.calc_sampling_waistrad[wavelength]
        z = OpticalElementData.oe_coordinates[2] - self.calc_sampling_offsets[wavelength][2]
        k=(2*numpy.pi)/l
        res=0
        #if within area of optical element, otherwise set field to 0
        if True: #(x>=self.OpticalElementData.oe_samplingarea[0][0] and x <=self.OpticalElementData.oe_samplingarea[0][1] and y>=self.OpticalElementData.oe_samplingarea[1][0] and y<=self.OpticalElementData.oe_samplingarea[1][1]):
            frac=(1/complex(1+2j*z/(k*E_0**2)))
            e1=(E_0*(numpy.exp(1j*k*z))*frac)
            e2=numpy.exp(-((y**2)*frac)/(W_0**2))
            e3=numpy.exp(-((x**2)*frac)/(W_0**2))
            e4=(E_0*(numpy.exp(1j*k*z))*frac)*numpy.exp(-((x**2+y**2)*frac)/(W_0**2))
            res= complex(e4)
        return res

    def Calculate_for_Wavelength(self, wavelength):
        print("Starting calculation")
        "Calculates Fields for both planes and writes into Data"
        #coherence length
        L=self.SourceData.source_coherencelength
        #scaling factor
        C=1
        i=wavelength
        #distances
        dist_source_opt=self.OpticalElementData.oe_coordinates[2]
        dist_opt_im = self.Settings.image_coordinates[2] - self.OpticalElementData.oe_coordinates[2]
        # Sample the Intensity function
        # Get Lambda
        la=self.SourceData.source_samplingarea[0] + self.d_lambda_step * i
        self.calc_sampling_lambda[i]=la
        # Offsets
        self.calc_sampling_offsets[i]=[0, 0, self.Calculate_z_offset(i)]
        # Waistrad
        self.calc_sampling_waistrad[i]=self.Calculate_Waistrad(i)
        # E_0(lambda) Field of Wavelengths
        self.calc_sampling_E0[i]=self.SourceData.source_spectrum_sympify.subs("x", self.calc_sampling_lambda[i])
        # loop x
        for m in range(0, 2 ** self.Settings.sampling_FFT_N[0]):
            # loop y
            for n in range(0, 2 ** self.Settings.sampling_FFT_N[1]):
                # Calculate coordinates in optical and result plane
                self.calc_CoordsOPT_lambda_xy[i][m][n][0]=self.OpticalElementData.oe_samplingarea[0][0] + self.d_x_step_OPT * m #x
                self.calc_CoordsOPT_lambda_xy[i][m][n][1]=self.OpticalElementData.oe_samplingarea[1][0] + self.d_y_step_OPT * n #y
                self.calc_CoordsRES_lambda_xy[i][m][n][0]=self.Settings.image_samplingarea[0][0] + self.d_x_step_RES * m #x
                self.calc_CoordsRES_lambda_xy[i][m][n][1]=self.Settings.image_samplingarea[1][0] + self.d_y_step_RES * n #y
                # Calculate E(x,y,z_optic) in optical plane for each wavelength
                self.calc_Eopt_lambda_xy[i,m,n]=self.Calculate_Field(i,self.calc_CoordsOPT_lambda_xy[i][m][n][0],self.calc_CoordsOPT_lambda_xy[i][m][n][1])
        #calculate E in resultplane
        #Calculate resulting Field
        print("calculating E_res")
        phaseshift= lambda l,x,u,y,v:numpy.exp((2j*numpy.pi/l)*((x-u)**2+(y-v)**2)**0.5)
        coherencefactor=lambda l,x,u,y,v:numpy.exp(-((x-u)**2+(y-v)**2)/L**2)

        #Transmission Matrix
        for m in range(0, 2 ** self.Settings.sampling_FFT_N[0]):
            for n in range(0, 2 ** self.Settings.sampling_FFT_N[1]):
                x=self.calc_CoordsOPT_lambda_xy[i][m][n][0]
                y=self.calc_CoordsOPT_lambda_xy[i][m][n][1]
                self.calc_transmission_lambda_xy[i][m][n]=self.OpticalElementData.oe_transmissionfunction_sympify.subs((["x",x],["l",la],["y",y]),evaluate=True)
        #calculate Results for each xy
        for u_i in range(0, 2 ** self.Settings.sampling_FFT_N[0]):

            for v_i in range(0, 2 ** self.Settings.sampling_FFT_N[1]):
                u = self.calc_CoordsRES_lambda_xy[i][u_i][v_i][0]
                v = self.calc_CoordsRES_lambda_xy[i][u_i][v_i][1]
                res=0
                for x_i in range(0, 2 ** self.Settings.sampling_FFT_N[0]):
                # loop y
                    for y_i in range(0, 2 ** self.Settings.sampling_FFT_N[1]):
                        x = self.calc_CoordsOPT_lambda_xy[i][x_i][y_i][0]
                        y = self.calc_CoordsOPT_lambda_xy[i][x_i][y_i][1]
                        ps = phaseshift(la, y, v, x, u)
                        cf=coherencefactor(la, y, v, x, u)
                        trami=self.calc_transmission_lambda_xy[i][x_i][y_i]
                        res+=C*numpy.fft.fftn(self.calc_Eopt_lambda_xy[i,x_i,y_i]*self.calc_transmission_lambda_xy[i][x_i][y_i]*ps*cf)
                        k=""
                        # maybe also put coherence constant here
                self.calc_Eres_lambda_xy[i][u_i][v_i]=res

    def Calculate_Result(self):
        "Calculate & plot for all Wavelengths as a whole"
        #Select according field
        E=self.calc_Eres_lambda_xy
        #Have a look at temporal and spacial dimensions to make a decision
        x=[]
        y=[]
        z=[]
        for n in range(2 ** self.Settings.sampling_FFT_N[0]):#loop x
            for m in range(2 ** self.Settings.sampling_FFT_N[1]):#loop y
                for i in range(self.Settings.sampling_spectral_N):
                    # no coherence
                    self.calc_IntensityResult[n,m]+= numpy.real(E[i,n,m]*numpy.complex.conjugate(E[i,n,m]))
                # get coordinates
                x.append(self.Settings.image_samplingarea[0][0] + self.d_x_step_RES * n)
                y.append(self.Settings.image_samplingarea[1][0] + self.d_y_step_RES * m)
                z.append(self.calc_IntensityResult[n,m])
        #plot and give out
        fig = plt.figure()
        ax = Axes3D(fig,elev=self.Settings.plotting_angles[0],azim=self.Settings.plotting_angles[1])
        ax.set_title("Resulting Intensity in result plane")
        ax.set_xlabel('x-axis (cm)', fontweight='bold')
        ax.set_ylabel('y-axis (cm)', fontweight='bold')
        ax.set_zlabel('Intensity', fontweight='bold')
        ax.plot_trisurf([xi*100 for xi in x], [yi*100 for yi in y], z,cmap=cm.jet)

        try:
            plt.savefig(self.Directory+"/Result.png")
        except:
            self.CreateFolder()
            plt.savefig(self.Directory+"/Result.png")
        plt.close(fig)
        #Also save Raw Data to file
        file = open(self.Directory+"/Result.txt","w+")
        content = []
        content.append("Resulting Intensity Vectors in result plane")
        content.append("\nVector Format [x,y,Intensity]")
        for i in range(len(x)):
            content.append("\n"+str([x[i],y[i],z[i]]))
        file.writelines(content)
        file.close()

    def Calculation(self):
        "Main Calculation Function-Legacy Console based version"
        start = time.time()
        p=[]
        for i in range (0,self.Settings.sampling_spectral_N):
            p.append(threading.Thread(target=self.Calculate_for_Wavelength,args=(i,)))
            p[i].start()
        [pi.join() for pi in p]
        end = time.time()
        print("Calculation done in "+str(end-start))


    def Plot_All_SaveAll(self):
        "Main Plotting function-Legacy Console based version"
        self.CreateFolder()
        p=[]
        for i in range(0, self.Settings.sampling_spectral_N):
            print("Plotting "+str(self.calc_sampling_lambda[i]*10**9)+"nm")
            #plot Optical
            self.Plot_Intensity(i,True)
            #plot Result
            self.Plot_Intensity(i, False)
            # Create Beamplots
            self.Plot_Beams(i)
        # Plot Spectrum
        print("Plotting Spectrum")
        self.Plot_Spectrum()
        # Save Data
        print("Saving Data")
        self.SaveInputData()
        self.Save_Data()
        print("Calculating Result")

    def Save_Data(self):
        "Save SourceData,OpticalElementData,Settings"
        try:
            path=self.Directory+"/Data"
        except:
            self.CreateFolder()
            path = self.Directory + "/Data"
        datafile = open(path+"/SaveData.obj","wb+")
        pickle.dump([self.SourceData,self.OpticalElementData,self.Settings], datafile)

    def Load_Data(self,path):
        "Load SourceData,OpticalElementData,Settings from file -Legacy Console based version"
        datafile = open(path, 'rb')
        Data = pickle.load(datafile)
        self.SourceData=Data[0]
        self.OpticalElementData=Data[1]
        self.Settings=Data[2]




