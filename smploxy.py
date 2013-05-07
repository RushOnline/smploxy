#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
from urlparse import parse_qs

from twisted.web import server, resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.protocols.basic import LineOnlyReceiver
from twisted.python.failure import Failure
#from pprint import pprint

# SMPlayer 0.7.0 (SVN r3809)
# Type help for a list of commands
# add_files_start
# OK, send first file
# add_files http://mds.datagrad.ru/download/cothuk/mp3/721-Moris_Richardson-Den_nashej_pobedy_nad_Marsom.mp3
# OK, file received
# add_files_end
# OK, sending files to GUI


class SMPlayer(LineOnlyReceiver):
    def __init__(self, *args, **kwargs):
        self.item = kwargs['item']

    def lineReceived(self, line):
        if line == 'Type help for a list of commands':
            self.transport.write("add_files_start\r\n")
        elif line == 'OK, send first file':
            self.transport.write("add_files %s\r\n" % self.item)
        elif line == 'OK, file received':
            self.transport.write("add_files_end\r\n")
        elif line == 'OK, sending files to GUI':
            self.transport.write("quit\r\n")
        elif line == 'Goodbye':
            self.transport.loseConnection()

class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return '''
            <html>
            <body>
            <h1>SMPloxy: SMPlayer WebProxy</h1>
            Usage:

            $.post('http://localhost:8001/', {command: 'playlist.add', item: 'http://www.youtube.com/watch?v=VIDEO_ID'});

            </body>
            </html>
            '''

    def render_POST(self, request):

        def _renderResponse(response):
            if isinstance(response, Failure):
                request.write(json.dumps({'success': False, 'message': response.getErrorMessage()}))
            else:
                request.write(json.dumps({'success': True}))
            request.finish()

        content = parse_qs(request.content.read())

        command = content.get('playlist.add', [None])[0]
        item = content['item'][0]

        creator = ClientCreator(reactor, SMPlayer, item = item)
        creator.connectTCP('127.0.0.1', 8000).addBoth(_renderResponse)

        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Content-Type', 'application/json')
        return NOT_DONE_YET

site = server.Site(Simple())
reactor.listenTCP(8001, site)
reactor.run()
