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

# with fits.open(image_file, ignore_missing_end=True) as hduc:
#     cubec = sc.read(hduc)
#     cont_data = hdu[0].data
    


fits.info(image_file)
cont_image_data = fits.getdata(image_file, ext=0)
cube_file = 'IRAS-4B-hr-14_line.fits' # 

with fits.open(cube_file, ignore_missing_end=True) as hdu:
    del hdu[0].header['LINE']                               # deletes non-ascii in header
    #hdu.writeto('spw9-cts-new.fits')                       # optional: write new fits file after deleting 'LINE' header
    bmaj = hdu[0].header['BMAJ']
    bmin = hdu[0].header['BMIN']
    #print(hdu[0].header)
    
    cube = sc.read(hdu)
    im_data = hdu[0].data
    wcs = WCS(hdu[0])                                       # read the header info of the file
    fit_shape = cube.shape
    
    num_chan = fit_shape[0]
    #print(num_chan)
    #hdu[0].header['CRPIX1'] = 122 # reference pixel (257) - start index of y range: 137  || extend pictures: 137
    #hdu[0].header['CRPIX2'] = 97 # reference pixel (257) - start index of x range: 117  || extend pictures: 117
    wcs_updated = WCS(hdu[0]) # updated wcs with new CRPIX values
    # retrieve beam size from the header
    header = fits.getheader(cube_file)
    w = proj_plane_pixel_scales(wcs)                        # get pixel scales
    my_beam = Beam.from_fits_header(header)                 # get beam size from header
    #print(my_beam)
    px = w[0] * 3600  # take pixel scale, * 3600 to convert degrees to arcsec
    pixscale = px * u.arcsec


# this makes a smaller cube with a selected range of channels and coordinates
# don't change 2nd & 3rd ranges, for image size
                # t : b , l : r
#subcube = cube[1085:1132,150:350,150:350]                   # use for zoomed images
#subcube = cube[825:955,160:340,135:365] # 140,365 | 120:385      # use for non-compact emission
#subcube = cube[825:955,:,:] # 140,365 | 120:385      # use for non-compact emission

# ***********************************************************************************************************************
subcube = cube[859:867,:,:]     # 1536:1641 shape(n_s,n_y,n_x) s is spectral axis (channels)
# 
# ***********************************************************************************************************************
#spec_cube = cube[:, 100:250,70:200] #uncomment this if plotiing a spectrum of subcube
#cont_cube = cubec[:, 160:340,135:365]
#subcube = cube[:,:,:] # 140,365 | 120:385      # use for non-compact emission


#############################################################
# plotting spectrum

# take a slice for a spectrum
#spec_slice = np.array(spec_cube[:,115,108]) #left core: (116,115) / right core: (115,139)
#x_arr = np.linspace(144714, 144910,num_chan)
#spec_slice = np.array(subcube[:,51,52])

#plt.rcParams['axes.formatter.useoffset'] = False #changes offset x axis
#fig, ax = plt.subplots()

#ax.set_xticklabels(x)
#plt.plot(spec_slice, color='black', linewidth=0.7)
#plt.plot(115,115, marker='2',color='white') # 78, 80
#plt.savefig('Spectrum-SPW28-LeftCore.png')
#plt.show()

#############################################################
# create moment map

# try:
#     os.remove('../Moment-0-Maps-single-emission/SiO-moment_0.fits')
# except OSError:
#     pass


moment_0 = subcube.moment0() 
moment_1 = subcube.moment1() 

#fwhm_map = cube.linewidth_fwhm() 

# moment_0.write('../Moment-0-Maps-single-emission/DCCCN-moment_0.fits') 
with fits.open('../../Moment-0-Maps-single-emission/CNCN-moment_0.fits') as hdum:
    #cubem = sc.read(hdum)
    im_data_m = (hdum[0].data)/1000
    vmax=round(im_data_m.max(),5) #in Jy/beam*km/s from the /1000 above, max flux value
    sigma=vmax #write in Jy/beam*km/s
    vmin=round(3*rms[5],5) #This is 3*sigma_emission of your #-hr_line.fits cube
    #wcs = WCS(hdum[0]) 
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
    #r'CH$_3$SH v$_t$=0 A',
    r'CNCN',
    #r'6$_{1,5}$ - 5$_{1,4}$',
    r'J=14-13, F$_1$=14-14, F=14-14',
    #r'53 - 52',
    r'E$_{up}$ = 45.19 K')) 
props = dict(boxstyle='round', facecolor='black', alpha=0.3)
print(pixscale)
print(my_beam)

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


ax.text(0.24, 0.22, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props, color='white')     
        # extended: SO, SiO, HCCCN, OCS: 0.62, 0.2
        #blended: 0.8, 0.1
        # compact: 13CH3CN, DCCCN, HDO, C5O: 0.76, 0.28
        #H213CO: 0.77, 0.26
#cbar.set_ticks([0.05, 0.1, 0.2, 0.3, 0.4, 0.5])

ax.text(0.04, 0.96, f'$\\sigma$={vmax}', transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props, color='white')  #extended: 0.04, 0.96
#ax.text(0.04, 0.96, '$\\sigma$=0.14220', transform=ax.transAxes, fontsize=12,verticalalignment='top', bbox=props, color='white')
# EXTENDED LIMITS
#H2CO
# plt.xlim(100,280)
# plt.ylim(75,230)
#SO, SiO
plt.xlim(100,230)
plt.ylim(75,210)
# COMPACT LIMITS
#13CH3CN, HDO, C5O
# plt.xlim(120,230)
# plt.ylim(130,180)
#H213CO
#plt.xlim(120,230)
#plt.ylim(130,190)
plt.show()

