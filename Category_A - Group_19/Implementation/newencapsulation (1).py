#!/usr/bin/python
from mininet.net import Containernet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Link, TCLink
from mininet.link import Intf
import time
import glob, os


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()



def mytopo():

        net = Containernet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )
        # define 8 routers and assign IP to them
        r1 = net.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = net.addHost('r2', cls=LinuxRouter, ip='1.1.1.2/24')
        r3 = net.addHost('r3', cls=LinuxRouter, ip='2.2.2.2/24')
        r4 = net.addHost('r4', cls=LinuxRouter, ip='4.4.4.2/24')
        r5 = net.addHost('r5', cls=LinuxRouter, ip='6.6.6.2/24')
        r6 = net.addHost('r6', cls=LinuxRouter, ip='3.3.3.2/24')
        r7 = net.addHost('r7', cls=LinuxRouter, ip='7.7.7.2/24')
        r8 = net.addHost('r8', cls=LinuxRouter, ip='10.0.1.1/24')

        c0 = net.addController( 'c0', controller=Controller, ip='127.0.0.1', port=6633 )

        # Add 2 switches
        s1 = net.addSwitch('s1')
        s2 = net.addSwitch('s2')
        s3 = net.addSwitch('s3')
        s4 = net.addSwitch('s4')

        # connection between routers and switches and assign IP to the routers' interfaces
        net.addLink(
                     r1,s1,
                     intfName1='r1-eth0',
                     params1={'ip': '10.0.0.1/24'})

        net.addLink(
                     r8,s2,
                     intfName1='r8-eth0',
                     params1={'ip': '10.0.1.1/24'})
        net.addLink(
                     r1,s3,
                     intfName1='r1-eth2',
                     params1={'ip': '20.20.20.1/24'})
        net.addLink(
                     r8,s4,
                     intfName1='r8-eth2',
                     params1={'ip': '10.5.5.1/24'})
        
       # router-router connection and assign IP to the routers' interfaces
        net.addLink(r1,
                     r2,
                     intfName1='r1-eth1',
                     intfName2='r2-eth0',
                     params1={'ip': '1.1.1.1/24'},
                     params2={'ip': '1.1.1.2/24'})

        net.addLink(r2,
                     r3,
                     intfName1='r2-eth1',
                     intfName2='r3-eth0',
                     params1={'ip': '2.2.2.1/24'},
                     params2={'ip': '2.2.2.2/24'})

        net.addLink(r2,
                     r6,
                     intfName1='r2-eth2',
                     intfName2='r6-eth0',
                     params1={'ip': '3.3.3.1/24'},
                     params2={'ip': '3.3.3.2/24'})

        net.addLink(r3,
                     r4,
                     intfName1='r3-eth1',
                     intfName2='r4-eth0',
                     params1={'ip': '4.4.4.1/24'},
                     params2={'ip': '4.4.4.2/24'})

        net.addLink(r4,
                     r6,
                     intfName1='r4-eth1',
                     intfName2='r6-eth1',
                     params1={'ip': '5.5.5.1/24'},
                     params2={'ip': '5.5.5.2/24'})
        net.addLink(r6,
                     r7,
                     intfName1='r6-eth2',
                     intfName2='r7-eth0',
                     params1={'ip': '7.7.7.1/24'},
                     params2={'ip': '7.7.7.2/24'})

        net.addLink(r4,
                     r5,
                     intfName1='r4-eth2',
                     intfName2='r5-eth0',
                     params1={'ip': '6.6.6.1/24'},
                     params2={'ip': '6.6.6.2/24'})
        net.addLink(r5,
                     r8,
                     intfName1='r5-eth1',
                     intfName2='r8-eth1',
                     params1={'ip': '8.8.8.2/24'},
                     params2={'ip': '8.8.8.1/24'})


        net.addLink(r7,
                     r5,
                     intfName1='r7-eth1',
                     intfName2='r5-eth2',
                     params1={'ip': '9.9.9.1/24'},
                     params2={'ip': '9.9.9.2/24'})






        # Adding hosts specifying the default route
        d1 = net.addDocker(name='d1',
                          ip='10.0.0.251/24',
                          defaultRoute='via 10.0.0.1',dimage='phonehost:latest')
        d2 = net.addDocker(name='d2',
                          ip='10.0.0.252/24',
                          defaultRoute='via 10.0.0.1',dimage='phonehost:latest')

        d3 = net.addDocker(name='d3',
                          ip='10.0.1.251/24',
                          defaultRoute='via 10.0.1.1',dimage='phonehost:latest')

        d4 =  net.addDocker(name='d4',
                          ip='10.0.1.252/24',
                          defaultRoute='via 10.0.1.1',dimage='phonehost:latest')
        sv1 = net.addDocker(name='sv1',
                          ip='20.20.20.5/24',
                          defaultRoute='via 20.20.20.1',dimage='callserv:latest')
        sv2 = net.addDocker(name='sv2',
                          ip='10.5.5.5/24',
                          defaultRoute='via 10.5.5.1',dimage='dhcp_server:latest')
        d5 =  net.addDocker(name='d5',
                          ip='10.5.5.15/24',
                          defaultRoute='via 10.5.5.1',dimage='phonehost:latest')

      # Add host-switch link
        net.addLink(d1, s1)
        net.addLink(d2, s1)
        net.addLink(d3, s2)
        net.addLink(d4, s2)
        net.addLink(sv1,s3)
        net.addLink(sv2,s4)
        net.addLink(d5,s4)
        
        net.build()
        c0.start()
        s1.start( [c0] )
        s2.start( [c0] )
        s3.start( [c0] )
        s4.start( [c0] )

        # assign MAC in the routers'(r1 & r8) interfaces and OVS filtering in the switches
        info(net['r1'].cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01"))
        info(net['r8'].cmd("ifconfig r8-eth0 hw ether 00:00:00:00:01:02"))
        info(net['r1'].cmd("ifconfig r1-eth2 hw ether 00:00:00:00:01:03"))
        info(net['r8'].cmd("ifconfig r8-eth2 hw ether 00:00:00:00:01:04"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=00:00:00:00:01:01,actions=output:1"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=10.0.1.251,nw_dst=10.0.0.251,actions=output:2"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=10.0.1.252,nw_dst=10.0.0.251,actions=drop"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=20.20.20.5,nw_dst=10.0.0.251,actions=output:2"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=10.0.1.252,nw_dst=10.0.0.252,actions=output:3"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=10.0.1.251,nw_dst=10.0.0.252,actions=drop"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=20.20.20.5,nw_dst=10.0.0.252,actions=output:3"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=10.5.5.5,nw_dst=10.0.0.251,actions=output:2"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=10.5.5.5,nw_dst=10.0.0.252,actions=output:3"))
        info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=d5 ,nw_dst=10.0.0.252,actions=output:3"))

        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=1,arp,actions=flood"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:01:02,actions=output:1"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=10.0.0.251,nw_dst=10.0.1.251,actions=output:2"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=10.0.0.252,nw_dst=10.0.1.251,actions=drop"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=20.20.20.5,nw_dst=10.0.1.251,actions=output:2"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=10.0.0.252,nw_dst=10.0.1.252,actions=output:3"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=10.0.0.251,nw_dst=10.0.1.252,actions=drop"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=20.20.20.5,nw_dst=10.0.1.252,actions=output:3"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=10.5.5.5,nw_dst=10.0.1.251,actions=output:2"))
        info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=10.5.5.5,nw_dst=10.0.1.252,actions=output:3"))
        info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=1,arp,actions=flood"))
        info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=65535,ip,dl_dst=00:00:00:00:01:03,actions=output:1"))
        info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_dst=20.20.20.5,actions=output:2"))
        info(net['s4'].cmd("ovs-ofctl add-flow s4 priority=1,arp,actions=flood"))
        info(net['s4'].cmd("ovs-ofctl add-flow s4 priority=65535,ip,dl_dst=00:00:00:00:01:04,actions=output:1"))
        info(net['s4'].cmd("ovs-ofctl add-flow s4 priority=10,ip,nw_dst=10.5.5.5,actions=output:2"))
        info(net['s4'].cmd("ovs-ofctl add-flow s4 priority=10,ip,actions=output:3"))
       
        #info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_dst=20.20.20.5,actions=output:3"))
     
    # Add routing for reaching networks that aren't directly connected
        
        info(net['r1'].cmd("ip route add 2.2.2.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 4.4.4.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 6.6.6.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 4.4.4.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 8.8.8.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 3.3.3.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 7.7.7.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 9.9.9.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r1'].cmd("ip route add 5.5.5.0/24  via 1.1.1.2 dev r1-eth1"))
        info(net['r2'].cmd("ip route add 4.4.4.0/24  via 2.2.2.2  dev r2-eth1"))
        info(net['r2'].cmd("ip route add 6.6.6.0/24  via 2.2.2.2 dev r2-eth1"))
        info(net['r2'].cmd("ip route add 8.8.8.0/24   via 2.2.2.2 dev r2-eth1"))
        info(net['r2'].cmd("ip route add 7.7.7.0/24   via 3.3.3.2 dev r2-eth2"))
        info(net['r2'].cmd("ip route add 5.5.5.0/24   via 3.3.3.2 dev r2-eth2"))
        info(net['r2'].cmd("ip route add 9.9.9.0/24   via 3.3.3.2 dev r2-eth2"))
        info(net['r3'].cmd("ip route add 1.1.1.0/24   via 2.2.2.1 dev r3-eth0"))
        info(net['r3'].cmd("ip route add 3.3.3.0/24   via 2.2.2.1 dev r3-eth0"))
        info(net['r3'].cmd("ip route add 5.5.5.0/24   via 4.4.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 7.7.7.0/24   via 4.4.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 6.6.6.0/24   via 4.4.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 9.9.9.0/24   via 4.4.4.2 dev r3-eth1"))
        info(net['r3'].cmd("ip route add 8.8.8.0/24   via 4.4.4.2 dev r3-eth1"))
        info(net['r4'].cmd("ip route add 1.1.1.0/24   via 4.4.4.1 dev r4-eth0"))
        info(net['r4'].cmd("ip route add 2.2.2.0/24   via 4.4.4.1 dev r4-eth0"))
        info(net['r4'].cmd("ip route add 3.3.3.0/24   via 5.5.5.2 dev r4-eth1"))
        info(net['r4'].cmd("ip route add 7.7.7.0/24   via 6.6.6.2 dev r4-eth2"))
        info(net['r4'].cmd("ip route add 9.9.9.0/24   via 6.6.6.2 dev r4-eth2"))
        info(net['r4'].cmd("ip route add 8.8.8.0/24   via 6.6.6.2 dev r4-eth2"))
        

        info(net['r5'].cmd("ip route add 4.4.4.0/24   via 6.6.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 2.2.2.0/24   via 6.6.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 1.1.1.0/24   via 6.6.6.1 dev r5-eth0"))
        
        info(net['r5'].cmd("ip route add 3.3.3.0/24   via 6.6.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 5.5.5.0/24   via 6.6.6.1 dev r5-eth0"))
        info(net['r5'].cmd("ip route add 7.7.7.0/24   via 9.9.9.1 dev r5-eth2"))
        

        
        info(net['r6'].cmd("ip route add 1.1.1.0/24   via 3.3.3.1 dev r6-eth0"))
        info(net['r6'].cmd("ip route add 2.2.2.0/24   via 3.3.3.1 dev r6-eth0"))
        info(net['r6'].cmd("ip route add 4.4.4.0/24   via 5.5.5.1 dev r6-eth1"))
        info(net['r6'].cmd("ip route add 6.6.6.0/24   via 3.3.3.1 dev r6-eth0"))
        info(net['r6'].cmd("ip route add 9.9.9.0/24   via 7.7.7.2 dev r6-eth2"))
        info(net['r6'].cmd("ip route add 8.8.8.0/24   via 7.7.7.2 dev r6-eth2"))
        

        
        info(net['r7'].cmd("ip route add 1.1.1.0/24   via 7.7.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 2.2.2.0/24   via 7.7.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 3.3.3.0/24   via 7.7.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 5.5.5.0/24   via 7.7.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 4.4.4.0/24   via 7.7.7.1 dev r7-eth0"))
        info(net['r7'].cmd("ip route add 6.6.6.0/24   via 9.9.9.2 dev r7-eth1"))
        info(net['r7'].cmd("ip route add 8.8.8.0/24   via 9.9.9.2 dev r7-eth1"))
        
        info(net['r8'].cmd("ip route add 1.1.1.0/24   via 8.8.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 2.2.2.0/24   via 8.8.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 3.3.3.0/24   via 8.8.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 4.4.4.0/24   via 8.8.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 5.5.5.0/24   via 8.8.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 6.6.6.0/24   via 8.8.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 7.7.7.0/24   via 8.8.8.2 dev r8-eth1"))
        info(net['r8'].cmd("ip route add 9.9.9.0/24   via 8.8.8.2 dev r8-eth1"))



#Adding subsequent GRE and MPLS links R1,R8
    # apply GRE on r1 and r8

        info(net['r1'].cmd('ip tun a foo1 mode gre remote 8.8.8.1 local 1.1.1.1'))
        info(net['r1'].cmd('ip addr a 100.100.100.1 dev foo1'))
        info(net['r1'].cmd('ip link set foo1 up'))
        info(net['r1'].cmd('ip rou a 100.100.100.0/24 dev foo1'))
        info(net['r8'].cmd('ip tun a foo1 mode gre remote 1.1.1.1 local 8.8.8.1'))
        info(net['r8'].cmd('ip addr a 100.100.100.2 dev foo1'))
        info(net['r8'].cmd('ip link set foo1 up'))
        info(net['r8'].cmd('ip rou a 100.100.100.0/24 dev foo1'))


 # apply MPLS on r1 and r8

        info(net['r1'].cmd('sysctl -w net.ipv4.conf.all.rp_filter=2'))
        info(net['r1'].cmd('sysctl -w net.mpls.platform_labels=65535'))
        info(net['r1'].cmd('sysctl -w net.mpls.conf.foo1.input=1'))
        info(net['r1'].cmd('ip rou c 100.100.100.0/24 encap mpls 100 dev foo1'))
        info(net['r1'].cmd('ip -f mpls rou a 101 dev lo'))

        info(net['r8'].cmd('sysctl -w net.ipv4.conf.all.rp_filter=2'))
        info(net['r8'].cmd('sysctl -w net.mpls.platform_labels=65535'))
        info(net['r8'].cmd('sysctl -w net.mpls.conf.foo1.input=1'))
        info(net['r8'].cmd('ip rou c 100.100.100.0/24 encap mpls 101 dev foo1'))
        info(net['r8'].cmd('ip -f mpls rou a 100 dev lo'))

        r1.cmd('ip route add 10.0.1.0/24 encap mpls 100 via 100.100.100.2 dev foo1')
        r8.cmd('ip route add 10.0.0.0/24 encap mpls 101 via 100.100.100.1 dev foo1')
        r8.cmd('ip route add 20.20.20.0/24 encap mpls 101 via 100.100.100.1 dev foo1')
        r1.cmd('ip route add 10.5.5.0/24 encap mpls 100 via 100.100.100.2 dev foo1')
        CLI(net)
        net.stop()
   
  

if __name__ == '__main__':
    setLogLevel('info')
    mytopo()
