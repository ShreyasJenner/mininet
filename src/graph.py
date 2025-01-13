#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller, CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.topo import MultiGraph
from mininet.log import setLogLevel
from mininet.clean import Cleanup
import re

# function to calculate cost of a link
def calc_link_cost(params):
    k = 10
    if 'bw' in params:
        bw = params['bw']
    if 'delay' in params:
        match = re.match(r"(\d+)", params['delay'])
        if match:
            delay = int(match.group(1))
    if 'loss' in params:
        loss = params['loss']

    return (delay/bw) * (1 + (k * loss))

# function to add devices and links
def add_devices_links(net):
    # add devices to network
    net.addController('c0')  
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    # Add links between hosts and the switch
    net.addLink(h1, s1, bw=10, delay='5ms', loss=2)
    net.addLink(h2, s2, bw=10, delay='5ms', loss=2)
    net.addLink(h3, s3, bw=10, delay='5ms', loss=2)
    net.addLink(s1, s2, bw=10, delay='5ms', loss=2)
    net.addLink(s2, s3, bw=10, delay='5ms', loss=2)
    net.addLink(s3, s1, bw=10, delay='5ms', loss=2)


# function to cosntruct graph out of topology
def build_graph(net):
    graph = MultiGraph()

    # add hosts, links, controllers and switches to graph
    for host in net.hosts:
        graph.add_node(host.name, type='host')

    for switch in net.switches:
        graph.add_node(switch.name, type='switch')

    for controller in net.controllers:
        graph.add_node(controller.name, type='controller')

    for link in net.links:
        node1 = link.intf1.node.name
        node2 = link.intf2.node.name
        param = net.links[0].intf1.params
        graph.add_edge(node1, node2, cost=calc_link_cost(param),
                params=param)

    return graph

# function to create topology and start cli
def simple_topology():
    net = Mininet(controller=Controller,host=CPULimitedHost,link=TCLink)

    # Start the network
    net.start()
    
    # add device and links
    add_devices_links(net)

    # get graph
    graph = build_graph(net)
    print(graph.edges(data=True))

    # Start the CLI
    print("Starting Mininet CLI...")
    CLI(net)

    # Stop the network
    net.stop()

if __name__ == '__main__':
    Cleanup()
    simple_topology()
