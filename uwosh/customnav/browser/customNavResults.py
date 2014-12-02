from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import common
from Acquisition import aq_inner 
from zope.component import getMultiAdapter
from zope.interface import implements


from Products.CMFCore.ActionInformation import Action

class NavigationView(BrowserView):
    
    ##__call__ = ViewPageTemplateFile('dropdown.pt') esc period - ctrl - u - esc - period


    def getNavFolder(self):
        navFolder = self.context.restrictedTraverse('customNavFolder')
        return navFolder

    def getCurrentLevel(self, item):
        navFolder = self.getNavFolder()
        getCurrentLevel = len(item.getPhysicalPath()) - len(navFolder.getPhysicalPath())
        return getCurrentLevel

    def getCurrentObject(self, object):
        currentObject = self.context.get(object)
        return currentObject

    def getDepthOfCurrentObject(self, object):
        currentObject = self.getCurrentObject(object)
        depthOfCurrentObject = self.getCurrentLevel(currentObject)
        return depthOfCurrentObject
    
    def getItemsInFolder(self, folder):
        itemsInFolder = len(folder.objectIds())
        return itemsInFolder
        
    def getDepthOfStructure(self, folderToStartFrom):
        deepestFolder = 1
        if folderToStartFrom.portal_type == 'Folder':
            if len(currentFolder.objectIds()) > 0:
                for items in currentFolder:
                    itemsInSubfolder = items.getItemsInFolder()
                    if items.portal_type == 'Folder':
                        while itemsInSubfolder > 0:
                            folderLevel = getDepthOfCurrentObject(items)
                            if folderLevel > deepestFolder:
                                deepestFolder = folderLevel
                            getDepthOfStructure(items)
            return deepestLevel
                    
    def _formatFolderToNavStructure(self, folder):##should not be called TTW
        folderParent = 'folder parent'#folder.aq_parent()
        folderLevel = self.getCurrentLevel(folder)
        folderName = folder.getId()
        folderItems = []
        for item in folder.values():
            if item.portal_type == 'Folder':
                folderItems.append(self._formatFolderToNavStructure(item))
            elif item.portal_type == 'Link':
                folderItems.append(self._formatLinkToNavStructure(item))
                
        folder = {'object-type':'display-title',
                  'parent':folderParent,
                  'level':folderLevel,
                  'dropdown-title-name':folderName,
                  'items':folderItems}
                  
        return folder

    def _formatLinkToNavStructure(self, link):##should not be called TTW
        remoteUrl = link.getRemoteUrl()
        linkName = link.getId()
        linkLevel = self.getCurrentLevel(link)
        linkParent = 'the links parent'

        link = {'object-type':'link',
                'parent':linkParent,
                'level':linkLevel,
                'link-title-name':linkName,
                'link-url':remoteUrl}

        return link

    def addItemsInFolderToNavStructure(self, folder):
        navFolder = self.getNavFolder()
        for item in folder.values():
            if item.portal_type == 'Folder':
          
                folder = self._formatFolderToNavStructure(item)##recurse after adding the folder so they are in proper order
                navFolder.navigationStructure.append(folder)
                self.addItemsInFolderToNavStructure(item) 
            elif item.portal_type == 'Link':
                link = self._formatLinkToNavStructure(item)
                navFolder.navigationStructure.append(link)


    def getNavigation(self):

        navFolder = self.getNavFolder()
        navFolder.navigationStructure = []
        cnfItems = navFolder.values()
        cnfItemsOM = navFolder.objectMap()
        if len(navFolder.objectIds()) > 0:
            for items in cnfItems:
                if self.getCurrentLevel(items) == 1 and items.portal_type == 'Folder':
                    folderName = items.getId()
                    portal_tab_id = {'Portal Tab Name':folderName}
                    navFolder.navigationStructure.append(portal_tab_id)
                    self.addItemsInFolderToNavStructure(items)
                    navStructure = navFolder.navigationStructure
                                               
                elif self.getCurrentLevel(items) != 1 or items.portal_type != 'Folder':
                    navStructure = 'Only folders are allowed in the first level of the folder'###Complete this to throw an error stating only 1st level folders allowed

            ##move items to end of dict, reorder the elements in a dict

            return navStructure##to check the navStructure... remove eventually

    def extractPortalTabLink(self, folder):
        fDesc = folder.getRawDescription()##says string object is not callable???
        if fDesc.find('<tablink>') != -1:
            startIndex = fDesc.index('<tablink>')##need to get description
            if fDesc[startIndex:].find('</tablink>') != -1:
                endIndex = fDesc.index('</tablink>')
                PTLink = fDesc[startIndex+9:endIndex]
                removeLink = fDesc[startIndex:endIndex+10]
                fDesc.replace(removeLink, '')##remove the link after it has been set
                folder.setDescription(fDesc)
            elif fDesc[startIndex:].find('</tablink>') == -1:
                PTLink = ''

        if fDesc.find('<tablink>') == -1:
            PTLink = ''

        return PTLink
       
    def createPortalTabs(self):
        self.getNavigation()
        self.deleteTabsNotInCustomNavFolder()
        pa = getToolByName(self,'portal_actions')
        pt = pa.portal_tabs
        navFolder = self.getNavFolder()
        ns = navFolder.navigationStructure
        portalTabsToAdd = []##tabs to add to the site gathered from 1st level folder in CN folder
        tabsList = []##current list of portal_tabs
        n = 0
        for items in ns:
            for item in ns[n]:
                if item == 'Portal Tab Name':
                    if ("cn_tab_" + ns[n]['Portal Tab Name']) not in pt.objectIds():##check for previously created cn_tab
                        portalTabsToAdd.append(ns[n]['Portal Tab Name'])
                else:
                    pass
            if n != (len(ns) - 1):
                n = n + 1###RETURNS THE LIST OF PORTAL TABS TO ADD  
        tabsToDelete = []##need this?
        itemsAdded = []##need this? 
        for item in portalTabsToAdd:##item == 'Portal Tab Name'
            item = "cn_tab_" + item
            if item in pt.objectIds():
                pass    
            elif item not in pt.objectIds():
                itemName = ""
                itemName = item.replace('cn_tab_','')
                itemName = itemName.replace('-', ' ')
                itemName = itemName.title()##Format the title of the portal tab so it looks nicer...to upper case and replace hyphens with spaces
                subFolder = item.replace('cn_tab_', '')
                thisFolder = navFolder[subFolder]##get child object of cnf that had this id
                PTlink = self.extractPortalTabLink(thisFolder)
                PTlink = "string:" + PTlink
                action = Action(id=item, title=itemName, url_expr=PTlink, permissions=['View', 'Access contents information'])##need to add access contents information
                pt._setObject(item, action)##def _setObject(self, id, object):
                pt._setPropValue( 'subItems', [] )##create list to hold subitems
                pt[item].indexObject()


        request = self.context.REQUEST
        request.response.redirect(self.context.absolute_url())

    def deleteTabsNotInCustomNavFolder(self):
        
        pa = getToolByName(self,'portal_actions')
        pt = pa.portal_tabs
        navFolder = self.getNavFolder()
        ns = navFolder.navigationStructure
        n = 0
        portalTabsInCNFolder = []
        for items in ns:
            for item in ns[n]:
                if item == 'Portal Tab Name':
                    if ("cn_tab_" + ns[n]['Portal Tab Name']) not in pt.objectIds():##check for previously created cn_tab
                        portalTabsInCNFolder.append(ns[n]['Portal Tab Name'])
                else:
                    pass
            if n != (len(ns) - 1):
                n = n + 1###RETURNS THE LIST OF PORTAL TABS IN CN FOLDER
        
        for tab in pt.objectIds():
            if tab.startswith("cn_tab_"):
                if tab not in portalTabsInCNFolder:
                    getTab = pt.get(tab)
                    id = getTab.id
                    pt._delObject(id)
                    ##def _delObject(self, id):
        
   ###FORCE PAGE REFRESH AFTER ADDING TABS?
    def returnBrowser(self):

        REQUEST=self.context.REQUEST['HTTP_USER_AGENT']

        ##identity=REQUEST.HTTP_USER_AGENT.replace('/',' ').lower()
        ##identity=identity.replace('(','')
        ##identity=identity.replace(')','')
        ##identity=identity.replace(';','')
        ##identityParts=identity.split(' ')
            
        return REQUEST


