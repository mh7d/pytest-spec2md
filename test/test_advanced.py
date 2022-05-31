"""
Advanced specification test
"""

def function_to_test(p1, p2):
    pass


def test_function_to_test_simple():
    assert True


class TestFunctionToTest:

    def test_has_one_parameter(self):
        """the run function is called with the test parameter"""
        assert True

    def test_has_two_parameter(self):
        assert True

    class TestSubClass:

        def test_another_one(self):
            assert True

    def test_under_sub_class(self):
        assert True