# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 08:41:29 2026

@author: Collette
"""

from astropy.io import fits
hdulist = fits.open('IRAS-4B-hr-14_line.fits')
hdulist.info()
hdu = hdulist[0]
hdu.header
print(hdulist[0].header['BMAJ']*3600)

