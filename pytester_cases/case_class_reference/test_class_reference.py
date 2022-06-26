import pytest


class MyClass:
    """This is the documentation for *MyClass*"""

    def function_to_test(self):
        """this is the documentation for *function_to_test*"""


@pytest.mark.spec_reference(MyClass.__qualname__, MyClass.__doc__)
class TestMyClass:
    """this is the documentation for the Test Class"""

    @pytest.mark.spec_reference(MyClass.function_to_test.__qualname__, MyClass.function_to_test.__doc__)
    class TestFunctionToTest:
        """this is the documentation for the function test class"""

        def test_passes_every_time(self):
            """this is the implementation of the test"""
            assert True