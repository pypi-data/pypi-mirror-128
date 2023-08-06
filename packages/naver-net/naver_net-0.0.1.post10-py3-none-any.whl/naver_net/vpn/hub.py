#!/usr/bin/env python3

import socket 
import logging
import datetime 
import protocol


MAX_PACKET_SIZE = 8192
HOST_ADVERT_TIMEOUT_SEC = 60

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class VPNHub():
    def __init__(self, args, **kwargs):
        self.args = args | kwargs
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.hosts = {}
        self.main(self.args)

    def main(self):
        log.info('starting server at [%s]:%s' %
                 (self.args.addr, self.args.port))
        self.sock.bind((self.args.addr, self.args.port))

        try:
            self.main_loop()
        finally:
            log.info('closing server socket')
            self.sock.close()

    def main_loop(self):
        # hosts map (addr,port) -> ts_last_packet

        while True:
            try:
                packet = protocol.receive()
            except protocol.MalformedPacket as e:
                log.debug('skipping malformed packet: %s' % e)
                continue

            if packet.magic is not protocol.Magic.C2H:
                log.debug('non-c2h packet, ignoring')
                continue

            self.hosts[packet.peer] = datetime.datetime.now()

            c2h = packet.payload
            assert c2h is not None
            assert isinstance(c2h, protocol.Packet_c2h)

            self.broadcast_peer(packet.peer, c2h, self.hosts)

    def broadcast_peer(self,  src_peer, packet, hosts, ):
        log.debug('broadcasting: %s:%d' % src_peer)

        data = protocol.to_bytes(protocol.Magic.H2C, protocol.Packet_h2c(
            src_addr=src_peer[0], src_port=src_peer[1], protocol_version=packet.protocol_version, session_id=packet.session_id, ))

        # make a copy because iteration may delete stale entries
        now = datetime.datetime.now()
        for peer, ts_last_advert in list(hosts.items()):
            if (now - ts_last_advert).total_seconds() > HOST_ADVERT_TIMEOUT_SEC:
                log.debug('deleting stale host %s:%d' % peer)
                del hosts[peer]
            elif peer == src_peer:
                pass  # don't echo the packet back to the sender
            else:
                log.debug('  -> %s:%d' % peer)
                self.sock.sendto(data, peer)
