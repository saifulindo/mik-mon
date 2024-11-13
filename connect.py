from librouteros import connect

api = connect(username='admin', password='123456', host='192.168.56.2')
for resource in api(cmd='/interface/print'):
    print(resource)