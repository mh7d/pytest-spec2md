import os

import pytest


@pytest.fixture
def pytester_advanced(request, pytester):
    test_data_dir = os.path.join(request.config.rootdir, 'pytester_cases', 'case_advanced')

    pytester.syspathinsert(os.path.join(request.config.rootdir, 'pytest_spec2md'))

    with open(os.path.join(request.config.rootdir, 'pytester_cases', 'conftest.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makeconftest(source=source)

    with open(os.path.join(test_data_dir, 'test_advanced.py')) as file_content:
        source = "".join(file_content.readlines())
        pytester.makepyfile(source)

    return pytester


def test_runs_6_successful_tests(pytester_advanced: pytest.Pytester):
    result = pytester_advanced.runpytest("--spec2md")
    result.assert_outcomes(passed=6)


def test_creates_30_lines_of_documentation(pytester_advanced: pytest.Pytester):
    pytester_advanced.runpytest("--spec2md")

    with open(os.path.join(pytester_advanced.path, 'documentation/spec.md')) as spec:
        spec = spec.readlines()

    assert len(spec) == 30
