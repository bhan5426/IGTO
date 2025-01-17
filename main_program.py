#AUTHOR : YASA VISWAMBHAR REDDY
#MATRICULATION NUMBER : 65074
#Personal Programming Project
#------------------------------------------------------------#
#STRUCTURAL TOPLOGY OPTIMIZATION USING ISO-GEOMETRIC ANALYSIS
# -----------------------------------------------------------# 
#_____________________________________________________________
#NOTE: if the program fails to run due to plotting issue, enter verbose=0
#NOTE: optimizated structure can be plotted using VTK file in paraview
#_____________________________________________________________
#########################################################################
'''
TEST CASE-1
INPUTS (MMA):
8 5 1 35 25 3 -100 0.4 3 1.5 150000 0.30 7850 0 1 1 
INPUTS (OC):
8 5 1 35 25 3 -100 0.4 3 1.5 150000 0.30 7850 0 0 1

TEST CASE-2
INPUTS (MMA):
8 5 1 35 25 3 -100 0.4 3 1.5 150000 0.30 7850 5 1 1 
INPUTS (OC):
8 5 1 35 25 3 -100 0.4 3 1.5 150000 0.30 7850 5 0 1

TEST CASE-3
INPUTS (MMA):
8 5 1 35 25 3 -100 0.2 3 1.5 150000 0.30 7850 1 1 1 
INPUTS (OC):
8 5 1 35 25 3 -100 0.2 3 1.5 150000 0.30 7850 1 0 1
'''
##########################################################################
import sys
import subprocess
import pkg_resources
import pip
import time 

TYELLOW =  '\033[33;1m' 
TGREEN = '\033[32;1m'
TRED='\033[31;1m'
TBLUE = '\033[34;1m'
ENDC = '\033[m' 

main_program_start=time.time()   #Start of the program

#Checks for the given python libraries and installs them if not installed.
for package in ['numpy', 'matplotlib', 'pyvista', 'pyEVTK','pytest']:
    try:
        
        dist = pkg_resources.get_distribution(package)
        print(TGREEN+'{} ({}) is installed'.format(dist.key, dist.version)+ENDC)
    except pkg_resources.DistributionNotFound:
        print(TRED+'{} is NOT installed'.format(package)+ENDC)
        pip.main(['install', package])
 
import os
def Folder(path):
    '''
    It checks if the folder exists else creates a new folder.
    
    Parameter
    ----------
    path : str
        path of the folder (independent of os).

    Returns
    -------
    Folder is generated at the specified path.

    '''
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Error: Creating directory. ' + path)


Folder('./results/')   #creates a results folder to store results
Folder('./log_files/')  #creates a log folder to store the program log file like time analysis and input parameters etc
print("\n Enter 0 for time analysis else Press ENTER for default")
time_options=input()
if __name__ == "__main__":
    if time_options=='0':
        from main_program_bottle_neck import *  #time analysis is performed 
        
    else:
        from processing import *  #Topology optimization using IGA

from plotting import *
plotting(ii,CC,VV,Mnd,element_density,optimizer,option)
