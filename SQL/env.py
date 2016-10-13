# -*- python -*-
# env.py: created 2011/01/21.
#
# Copyright (C) 2008-2010 Networks In Motion, Inc. All rights reserved.
#
# The information contained herein is confidential and proprietary to
# Networks In Motion, Inc., and is considered a trade secret as
# defined in section 499C of the California Penal Code. Use of this
# information by anyone other than authorized employees of Networks
# In Motion is granted only under a written non-disclosure agreement
# expressly prescribing the scope and manner of such use.
#

"""ISMS. ENV"""

from tesla import envloader
envloader.load_configuration(globals(), '/usr/local/home/krozin/sqllite/sqlite.conf')

