import json

def save_json(dict_, json_filepath):
    ''' [Example] Write JSON '''
    '''
    dict_ = {"0":{"title":"test-A", "is-available": False, "link":"https://www.AAA.XXX..."},
             "1":{"title":"test-B", "is-available": True, "link":"https://www.BBB.XXX..."}}
    with open("dict_.txt", 'w') as output_file:
        json.dump(dict_, output_file)
    '''
    with open(json_filepath, 'w') as output_file:
        json.dump(dict_, output_file)

def load_json(json_filepath):
    ''' [Example] Read JSON '''
    '''
    with open("dict_.txt", 'r') as json_file:
        dict_ = json.load(json_file)
        print(dict_)
        print(type(dict_))
    '''
    with open(json_filepath, 'r') as json_file:
        dict_ = json.load(json_file)
        #print(dict_)
        #print(type(dict_))
    return dict_