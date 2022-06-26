def test_in_lower():
    assert True


class TestClassInLower:
    def test_in_class_lower(self):
        assert True

    class TestSubClassInLower:
        def test_before_in_class_lower(self):
            assert True

    def test_third_in_class_lower(self):
        assert True


def test_after_class_in_lower():
    assert True
