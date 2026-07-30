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


image_file = get_pkg_data_filename('IRAS-4B-hr-11_continuum.fits')


fits.info(image_file)
cont_image_data = fits.getdata(image_file, ext=0)

####################
##You can uncomment this section if you need, but even with the two errors it throws, it still seems to do it anyway in spyder (undefined wsc_updated and my_beam). 
##If you need this section, just put any of your high res line fits file in, it does not matter. We are literally just taking the coordinates from it.
cube_file = 'IRAS-4B-hr-11_line.fits' # 

with fits.open(cube_file, ignore_missing_end=True) as hdu:
    del hdu[0].header['LINE']                               # deletes non-ascii in header
    bmaj = hdu[0].header['BMAJ']
    bmin = hdu[0].header['BMIN']
    
    cube = sc.read(hdu)
    im_data = hdu[0].data
    wcs = WCS(hdu[0])                                       # read the header info of the file
    fit_shape = cube.shape
    
    num_chan = fit_shape[0]
    wcs_updated = WCS(hdu[0]) # updated wcs with new CRPIX values
    header = fits.getheader(cube_file)
    w = proj_plane_pixel_scales(wcs)                        # get pixel scales
    my_beam = Beam.from_fits_header(header)                 # get beam size from header
    px = w[0] * 3600  # take pixel scale, * 3600 to convert degrees to arcsec
    pixscale = px * u.arcsec
subcube = cube[3575:3591,:,:]     # 1536:1641 shape(n_s,n_y,n_x) s is spectral axis (channels)
try:
    os.remove('moment_0.fits')
except OSError:
    pass
moment_0 = subcube.moment0() 
moment_1 = subcube.moment1() 

#fwhm_map = cube.linewidth_fwhm() 

moment_0.write('moment_0.fits') 
with fits.open('moment_0.fits') as hdum:
    #cubem = sc.read(hdum)
    im_data_m = (hdum[0].data)/1000
    #vmax=round(im_data_m.max(),5) #in Jy/beam*km/s from the /1000 above, max flux value
    #sigma=vmax #write in Jy/beam*km/s
    #vmin=round(3*rms[17],5) #This is 3*sigma_emission of your #-hr_line.fits cube
    #wcs = WCS(hdum[0]) 
    #norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=SqrtStretch())
#print(vmin)
#print(vmax)
#########################

# OVERLAY COORDINATES
ax = plt.subplot(projection=wcs_updated, slices=('x', 'y', 10))
dec_axis = ax.coords[1]
dec_axis.set_major_formatter('dd:mm:ss.s')
dec_axis.set_axislabel('Declination (J2000)', size=12)
dec_axis.set_axislabel_position('l')
ra_axis = ax.coords[0]
ra_axis.set_major_formatter('hh:mm:ss.s')
ra_axis.set_axislabel('Right Ascension (J2000)', size=12)
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels


# PLOT Continuum EMISSION
#Change 0.0039 to be your 3*sigma_cont
continuumlevels=np.linspace(0.0039,cont_image_data.max(),5) #from noise of your cont fits cube, starts at 3*sigma_cont up to max value, 5 levels)
norm = ImageNormalize(vmin=0.0039, vmax=cont_image_data.max(), stretch=SqrtStretch())
plt.contour(cont_image_data, levels=continuumlevels, colors='white', linewidths=0.7, alpha=0.7) #plots continuum emission contours
plt.imshow(cont_image_data, cmap='inferno', origin='lower') #
print(np.round(cont_image_data.max(),4)) #prints your max continuum emission in Jy/beam
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10,6) #size of figure
plt.tight_layout(pad=7.5, h_pad=7.0) # fixes axis labels from being cutoff


# OVERLAY BEAM
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

#This places your sythesized beam
ax = plt.subplot(111)
ax.tick_params(direction='in', length=3, color='grey')
ell = my_beam.ellipse_to_plot(127,136, pixscale) 
ell.set_facecolor('w')
_ = ax.add_artist(ell)
plt.colorbar(pad=0.008, extend='min', label='Jy Beam$^{-1}$ ')#km s$^{-1}$

#Places Text on the image labeling your cores, 
ax.text(0.58, 0.92, '4B', transform=ax.transAxes, fontsize=16,
        verticalalignment='top', color='white')     
ax.text(0.13, 0.8, '4B\'', transform=ax.transAxes, fontsize=16,
        verticalalignment='top', color='white') 
#Adds a small mark where you extracted the peak continuum flux pixel for fitting
ax.text(0.597, 0.593, 'O', transform=ax.transAxes, fontsize=10,
        verticalalignment='center', color='red') 
ax.text(0.181, 0.494, 'O', transform=ax.transAxes, fontsize=10,
        verticalalignment='center', color='red') 



#Change your field of view
# plt.xlim(170,203)
# plt.ylim(150,170)
plt.xlim(120,230)
plt.ylim(130,180)
plt.show()

