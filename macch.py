import random
import subprocess
import argparse

desc = 'Скрипт для смены mac адреса'
epilog = '''
Использование:
  macch.py -i eth0                         Сенерировать валидный мак аддрес и назначить интерфейсу eth0
  macch.py -i wlan0 -m 00:22:33:44:55:66   Назначить указаный мак адрес интерфейсу wlan0
  macch.py -i wlan0 -r                     Сгенерировать полностью случайный мак адрес и назначить интерфейсу wlan0
'''
parser = argparse.ArgumentParser(description=desc,add_help=False,epilog=epilog,usage=argparse.SUPPRESS,formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-i',dest='interface',help='Имя интерфейса на котором нужно поменять mac')
parser.add_argument('-m',dest='mac',help='Установить этот mac адрес, формат xx:xx:xx:xx:xx:xx')
parser.add_argument('-r',dest='frandom',action='store_true',help='Полностью рандомный mac, если не задано генерируется валидный')
parser.add_argument('-h','--help',action='help',default=argparse.SUPPRESS,help='Показать эту справку и выйти')
parser._optionals.title = 'Опциональные аргументы'
args = parser.parse_args()

if args.frandom is False and args.interface is None:
    exit(parser.print_help())
elif args.frandom and args.mac is not None and args.interface is None:
    exit(parser.print_help())
elif args.frandom and args.mac is None and args.interface is None:
    exit(parser.print_help())

oui =  ('98:de:d0:','dc:d9:16:','00:1c:26:','84:be:52:','00:08:22:','00:72:63:','9c:93:4e:','8c:79:67:','00:87:01:','88:79:7e:','50:9e:a7:','48:88:ca:','c8:d7:b0:',
        '54:27:58:','8c:77:16:','c4:85:08:','c8:38:70:','28:ed:6a:','f0:34:04:','58:12:43:','60:a4:4c:','14:9f:e8:','50:46:5d:','ac:f1:df:','00:1e:58:','c4:a8:1d:',
        'c8:91:f9:','64:66:b3:','44:e9:dd:','1c:74:0d:','74:b5:7e:','04:8d:38:','fc:f5:28:','e8:37:7a:','8c:10:d4:','b0:b2:dc:','28:28:5d:','60:31:97:','c0:4a:00:',
        '10:fe:ed:','04:bf:6d:','68:15:90:','84:16:f9:','f0:82:61:','b8:a3:86:','fc:a6:67:','1c:cd:e5:','bc:75:74:','00:15:af:','00:18:b0:','00:18:de:','00:1b:fc:',
        '00:08:ca:','ec:08:6b:','b4:99:ba:','e0:43:db:','00:50:ba:','cc:46:d6:','48:ad:08:','f0:a2:25:','8c:f5:a3:','d4:6e:0e:','e4:58:b8:','30:f3:35:','5c:93:a2:',
        'bc:ec:23:','38:f2:3e:','80:7a:bf:','00:1a:11:','00:11:75:','c4:e9:84:','d4:a1:48:','30:92:f6:','e0:aa:96:','2c:33:7a:','74:a7:8e:','8c:21:0a:','e4:d5:3d:',
        '00:15:58:','00:50:56:','04:b1:67:','80:26:89:','14:36:c6:','0c:8f:ff:','4c:b1:99:','74:da:38:','00:e0:18:','74:5f:00:','bc:3b:af:','00:19:66:','54:fc:f0:',
        '18:21:95:','00:0e:8f:','00:1f:ce:','98:0c:a5:','f8:1a:67:','40:cb:c0:','18:87:96:','f4:ca:24:','00:16:cf:','00:07:e9:','00:01:42:','30:75:12:','f4:6d:0d:',
        '00:c0:ca:','94:b1:0a:','28:3b:82:','84:10:0d:','75:5a:67:','6c:e3:b6:','94:2c:b3:','00:40:26:','00:01:24:','e8:94:f6:','68:05:71:','64:bc:0c:','b8:08:d7:',
        'e8:4e:06:','c0:98:79:','b0:45:15:','10:12:18:','64:00:2d:','ec:80:09:','00:16:d4:','bc:72:b1:','94:44:44:','b0:55:08:','00:1e:10:','00:27:15:','70:0b:c0:',
        '00:c0:fc:','24:2e:02:')

link = args.interface
def changemac(mac):
    subprocess.call('ip link set '+link+' down',shell=True)
    subprocess.call('ip link set '+link+' address '+mac,shell=True)
    subprocess.call('ip link set '+link+' up',shell=True)

def validmac():
    rnum = random.choice(range(16**6))
    hex_num = hex(rnum)[2:].zfill(6)
    mac = "{}{}{}:{}{}:{}{}".format(random.choice(oui),*hex_num)
    print('Новый валидный mac адрес на интерфейсе '+link,mac)
    return mac

def fullrandommac():
    octet = '%x%s:' % (random.randint(0x0,0xf),random.choice((0,2,4,6,8,'a','c','e')))
    mac = octet+':'.join(("%012x" % random.randint(0x0, 0xffffffffffff))[i:i+2] for i in range(0, 10, 2))
    print('Новый случайный mac адрес на интерфейсе '+link,mac)
    return mac

if args.mac is not None:
    mac = args.mac
    changemac(mac)
    print('Новый mac на интерфейсе '+link,mac)
elif args.frandom is False:
    changemac(validmac())
elif args.frandom:
    changemac(fullrandommac())
