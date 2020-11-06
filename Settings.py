class Settings:
    def __init__(self):
        self.parentdir='C:/Users/Shadow/Desktop/Bachelorarbeit'
        #FFT needs 2^N in each coordinate, Default 0 in Z
        self.sampling_FFT_N=[4,4,0] #used for sampling the result or optical plane
        self.sampling_spectral_N=2
        self.image_coordinates=[0,0,0.7]
        self.image_samplingarea=[[-0.0015,0.0015],[-0.0015,0.0015],[0,0]]
        self.plotting_angles=[30,30] #plotting elevation angles, azimuth [90,90] for top down view


