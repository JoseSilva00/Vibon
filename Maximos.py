

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

# Encontrar Maximos e Minimos

def FindPeakUtils(t, y):
    indexes = peakutils.indexes(y, thres=0.3, min_dist=10)
    t_maxs = t[indexes]
    y_maxs = y[indexes]
    return t_maxs, y_maxs

def func(t, a, b, c):
    return a*np.exp(-b*t) + c


t_maxs, y_maxs = FindPeakUtils(t, y)

popt, pcov = curve_fit (func, t_maxs, y_maxs)

t_exp = t
y_exp = func(t ,*popt)





diff_t_maxs = np.diff(t_maxs)

T_osc_avg = np.mean(diff_t_maxs)
T_osc_std = np.std(diff_t_maxs)
T_osc_inc = (T_osc_std/np.sqrt(len(diff_t_maxs)))
T_osc_rel = 100*(T_osc_inc/T_osc_avg)


num_peaks = len(t_maxs)
print ( 'number of peaks =', num_peaks )


titulo = 'Maximos = %i' % (num_peaks)
legendas = ['data', 'exp', 'picos']

fig = plt.figure()
fig.add_subplot(1,1,1)
plt.title( titulo, fontsize=14 )
plt.xlabel('Tempo, t (s)', fontsize=14 )
plt.ylabel('Amplitude, X (m)', fontsize=14 )
plt.plot(t, y, marker='', linestyle='-', label=legendas[0])
plt.scatter(t_maxs,y_maxs, 20, c='r', marker='o', label=legendas[2])

plt.plot(t_exp, y_exp, marker='', linestyle='-', label=legendas[1])


plt.axvline(x=0, linewidth=1, linestyle='-.', color='k')
plt.axhline(y=0, linewidth=1, linestyle='-', color='k')
#plt.axis([-10, 10, -1, 1])
plt.legend()
plt.grid(True)

outputFilename = "peaks.png"
print ( 'Writing: ' + outputFilename )
plt.savefig( outputFilename, bbox_inches='tight')
outputFilename_pdf = "peaks.pdf"
plt.savefig( outputFilename_pdf, bbox_inches='tight')

plt.show(True)



dados=np.c_[y_maxs, t_maxs]
np.savetxt( "sonarMAX.dat", dados, fmt='%.3f', delimiter="             ",header="Amplitude(m) , Tempo(s)")


f=open('sonarMAX.dat','a')
f.write("\n")
f.write("T_osc_avg (s) :")
np.savetxt(f, (T_osc_avg, ),fmt='%.3f')
f.write("Desvio padrão :")
np.savetxt(f, (T_osc_std, ),fmt='%.3f')
f.write("Incerteza :")
np.savetxt(f, (T_osc_inc, ),fmt='%.3f')
f.write("Incerteza relativa :")
np.savetxt(f, (T_osc_rel, ),fmt='%.3f')
f.close()
# ------------------------------------------------
print ('EOF.')


