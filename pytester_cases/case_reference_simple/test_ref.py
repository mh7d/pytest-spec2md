import pytest


def function_to_ref():
    pass


@pytest.mark.spec_reference(function_to_ref.__name__)
def test_use_a_reference_in_doc():
    assert True
