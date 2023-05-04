#
# Owner: Utkarsh Shukla
# Created date: 20 January,202
# Version: 1.0
# Description: Custom Script to Capture User's Input to Cancel WO
# LANGUAGE: python
# Script: WPD_WOCANCEL
# Launchpoint: Attribute --> Status, Object -->WOCHANGESTATUS
# Event : Run Action 
#
# Version History##
#
###------------------------------------------------------------------------------------------------------------
# Version       Developer          Date Modified          Reason for modifiaction       Developer Comments            
###------------------------------------------------------------------------------------------------------------
#
# Intial Draft  Utkarsh Shukla     20 January,2022            Original script                  Created                   
#
#--------------------------------------------------------------------------------------------------------------

###-------------------------------------------------------------------------------------------------------------
# Import Librarires
###-------------------------------------------------------------------------------------------------------------

from psdi.server import MXServer 
from psdi.common.context import UIContext
from psdi.webclient.system.controller import SessionContext, Utility, WebClientEvent

###------------------------------------------------------------------------------------------------------------------
# Define your Variables
###------------------------------------------------------------------------------------------------------------------

ownerMbo=mbo.getOwner()
context = UIContext.getCurrentContext()
###------------------------------------------------------------------------------------------------------------------
# Define your Functions 
###------------------------------------------------------------------------------------------------------------------          
def closeDialog():
    if context:
        wcs = context.getWebClientSession()
        Utility().sendEvent(WebClientEvent("dialogclose", wcs.getCurrentPageId(), None, SessionContext(wcs)))
###------------------------------------------------------------------------------------------------------------------
# Main Program
###------------------------------------------------------------------------------------------------------------------
if ownerMbo and ownerMbo.isBasedOn("WORKORDER"):
    currentStatus = mbo.getString("STATUS")
    if currentStatus in ('CAN','CANCEL','CANWORK'):
        def yes(): 
            ownerMbo.setValue("STATUS",currentStatus , 11L)
            #ownerMbo.changeStatus(currentStatus, MXServer.getMXServer().getDate(), "Set by "+ user)
            service.log("Yes Button has been Pressed")
            ownerMbo.getThisMboSet().save()
            closeDialog()
        def no(): 
            service.log("No Button has been Pressed")
            closeDialog()
            # v_required = False; 
        def dflt(): 
            service.log("dflt") 
          
            service.yncerror("wpd_cancel", "wpd_wo_cancel") 
        cases = {service.YNC_NULL:dflt, service.YNC_YES:yes, service.YNC_NO:no} 
        if interactive:
            x = service.yncuserinput() 
            cases[x]()
