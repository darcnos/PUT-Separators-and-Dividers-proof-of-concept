import requests, json, csv
fbheaders = {'content-type': 'application/json'}


"""
Logins to a site with provided credentials, obtains blank separator and divider templates, and PUTs
them into a project. Update the projectID before deploying into actual production

Also, Separators must be defined before PUTing Dividers onto the site that are assigned to a separator

"""


site = 'https://{}'.format(input('https://'))
api = '{}/api/'.format(site)

#testing with a projectid of 215
projectid = '215'

def login():
    """Logins in to the site, returns the GUID as a string"""
    u = input('Username: ')
    p = input('Password: ')
    data = {
        'username': u,
        'password': p
    }
    login = '{}login'.format(api)

    try:
        r = requests.post(login, data)
        guid = r.json()
        return guid
    except Exception as e:
        print('Error: {}'.format(e)


def get_template(template_type):
    """Takes a string as input, finds an empty template and returns the template as a dict"""
    empty = '{}empty?template={}&guid={}'.format(api, template_type, guid)
    print(empty)
    r = requests.get(empty)
    return r.json()


def put_divider(divider, projectid):
    """Takes a divider template dict that's been assigned a name and other optional values and
    PUTs it onto the FileBound server
    Dividers can only be assigned to separators if separators are enabled and exist prior to the divider"""
    dumped_divider = json.dumps(divider)
    put_string = '{}projects/{}/dividers?guid={}'.format(api, projectid, guid)
    print(put_string)
    r = requests.put(put_string, dumped_divider, headers = fbheaders)
    #print(r.text)
    return(r.text)


def put_separator(separator, projectid):
    """Takes a separator template dict that's been assigned a name and other optional values and
    PUTs it onto the FileBound server
    If a divider will be assigned to a separator, enable separators and add the separators first"""
    dumped_separator = json.dumps(separator)
    put_string = '{}projects/{}/separators?guid={}'.format(api, projectid, guid)
    print(put_string)
    r = requests.put(put_string, dumped_separator, headers = fbheaders)
    #print(r.text)
    return(r.text)


def read_text_file(path_to_text_file):
    """Takes a sting path as input, reads its contents and returns a tuple containing the values in its rows"""
    sep_list = []; div_list = []
    with open(path_to_text_file, "r") as csvfile:
        reader = csv.reader(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            sep_list.append(row[0])
            div_list.append(row[1])
        return list(zip(sep_list, div_list))
        

text_path = 'C:/Users/dcarson/Desktop/divs.txt'

contents = read_text_file(text_path)
print(contents)

        
divider_list = ['ayy', 'bee', 'cee', 'dee', 'eee', 'eff', 'gee']
separator_list = ['one', 'two', 'three']




if __name__ == '__main__':
    print('Running code as main')
    guid = login()
    divider_template = get_template('divider')
    separator_template = get_template('separator')
    count = 0

    for sep in separator_list:
        new_sep = separator_template.copy()
        new_sep['name'] = sep
        put_separator(new_sep, projectid)

    for div in divider_list:
        new_div = divider_template.copy()
        new_div['name'] = div
        new_div['separator'] = separator_list[count%3]
        count += 1
        put_divider(new_div, projectid)


exit()


