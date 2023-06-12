def print_dict_tree(dictionary, indent=''):
    BLUE = '\033[34m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(f'{indent}{BLUE}├─ {WHITE}{key}:{RESET}')
            print_dict_tree(value, indent + f'{BLUE}│  {RESET}')
        else:
            print(f'{indent}{BLUE}├─ {WHITE}{key}: {value}{RESET}')

def object_tree(data, indent='', is_last=True):
    BLUE = '\033[34m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f'{indent}{BLUE}{"└─ " if is_last else "├─ "}{WHITE}{key}:{RESET}')
                if isinstance(value, dict):
                    object_tree(value, indent + '    ', True)
                else:
                    object_tree(value, indent + f'{BLUE}│   {RESET}', True)
            else:
                print(f'{indent}{BLUE}{"└─ " if is_last else "├─ "}{WHITE}{key}: {value}{RESET}')
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                print(f'{indent}{BLUE}{"└─ " if is_last else "├─ "}{RESET}')
                object_tree(item, indent + f'{BLUE}│   {RESET}', i == len(data) - 1)
            else:
                if hasattr(item, 'name'):
                    print(f'{indent}{BLUE}{"└─ " if is_last else "├─ "}{WHITE}{item.name}{RESET}')
                else:
                    print(f'{indent}{BLUE}{"└─ " if is_last else "├─ "}{WHITE}{item}{RESET}')