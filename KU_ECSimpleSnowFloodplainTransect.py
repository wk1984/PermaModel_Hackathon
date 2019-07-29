#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:48:33 2019

@author: kangwang
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Load PyMT model(s)
import pymt.models
ku = pymt.models.Ku()
ec = pymt.models.ECSimpleSnow()

def func(x, a, b, c):
    
    # a: annual amplitude
    # c: mean annual temperature
    
    return a * np.sin(x/365*2*np.pi+b) + c

# Initialize the model with the defaults.
ec.initialize('snow_model.cfg')

# List input and output variable names.
print(ec.get_output_var_names())
print(ec.get_input_var_names())
ec.finalize()

config_file, run_folder = ku.setup(lat  = 71.31,
                                   lon  = -156.66,
                                   T_air = -10.0) #Barrow as an example
ku.initialize(config_file, run_folder)
print(ku.get_component_name())
print(ku.get_input_var_names())

print(ku.get_value('vegetation__Dvt'))
ku.finalize()

vegfloodplain= np.zeros(10)

air_temperature = np.loadtxt('tair.csv') # this is used for estimating annual cycle in following
precipitation   = np.loadtxt('prec.csv')

air_temperature = air_temperature[0:365]
precipitation   = precipitation[0:365]

t365 = np.arange(365)

popt, pcov = curve_fit(func, 
                       t365, 
                       air_temperature, 
                       bounds=([0.0,-99.0,-99.0], [50., 99.0, 99.0]))

MAAT = popt[2]
MAAA = popt[0]

print(MAAT, MAAA)

print(config_file, run_folder)


for i in np.arange(1):
    
    ec = pymt.models.ECSimpleSnow() 
    ec.initialize('snow_model.cfg')
    
#    ku = pymt.models.Ku()
    ku.initialize(config_file, run_folder)
    
    ec.set_value('snow_class',2)
    ec.set_value('open_area_or_not', 0)
#    
##     print('initial')
#    
#    # DEFINE some variables for annual summary
#
#    snod     = 0
#    sden     = 0
#    snow_day = 0
#
#    if i == 1 or i == 0:
#        
#        print('setting column 0, 1')
#        
#        ku.set_value('vegetation__Hvgt', 1.0)
#        ku.set_value('vegetation__Hvgf', 1.0)
#        ku.set_value('vegetation__Dvt' , 1.0E-8)
#        
#        ec.set_value('snow_class',2)