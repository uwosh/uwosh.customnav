from persistent.list import PersistentList 
from Products.CMFCore.utils import getToolByName

def import_all(self):
    site = self.getSite()
    
    if 'customNavFolder' not in site.objectIds():
        site.invokeFactory(type_name="Folder", id="customNavFolder")
        site['customNavFolder'].setTitle('Custom Navigation Folder')
        site['customNavFolder'].allowedContentTypes(['File', 'Link', 'Folder'])
        site['customNavFolder'].manage_permission('View', roles=['Manager'], acquire=0)
        site['customNavFolder'].manage_permission('Access contents information', roles=['Manager'], acquire=0)
        site['customNavFolder'].manage_permission('List folder contents', roles=['Manager'], acquire=0)
        site['customNavFolder'].setExcludeFromNav(True)
        site['customNavFolder'].navigationStructure = PersistentList()##added but not showing up in schema
        site.portal_workflow.doActionFor(site['customNavFolder'], 'publish')

