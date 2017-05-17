import unittest
import pytest

import test_py2_trial_connect_for_client_port1
import test_py2_trial_connect_for_client_port2

loader = unittest.TestLoader()

suite = loader.loadTestsFromModule(test_py2_trial_connect_for_client_port1)
suite.addTests(loader.loadTestsFromModule(test_py2_trial_connect_for_client_port2))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
