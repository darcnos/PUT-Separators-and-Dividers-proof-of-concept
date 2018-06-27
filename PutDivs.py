import requests, json
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
    u = input('Username: ')
    p = input('Password: ')
    data = {
        'username': u,
        'password': p
    }
    login = '{}login'.format(api)
    print(login)

    try:
        #r = requests.post(login, data, verify=False)
        r = requests.post(login, data)
        guid = r.json()
        return guid
    except requests.exceptions.Timeout:
        print('Connection timed out. Please try again.')
    except requests.exceptions.TooManyRedirects:
        print('Too many redirects. Check your URL and try again.')
    except requests.exceptions.RequestException as e:
        print('Catastrophic error. Bailing.')
        print(e)
        sys.exit(1)


def get_template(template_type):
    empty = '{}empty?template={}&guid={}'.format(api, template_type, guid)
    print(empty)
    r = requests.get(empty)
    return r.json()


def put_divider(divider, projectid):
    dumped_divider = json.dumps(divider)
    put_string = '{}projects/{}/dividers?guid={}'.format(api, projectid, guid)
    print(put_string)
    r = requests.put(put_string, dumped_divider, headers = fbheaders)
    print(r.text)

def put_separator(separator, projectid):
    dumped_separator = json.dumps(separator)
    put_string = '{}projects/{}/separators?guid={}'.format(api, projectid, guid)
    print(put_string)
    r = requests.put(put_string, dumped_separator, headers = fbheaders)
    print(r.text)


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


