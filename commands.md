## MD file that stores helpful commands for mininet

- `node` ifconfig
 - Get information about the ip address of a node

- net
  - Get connection links between nodes

### command to view flow entries in a switch
- ovs-ofctl dump-flows s1 -O OpenFlow13
- ovs-ofctl dump-flows s2 -O OpenFlow13
- ovs-ofctl dump-flows s3 -O OpenFlow13

