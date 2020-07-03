############################################################################################################################ 
# Name:  
# Launch Point: Action 
# Event: Save 
# 
# Script to trigger Primavera Integration
#                
############################################################################################################################
# Developer						Version		Date			launchPoint						Remarks                              
#-------------------------------------------------------------------------------------------------------------------------- 
#
# Utkarsh Shukla					1.0     11/05/2020			WAM_STAGING		Defect: 6243 Send Outbound to Primavera on workorder updates from staging table in every 10 mins interval.
# 
############################################################################################################################
from psdi.server import MXServer
from psdi.security import UserInfo 
from psdi.util.logging import MXLoggerFactory
import sys
server = MXServer.getMXServer()
userInfo = mbo.getUserInfo()
maximoLogger = MXLoggerFactory.getLogger("maximo")
maximoLogger.debug("WAM:::DEBUG:::WAM_STAGING:::START:::")
headerid=mbo.getString("WAM_INT_BATCHID")
detailmboSet= mbo.getMboSet("WAMBATCHREL")
mbo.setValue("WAMSTATUS","PROCESSING")
mbo.getThisMboSet().save()
error = False
if (detailmboSet.isEmpty()== False):	
	for i in range(0,detailmboSet.count()):
		try :
			detailmbo = detailmboSet.getMbo(i)
			server.lookup("MIC").exportData( mbo.getString("WAMIFACENAME"), mbo.getString("WAMEXTSYS"), "wonum='"+detailmbo.getString("WAM_RECORDKEY")+"' and siteid='"+detailmbo.getString("WAMSITEID")+"'", userInfo, 1)
			detailmbo.setValue("WAMSTATUS","PROCESSED")			
		except :
			e=sys.exc_info()
			detailmbo.setValue("WAMSTATUS","ERROR")
			detailmbo.setValue("WAMERRORMSG",str(e))
			error = True
		
	detailmboSet.save()
	headerset=MXServer.getMXServer().getMboSet("WAM_INT_BATCH", MXServer.getMXServer().getSystemUserInfo())
	headerset.setWhere("WAM_INT_BATCHID='"+headerid+"'")
	headerset.reset()
	if (error):
		headerset.getMbo(0).setValue("WAMSTATUS","PROCESSED w/ERROR/")
		headerset.save()
	else:
		
		headerset.getMbo(0).setValue("WAMSTATUS","PROCESSED")
		headerset.save()
	
maximoLogger.debug("WAM:::DEBUG:::WAM_STAGING:::END:::")
