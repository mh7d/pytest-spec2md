"""
Advanced specification test
"""


def function_to_test(p1, p2):
    """docstring for function_to_test"""
    pass


def test_function_to_test_simple():
    """docstring for test to test function_to_test"""
    assert True


def test_function_to_test_simple_v2():
    """docstring for test to test function_to_test_v2"""
    assert True


class TestClassForFunctionToTest:

    def test_has_one_parameter(self):
        """the run function is called with the test parameter"""
        assert True

    def test_has_two_parameter(self):
        assert True

    class TestSubClass:
        """description of sub class"""

        def test_under_sub_class(self):
            """sub_class_test_function is running"""
            assert True

    def test_another_one(self):
        assert True
