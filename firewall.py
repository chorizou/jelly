from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

log = core.getLogger()

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here... '''
        msg = of.ofp_flow_mod()
        msg.priority = 42000
        msg.match.dl_src = EthAddr("00:00:00:00:00:02")
        msg.match.dl_dst = EthAddr("00:00:00:00:00:03")
        # to block packets, don't give an action / output port
        event.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    core.registerNew(Firewall)
