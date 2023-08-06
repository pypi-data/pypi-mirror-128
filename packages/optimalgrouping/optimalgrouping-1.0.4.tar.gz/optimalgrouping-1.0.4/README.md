#Optinal Grouping
This is a module to run optimal grouping of spectra using recipe of Kaastra & Bleeker (2016)
Note that it does not optimize the response matrix.

### Author
Carlo Ferrigno (carlo.ferrigno AT unige.ch)

### Installation
To install it, use the command
````
pip install optimalgrouping
````
or
````
python setup.py install
````
(better from a virtual environment)

It will provide the module optimalgrouping and the script optimal_binning.py (for backward compatibility)

*Note that heasoft must be initialized before the use, as this tool uses grppha from heasoft*

### Usage

Issuing optimal_binning.py without arguments displays a full help.

Example of usage are in ./tests:

Direct run from shell can be:
````bash
optimal_binning.py PNsource_spectrum.fits -b PNbackground_spectrum.fits -r PN_spectrum.rmf -a PN_spectrum.arf -e 0.5 -E 10
````

From inside a python session, it can be
````python
from optimalgrouping.optimalgrouping import execute_binning
execute_binning('PNsource_spectrum.fits', 'PNbackground_spectrum.fits',  'PN_spectrum.rmf',  'PN_spectrum.arf',  0.5, 10.0)
````

This is the help output
````
usage: optimal_binning.py [-h] [-b BACKNAME] [-r RESPNAME] [-a ANCRNAME]
                          [-e MINE] [-E MAXE] [-m MINCOUNTS] [--eref EREF]
                          [--res RES] [--en_dep EN_DEP]
                          fname

Optimal grouping for the spectrum

positional arguments:
  fname                 Spectrum PHA1 file

optional arguments:
  -h, --help            show this help message and exit
  -b BACKNAME, --backname BACKNAME
                        Background file (default: none)
  -r RESPNAME, --respname RESPNAME
                        RMF or RSP file (response matrix) (default: none)
  -a ANCRNAME, --ancrname ANCRNAME
                        ARF file (effective area) (default: none)
  -e MINE, --mine MINE  Minimum energy (keV), default is minimum of response
                        (default: -10)
  -E MAXE, --maxe MAXE  Maximum energy (keV), default is maximum of response
                        (default: 10000000000.0)
  -m MINCOUNTS, --mincounts MINCOUNTS
                        Minimum number of counts per bin (for Xspec >0, for
                        other instruments also 0) (default: -10000000000.0)
  --eref EREF           reference energy for custom resolution (keV) (default:
                        -1)
  --res RES             resolution at the reference energy for custom input
                        (keV) (default: -1)
  --en_dep EN_DEP       energy dependence of resolution (power-law index) for
                        custom input (keV) (default: -1)

PURPOSE:
Group the spectra using Kaastra & Bleeker's recipe plus an option for a minimal number of counts
the input spectrum file is grouped using grppha and the output has the _rbn.pi extension added to the root file name
It is recommended not to set a minimum number of counts for spectral fitting of high-resolution spectra
with a line-rich spectrum to avoid large bins that would bias the line centroid determination.
However, it should be noted that Xspec has a problem with C-statistics when there are empmty bins.

The response and background files are taken from the keywords in the input spectrum, but can be overriden by setting the optional parameters.

The following parameters can be provided for a custom resolution, otherwise the optimal resolution is derived from the RMF file:
eref = reference energy for energy resolution (keV)
res = resolution at the reference energy (keV)
en_dep = dependence of the resolution on energy (power-law index)


Examples:
optimal_binning.py PNspectrum.fits -e 1.7 -E 11 -m 10
optimal_binning.py -r acisf_heg_p1.rmf -a acisf_heg_p1.arf heg_p1.fits -e 2.0
optimal_binning.py hxd_pin_sr.fits -e 12.  -E 60.
optimal_binning.py xi0.pi -e 0.4 -E 11
optimal_binning.py xi0_rbn.pi -e 0.4 -E 11. --eref 6 --en_dep -0.5 --res 0.6


To mimic the typical resolution of current instrumewnts, we provide the following suggestions
Suzaku XIS1 eref=6 res=0.168 en_dep = -0.5
Suzaku XIS0,XIS3 eref=6 res=0.153 en_dep = -0.5
Suzaku PIN eref=15 res=4.125 en_dep = 0
XMM EpicPN eref=6 res=0.175 en_dep = -0.5
XMM EpicMOS eref=6 res=0.155 en_dep = -0.5


For bugs and requests email to carlo.ferrigno AT unige.ch
````

##REFERENCE: 
Kaastra & Bleeker, 2016, A&A, 587, 151, Sect.5.3


