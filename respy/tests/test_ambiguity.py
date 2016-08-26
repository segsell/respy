from pandas.util.testing import assert_frame_equal

import numpy as np
import pandas as pd
import pytest

from respy.python.shared.shared_auxiliary import print_init_dict

from respy.scripts.scripts_estimate import scripts_estimate
from respy.scripts.scripts_simulate import scripts_simulate
from respy.scripts.scripts_update import scripts_update
from respy.scripts.scripts_modify import scripts_modify
from respy.python.process.process_python import process
from respy.python.shared.shared_constants import IS_FORTRAN

from respy import estimate
from respy import simulate
from respy import RespyCls

from codes.random_init import generate_init

@pytest.mark.usefixtures('fresh_directory', 'set_seed')
class TestClass(object):
    """ This class groups together some tests.
    """
    def test_1(self):

        constr = dict()
        constr['level'] = 0.00
        constr['maxfun'] = 0

        init_dict = generate_init(constr)

        # We also check explicitly across the different program implementations.
        versions = ['PYTHON']
        if IS_FORTRAN:
            versions += ['FORTRAN']

        base_val = None
        for version in versions:
            for is_ambiguity in [True, False]:

                init_dict['AMBIGUITY']['flag'] = is_ambiguity
                init_dict['PROGRAM']['version'] = version

                print_init_dict(init_dict)

                respy_obj = RespyCls('test.respy.ini')

                simulate(respy_obj)
                _, crit_val = estimate(respy_obj)

                if base_val is None:
                    base_val = crit_val

                np.testing.assert_allclose(base_val, crit_val)
