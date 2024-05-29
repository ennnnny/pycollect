import requests
import json
import os

PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DATA_BASE = os.path.join(PATH, "data")

if __name__ == "__main__":
    gist_id2 = os.environ.get("GIST_ID2", "")
    pat = os.environ.get("GIST_PAT", "")
    sub_store = os.environ.get("SUB_STORE", "")

    headers = {'Authorization': 'token ' + pat}
    response = requests.get('https://api.github.com/gists/'+gist_id2, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        data2 = json.loads(data['files']['Sub-Store']['content'])

        local_file = os.path.join(DATA_BASE, "subscribes.txt")
        file = open(local_file, "r")
        content = file.read()
        file.close()
        data2['subs'][2]['url'] = content

        data['files']['Sub-Store']['content'] = json.dumps(data2)
        json_data = json.dumps(data)
        update_response = requests.patch('https://api.github.com/gists/'+gist_id2, headers=headers, data=json_data)

        if update_response.status_code != 200:
            print('Failed to update Gist')
        else:
            print('Gist updated')
            requests.get('https://sub2.paomian.party/'+sub_store+'/api/utils/backup?action=download')
    else:
        print('Failed to get Gist')
