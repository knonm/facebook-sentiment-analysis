import facebookAPI
import yaml

file_stream = open('feeds.yaml', 'r')

try:
    data = yaml.load(file_stream)
except yaml.YAMLError as exc:
    print(exc)
    
file_stream.close()

fields = 'id,created_time,description,link,name,type,message,message_tags'

page = facebookAPI.request_API('344408492407172/posts', 'limit=2&fields=%s' % (fields))

page = facebookAPI.request_API('%s' % (data[key]['fb_id']), 'fields=id,name')

print(page)

# for key in data:
#     fields = 'id,created_time,description,link,name,type,message,message_tags'
#     page = facebookAPI.request_API(
#         '%s/posts' % (data[key]['fb_id']),
#         'limit=100&fields=%s' % (fields))
