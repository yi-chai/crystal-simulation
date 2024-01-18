# MD-Structure-Factor
Calculates 3d structure factor and simulated x-ray diffraction pattern from molecular dynamics trajectories

## Badges

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/98f35ccf8532431db930b7c7f34c1c92)](https://www.codacy.com/app/JoshuaSBrown/MD-Structure-Factor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joeyelk/MD-Structure-Factor&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.com/joeyelk/MD-Structure-Factor.svg?branch=master)](https://travis-ci.com/joeyelk/MD-Structure-Factor)

## Dependencies

 * [scipy](https://www.scipy.org/)
 * [mayavi](https://docs.enthought.com/mayavi/mayavi/)
 * [tqdm](https://pypi.org/project/tqdm/)
 * [MDAnalysis](https://www.mdanalysis.org/)
 * [duecredit](https://github.com/duecredit/duecredit)
 * [mdtraj](http://mdtraj.org/1.8.0/installation.html)
 * [pandas](https://pandas.pydata.org/)
 * future
 * setuptools
 * wheel
 * vtk
 
## Installation 

```
pip install --upgrade pip                                                   
pip install cython                                                          
pip install vtk                                                             
pip install pandas                                                          
pip install -r requirements.txt
```

## Example

example program usage:
```
main_gromacs.py -i foo    
```
(loads foo.gro and foo.trr)

```
main_gromacs.py -top foo.gro -traj foo.trr
```

The program will then create two intermediate files, out_foo_traj.npz and out_foo_sf.npz.  On subsequent runs of the program with the same inputs, these files will be automatically reloaded.  

Output:

The program will create a folder foo_plots, which will contain subfolders with various cross sections through the 3d structure factor.  Additionally, Ewald-corrected plots will be produced.  These more accurately show what would be seen in an x-ray diffraction experiment.  

## Papers

Coscia, B. J., Yelk, J., Glaser, M. A., Gin, D. L., Feng, X., & Shirts, M. R. (2019). Understanding the Nanoscale Structure of Inverted Hexagonal Phase Lyotropic Liquid Crystal Polymer Membranes. Journal of Physical Chemistry B, 123(1), 289–309. https://doi.org/10.1021/acs.jpcb.8b09944

