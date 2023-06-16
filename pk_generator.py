# -*- coding: utf-8 -*-


from os import path, getenv

import requests

from auth import Auth0


def run():
    proxy = getenv('CHATGPT_PROXY', None)
    expires_in = 0
    unique_name = getenv('UNIQUE_NAME', 'my share token')
    pool_token = getenv('POOL_TOKEN', '')
    current_dir = path.dirname(path.abspath(__file__))
    credentials_file = path.join(current_dir, 'file', 'credentials.txt')
    tokens_file = path.join(current_dir, 'file', 'tokens.txt')
    share_tokens_file = path.join(current_dir, 'file', 'share_tokens.txt')

    with open(credentials_file, 'r', encoding='utf-8') as f:
        credentials = f.read().split('\n')
    credentials = [credential.split(',', 1) for credential in credentials]

    count = 0
    token_keys = []
    for credential in credentials:
        progress = '{}/{}'.format(credentials.index(credential) + 1, len(credentials))
        if not credential or len(credential) != 2:
            continue

        count += 1
        username, password = credential[0].strip(), credential[1].strip()
        print('Login begin: {}, {}'.format(username, progress))

        token_info = {
            'token': 'None',
            'share_token': 'None',
        }
        token_keys.append(token_info)

        try:
            token_info['token'] = Auth0(username, password, proxy).auth(True)
            print('Login success: {}, {}'.format(username, progress))
        except Exception as e:
            err_str = str(e).replace('\n', '').replace('\r', '').strip()
            print('Login failed: {}, {}'.format(username, err_str))
            token_info['token'] = err_str
            continue

        data = {
            'unique_name': unique_name,
            'access_token': token_info['token'],
            'expires_in': expires_in,
        }
        resp = requests.post('https://ai.fakeopen.com/token/register', data=data)
        if resp.status_code == 200:
            token_info['share_token'] = resp.json()['token_key']
            print('share token: {}'.format(token_info['share_token']))
        else:
            err_str = resp.text.replace('\n', '').replace('\r', '').strip()
            print('share token failed: {}'.format(err_str))
            token_info['share_token'] = err_str
            continue

    with open(tokens_file, 'w', encoding='utf-8') as f:
        for token_info in token_keys:
            f.write('{}\n'.format(token_info['token']))

    with open(share_tokens_file, 'w', encoding='utf-8') as f:
        for token_info in token_keys:
            f.write('{}\n'.format(token_info['share_token']))

    if count > 20:
        print('too many accounts!')
        return

    data = {
        'share_tokens': '\n'.join([token_info['share_token'] for token_info in token_keys]),
        'pool_token': pool_token
    }
    resp = requests.post('https://ai.fakeopen.com/pool/update', data=data)

    if resp.status_code == 200:
        print('pool token: {}', resp.json()['pool_token'])
    else:
        print('generate pool token failed: {}'.format(resp.text))


if __name__ == '__main__':
    run()
