#--------------------------------------------------------------------------
# Created by - 
# Date - 24 June
#Script: IALOGSAVE
# Launch Point: COC_APPLY_CREW2SRDIALOGSAVE - Save - Add - Before Save
# Handles the Create Work Order dialog OK button
#--------------------------------------------------------------------------
from psdi.server import MXServer
from psdi.security import UserInfo 
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory
from psdi.common.context import UIContext
userinfo = MXServer.getMXServer().getSystemUserInfo()

logger = MXLoggerFactory.getLogger("maximo.script")
logger.info(">>> Entering script COC_APPLY_CREW2SRDIALOGSAVE")

# to get the non persistent object of the dialog we need a small trick
mbo = mboset.getMbo(0)
crew=mbo.getString("AMCREW")
crewSet=MXServer.getMXServer().getMboSet("AMCREW",userinfo)
crewSet.setWhere("AMCREW='"+crew+"'")
crewMbo=crewSet.getMbo(0)
type=crewMbo.getString("AMCREWTYPE")
crewSet.clear()
crewSet.close()


#whereClause = service.webclientsession().getCurrentApp().getResultsBean().getMboSet().getUserAndQbeWhere() 
#service.error("The WHERE clause is", whereClause);
selectionSize = service.webclientsession().getCurrentApp().getResultsBean().getMboSet().getSelection().size()
selectionRecords = service.webclientsession().getCurrentApp().getResultsBean().getMboSet().getSelection()
srSet=service.webclientsession().getCurrentApp().getResultsBean().getMboSet()


for i in range(selectionSize):
    sr=selectionRecords.get(i)
    srcrewtype=sr.getString("COC_OWNERCREWTYPE")
    if (srcrewtype==type):
        sr.setValue("COC_OWNERCREW",crew,MboConstants.NOVALIDATION)
       
    else:
        params=[crew]
        errorgroup = "COC311SR"
        errorkey = "InvalidOwnerCrew"
        srSet.clear()
        srSet.close()
        
    
srSet.save()
srSet.clear()
srSet.close()
