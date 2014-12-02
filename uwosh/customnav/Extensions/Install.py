from Products.CMFCore.utils import getToolByName

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-uwosh.customnav:default')
    return "Ran all import steps."

def uninstall(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-uwosh.customnav:uninstall')
    ##Remove all cn_tabs    
    pa = getToolByName(portal,'portal_actions')
    pt = pa.portal_tabs   
    for tab in pt.objectIds():
        if tab.startswith("cn_tab_"):
                getTab = pt.get(tab)
                id = getTab.id
                pt._delObject(id)

    ##Remove customNav folder
    portal.manage_delObjects('customNavFolder')
    
    
    return "Ran all uninstall steps."
