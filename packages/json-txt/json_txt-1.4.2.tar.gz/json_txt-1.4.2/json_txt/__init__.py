import re
from filemod import reader

def number_detect(letter):
    """Detect the nature of letter is number or not"""

    try:
        int(letter)
        return True
    except:
        return False

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
                if characters[value_index] not in [":", "\n", " "]:
                    temp.append(characters[value_index])

    return keys


def generate_array(data):
    array_temp=[]
    array=[]
    for array_elements in data:
        if array_elements in ["["]:
            continue 
        elif array_elements in [",","]"]:
            if number_detect(collab_words_in_list(array_temp)):
                array.append(int(collab_words_in_list(array_temp)))
            else:
                array.append(collab_words_in_list(array_temp))
            array_temp.clear()
        else:
            array_temp.append(array_elements)
    return array


def extract_values(txt_file_data):
    """extract values from file"""
    temp = []
    values = []
    characters = list(txt_file_data)

    for index in range(len(characters)):
        if characters[index] == ":":
            for value_index in range(index, len(characters)):               
                if characters[value_index] == "\n":
                    if temp[0]=="[":
                        values.append(list(generate_array(temp)))
                        temp.clear()  
                        continue                  
                    values.append(collab_words_in_list(temp))
                    temp.clear()
                    break
                if characters[value_index] not in [":", "'", "\n", " ", '"']:
                    temp.append(characters[value_index])

    return values


def extract_data(data):
    """create a dictonary"""
    keys = extract_keys(data)
    values = extract_values(data)
    return {keys[index]: values[index] for index in range(len(keys))}


def load_txt(data):
    """compiling the text file"""
    try:
        from json_txt.compiler import compiles
        return compiles(data)
    except:
        reader("data")


