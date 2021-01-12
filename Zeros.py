import numpy as np
import matplotlib.pyplot as plt
import peakutils
from scipy import signal
from scipy.optimize import curve_fit



pi = np.pi

# Load DATA from file
print("A LER: sonar_test.dat " )
data = np.loadtxt( "sonar_test.dat", dtype=np.int, delimiter=" ", skiprows=0)
time_ms = data[:,0]
dist_mm = data[:,1]


time_s = 0.001 * time_ms
dist_m = 0.001 * dist_mm
ampl_m = dist_m - np.mean (dist_m)

t = time_s
y = ampl_m
N = len( t )


diff_time_ms = np.diff(time_ms)

T_s_avg = np.mean(diff_time_ms)
T_s_std = np.std(diff_time_ms)
T_s_inc = (T_s_std/np.sqrt(len(diff_time_ms)))
T_s_rel = 100*(T_s_inc/T_s_avg)


f_s_avg = 1000/T_s_avg              #freq(Hz) amostragem, 1/periodo
f_s_inc = f_s_avg*(T_s_inc/T_s_avg)
f_s_rel = 100*(f_s_inc/f_s_avg)





zero_crossings = np.where(np.diff(np.signbit(y)))[0]
tc1 = t[zero_crossings]
yc1 = y[zero_crossings]
tc2 = t[zero_crossings + 1]
yc2 = y[zero_crossings + 1]

t_cross = tc1 + yc1*(tc2 - tc1)/(yc1 - yc2)
y_cross = 0.0*np.ones(len(t_cross))






titulo = 'Zeros' 
legendas = ['data', 'prev', 'next', 'cross']

fig = plt.figure()
fig.add_subplot(1,1,1)
plt.title( titulo, fontsize=14 )
plt.xlabel('Tempo, t (s)', fontsize=14 )
plt.ylabel('Amplitude, X (m)', fontsize=14 )
plt.plot(t, y, marker='', linestyle='-', label=legendas[0])
plt.scatter(tc1,yc1, 20, c='r', marker='o', label=legendas[1])
plt.scatter(tc2,yc2, 20, c='g', marker='o', label=legendas[2])
plt.scatter(t_cross,y_cross, 20, c='b', marker='o', label=legendas[3])
plt.axvline(x=0, linewidth=1, linestyle='-.', color='k')
plt.axhline(y=0, linewidth=1, linestyle='-', color='k')
plt.legend()
plt.grid(True)

outputFilename = "Zeros.png"
print ( 'Writing: ' + outputFilename )
plt.savefig( outputFilename, bbox_inches='tight')
outputFilename_pdf = "zeros.pdf"
plt.savefig( outputFilename_pdf, bbox_inches='tight')

plt.show(True)

a = [ 1,2,3,4,5,6,7,8,9,10,11,12,13,14]
dados=np.c_[a, t_cross]
np.savetxt( "sonarZEROS.dat", dados, fmt='%.3f', delimiter="             ",header="Zero nº , Tempo(s)")

f=open('sonarZEROS.dat','a')
f.write("\n")
f.write("Período (s) :")
np.savetxt(f, (1/f_s_avg, ),fmt='%.3f')
f.write("Incerteza :")
np.savetxt(f, (f_s_inc, ),fmt='%.3f')
f.write("Incerteza relativa :")
np.savetxt(f, (f_s_rel, ),fmt='%.3f')
f.close()