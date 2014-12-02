from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils
ADD_CONTENT_PERMISSION = "Add portal content"

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    content_types, constructors, ftis = atapi.process_types(atapi.listTypes('uwosh.customnav'), 'uwosh.customnav')

    cmfutils.ContentInit(
        'uwosh.customnav Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)
