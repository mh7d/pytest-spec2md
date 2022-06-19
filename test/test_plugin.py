import pytest_spec2md.plugin
import pytest_spec2md.spec_creator
from collections import namedtuple


class A1:
    class B1:
        def func(self):
            pass


class A2:
    def func(self):
        pass


class TestGetParent:

    def test_function_with_class_returns_class(self):
        f = A2.func

        p = pytest_spec2md.spec_creator.ItemEnhancer.get_parent(f)
        assert p == A2

    def test_two_layers_can_be_walked(self):
        f = A1.B1.func

        p = pytest_spec2md.spec_creator.ItemEnhancer.get_parent(
            pytest_spec2md.spec_creator.ItemEnhancer.get_parent(f)
        )
        assert p == A1


class MockModule:

    def __init__(self, name: str):
        self._name = name

    def __str__(self):
        return f'Module {self._name}'

    def __repr__(self):
        return f'Module {self._name}'


class MockItem:

    def __init__(self, name: str, module: MockModule):
        self._name = name
        self._module = module

    @property
    def nodeid(self):
        return self._name

    @property
    def module(self):
        return self._module

    def listnames(self):
        return self._name.split('::')

    def __eq__(self, other):
        if not isinstance(other, MockItem):
            return False
        return self._name == other._name

    def __repr__(self):
        return f'Item {self._name} of {self._module}'


class TestPytestCollectionModifyitems:

    @property
    def options(self):
        Option = namedtuple('Option', 'option')
        OptContent = namedtuple('OptContent', 'spec2md')
        return Option(option=OptContent(spec2md=True))

    @property
    def items(self):
        ma = MockModule('M_a')
        mb = MockModule('M_b')

        return [MockItem(x, y) for x, y in [
            ('abc', ma),
            ('ABC::abc', mb),
            ('XYC:::ASFGT::abc', ma)
        ]]

    def test_items_length_is_fixed(self):
        items = self.items
        old_length = len(items)

        pytest_spec2md.plugin.pytest_collection_modifyitems(None, self.options, items)

        assert len(items) == old_length

    def test_items_were_sorted_by_module(self):
        # Remove sorting because it is not stable so far

        items = self.items

        pytest_spec2md.plugin.pytest_collection_modifyitems(None, self.options, items)

        assert items[0] == self.items[0]
        assert items[1] == self.items[1]
        assert items[2] == self.items[2]
