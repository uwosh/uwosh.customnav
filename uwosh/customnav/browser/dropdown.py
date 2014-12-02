from Acquisition import aq_inner 
from zope.component import getMultiAdapter
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.ram import cache
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.portlets.navigation import Assignment
from plone.app.layout.viewlets import common
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from uwosh.customnav.browser.interfaces import ICustomNavDropdownViewlet
from uwosh.customnav.browser.customNavResults import NavigationView

class CustomNavDropdownViewlet(common.GlobalSectionsViewlet):##GlobalSectionsViewlet, navTreeProperties, selected_portal_tabs

    implements(ICustomNavDropdownViewlet)
    
    def _render_cachekey(fun, self):
        context = aq_inner(self.context)
        anonymous = getToolByName(context, 'portal_membership').isAnonymousUser()

        def get_language(context, request):
            portal_state = getMultiAdapter(
                (context, request), name=u'plone_portal_state')
            return portal_state.locale().getLocaleID()
        
        return ''.join((
            self.selected_portal_tab,
            get_language(aq_inner(self.context), self.request),          
            str(anonymous),          
        ))

    _template = ViewPageTemplateFile('dropdownSectionsTable.pt')##calling this instead of normal rendering of this section

    @cache(_render_cachekey)
    def cached_viewlet(self):##for each individual tab?
        return xhtml_compress(self._template())

    def index(self):
        if self.enable_caching:
            return self.cached_viewlet()

        else:
            return self._template()

    def update(self):
        common.ViewletBase.update(self)
        super(CustomNavDropdownViewlet, self).update()
        self.dropdown_properties = getToolByName(self.context, 'portal_properties').dropdown_properties
        self.enable_caching = self.dropdown_properties.getProperty('enable_caching', False)
        ##create configlet with CustomNavDropdownProperties

    def _parseDict(self, dict):
        mySubItems = []
        if dict['object-type'] == 'link':
            mySubItems.append(dict['link-title-name'])
        if dict['object-type'] == 'display-title':
            mySubItems.append(dict['dropdown-title-name'])


        return mySubItems

    def formatTitle(self, title, level):##add indentation to the title
        fTitle = ""
        n = 0
        indent = '\t'
        while n < level:
            indent = indent + '\t'
            n = n + 1
        title = title.title()
        title = title.replace('-',' ')
        fTitle = indent + title

        return fTitle

    def getItemIndex(self, item, subItems):
        itemIndex = subItems.index(item)
        return itemIndex

    def isCustomNavTab(self, tab):##CHECK IF IT IS A PORTAL TAB... OTHER WAY TO DO THIS?
        isCustomNavTab = 0
        if tab.has_key('category'):
            if tab['category'] == 'portal_tabs':
                if tab['id'].startswith('cn_tab_'):
                    isCustomNavTab = 1
                elif not tab['id'].startswith('cn_tab_'):
                    isCustomNavTab = 0

            elif tab['category'] != 'portal_tabs':
                isCustomNavTab = 0
        elif not tab.has_key('category'):
            isCustomNavTab = 0
        return isCustomNavTab

    def getSubItems(self, tab):
        ##if the results are cached get them instead
        navFolder = self.context.restrictedTraverse('customNavFolder')##just do this once... not on every iteration
        navStructure = navFolder.navigationStructure
        subItems = []##what we will return
            ##iterate over navStructre starting at index right after name of portal tab and ending one index before next portal tab or end of list
            ##get Index of this portal tab

        n = 0
        ignoredTabs = ['Members','events','news','index_html','customNavFolder']
        nsLen = len(navStructure)
        if tab['id'] in ignoredTabs:
            return []##if the passed tab is in the ignored tabs return immediately as it is pointless to iterate over these
        elif tab['id'] not in ignoredTabs:
            for items in navStructure:
                if items.has_key('Portal Tab Name'):
                    if not tab['id'].startswith('cn_tab_'):
                        return []
                    elif tab['id'].startswith('cn_tab_'):
                        if tab['id'].replace('cn_tab_','') != items['Portal Tab Name']:
                            pass##pass or return
                        if tab['id'].replace('cn_tab_','') == items['Portal Tab Name']:
                            indexOfTab = navStructure.index(items)

                            if navStructure.index(navStructure[indexOfTab]) < (nsLen - 1):##so index out of range error is not thrown
                                if 'Portal Tab Name' in navStructure[indexOfTab+1].keys():##throwing IndexError: list index out of range on cob site##fixed
                                    pass##there are no subitems for this tab                     

                                elif 'Portal Tab Name' not in navStructure[indexOfTab+1].keys():
                                    indexOfNextTab = 0
                                    for dict in navStructure[indexOfTab+1:]:##give me a dictionary representing each item
                                        i = 0
                                        if dict.has_key('Portal Tab Name'):##much more concise
                                            return subItems##should always return something that can evaluate to true or false LOOK AT THIS 
                                        elif not dict.has_key('Portal Tab Name'):
                                            subItems.append(dict)
                            elif navStructure.index(navStructure[indexOfTab]) == (nsLen - 1):##last element in list
                                if 'Portal Tab Name' in navStructure[indexOfTab].keys():##if portal tab is last item
                                    return subItems##there are obviously no subitems
                                    
                        
            else:
                pass
#             if n != (len(navStructure) - 1):
#                 n = n + 1
        if len(subItems) > 0:##need this condition since there is one in the pt
            subItems = subItems##returns the slice of items relevant to the passed portal tab

        else:
            subItems = []

        return subItems

