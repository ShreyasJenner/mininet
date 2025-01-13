
#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller, CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.clean import Cleanup
from mininet.topo import MultiGraph
from mininet.node import OVSSwitch
from openflow_setup import set_openflow_rules
import re


def calc_link_cost(params):
    k = 10
    bw = params.get('bw', 1)
    delay = int(re.match(r"(\d+)", params.get('delay', '0ms')).group(1))
    loss = params.get('loss', 0)
    return (delay / bw) * (1 + (k * loss))


def add_devices_links(net):
    net.addController('c0')
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    net.addLink(h1, s1, bw=10, delay='5ms', loss=2)
    net.addLink(h2, s2, bw=10, delay='5ms', loss=2)
    net.addLink(h3, s3, bw=10, delay='5ms', loss=2)
    net.addLink(s1, s2, bw=10, delay='5ms', loss=2)
    net.addLink(s2, s3, bw=10, delay='5ms', loss=2)
    net.addLink(s3, s1, bw=10, delay='5ms', loss=2)


def build_graph(net):
    graph = MultiGraph()
    for host in net.hosts:
        graph.add_node(host.name, type='host')
    for switch in net.switches:
        graph.add_node(switch.name, type='switch')
    for link in net.links:
        node1 = link.intf1.node.name
        node2 = link.intf2.node.name
        params = link.intf1.params
        graph.add_edge(node1, node2, cost=calc_link_cost(params), params=params)
    return graph


def simple_topology():
    net = Mininet(controller=Controller, host=CPULimitedHost, link=TCLink, switch=OVSSwitch)
    net.start()
    add_devices_links(net)
    graph = build_graph(net)
    print("Starting Mininet CLI...")
    CLI(net)
    net.stop()


if __name__ == '__main__':
    Cleanup()
    setLogLevel('info')
    simple_topology()
