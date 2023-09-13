"""
General Documentation test
"""
import pytest


class CaseForTest:

    def run(self):
        pass


class TestCaseForTest:
    """
    docstring for testclass
    """

    @pytest.mark.spec_identifier('Dummy.One')
    @pytest.mark.parametrize('test', [1, 2, 3])
    def test_run(self, test):
        """the run function is called with the test parameter"""
        assert True

    @pytest.mark.spec_identifier('Dummy.2', 'Dummy.Three')
    def test_run2(self):
        assert True
