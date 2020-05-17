
#Вводим id или имя пользователя
#Для введенного id получаем список групп, в которых он состоит (список 1)
#Для введеного id или имени получаем список друзей (список 2)
#для каждого друга из списка получаем список групп в которых он состоит (список 3)
#сводим список_1 и список_3 в множество set_1
#для полученного set_1 делаем операцию difference


import requests
import time


TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
user_id = 171691064

#получаем список ID групп пользователя
response_id = requests.get(
    "https://api.vk.com/method/groups.get",
    params = {
        'access_token': TOKEN,
        'user_id': user_id,
        'extended': 0,
        'v': 5.103
    }
)
print("Status code:", response_id.status_code)
user_group_id = set(response_id.json()['response']['items'])
#print(type(user_group_id))

#получаем список ID друзей пользователя
response_friends = requests.get(
    "https://api.vk.com/method/friends.get",
    params = {
        'access_token': TOKEN,
        'user_id': user_id,
        'order': 'name',
        'offset': 5,        
        'v': 5.103
    }
)

print("Status code:", response_friends.status_code)
#print(response_friends.json())

user_friends_id = response_friends.json()['response']['items']
#print(user_friends_id)

friends_group_id = []
for friends_id in user_friends_id:    
    response_id = requests.get(
        "https://api.vk.com/method/groups.get",
        params = {
            'access_token': TOKEN,
            'user_id': friends_id,
            'extended': 0,
            'v': 5.103
        }
    )
    print("Status code:", response_id.status_code)
    r = response_id.json()
    for key, value in r.items():
        if key == 'response':
            friends_group_id.append(r['response']['items'])
            print(f'{friends_id} добавлен в список')
        else:
            print(f'{friends_id} исключен из списка')
    time.sleep(0.4)

friends_group_id_set = []
for sort_id in friends_group_id:
    sort_id = tuple(sort_id)
    friends_group_id_set.append(sort_id)
sort_set = set(friends_group_id_set)
#print(sort_set)

sorted_group_id = user_group_id - sort_set
#sort_group = user_group_id.difference(sort_set)

#print(user_group_id)
print(sorted_group_id)
#print(sort_group)
time.sleep(1)

for group in sorted_group_id:
    response_group = requests.get(
        "https://api.vk.com/method/groups.getById",
        params= {
            'access_token': TOKEN,
            'group_ids': group,
            'fields': 'members_count',
            'v': 5.103
        }
    )
    time.sleep(1)
    print("Status code:", response_group.status_code)
    g = response_group.json()['response']
    print(g)
