import datetime
import os


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


def create_logreport(self, report, use_terminal=True):
    filename = self.config.getini('spec_target_file')
    _create_spec_file_if_not_exists(filename)
    _write_node_to_file(filename, _create_file_content(report))


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


def _create_file_content(report):
    return report.nodeid


def _split_scope(testnode):
    return [i for i in testnode.split('::') if i != '()']


def _write_node_to_file(filename, node_content):
    if not os.path.exists(filename):
        raise ValueError(f'File not found: {filename}')

    print(node_content)
    with open(filename, 'a') as file:
        file.write(node_content + '\n')
