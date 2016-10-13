import os
from tesla import envloader

#if os.path.exists('/usr/local/nb/nbserver/config/public_transit_feeds.conf'):
#    envloader.load_configuration(globals(), '/usr/local/nb/nbserver/config/public_transit_feeds.conf')
#elif os.path.exists('/usr/local/nb/nbserver/baseconfig/public_transit_feeds.conf'):
#    envloader.load_configuration(globals(), '/usr/local/nb/nbserver/baseconfig/public_transit_feeds.conf')
#else:
#    envloader.load_configuration(globals(), './public_transit_feeds.conf')
envloader.load_configuration(globals(), './public_transit_feeds.conf')
