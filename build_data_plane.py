#!/usr/bin/python

## Example topology for containernet
## Created by Jorge Lopez 

"""
This is a simple example of a Containernet custom topology.
"""


from mininet.net import Containernet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import sys
setLogLevel('info')

#exec(open("./sflow-rt/extras/sflow.py").read())

net = Containernet()
info('*** Adding controller\n')
c0 = RemoteController( 'c0', ip=sys.argv[1], port=int(sys.argv[2]))
#c0 = RemoteController( 'c0', ip='127.0.0.1', port=6633)
net.addController(c0)
info('*** Adding docker containers\n')
h1 = net.addDocker('h1', ip='10.0.0.251', mac='9a:d8:73:d8:90:6a', dimage="ubuntu:trusty")
h2 = net.addDocker('h2', ip='10.0.0.252', mac='9a:d8:73:d8:90:6b', dimage="ubuntu:trusty")
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
net.addLink(h1, s1, 1, 1)
net.addLink(h2, s2, 1, 1)
net.addLink(s1, s2, 2, 2)
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
net.stop()


'''
from mininet.node import RemoteController
from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import sys
setLogLevel('info')

c0 = RemoteController('c0', ip='127.0.0.1', port=6633, protocols="OpenFlow13")

topo=LinearTopo(2)
#net = Mininet(topo=topo,switch=OVSSwitch,build=False, cleanup=True)
#net = Mininet(topo=topo,build=False, cleanup=True)
net = Mininet()
net.addController(c0)
s1 = net.addSwitch( 's1' )
#net.build()
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
net.stop()

print("qwe")
'''