import datetime
import importlib
import os

import _pytest.reports


def modify_items_of_collection(session, config, items):
    """
    Sort the found tests for better results in output
    """
    _delete_existing_file(config.getini('spec_target_file'))

    def get_module_name(f):
        return f.listchain()[1].name

    def get_nodeid(f):
        return "::".join(f.nodeid.split('::')[:-1])

    items.sort(key=get_nodeid)
    items.sort(key=get_module_name)
    return items


def _delete_existing_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def create_logreport(self, report: _pytest.reports.TestReport, use_terminal=True):
    filename = self.config.getini('spec_target_file')
    _create_spec_file_if_not_exists(filename)
    if report.when == 'call':
        result, _, _ = self.config.hook.pytest_report_teststatus(report=report, config=self.config)

        _write_node_to_file(filename, _create_file_content(report, result))

        if use_terminal:
            print(f'{report.outcome}: {report.head_line}')


def _create_spec_file_if_not_exists(filename):
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as file:
            file.writelines([
                '# Specification\n',
                'Automatically generated using pytest_spec2md\n'
                '\n',
                f'Generated: {datetime.datetime.now()}\n',
                '\n'
            ])


def _create_file_content(report, state):
    return report


def _split_scope(testnode):
    return [i for i in testnode.split('::') if i != '()']


_last_node: _pytest.reports.TestReport = None


def _format_test_name(name: str):
    return name.replace('test_', '', 1).replace('_', ' ')


def _format_class_name(name: str):
    name = name.replace('Test', '', 1)
    return ''.join(' ' + x if x.isupper() else x for x in name)


def _write_node_to_file(filename, node_content: _pytest.reports.TestReport):
    global _last_node

    if not os.path.exists(filename):
        raise ValueError(f'File not found: {filename}')

    content = _split_scope(node_content.nodeid)
    last_content = _split_scope(_last_node.nodeid) if _last_node else ["", "", ""]

    with open(filename, 'a') as file:
        if not _last_node or content[0] != last_content[0]:  # changed test file
            module_name = content[0].replace('/', '.')[:-3]
            mod = importlib.import_module(module_name)

            file.write(f'\n'
                       f'## Spec from {content[0]}\n'
                       f'{mod.__doc__ if mod.__doc__ else ""}\n')

        if len(content) != len(last_content) \
                or content[1:-1] != last_content[1:-1]:
            if len(content) == 2:
                file.write(f'### General\n')
            else:

                file.write(f'### {":".join(_format_class_name(x) for x in content[1:-1])}\n'
                           f'{getattr(node_content, "parent_summary", "")}\n')

        file.write(f' - {_format_test_name(content[-1])}\n'
                   f'{getattr(node_content, "docstring_summary", "")}\n')

    _last_node = node_content