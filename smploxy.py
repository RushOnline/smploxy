#!/usr/bin/env python
# -*- coding: utf8 -*-

from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.protocols.basic import LineOnlyReceiver
from pprint import pprint
from urlparse import parse_qs

# SMPlayer 0.7.0 (SVN r3809)
# Type help for a list of commands

# C add_files_start
# S OK, send first file
# C add_files <file>
# add_files_end

from twisted.internet.protocol import Protocol

class SMPlayer(LineOnlyReceiver):
    def __init__(self, *args, **kwargs):
        self.item = kwargs['item']

    def lineReceived(self, line):
        print line
        if 'commands' in line:
            self.transport.write("add_files_start\r\n")
        elif 'send first file' in line:
            response = "add_files %s\r\nadd_files_end\r\n" % self.item
            print response
            self.transport.write(response)
            
            self.transport.loseConnection()

class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return """<html>
<body>
<h1>SMPloxy: SMPlayer WebProxy</h1>
Usage:

$.post('http://localhost:8001/', {command: 'playlist.add', item: 'http://www.youtube.com/watch?v=VIDEO_ID'});

</body>
</html>
"""

    def render_POST(self, request):
        content = parse_qs(request.content.read())
        pprint(content)
        command = content.get('playlist.add', [None])[0]
        item = content['item'][0]
        creator = ClientCreator(reactor, SMPlayer, item = item)
        creator.connectTCP('127.0.0.1', 8000)
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Content-Type', 'application/json')
        return '{"success": true}'

site = server.Site(Simple())
reactor.listenTCP(8001, site)
reactor.run()
