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
""" index implementation

$Id$
"""
from zope import interface
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.traversing.api import getParents
from zope.app.intid.interfaces import IIntIds
from zc.catalog.index import SetIndex, parseQuery

from interfaces import IPathIndex


class PathIndex(SetIndex):
    interface.implements(IPathIndex)

    def _get_values(self, value, includeValue=False):
        try:
            intid = getUtility(IIntIds)
            parents = getParents(value)
        except:
            return None

        if includeValue:
            parents.append(value)

        ids = []
        for ob in parents:
            id = intid.queryId(removeAllProxies(ob))
            if id is not None:
                ids.append(id)

        if ids:
            return ids
        else:
            return None

    def index_doc(self, doc_id, value):
        values = self._get_values(value)
        if values is not None:
            super(PathIndex, self).index_doc(doc_id, values)

    def apply(self, query):
        orig_query = query
        query_type, query = parseQuery(query)
        if query_type == 'any_of':
            result = None
            for value in query:
                values = self._get_values(value, True)
                if values is not None:
                    res = super(PathIndex, self).apply({'all_of': values})
                    if result is None:
                        result = res
                    else:
                        result.update(res)
            return result
        elif query_type == 'all_of':
            # this query types is useless for path index
            return None
        elif query_type == 'between':
            # not implemented
            return None

        return super(PathIndex, self).apply(orig_query)
