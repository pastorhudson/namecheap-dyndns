import argparse
import urllib.request
import xml.etree.ElementTree as ET

def get_ip():
	req = urllib.request.Request(url='https://dynamicdns.park-your-domain.com/getip')
	response = urllib.request.urlopen(req)
	ip = response.read().decode('utf-8')
	return ip

def change_ip(domain, host, ip, password):
	request_url_pattern = 'https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain}&password={password}&ip={ip}'
	request_url = request_url_pattern.format(host=host, domain=domain, password=password, ip=ip)
	request = urllib.request.Request(request_url)
	response = urllib.request.urlopen(request)
	response = response.read().decode('utf-8')
	root = ET.fromstring(response)
	ip = root.find('IP').text
	errcount = root.find('ErrCount').text
	done = root.find('Done').text
	return {'ip' : ip, 'errors' : int(errcount)}

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--host', required=True)
	parser.add_argument('--domain', required=True)
	parser.add_argument('--password', required=True)
	args = parser.parse_args()
	return args

def main():
	args = parse_args()
	ip = get_ip()
	status = change_ip(domain=args.domain, host=args.host, ip=ip, password=args.password)

	if (status['ip'] != ip or status['errors'] != 0):
		print('ERROR')
	else:
		print('OK')

if __name__ == '__main__':
	main()