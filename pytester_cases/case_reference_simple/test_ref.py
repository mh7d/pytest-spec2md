import pytest


def function_to_ref():
    """ Simple doc comment
    with two lines
    """
    pass


@pytest.mark.spec_reference(function_to_ref.__name__, function_to_ref.__doc__)
def test_use_a_reference_in_doc():
    assert True
