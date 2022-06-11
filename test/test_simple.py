import os

import pytest


@pytest.fixture
def pytester_simple(request, pytester):
    test_data_dir = os.path.join(request.config.rootdir, 'pytester_cases', 'case_simple')

    pytester.syspathinsert(os.path.join(request.config.rootdir, 'pytest_spec2md'))

    with open(os.path.join(request.config.rootdir, 'pytester_cases', 'conftest.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makeconftest(source=source)

    with open(os.path.join(test_data_dir, 'test_simple.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makepyfile(source)

    return pytester


def test_simple_runs_4_successful_tests(pytester_simple: pytest.Pytester):
    result = pytester_simple.runpytest("--spec2md")
    result.assert_outcomes(passed=4)


def test_simple_creates_17_lines_of_documentation(pytester_simple: pytest.Pytester):
    pytester_simple.runpytest("--spec2md")

    with open(os.path.join(pytester_simple.path, 'documentation/spec.md')) as spec:
        spec = spec.readlines()

    assert len(spec) == 17
