import facebookAPI
import yaml
from urllib.parse import quote
import traceback

file_stream = open('feeds.yaml', 'r')
file_csv = open('feeds.csv', 'w+')

try:
    data = yaml.load(file_stream)
except yaml.YAMLError as exc:
    print(exc)

file_stream.close()

file_csv.write('%s;%s;%s;%s;%s' % ('Tipo', 'Desc', 'FB ID', 'YAML Name', 'Real Name'))

try:
    data_new = {}
    for key in data:
        # key_search = quote(key).format()
        if 'fb_id' in data[key]:
            try:
                page = facebookAPI.request_API('%s' % (data[key]['fb_id']), 'fields=id,name')
                if key in data_new:
                    data_new.pop(key)
                if 'tags' in data[key]:
                    data_new[page['name']] = {'fb_id': page['id'], 'tags': data[key]['tags']}
                else:
                    data_new[page['name']] = {'fb_id': page['id']}
                file_csv.write('INFO;%s;%s;%s;%s\n' % ('N/A', page['id'], key, page['name']))
            except facebookAPI.HTTPError as exc:
                file_csv.write('ERROR;%s;%s;%s;%s\n' % (exc.get_facebook_error(), data[key]['fb_id'], key, key))
        else:
            search_result = facebookAPI.request_API('search', 'q=%s&type=page' % (key))['data']
            if len(search_result) == 0:
                file_csv.write('WARNING;%s;%s;%s;%s\n' % ('Not found', 'N/A', key, 'N/A'))
            else:
                if key in data_new:
                    data_new.pop(key)
                if 'tags' in data[key]:
                    data_new[search_result[0]['name']] = {'fb_id': search_result[0]['id'], 'tags': data[key]['tags']}
                else:
                    data_new[search_result[0]['name']] = {'fb_id': search_result[0]['id']}
                file_csv.write('INFO;%s;%s;%s;%s\n' % ('Found', search_result[0]['id'], key, search_result[0]['name']))
    file_stream = open('feeds.yaml', 'w')
    yaml.dump(data_new, file_stream, default_flow_style=False, explicit_start=True, allow_unicode=True)
except Exception as exc:
    traceback.print_exc()
    print(data[key])
    
file_csv.close()
file_stream.close()

# print("%s - %s" % (key, fbid))

# facebookAPI.request_API('search', 'q=&type=page');

# print(facebookAPI.request_API('200292646669956/posts', 'fields=id&limit=100'))
