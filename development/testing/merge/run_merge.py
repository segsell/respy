#!/usr/bin/env python
""" This script runs a series of tests that are required before merging a
candidate branch into a target branch.
"""

from respy.python.shared.shared_constants import ROOT_DIR
import respy
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGE_DIR = ROOT_DIR.replace('respy', '')
TEST_DIR = PACKAGE_DIR + '/development/testing/'


# We need to specify the tests to run.
request_dict = dict()
request_dict['REGRESSION'] = True
request_dict['PROPERTY'] = True
request_dict['RELEASE'] = True
request_dict['PYTEST'] = True

# We need to specify the arguments for each of the tests.
test_spec = dict()
test_spec['PYTEST'] = dict()

test_spec['REGRESSION'] = dict()
test_spec['REGRESSION']['request'] = ('check', 1)
test_spec['REGRESSION']['is_background'] = False
test_spec['REGRESSION']['is_compile'] = False

test_spec['PROPERTY'] = dict()
test_spec['PROPERTY']['request'] = ('run', 0.00001)
test_spec['PROPERTY']['is_background'] = False
test_spec['PROPERTY']['is_compile'] = False

# During release testing we compare the results from short estimation runs
# from the candidate branch to the relevant master.
test_spec['RELEASE'] = dict()
test_spec['RELEASE']['new_release'] = '2.0.0.dev11'
test_spec['RELEASE']['old_release'] = '2.0.0.dev12'
test_spec['RELEASE']['request'] = ('run', 0.00001)
test_spec['RELEASE']['is_background'] = False
test_spec['RELEASE']['is_create'] = True


for dirname in ['regression', 'property', 'release']:
    sys.path.insert(0, TEST_DIR + '/' + dirname)

from run_regression import run as run_regression
from run_property import run as run_property
from run_release import run as run_release

# TODO: NOtifications ?
# TODO: Add runs in Python 2 and 3

if request_dict['PYTEST']:
    respy.test()

if request_dict['REGRESSION']:
    is_success_regression = run_regression(**test_spec['REGRESSION'])

if request_dict['PROPERTY']:
    run_property(**test_spec['PROPERTY'])

if request_dict['RELEASE']:
    run_release(**test_spec['RELEASE'])
