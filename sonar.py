# Vibracoes e Ondas
# Trabalho Experimental - SONAR
# Codigo base (sonar.py)
# Carlos Vinhais, Out 2020

import serial
import numpy as np
import matplotlib.pyplot as plt

# Serial port
ser = serial.Serial( 'com3', 9600 )

# Acquire N samples (data)
t_data = []
d_data = []

N = 150

n = 0
while (n < N):
    if ( ser.inWaiting() > 0 ):
        data = ser.readline()[:-2]
        t_ms, d_mm = data.split()
        #print (t_ms, d_mm)
        t_data.append( int(t_ms) )
        d_data.append( int(d_mm) )
        n += 1 

# SONAR DATA:
dados = np.c_[t_data, d_data]

# Save DATA to file
np.savetxt( "sonar_test.dat", dados, fmt='%d', delimiter=" ")

# -----------------------

# Load DATA from file
data = np.loadtxt( "sonar_test.dat", dtype=np.int, delimiter=" ")
time_ms = data[:,0]
dist_mm = data[:,1]
N = len( time_ms )

# Plot DATA
fig = plt.figure()
fig.add_subplot(1,1,1)
titulo = ("Sonar Data: N = %d points")%(N)
plt.title(titulo, fontsize=14 )
plt.xlabel('Time, t (ms)', fontsize=14 )
plt.ylabel('Distance, d (mm)', fontsize=14 )
plt.plot(time_ms, dist_mm, marker='.', linestyle='-', label="sonar data")
plt.axhline(y = np.mean(dist_mm), linewidth=1, linestyle='-' )
plt.axhline(y = 0, color="k", linewidth=1, linestyle='-' )
plt.legend()
plt.grid(True)
#plt.show()

# Save FIG to PNG file
outputFilename_png = "sonar_data.png"
plt.savefig( outputFilename_png, bbox_inches='tight')

# Save FIG to PDF file
outputFilename_pdf = "sonar_data.pdf"
plt.savefig( outputFilename_pdf, bbox_inches='tight')

plt.show()

# -----------------------
print ("EOF.")


