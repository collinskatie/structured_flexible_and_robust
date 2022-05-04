import yaml

def read_specs(file_pointer):
    specs = yaml.load(file_pointer, Loader=yaml.SafeLoader)
    collect = []
    for i, s in enumerate(specs):
        s['name'] = f'problem_{i:03d}'
        if 'test' not in s:
            s['test'] = False
        s['id'] = f'{i:03d}'
        collect.append(s)
    return collect