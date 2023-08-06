""" GET
"""
# -*- coding: utf-8 -*-
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class EEARelations(object):
    """ Get backward forward and auto relations
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"eea.relations": {
            "@id": "{}/@eea.relations".format(self.context.absolute_url())
        }}
        if not expand:
            return result

        if IPloneSiteRoot.providedBy(self.context):
            return result

        objrview = self.context.restrictedTraverse('eea.relations.macro', None)
        relations = objrview and objrview.forward_backward_auto() or None
        relations_dict = {}
        if relations:
            wftool = getToolByName(self.context, 'portal_workflow')
            for relation_tuples in relations:
                res_list = []
                relation_label = relation_tuples[0]
                relations_list = relation_tuples[1]
                for obj in relations_list:
                    obj_dict = {'title': obj.Title(), '@type': obj.portal_type,
                                '@id': obj.absolute_url(),
                                'description': obj.Description(),
                                'is_expired': obj.isExpired(),
                                'review_state': wftool.getInfoFor(obj,
                                                                'review_state')}
                    res_list.append(obj_dict)
                relations_dict[relation_label] = res_list

            result["eea.relations"]['items'] = json_compatible(
                relations_dict)
        return result


class EEARelationsGet(Service):
    """Get eea.relations information"""

    def reply(self):
        """ Reply
        """
        info = EEARelations(self.context, self.request)
        return info(expand=True)["eea.relations"]
