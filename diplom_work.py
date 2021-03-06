import requests
import time
import json


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
        user_group_id = set(response_id.json()['response']['items'])

        return user_group_id

    def get_user_friends(self):
        """Функция для получения списка друзей"""
        response_friends = requests.get(
            "https://api.vk.com/method/friends.get",
            params = {
                'access_token': TOKEN,
                'user_id': user_id,
                'order': 'name',
                'offset': 0,        
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
            for key in r:
                if key == 'response':
                    for i in user_group_id:
                        if i in r['response']['items']:
                            friends_group_id.append(i)
                    print(f'{friends_id} добавлен в список')
                else:
                    print(f'{friends_id} исключен из списка')
            time.sleep(0.4)
        sort_friends_group_id = set(friends_group_id)

        return sort_friends_group_id

    def uniq_user_group(self, user_group_id, sort_friends_group_id):
        uniq_user_group = user_group_id - sort_friends_group_id

        return uniq_user_group

    def get_group_info(self, uniq_user_group):
        """Функция получающая информацию о группах"""
        group_list = []
        for group in uniq_user_group:
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
            group_list.append(g)

        return group_list

    def write_file(self, group_list):
        with open('Groups.json', 'a', encoding='utf-8') as f:
            json.dump(group_list, f, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

if __name__ == '__main__':
    user = User(TOKEN, user_id)
    user_group_id = user.get_user_group()
    user_friends_id = user.get_user_friends()
    sort_friends_group_id = user.get_friends_groups(user_friends_id, user_group_id)
    uniq_user_group = user.uniq_user_group(user_group_id, sort_friends_group_id)
    group_list = user.get_group_info(uniq_user_group)
    user.write_file(group_list)