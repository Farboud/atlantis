import os
import csv
import json
import requests
from datetime import datetime

# Key:
api_key = 'da03d4d2c9d70753c5b918009711b9ea'

# Secret:
secret = 'f35c6f99121e3e83'

# natural_list = list()
artificial_list = list()

# with open('list.csv', encoding="utf8", errors='ignore') as csvfile:
#     list_csv_dict = csv.DictReader(csvfile)
#     for row in list_csv_dict:
#         natural_list.append(row.get('natural'))
#         artificial_list.append(row.get('artificial'))

# natural_list = list(filter(None, natural_list))
# artificial_list = list(filter(None, artificial_list))

artificial_list = ['reservoir', 'water reservoir', 'spillway' 'spillway dam',
                   'morning glory spillway', 'hole spillway', 'swimming pool', 'water well']


licenses = [
    {"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
        "id": 1, "name": "Attribution-NonCommercial-ShareAlike License"},
    {"url": "http://creativecommons.org/licenses/by-nc/2.0/",
        "id": 2, "name": "Attribution-NonCommercial License"},
    {"url": "http://creativecommons.org/licenses/by-nc-nd/2.0/",
        "id": 3, "nameswimming pool": "Attribution-NonCommercial-NoDerivs License"},
    {"url": "http://creativecommons.org/licenses/by/2.0/",
        "id": 4, "name": "Attribution License"},
    {"url": "http://creativecommons.org/licenses/by-sa/2.0/",
        "id": 5, "name": "Attribution-ShareAlike License"},
    {"url": "http://creativecommons.org/licenses/by-nd/2.0/",
        "id": 6, "name": "Attribution-NoDerivs License"},
    {"url": "http://flickr.com/commons/usage/", "id": 7,
        "name": "No known copyright restrictions"},
    {"url": "http://www.usa.gov/copyright.shtml",
        "id": 8, "name": "United States Government Work"}
]

os.chdir('/home/serfani/Downloads/images_pn2')
# emp_dir = os.mkdir('images_pn2')
main_dir = os.getcwd()

for dir1 in artificial_list:
    for num in range(len(licenses)):
        file_path = os.path.join(dir1, str(licenses[num].get('id')))
        file_path2 = os.path.join(main_dir, file_path)
        os.makedirs(file_path2)

        tag = dir1
        license_type = licenses[num].get('id')
        per_page = 50
        page_number = 2

        url = 'https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key={api_key}&tags={tag}&license={license_type}&is_commons=&per_page={per_page}&page={page_number}&format=json&nojsoncallback=1'.format(
            api_key=api_key, tag=tag, license_type=license_type, per_page=per_page, page_number=page_number)
        r = requests.get(url)
        data = r.json()

        for element in data['photos']['photo']:
            del element['title'], element['owner'], element['ispublic'], element['isfriend'], element['isfamily']
            element['license'] = licenses[num].get('id')
            element['flickr_url'] = 'https://farm{farm_id}.staticflickr.com/{server_id}/{id}_{secret}_z.jpg'.format(
                farm_id=element['farm'], server_id=element['server'], id=element['id'], secret=element['secret'])
            element['file_name'] = str(element['id']) + '.jpg'
            element['date_captured'] = datetime.now(
            ).strftime("%m/%d/%Y, %H:%M:%S")

            # "flickr.photos.getSizes" method to add width and length information of the images
            url2 = 'https://www.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={api_key}&photo_id={photo_id}&format=json&nojsoncallback=1'.format(
                api_key=api_key, photo_id=element['id'])
            r2 = requests.get(url2)
            data2 = r2.json()
            for dictionary in data2['sizes']['size']:
                if dictionary['label'] == "Medium 640":
                    element['width'] = int(dictionary['width'])
                    element['height'] = int(dictionary['height'])
                    break
                else:
                    element['width'] = 640
                    element['height'] = 480

        # dump a json file
        with open(os.path.join(file_path2, 'json_file.json'), 'w') as tf:
            json.dump(data, tf, indent=2)

        # save the images as "id.jpg"
        for element in data['photos']['photo']:
            try:
                img_lnk = requests.get('https://farm{farm_id}.staticflickr.com/{server_id}/{id}_{secret}_z.jpg'.format(
                    farm_id=element['farm'], server_id=element['server'], id=element['id'], secret=element['secret']))
                with open(os.path.join(file_path2, element['file_name']), 'wb') as tf2:
                    tf2.write(img_lnk.content)
            except OSError:
                print('File name too long')
            except (requests.ConnectTimeout, requests.HTTPError, requests.ReadTimeout, requests.Timeout, requests.ConnectionError):
                print(' Max retries exceeded with url')
        print('license {} has been downloaded'.format(num))
    print('label {} has been done'.format(dir1))
print('mission complete')
