import filemod
from termcolor import colored


def collab_words_in_list(list):
    """collab word into strings"""
    return ''.join(list)


def extract_keys(txt_file_data):
    """extract keys from file"""
    characters = list(txt_file_data)
    temp = []
    keys = []
    for index in range(len(characters)):
        if characters[index] == "\n":
            for value_index in range(index, len(characters)):
                if characters[value_index] == ":":
                    keys.append(collab_words_in_list(temp))
                    temp.clear()
                    break
                elif characters[value_index] not in [":", "\n", " "]:
                    temp.append(characters[value_index])

    return keys


def extract_values(txt_file_data):
    """extract values from file"""
    temp = []
    values = []
    characters = list(txt_file_data)

    for index in range(len(characters)):
        if characters[index] == ":":
            for value_index in range(index, len(characters)):
                if characters[value_index] == "\n":
                    values.append(collab_words_in_list(temp))
                    temp.clear()
                    break
                if characters[value_index] not in [":", "'", "\n", " ", '"']:
                    temp.append(characters[value_index])
    return values


def test1(data):
    if data is None:
        print(colored('x Test 1 Fail', 'red'))
    else:
        print(colored('✓ Test 1 pass', 'green'))
        return True


def test2(data):
    if data[0:1] == "{" and data[len(data)-1] == "}":
        print(colored("✓ Test 2 pass", 'green'))
        return True
    elif data[0:1] != "{":
        print(colored('missing { ', 'red'))
        print(colored('x Test 2 Fail', 'red'))
    else:
        print(colored('x Test 2 Fail', 'red'))
        print(colored('missing } never closed', 'red'))


def test3(data):
    if len(extract_keys(data)) == len(extract_values(data)) == data.count(":"):
        print(colored("✓ Test 3 pass", 'green'))
        return True

    print(colored("X Test 3 Fail", 'red'))
    print(colored("Uneven values or number found in the values", 'red'))


def compiles(data):
    data = filemod.reader(data)
    if test1(data) == test2(data) == test3(data):
        print(colored("All Test Passed", 'green'))
    return data
