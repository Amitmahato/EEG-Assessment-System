Electroencephalogram is a type of brain computer interface.
Fast Fourier Transform (FFT) to decompose the set of data to be transformed into a series of smaller data sets, 
obtain data in frequency domain.
Electric signal slicing at 50Hz- to remove noise due to grounding and electrical interference
Power of each frequency range calculated.

Classification required relative power of the characteristics wave, calculated by squaring the amplitude of the Fourier transform.
total of rhythmic characteristics declared as rhythmic power.
Channels with the rhythmic percentage) less than 10% labelled as bad channels i.e. no adequate information of rhythmic content
Rhythmic and Artifact (noise) values used as axes for  SVM classifier. 
Plotted the obtained data along with label used, observed linearly separable distribution of the classes of data.
Used linear kernel for the SVM classifier.
Opted for the value C=2^50 as the misclassification cost
3D-model synthesis focused on 16 main electrodes.
Fourier transformed again, gave amplitude of the signal at various voltages.
Calculated the total voltage of the signal in alpha, beta and delta range for each second and normalized with known standard voltage.
Voltages greater than 1 were cut off at 1, negative values were also cutoff for clean color data.
Color codes for alpha, beta, and delta :Red, Green and Blue. 
Data was kept in 3D array to display in the rendering engine


Used python-tkinter for building GUI interface. The GUI interface is OS dependent and originally built on windows so might not work as expected on linux distro/other os.

The documents here are our experiences you may not get same results.
the data should be kept in "EDFdata" folder in data
the pt files or te files from the hospital should be kept in the cheats Directory in the same folder
