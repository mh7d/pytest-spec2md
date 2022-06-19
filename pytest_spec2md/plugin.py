import _pytest
import _pytest.python
import _pytest.terminal
import pytest

import pytest_spec2md.spec_creator


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        '--spec2md',
        action='store_true',
        dest='spec2md',
        help='Saves test results as specification document in markdown format.'
    )

    parser.addini(
        'spec_target_file',
        default='documentation/spec.md',
        help='The target file to save the generated specification.'
    )

    parser.addini(
        'spec_indent',
        default='  ',
        help='Indention of spec in console.'
    )


_act_config = None


def pytest_configure(config):
    global _act_config
    _act_config = config

    if config.option.spec2md:
        pytest_spec2md.spec_creator.SpecWriter.delete_existing_specification_file(config)

        config.addinivalue_line(
            "markers", "spec_reference(name, docstring): mark specification reference for the test"
        )


def _sort_by_module(items: list[_pytest.python.Function]):
    unique_modules = list(set(item.module for item in items))

    def index_of_module(obj: _pytest.python.Function):
        return unique_modules.index(obj.module)

    # items.sort(key=index_of_module)


def pytest_collection_modifyitems(session, config, items: list[_pytest.python.Function]):
    pass
#    if config.option.spec2md:
#        _sort_by_module(items)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Adds docstring to the item usage in report"""
    outcome = yield
    pytest_spec2md.spec_creator.ItemEnhancer.enhance(outcome, item)


@pytest.hookimpl(trylast=True)
def pytest_runtest_logreport(report):
    if report.when == 'call':
        pytest_spec2md.spec_creator.SpecWriter.create_specification_document(
            config=_act_config, report=report)
