########################
# Author: Utkarsh Shukla
# Created date: 24 June, 2020
# Version: 1.0
# Description:Asset Meter New Reading
# LANGUAGE: PYTHON
#######################
###
# Version History##
###
# Version     Developer          Date Modified          Reason for modifiaction       Developer Comments
###
# 1.0         Utkarsh Shukla     24 June,2020            Original script              Created Orginal Script
#
################################

import java
from psdi.util.logging import MXLogger
from java.lang import System, Class, String, StringBuffer
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory

logger=MXLoggerFactory.getLogger("maximo.script")

java.lang.System.out.println("Line1 Pallet Count:" + mbo.getString("METERNAME"));

logger.debug(" ======= Executing COCASSETMETER:" + mbo.getString("METERNAME"))
if mbo.getString("METERNAME")=="SAP1PA150001":
 logger.debug("Meter Name ="+mbo.getString("METERNAME"))
 pOrderNum=""
 newPOrderNum=""
 palletCases=""
 shiftNum="X"
 woActivitySet=mbo.getMboSet("$tmpWoActivity","WOACTIVITY"," assetnum=:assetnum and siteid=:siteid and status ='INPRG' ")
 logger.debug("WoActivity count ="+str(woActivitySet.count())+",    Where ="+woActivitySet.getCompleteWhere())
 if not woActivitySet.isEmpty():
  woActivity=woActivitySet.getMbo(0)
  palletCases=woActivity.getString("COCCASEFORPALLET3")
  logger.debug("palletCases ="+palletCases)
  woSet=woActivity.getMboSet("$tmpWorkOrder","WORKORDER","wonum=:parent and siteid=:siteid")
  if not woSet.isEmpty():
   pOrderNum=woSet.getMbo(0).getString("PROCESSORDERNUM")
   logger.debug("pOrderNum ="+pOrderNum)
 
  personSet=woActivity.getMboSet("$tmpPerson","PERSON","personid=:owner ")
  if not personSet.isEmpty() and personSet.getMbo(0).getString("PRIMARYSHIFTNUM")!="":
   shiftNum=personSet.getMbo(0).getString("PRIMARYSHIFTNUM")
   logger.debug("shiftNum ="+shiftNum)
 
  if len(pOrderNum)  < 12:
   tmpOrder=""
   for x in range(12-len(pOrderNum)):
    tmpOrder=tmpOrder+"0"
   newPOrderNum=tmpOrder+pOrderNum
   logger.debug("newPOrderNum Final ="+newPOrderNum)

  cocPalletSet=mbo.getMboSet("$tmpCOCPALLET","COCPALLET","COCPROCESSNUM='"+pOrderNum+"' and siteid=:siteid ")
  cocPallet=cocPalletSet.addAtEnd()
  cocPallet.setValue("COCPROCESSNUM", pOrderNum)
  cocPallet.setValue("COCPALLETNUM",palletCases)

  setCnt=cocPalletSet.count()
  srNum=""
  if len(str(setCnt)) <4:
   for x in range(4 - len(str(setCnt))):
    srNum=srNum+"0"
  srNum=srNum+str(setCnt)
  logger.debug("srNum ="+srNum)
  cocPallet.setValue("COCPALLETCODE",shiftNum+newPOrderNum+srNum)
  #cocPalletSet.save()

elif mbo.getString("METERNAME")=="RS-FLOWMTR":
 woSet=mbo.getMboSet("$tmpWoAct","WORKORDER","assetnum=:assetnum and siteid=:siteid and status='INPRG' AND istask=1 ")
 if not woSet.isEmpty():
  matUseTransSet=woSet.getMbo(0).getMboSet("SHOWACTUALMATERIAL")
  matUseTransSet.reset()
  matUseTransSet.setWhere(" DESCRIPTION like '%READY SYRUP%' ")
  if not matUseTransSet.isEmpty():
   totalQty=0
   for x in range(matUseTransSet.count()):
    totalQty=totalQty+matUseTransSet.getMbo(x).getDouble("QUANTITY")
   qty=mbo.getDouble("NEWREADING") - totalQty
   matUse=matUseTransSet.getMbo(0)
   matUseTrans=matUseTransSet.addAtEnd()
   matUseTrans.setValue("itemnum",matUse.getString("ITEMNUM"))
   matuseTrans.setValue("quantity",qty)
   matUseTrans.setValue("STORELOC",matUse.getString("STORELOC"))
   matUseTransSet.save()
