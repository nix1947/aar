from mininet.net import Mininet
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI


class AarTopology(Topo):
    """Application aware routing custom toplogy"""

    def __init__(self):
        """Initialize base class topology"""

        Topo.__init__(self)
        hosts = [
            self.addHost('h%s' % (n + 1)) for n in range(6)
        ]
        switches = [
            self.addSwitch('s%s' % (n + 1)) for n in range(6)
        ]
       
        for i in range(3):
            self.addLink(
                hosts[i], 
                switches[0],
                bw=100, 
                delay="2ms",
                max_queue_size=1000,
                use_htb=True
            )  # add host1, host2, and host3 to switch

        for i in range(3, 6):
            self.addLink(
                hosts[i], 
                switches[5], 
                bw=100, 
                delay="2ms", 
                max_queue_size=1000,
                use_htb=True
            )  # add host4, host5, and host6 to switch6

        # Connect s1 and s2 switch with 100mb link with 2ms delay
        self.addLink(
            switches[0], 
            switches[1],
            bw=100, 
            delay="2ms", 
            max_queue_size=1000, 
            use_htb=True
        )

        # connect s2 and s3 with 100mb and 10 ms
        self.addLink(
            switches[1], 
            switches[2], 
            bw=100, 
            delay="10ms", 
            max_queue_size=1000, 
            use_htb=True
        )

        # connect s2 and s5 with 10mb and 2ms delay
        self.addLink(
            switches[1], 
            switches[4], 
            bw=10, 
            delay="2ms", 
            max_queue_size=1000, 
            use_htb=True
        )

        # connect s3 and s4 100mb and 10ms delay
        self.addLink(
            switches[2], 
            switches[3], 
            bw=100, 
            delay="10ms", 
            max_queue_size=1000, 
            use_htb=True
        )

        # connect s4 and s5 switches with 10mb and 2ms delay link
        self.addLink(
            switches[3], 
            switches[4], 
            bw=10, 
            delay="2ms", 
            max_queue_size=1000, 
            use_htb=True
        )

        # connect s4 and s6 switch with 100mb and 2ms delay link
        self.addLink(
            switches[3], 
            switches[5], 
            bw=100, 
            delay="2ms",
            max_queue_size=1000, 
            use_htb=True
        )


def build_network():
    topo = AarTopology()
    network = Mininet(topo, link=TCLink)
    network.start()

    # h1, h2, s1 = network['h1'], network['h2'], network['s1']
    h1, h4 = network.hosts[0], network.hosts[2]
    print
    h1.cmd("ping -c1 %s" % h4.IP())
    h1 = network['h1']
    # virtual host can accept the bash commands
    h1.cmd('while true; do date; sleep 1; done > /tmp/date.out &')
    result = h1.cmd('ifconfig')
    print
    result
    CLI(network)
    network.stop()


def main():
    build_network()


if __name__ == "__main__":
    main()

topos = {'mytopo': (lambda: AarTopology())}
