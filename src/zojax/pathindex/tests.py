##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" zojax.pathindex  tests

$Id$
"""
__docformat__ = "reStructuredText"

import os, sys
import unittest, doctest
from zope import interface
from zope.component import provideAdapter, getSiteManager, provideUtility
from zope.app.testing import setup
from zope.traversing import testing
from zope.location.interfaces import ILocation
from zope.app.container.sample import SampleContainer

from persistent import Persistent
from persistent.interfaces import IPersistent
from transaction import commit
from ZODB.interfaces import IConnection
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.keyreference.persistent import KeyReferenceToPersistent
from zope.app.keyreference.persistent import connectionOfPersistent
from zope.app.keyreference.interfaces import IKeyReference


class ConnectionStub(object):
    next = 1

    def db(self):
        return self

    database_name = 'ConnectionStub'
    
    def add(self, ob):
        ob._p_jar = self
        ob._p_oid = self.next
        self.next += 1


class Folder(Persistent, SampleContainer):
    interface.implements(ILocation)


def setUp(test):
    root = setup.placefulSetUp(site=True)
    testing.setUp()

    provideAdapter(connectionOfPersistent, (IPersistent,), IConnection)
    provideAdapter(KeyReferenceToPersistent, (IPersistent,), IKeyReference)

    utility = IntIds()
    provideUtility(utility, IIntIds)

    root._p_jar = ConnectionStub()

    root['folder1'] = Folder()
    root['folder1']['folder1_1'] = Folder()
    root['folder1']['folder1_1']['folder1_1_1'] = Folder()

    root['folder2'] = Folder()
    root['folder2']['folder2_2'] = Folder()
    root['folder2']['folder2_2']['folder2_2_2'] = Folder()

    utility.register(root)
    utility.register(root['folder1'])
    utility.register(root['folder1']['folder1_1'])
    utility.register(root['folder1']['folder1_1']['folder1_1_1'])
    utility.register(root['folder2'])
    utility.register(root['folder2']['folder2_2'])
    utility.register(root['folder2']['folder2_2']['folder2_2_2'])
    test.globs['root'] = root


def tearDown(test):
    setup.placefulTearDown()

def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite(
                'README.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
