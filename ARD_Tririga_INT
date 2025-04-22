#
# Owner: Utkarsh Shukla
# Created date: 03 April, 2025
# Version: 1.0
# Description: Custom Script to pull the data from Tririga APIs
# LANGUAGE: JYTHON
# Script: ARD_TRIRIGA_INT
#
# Version History
#
###------------------------------------------------------------------------------------------------------------
# Version       Developer          Date Modified          Reason for modification       Developer Comments            
###------------------------------------------------------------------------------------------------------------
#
# Intial Draft  Utkarsh Shukla         03 April, 2025            Original script                  Created                   
#
#--------------------------------------------------------------------------------------------------------------

###-------------------------------------------------------------------------------------------------------------
# Import Librarires
###-------------------------------------------------------------------------------------------------------------
import java
from psdi.server import MXServer
from psdi.util import MXException
from java.lang import String
from java.util import HashMap
from psdi.iface.router import HTTPHandler
from com.ibm.json.java import JSON
###------------------------------------------------------------------------------------------------------------------
# Define Global Variable
###------------------------------------------------------------------------------------------------------------------
properties = HashMap()
#url = "http://universities.hipolabs.com/search?country=United+States"
url = "http://tririga.ardemas.io:9001/tririga/oslc/spq/triAPICOutboundWorkTaskQC"
params = "oslc.select=*&oslc.paging=true&oslc.page=1&oslc.pageSize=2"
woSet = mbo.getMboSet("$WORKORDER", "WORKORDER","1==2")

###------------------------------------------------------------------------------------------------------------------
# Define Functions
###------------------------------------------------------------------------------------------------------------------
def generateWO(WoTask,woSet):
    wo = woSet.add()
    wo.setValue("WONUM",str(WoTask.get(0).get("spi:triIdTX"))) #spi:triIdTX
    wo.setValue("DESCRIPTION",str(WoTask.get(0).get("spi:triNameTX"))) #spi:triNameTX
    if (str(WoTask.get(0).get("spi:triTaskTypeCL")) == 'Corrective'):
        wo.setValue("WORKTYPE","CM", 11L) #spi:triTaskTypeCL
    wo.setValue("ACTSTART",str(WoTask.get(0).get("spi:triActualStartDT"))) #spi:triActualStartDT
    woSet.save(11L)
###------------------------------------------------------------------------------------------------------------------
# Main Program
###-------------------------------------------------------------------------------------------------------------------
properties.put("HTTPMETHOD", "GET")
properties.put("URL", url)
properties.put("HEADERS","Authorization: Basic c3N5c3RlbTp0cmktZGVtbw==, content-type: application/json")
respBytes = HTTPHandler().invoke(properties,params)
obj = JSON.parse(String(respBytes))
WoTask = obj.get("rdfs:member")
if WoTask:
    mbo.setValue("DESCRIPTION_LONGDESCRIPTION", str(WoTask))
    generateWO(WoTask,woSet)
