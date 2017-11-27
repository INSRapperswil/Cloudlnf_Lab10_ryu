#!/usr/bin/python
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI


class Clos(Topo):
    """Clos topology example."""

    """Init.
        leaf: number of leaf switches
        spine: number of spine switches"""
    def __init__(self, leaf=3, spine=2):
        """Create custom topology."""
        self.net = Mininet(topo=None)
        self.spines = []
        self.leafs = []

        # Initialize topology
        Topo.__init__(self)

        # Add leaf switches with hosts
        for leaf_nr in range(0, leaf):
            leaf_sw = self.net.addSwitch('l'+str(leaf_nr), failMode='secure', protocols='OpenFlow13')
            self.leafs.append(leaf_sw)
            host = self.net.addHost('h'+str(leaf_nr))
            self.net.addLink(leaf_sw, host)

        # Add spine switches
        for spine_nr in range(0, spine):
            spine_sw = self.net.addSwitch('s'+str(spine_nr), failMode='secure', protocols='OpenFlow13')
            self.spines.append(spine_sw)

        # addLink leafs to all spines
        for spine_link in self.spines:
            for leaf_link in self.leafs:
                self.net.addLink(spine_link, leaf_link)

        self.net.start()
        CLI(self.net)
        self.net.stop()


topos = {'clos': (lambda leaf, spine: Clos(leaf, spine))}