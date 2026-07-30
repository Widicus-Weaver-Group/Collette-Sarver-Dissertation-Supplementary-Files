import os
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization import quantity_support
from spectral_cube import SpectralCube as sc
from astropy import units as u
from astropy.wcs import WCS
#from astropy.coordinates import SkyCoord
from astropy.wcs.utils import proj_plane_pixel_scales
from astropy.visualization.mpl_normalize import ImageNormalize
from astropy.visualization import SqrtStretch
from radio_beam import Beam
quantity_support()  # for getting units on the axes below
import matplotlib.pyplot 

### Load in RMS high resolution_line.fits csv file
rms=np.loadtxt('IRAS-RMS-HR.CSV',delimiter=',')

image_file = get_pkg_data_filename('IRAS-4B-hr-11_continuum.fits')


fits.info(image_file)
cont_image_data = fits.getdata(image_file, ext=0)
cube_file = 'IRAS-4B-hr-23_line.fits' # 

with fits.open(cube_file, ignore_missing_end=True) as hdu:
    del hdu[0].header['LINE']
    bmaj = hdu[0].header['BMAJ']
    bmin = hdu[0].header['BMIN']
    #print(hdu[0].header)
    cube = sc.read(hdu)
    im_data = hdu[0].data
    wcs = WCS(hdu[0])                                       # read the header info of the file
    fit_shape = cube.shape
    num_chan = fit_shape[0]
    wcs_updated = WCS(hdu[0]) # updated wcs with new CRPIX values
    # retrieve beam size from the header
    header = fits.getheader(cube_file)
    w = proj_plane_pixel_scales(wcs)                        # get pixel scales
    my_beam = Beam.from_fits_header(header)                 # get beam size from header
    #print(my_beam)
    px = w[0] * 3600  # take pixel scale, * 3600 to convert degrees to arcsec
    pixscale = px * u.arcsec

with fits.open('../../Moment-0-Maps-mult-emission/CH3OH-extended-6-26/CH3OH-6-26_average_mom0.fits') as hdum:
    im_data_m = (hdum[0].data)/1000
    vmax=round(im_data_m.max(),5) #in Jy/beam*km/s from the /1000 above, max flux value
    sigma=vmax #write in Jy/beam*km/s
    #vmin=round(3*np.mean([rms[17],rms[22]]),5)#SO2
    #vmin=round(3*np.mean([rms[7],rms[14]]),5)#H2CO
    #vmin=round(3*np.mean([rms[26],rms[27]]),5)#t-HCOOH
    #vmin=round(3*np.mean([rms[17],rms[17],rms[17],rms[17],rms[17],rms[17],rms[17],rms[11],rms[11],rms[11],rms[11],rms[11],rms[11]]),5)#CH3CN
    #vmin=round(3*np.mean([rms[18],rms[18]]),5)#CH3Cnv8
    #vmin=round(3*np.mean([rms[16],rms[17],rms[22],rms[28],rms[12],rms[2]]),5)#CH3OD
    #vmin=round(3*np.mean([rms[16],rms[17],rms[22],rms[23],rms[23],rms[25],rms[27]]),5) #C2H5OH-old
    #vmin=round(3*np.mean([rms[22],rms[23],rms[23],rms[25],rms[27]]),5) #C2H5OH-new
    #vmin=round(3*np.mean([rms[16],rms[17],rms[22],rms[26],rms[26],rms[26],rms[26],rms[26],rms[26],rms[26],rms[26],rms[26],rms[27],rms[28],rms[28],rms[5],rms[14]]),5) #CH3CHO
    #vmin=round(3*np.mean([rms[21],rms[21],rms[21],rms[22],rms[22],rms[25],rms[28],rms[28],rms[28],rms[11],rms[11],rms[11],rms[11],rms[12],rms[14],rms[14]]),5)#HCOOCH3
    #vmin=round(3*np.mean([rms[1],rms[5],rms[5],rms[11],rms[11],rms[11],rms[11],rms[11],rms[12],rms[13],rms[13],rms[23],rms[23],rms[23],rms[23],rms[28]]),5)#CH3OCH3
    #vmin=round(3*np.mean([rms[17],rms[17],rms[22],rms[25],rms[5],rms[11],rms[12],rms[12],rms[14]]),5)#CH2DOH
    #vmin=round(3*np.mean([rms[22],rms[10]]),5)#CH3OH-masers
    #vmin=round(3*np.mean([rms[22],rms[24],rms[1],rms[13],rms[14]]),5)#CH3OH-NS-outflow
    #vmin=round(3*np.mean([rms[23],rms[22],rms[24],rms[25],rms[26],rms[1],rms[4],rms[4],rms[4],rms[4],rms[4],rms[4],rms[5],rms[5],rms[5],rms[5],rms[5],rms[5],rms[12],rms[13],rms[14]]),5)#CH3OH-compact
    vmin=round(3*np.mean([rms[22],rms[6],rms[6],rms[9],rms[10]]),5)#CH3OH-extended 
    #vmin=round(3*np.mean([rms[16],rms[18],rms[26],rms[2]]),5) #CH2OHCHO
    norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=SqrtStretch())
print(vmin)
print(vmax)

# OVERLAY COORDINATES
#fig, ax = plt.subplots()
ax = plt.subplot(projection=wcs_updated, slices=('x', 'y', 10))
dec_axis = ax.coords[1]
dec_axis.set_major_formatter('dd:mm:ss.s')
dec_axis.set_axislabel('Declination (J2000)', size=12)
dec_axis.set_axislabel_position('l')
ra_axis = ax.coords[0]
ra_axis.set_major_formatter('hh:mm:ss.s')
ra_axis.set_axislabel('Right Ascension (J2000)', size=12)



SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 14

#plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
#plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels


# PLOT EMISSION
continuumlevels=np.linspace(0.0039,cont_image_data.max(),5) #from noise of your cont fits cube, starts at 3*sigma_cont up to max value, 5 levels)
emissionlevels=[0.1*sigma,0.3*sigma,0.5*sigma,0.7*sigma,0.9*sigma]
plt.contour(cont_image_data, levels=continuumlevels, colors='white', linewidths=0.7, alpha=0.7) #plots continuum emission contours
plt.contour(im_data_m, levels=emissionlevels,colors='cyan',linewidths=0.7,alpha=0.7) #plots molecular emission contours
plt.imshow(im_data_m, norm=norm, cmap='inferno', origin='lower') #
#print(cont_image_data.max())
#print(im_data_m.max())
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10,6) #size of figure
plt.tight_layout(pad=7.5, h_pad=7.0) # fixes axis labels from being cutoff
# OVERLAY BEAM

params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)


# MOLECULE INFO
textstr = '\n'.join((
    r'CH$_3$OH',))
    #r'7$_{0}$ - 6$_{0}$', 
    #r'17 - 16',
    #r'E$_{up}$ = 12.88 K')) 
props = dict(boxstyle='round', facecolor='black', alpha=0.3)

ax = plt.subplot(111)
ax.tick_params(direction='in', length=3, color='grey')
ell = my_beam.ellipse_to_plot(110,85, pixscale) 
#extended: 
#H2CO, SO, SiO, blended, DCN (110,85)  
#compact: 
#13CH3CN, DCCCN, HDO (127,136)
#H213CO: 127,135
ell.set_facecolor('w')
_ = ax.add_artist(ell)

plt.colorbar(pad=0.008, extend='min', label='Jy Beam$^{-1}$ km s$^{-1}$')


ax.text(0.8, 0.1, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props, color='white')     
        #Compact: 0.84, 0.95
        #extended:0.72, 0.95
        #cartoon:
#cbar.set_ticks([0.05, 0.1, 0.2, 0.3, 0.4, 0.5])

#Adds a small mark where you extracted the peak continuum flux pixel for fitting
ax.text(0.632, 0.613, 'O', transform=ax.transAxes, fontsize=5,
        verticalalignment='center', color='red',weight='bold') 
ax.text(0.294, 0.575, 'O', transform=ax.transAxes, fontsize=5,
        verticalalignment='center', color='red',weight='bold') 



#ax.text(0.04, 0.95, f'$\\sigma$={vmax}', transform=ax.transAxes, fontsize=12,verticalalignment='top', bbox=props, color='white')  #extended: 0.04, 0.96
#ax.text(0.04, 0.95, '$\\sigma$=0.04137', transform=ax.transAxes, fontsize=12,verticalalignment='top', bbox=props, color='white')  #extended: 0.04, 0.96
# EXTENDED LIMITS
# plt.xlim(115,240)
# plt.ylim(80,205)
plt.xlim(100,235)
plt.ylim(80,210)
# COMPACT LIMITS
# plt.xlim(120,230)
# plt.ylim(130,180)
plt.show()
#print(0.1*sigma)

