import os, json, requests
from requests.models import Response
from tabulate import tabulate

def login(email, passwd):
    login_url = 'https://api.granular.ai/europa/auth/v2/login'
    register_url = 'https://api.granular.ai/europa/auth/v2/register'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    data = {
        'email': email,
        'password': passwd
    }

    response = requests.post(login_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        resdata = response.json()
        token = resdata['accessToken']

        return token
    else:
        print('failed to authenticate')
        print('authentication endpoint {} returned with HTTP status code : {}'.format(login_url, response.status_code))
        print('please register at {} if you havent'.format(register_url))

        return None


def get_labels(properties, labelmaps):
    labels = { key: [] for res in properties['responses'] for key in res }
    
    for res in properties['responses']:
        for key in res:
            labels[key].append(res[key][0])

    for key in labels:
        llist = []
        for i in range(len(labels[key])):
            llist.append(labelmaps[i][labels[key][i]])
        labels[key] = llist
    
    return labels

def get_image_details(id, headers):
    image_url = 'http://api.granular.ai/europa/api/v1/images/{}'

    response = requests.get(image_url.format(id), headers=headers)

    if response.status_code == 200:
        image = response.json()['image']
        return image['tiles'], image['geometry'], image['status']
    else:
        print('image details cannot be retrieved')
        print('image meta endpoint {} returned with HTTP status code : {}'.format(image_url.format(id), response.status_code))
        return None, None, None
        
def get_all_tasks_eu(email, passwd):
    get_task_url = 'https://api.granular.ai/europa/api/v1/tasks'
    
    token = login(email, passwd)
    
    if token is None:
        print('authentication token could not retrieved. exiting')
        return

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.get(get_task_url, headers=headers)

    if response.status_code == 200:
        tasks = response.json()['tasks']
        table = [[task['id'], task['name']] for task in tasks]

        print('\nList of Europa Tasks:\n')
        print(tabulate(table, headers=['ID', 'Name', 'Description'], tablefmt='pretty'))
        print()
    else:
        print('all Europa tasks cannot be retrieved')
        print('tasks endpoint {} returned with HTTP status code : {}\n'.format(get_task_url, response.status_code))

def get_task_details_eu(id, email, passwd):
    task_details_url = 'https://api.granular.ai/europa/api/v1/tasks/{}'

    token = login(email, passwd)
    
    if token is None:
        print('authentication token could not retrieved. exiting')
        return

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.get(task_details_url.format(id), headers=headers)
    
    if response.status_code == 200:
        ignorelist = ['populateCounter', 'owner', 'createdAt', 'updatedAt', 'deteledAt', 'annotators']
        
        print('\nTask Details:\n')
        
        task = response.json()['task']
        for key in task.keys():
            if key == 'questions':
                print(key+' : \n')
                for qstn in task[key]:
                    print('name : {}'.format(qstn['name']))
                    print('description : {}'.format(qstn['description']))
                    print('response options : {}'.format(qstn['responseOptions']))
                    print()
            elif key not in ignorelist:
                print('{} : {}'.format(key, task[key]))

        print()
    else:
        print('task details cannot be retrieved')
        print('task details endpoint {} returned with HTTP status code : \n'.format(task_details_url.format(id), response.status_code))

def get_annotations_eu(id, path, email, passwd):
    task_url = 'https://api.granular.ai/europa/api/v1/tasks/{}'
    annotations_url = 'http://api.granular.ai/europa/api/v1/annotations'

    token = login(email, passwd)

    if token is None:
        print('authentication token could not retrieved. exiting')
        return
    
    print('adding task details')

    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.get(task_url.format(id), headers=headers)

    if response.status_code != 200:
        print('cannot retrieve annotation labelmaps as task details cannot be retrieved')
        print('task details endpoint {} returned with HTTP status code : {}\n'.format(task_url.format(id), response.status_code))
        return

    task = response.json()['task']
    labelmaps = [question['responseOptions'] for question in task['questions']]

    with open(os.path.join(path,'task.json'),'w') as out:
        json.dump(task, out, indent=4)

    print('retrieving annotations metadata')

    payload = {'task_id': id,
               'status': 'annotated'}
    response = requests.get(annotations_url, params=payload, headers=headers)

    if response.status_code != 200:
        print('annotations cannot be retrieved')
        print('annotations endpoint {} returned with HTTP status code : {}\n'.format(annotations_url, response.status_code))
        return

    data = response.json()

    images = [ann['imageId'] for ann in data['annotations']]
    images = list(set(images))

    for image in images:
        print('retrieving and saving annotations for image : {}'.format(image))

        entry = {}
        entry['id'] = image
        entry['tiles'], entry['geometry'], entry['status'] = get_image_details(id=image, headers=headers) 
        entry['annotations'] = [{'geometry': ann['geometry'], 'labels': get_labels(ann['properties'], labelmaps=labelmaps), 'type': ann['type']} for ann in data['annotations'] if ann['imageId'] == image]

        if entry['status'] == 'complete':
            with open(os.path.join(path, '{}.json'.format(image)), 'w') as out:
                json.dump(entry, out, indent=4)
