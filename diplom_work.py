import requests
import time


TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
user_id = 171691064

class User():    

    def __init__(self, access_token, user_id):
        self.access_token = TOKEN
        self.user_id = user_id

    def get_user_group(self):
        """Функция для получения множества групп пользователя"""
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
        user_group_id = response_id.json()['response']['items']

        return user_group_id

    def get_user_friends(self):
        """Функция для получения списка друзей"""
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
        user_friends_id = response_friends.json()['response']['items']

        return user_friends_id

    def get_friends_groups(self, user_friends_id, user_group_id):
        """Функция которая получает разницу id групп пользователя и id групп его друзей"""
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
            for key in r.items():
                if key == 'response':
                    for i in user_group_id:
                        if i in r['response']['items']:
                            friends_group_id.append(i)
                    print(f'{friends_id} добавлен в список')
                else:
                    print(f'{friends_id} исключен из списка')
            time.sleep(0.2)
        sort_friends_group_id = set(friends_group_id)

        return sort_friends_group_id

    def write_file(self, sort_friends_group_id):
        """Функция получающая информацию о группах и записывающая в файл результат"""
        for group in sort_friends_group_id:
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

            with open('Groups.json', 'a') as f:
                f.write(f'{str(g)}, +\n')

user = User(TOKEN, user_id)
user.get_user_group()
user.get_user_friends()
user.get_friends_groups(user_friends_id, user_group_id)
user.write_file(sort_friends_group_id)