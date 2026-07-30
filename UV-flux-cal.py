# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:30:53 2023

@author: ccsarver
"""
import matplotlib.pyplot as plt

doublebonds_lit=[0,0.060569018,0.09298882,0.11836249,0.12601373,0.13067566]
xdata_lit=[0,20,30,40,50,60]
hundredwatts=[0,0.03256,0.04101,0.0471,0.052,0.0549,0.0566,0.0603,0.062,0.0629,0.0647,0.0662,0.0682,0.0692,0.0703,0.0729,0.0754,0.0756,0.0756]
fiftywatts=[0,0.01774,0.02628,0.032,0.0366,0.0429,0.0452,0.0479,0.0506,0.0527,0.0536,0.053,0.0509,0.0483,0.0401,0.046,0.0691,0.0768,0.0813]
irr_time=[0,5,10,17,21,25,30,35,40,45,50,55,60,70,80,90,100,110,120]
plt.plot(xdata_lit,doublebonds_lit,marker='o',color='blue')
plt.plot(irr_time,hundredwatts,marker='o',color='green')
plt.plot(irr_time,fiftywatts,marker='o',color='black')
#intensity4=np.asarray(intensity3)/(247*(1e-7)*126)
plt.xlabel('Irradiation Time (min)',size=15)
plt.ylabel('Integrated Absorbance 965 $cm^{-1}$',size=15)
plt.xticks(fontsize=17)
plt.yticks(fontsize=17)
plt.tick_params(length=10, width=2, which='major')
plt.ylim(0,0.14)


