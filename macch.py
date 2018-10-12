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

oui =  ('b4:99:ba:','e0:43:db:','00:50:ba:','cc:46:d6:','48:ad:08:',
		'bc:ec:23:','38:f2:3e:','80:7a:bf:','00:1a:11:','00:11:75:','c4:e9:84:',
		'74:a7:8e:','8c:21:0a:','e4:d5:3d:','00:15:58:','00:50:56:','04:b1:67:',
		'00:e0:18:','74:5f:00:','bc:3b:af:','00:19:66:','00:08:ca:','54:fc:f0:',
		'40:cb:c0:','18:87:96:','f4:ca:24:','00:16:cf:','00:07:e9:','00:01:42:',
		'84:10:0d:','75:5a:67:','6c:e3:b6:','94:2c:b3:','00:40:26:','00:01:24:',
		'c0:98:79:','b0:45:15:','10:12:18:','64:00:2d:','ec:80:09:','00:16:d4:')

link = args.interface
def changemac(mac):
	subprocess.Popen('ip link set '+link+' down',shell=True)
	subprocess.Popen('ip link set '+link+' address '+mac,shell=True)
	subprocess.Popen('ip link set '+link+' up',shell=True)

def validmac():
	rnum = random.choice(range(16**6))
	hex_num = hex(rnum)[2:].zfill(6)
	mac = "{}{}{}:{}{}:{}{}".format(random.choice(oui),*hex_num)
	print('Новый валидный mac адрес на интерфейсе '+link,mac)
	return mac

def fullrandommac():
	octet = '%x%s:' % (random.randint(0x0,0xf),random.choice((0,2,4,6,8,'a','c','e')))
	mac = octet+':'.join(("%012x" % random.randint(0x0, 0xFFFFFFFFFFFF))[i:i+2] for i in range(0, 10, 2))
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
