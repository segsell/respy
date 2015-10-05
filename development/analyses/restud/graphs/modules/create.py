#!/usr/bin/env python
""" This module produces the graphs for the lecture on the RESTUD economies.
"""


# standard library
import shutil
import sys
import os

# lexical analysis
import shlex

# numerical computing
import numpy as np

# hand-crafted plots
from auxiliary import *

# module-wide variables
HOME = os.environ['ROBUPY'] + '/development/analyses/restud/graphs'

# PYTHONPATH
sys.path.insert(0, os.environ['ROBUPY'])
sys.path.insert(0, HOME)

# project library
from robupy import read

# Start with a clean slate
os.chdir(HOME)

try:
    shutil.rmtree('rslts')
except FileNotFoundError:
    pass

os.mkdir('rslts')

os.chdir('rslts')
for spec in ['data_one', 'data_two', 'data_three']:
    os.mkdir(spec)
os.chdir('../')

# Wage functions
coeffs = {}

for spec in ['One', 'Two', 'Three']:

    os.chdir('../simulations/robupy/data_' + spec.lower())

    coeffs[spec] = dict()

    robupy_obj = read('model.robupy.ini')

    init_dict = robupy_obj.get_attr('init_dict')

    for label in ['A', 'B']:
        coeffs[spec][label] = init_dict[label]

    os.chdir(HOME)

# Read number of states from RESTUD output file
num_states = []
with open('../simulations/dp3asim/data_one/otest.txt', 'r') as output_file:
    for line in output_file.readlines():
        if ('kmax(t)' in line):
            num_states += [int(shlex.split(line)[-1])]

# Create and save plot
plot_dimension_state_space(num_states)

# Determine wages for varying level of experience in each occupation
for spec in ['One', 'Two', 'Three']:
    for which in ['A', 'B']:
        x, y = np.meshgrid(range(40), range(40))
        z = np.tile(np.nan, (40,40))
        for i in range(40):
            for j in range(40):
                z[i,j] = return_to_experience(i, j, coeffs[spec], which)

        # Create and save plot
        plot_return_experience(x, y, z, which, spec)

# Determine wages for varying years of education in each occupation
for spec in ['One', 'Two', 'Three']:
    xvals, yvals = range(10, 20), dict()
    for which in ['A', 'B']:
        yvals[which] = []
        for edu in xvals:
            yvals[which] += [return_to_education(edu, coeffs[spec], which)]

    # Create and save plot
    plot_return_education(xvals, yvals, spec)

# Determine choice patterns over time
for spec in ['One', 'Two', 'Three']:
    choice_probabilities = [[],[],[],[]]
    with open('../simulations/dp3asim/data_' + spec.lower() + '/otest.txt',
              'r') as \
            output_file:
        for line in output_file.readlines():
            if ('prob=' in line):
                list_ = shlex.split(line)
                for i in range(4):
                    choice_probabilities[i] += [float(list_[i + 3])]

    # Create and save plot
    plot_choice_patterns(choice_probabilities, spec)