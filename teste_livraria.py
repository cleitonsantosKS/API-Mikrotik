from librouteros import connect
import time

# Conectar ao dispositivo MikroTik
# connection = connect(username='admin', password='', host='10.0.0.154')
api.path = connect(username='admin', password='', host='192.168.1.55')


# First create desired path.
interfaces = api.path('interface')
# Traverse down into /interfaces/ethernet
ethernet = interfaces.join('ethernet')

# path() and join() accepts multiple arguments
ips = api.path('ip', 'address')


# Path objects are iterable
tuple(interfaces)
# This also will work, as well as anything else you can do with iterables
for item in interfaces:
    print(item)