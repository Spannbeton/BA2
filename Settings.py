class Settings:
    def __init__(self):
        self.parentdir='C:/Users/Shadow/Desktop/Bachelorarbeit'
        #FFT needs 2^N in each coordinate, Default 0 in Z
        self.sampling_FFT_N=[4,4,0] #used for sampling the result or optical plane
        self.sampling_spectral_N=16
        self.image_coordinates=[0,0,0.3]
        self.image_samplingarea=[[-0.0000025,0.0000025],[-0.0000025,0.0000025],[0,0]]
        self.plotting_angles=[90,90] #plotting elevation angles, azimuth [90,90] for top down view


