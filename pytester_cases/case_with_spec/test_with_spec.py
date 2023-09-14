"""
General Documentation test
"""
import pytest

from pytest_spec2md import TestType


class CaseForTest:

    def run(self):
        pass


class TestCaseForTest:
    """
    docstring for testclass
    """

    @pytest.mark.spec_identifier('Dummy.One')
    @pytest.mark.parametrize('test', [1, 2, 3, 'a'])
    def test_run(self, test):
        """the run function is called with the test parameter"""
        assert True

    @pytest.mark.spec_identifier('Dummy.One', 'Dummy Unknown')
    @pytest.mark.test_type(TestType.PERFORMANCE)
    def test_run_false(self):
        assert False

    @pytest.mark.spec_identifier('Dummy.2', 'Dummy.Three')
    def test_run2(self):
        assert True
