import unittest

from sbs_tester.jcs_service.jcs_compute_basic_test import JCSComputeBasicTest
from sbs_tester.jcs_service.jcs_compute_varargs_test import JCSComputeVarArgsTest
from sbs_tester.jcs_service.jcs_compute_negative_test import JCSComputeNegativeTest


def suite():
    """
        Gather all the sbs_tester from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(JCSComputeBasicTest))
    test_suite.addTest(unittest.makeSuite(JCSComputeVarArgsTest))
    test_suite.addTest(unittest.makeSuite(JCSComputeNegativeTest))
    return test_suite

mySuit=suite()


runner=unittest.TextTestRunner()
runner.run(mySuit)