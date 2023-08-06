""" Archetypes Referenceable patches
"""
from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName


def patched_optimizedGetObject(self, uid):
    tool = getToolByName(self, 'uid_catalog', None)
    if tool is None:  # pragma: no cover
        return ''
    tool = aq_inner(tool)
    traverse = aq_parent(tool).unrestrictedTraverse

    _catalog = tool._catalog
    rids = _catalog.indexes['UID']._index.get(uid, ())
    if isinstance(rids, int):
        rids = (rids,)

    for rid in rids:
        path = _catalog.paths[rid]
        obj = traverse(path, default=None)
        if obj is not None:
            return obj
    # 134485 get object from portal_catalog in case uid_catalog doesn't have it
    if not rids:
        ptool = getToolByName(self, 'portal_catalog', None)
        if ptool:
            brains = ptool(UID=uid)
            for brain in brains:
                try:
                    return brain.getObject()
                except Exception:
                    continue


def patched_getRefs(self, relationship=None, targetObject=None):
    """ getRefs patch to avoid returning None values """
    # get all the referenced objects for this object
    tool = getToolByName(self, 'reference_catalog')
    brains = tool.getReferences(self, relationship, targetObject=targetObject,
                                objects=False)
    if brains:
        results = []
        for b in brains:
            res = self._optimizedGetObject(b.targetUID)
            if res:
                results.append(res)
        return results
    return []
