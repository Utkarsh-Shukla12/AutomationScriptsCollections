############################################################################################################################ 
# Name:  
# Launch Point: OBJECT 
# Event: Save 
# 
# Script to trigger Primavera Integration
#                
############################################################################################################################
# Developer						Version		Date			launchPoint						Remarks                              
#-------------------------------------------------------------------------------------------------------------------------- 
#
# Utkarsh Shukla					1.0     	11/02/2018		WAM_OBJ_INTTRG_PRIMAVERA		Defect: 4646 Send Outbound to Primavera on workorder updates
# Utkarsh Shukla					2.0     	11/5/2018		WAM_OBJ_INTTRG_PRIMAVERA		Defect: 6243 Staging record to batchtabbles before sending to Primavera
# 
############################################################################################################################
from psdi.server import MXServer
from psdi.security import UserInfo 
from psdi.util.logging import MXLoggerFactory
server = MXServer.getMXServer()
userInfo = mbo.getUserInfo()
siteId = mbo.getString("SITEID")
maximoLogger = MXLoggerFactory.getLogger("maximo")
maximoLogger.debug("WAM:::DEBUG:::WAM_OBJ_INTTRG_PRIMAVERA:::START:::")
#Trigger Assignment updates to Primavera 
	
if launchPoint=="WAM_OBJ_P6_ASSIGNMENT":
	#raise TypeError(mbo.getOwner().getString("WONUM"))
	woSets=mbo.getMboSet("$PARENTSET", "WORKORDER", "wonum in (select parent from woactivity where wonum='"+mbo.getString("WONUM")+"')")
	if (woSets is not None and woSets.isEmpty()==0 and woSets.getMbo(0).getString("WAMCOMMODITY")=='ELECTRIC'):
		outbound=False
		asgcontrolset =server.getMboSet("MAXIFACECONTROL", server.getSystemUserInfo())
		asgcontrolset.setWhere("IFACECONTROL='WAM_ASG_ATTRIBUTE'")
		asgcontrolset.reset()
		if asgcontrolset is not None and asgcontrolset.isEmpty()==0:
			asgcontrolValueSet=asgcontrolset.moveFirst().getMboSet("MAXCONTROLVALUE")	
			if(asgcontrolValueSet is not None and asgcontrolValueSet.isEmpty()==False):
				asgicontrol = asgcontrolValueSet.moveFirst() 
				while (asgicontrol): 
					attribute=asgicontrol.getString("VALUE")
					if(mbo.isModified(attribute)==True):
						outbound=True
						break
					asgicontrol = asgcontrolValueSet.moveNext() 
		#Staging record to batchtabbles before sending to Primavera
		if (outbound==True):
			headerDetailset = server.getMboSet("WAM_INT_BATCH_DTL",server.getSystemUserInfo())
			headerDetailset.setWhere ("WAM_RECORDKEY='"+woSets.getMbo(0).getString("WONUM")+"' and WAMSTATUS='NEW'")
			headerDetailset.reset()
			#Staging record to batchtabbles before sending to Primavera
			if (headerDetailset.isEmpty()== True):
				
				headerSet=server.getMboSet("WAM_INT_BATCH",server.getSystemUserInfo());
				headerSet.setWhere ("WAMSTATUS='NEW'")
				headerSet.reset()
				if (headerSet.isEmpty() == True):
					headesetMbo=headerSet.add()
					headesetMbo.setValue("WAMEXTSYS","WAM_PRIMAVERA_EX")
					headesetMbo.setValue("WAMIFACENAME","WAM_MXTOP6_WO_PC")
					headesetMbo.setValue("WAMSTATUS","NEW")
				#setting detail table
					headerDetailsetmbo = headesetMbo.getMboSet("WAMBATCHREL").add()
					headerDetailsetmbo.setValue("WAM_RECORDKEY",woSets.getMbo(0).getString("WONUM"))
					headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",woSets.getMbo(0).getString("WAMBUSINESSFUNCTION"))
					headerDetailsetmbo.setValue("WAMCOMMODITY",woSets.getMbo(0).getString("WAMCOMMODITY"))
					headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
					headerDetailsetmbo.setValue("WAMSTATUS","NEW")
					headerDetailsetmbo.setValue("BATCHID",headesetMbo.getString("WAM_INT_BATCHID"))
					headesetMbo.getThisMboSet().save()
				else :
					headerDetailsetmbo = headerSet.getMbo(0).getMboSet("WAMBATCHREL").add()
					headerDetailsetmbo.setValue("WAM_RECORDKEY",woSets.getMbo(0).getString("WONUM"))
					headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",woSets.getMbo(0).getString("WAMBUSINESSFUNCTION"))
					headerDetailsetmbo.setValue("WAMCOMMODITY",woSets.getMbo(0).getString("WAMCOMMODITY"))
					headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
					headerDetailsetmbo.setValue("WAMSTATUS","NEW")
					headerDetailsetmbo.setValue("BATCHID",headerSet.getMbo(0).getString("WAM_INT_BATCHID"))
					headerSet.getMbo(0).getThisMboSet().save()
					
				
			
			#server.lookup("MIC").exportData("WAM_MXTOP6_WO_PC", "WAM_PRIMAVERA_EX", "wonum='"+mbo.getOwner().getString("PARENT")+"' and siteid='"+mbo.getOwner().getString("SITEID")+"'", userInfo, 1)
#Trigger Task/Prerequisite updates to Primavera 
if (launchPoint=="WAM_OBJ_P6_WOACTIVITY" and (mbo.getString("WAMCOMMODITY")=='ELECTRIC')):
	outbound=False
	wacontrolset =server.getMboSet("MAXIFACECONTROL", server.getSystemUserInfo())
	wacontrolset.setWhere("IFACECONTROL='WAM_WA_ATTRIBUTE'")
	wacontrolset.reset()
	if wacontrolset is not None and wacontrolset.isEmpty()==0:
		wacontrolValueSet=wacontrolset.moveFirst().getMboSet("MAXCONTROLVALUE")	
		if(wacontrolValueSet is not None and wacontrolValueSet.isEmpty()==False):
			waicontrol = wacontrolValueSet.moveFirst() 
			while (waicontrol): 
				attribute=waicontrol.getString("VALUE")
				if(mbo.isModified(attribute)==True):
					outbound=True
					break
				waicontrol = wacontrolValueSet.moveNext()
	
	if (outbound==True and mbo.getOwner() is not None and mbo.getOwner().getName()=='WORKORDER' and mbo.getOwner().isModified("STATUS")==0):		
		headerDetailset = server.getMboSet("WAM_INT_BATCH_DTL",server.getSystemUserInfo())
		
		headerDetailset.setWhere ("WAM_RECORDKEY='"+mbo.getString("PARENT")+"' and WAMSTATUS='NEW'")
		headerDetailset.reset()
		#Staging record to batchtabbles before sending to Primavera
		if (headerDetailset.isEmpty()== True):
			
			headerSet=server.getMboSet("WAM_INT_BATCH",server.getSystemUserInfo());
			headerSet.setWhere ("WAMSTATUS='NEW'")
			headerSet.reset()
			if (headerSet.isEmpty() == True):
				headesetMbo=headerSet.add()
				headesetMbo.setValue("WAMEXTSYS","WAM_PRIMAVERA_EX")
				headesetMbo.setValue("WAMIFACENAME","WAM_MXTOP6_WO_PC")
				headesetMbo.setValue("WAMSTATUS","NEW")
			#setting detail table
				headerDetailsetmbo = headesetMbo.getMboSet("WAMBATCHREL").add()
				headerDetailsetmbo.setValue("WAM_RECORDKEY",mbo.getString("PARENT"))
				headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",mbo.getString("WAMBUSINESSFUNCTION"))
				headerDetailsetmbo.setValue("WAMCOMMODITY",mbo.getString("WAMCOMMODITY"))
				headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
				headerDetailsetmbo.setValue("WAMSTATUS","NEW")
				headerDetailsetmbo.setValue("BATCHID",headesetMbo.getString("WAM_INT_BATCHID"))
				headesetMbo.getThisMboSet().save()
			else :
				headerDetailsetmbo = headerSet.getMbo(0).getMboSet("WAMBATCHREL").add()
				headerDetailsetmbo.setValue("WAM_RECORDKEY",mbo.getString("PARENT"))
				headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",mbo.getString("WAMBUSINESSFUNCTION"))
				headerDetailsetmbo.setValue("WAMCOMMODITY",mbo.getString("WAMCOMMODITY"))
				headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
				headerDetailsetmbo.setValue("WAMSTATUS","NEW")
				headerDetailsetmbo.setValue("BATCHID",headerSet.getMbo(0).getString("WAM_INT_BATCHID"))
				headerSet.getMbo(0).getThisMboSet().save()
			
						
		#server.lookup("MIC").exportData("WAM_MXTOP6_WO_PC", "WAM_PRIMAVERA_EX", "wonum='"+mbo.getString("PARENT")+"' and siteid='"+siteId+"'", userInfo, 1)
	
	if (outbound==True and mbo.getInt("PLUSDISPREREQ")==1 and mbo.isNew()==0 and mbo.isModified("STATUS")==1):	
		headerDetailset = server.getMboSet("WAM_INT_BATCH_DTL",server.getSystemUserInfo())
		headerDetailset.setWhere ("WAM_RECORDKEY='"+mbo.getString("PARENT")+"' and WAMSTATUS='NEW'")
		headerDetailset.reset()
		#Staging record to batchtabbles before sending to Primavera
		if (headerDetailset.isEmpty()== True):
			
			headerSet=server.getMboSet("WAM_INT_BATCH",server.getSystemUserInfo());
			headerSet.setWhere ("WAMSTATUS='NEW'")
			headerSet.reset()
			if (headerSet.isEmpty() == True):
				headesetMbo=headerSet.add()
				headesetMbo.setValue("WAMEXTSYS","WAM_PRIMAVERA_EX")
				headesetMbo.setValue("WAMIFACENAME","WAM_MXTOP6_WO_PC")
				headesetMbo.setValue("WAMSTATUS","NEW")
			#setting detail table
				headerDetailsetmbo = headesetMbo.getMboSet("WAMBATCHREL").add()
				headerDetailsetmbo.setValue("WAM_RECORDKEY",mbo.getString("PARENT"))
				headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",mbo.getString("WAMBUSINESSFUNCTION"))
				headerDetailsetmbo.setValue("WAMCOMMODITY",mbo.getString("WAMCOMMODITY"))
				headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
				headerDetailsetmbo.setValue("WAMSTATUS","NEW")
				headerDetailsetmbo.setValue("BATCHID",headesetMbo.getString("WAM_INT_BATCHID"))
				headesetMbo.getThisMboSet().save()
			else :
				headerDetailsetmbo = headerSet.getMbo(0).getMboSet("WAMBATCHREL").add()
				headerDetailsetmbo.setValue("WAM_RECORDKEY",mbo.getString("PARENT"))
				headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",mbo.getString("WAMBUSINESSFUNCTION"))
				headerDetailsetmbo.setValue("WAMCOMMODITY",mbo.getString("WAMCOMMODITY"))
				headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
				headerDetailsetmbo.setValue("WAMSTATUS","NEW")
				headerDetailsetmbo.setValue("BATCHID",headerSet.getMbo(0).getString("WAM_INT_BATCHID"))
				headerSet.getMbo(0).getThisMboSet().save()
				
		#server.lookup("MIC").exportData("WAM_MXTOP6_WO_PC", "WAM_PRIMAVERA_EX", "wonum='"+mbo.getString("PARENT")+"' and siteid='"+siteId+"'", userInfo, 1)
#Trigger workorder updates to Primavera 
if launchPoint=="WAM_OBJ_P6_WORKORDER"  and (mbo.getString("WAMCOMMODITY")=='ELECTRIC'):
	
	outbound=False
	wocontrolset =server.getMboSet("MAXIFACECONTROL", server.getSystemUserInfo())
	wocontrolset.setWhere("IFACECONTROL='WAM_WO_ATTRIBUTE'")
	wocontrolset.reset()
	if wocontrolset is not None and wocontrolset.isEmpty()==0:
		wocontrolValueSet=wocontrolset.moveFirst().getMboSet("MAXCONTROLVALUE")	
		if(wocontrolValueSet is not None and wocontrolValueSet.isEmpty()==False):
			woicontrol = wocontrolValueSet.moveFirst() 
			while (woicontrol): 
				attribute=woicontrol.getString("VALUE")
				if(mbo.isModified(attribute)==True):
					outbound=True
					break
				woicontrol = wocontrolValueSet.moveNext()	
	if (outbound==True):
		
		headerDetailset = server.getMboSet("WAM_INT_BATCH_DTL",server.getSystemUserInfo())
		
		headerDetailset.setWhere ("WAM_RECORDKEY='"+mbo.getString("WONUM")+"' and WAMSTATUS='NEW'")
		headerDetailset.reset()
		#Staging record to batchtabbles before sending to Primavera
		if (headerDetailset.isEmpty()== True):
			
			headerSet=server.getMboSet("WAM_INT_BATCH",server.getSystemUserInfo());
			headerSet.setWhere ("WAMSTATUS='NEW'")
			headerSet.reset()
			if (headerSet.isEmpty() == True):
				headesetMbo=headerSet.add()
				headesetMbo.setValue("WAMEXTSYS","WAM_PRIMAVERA_EX")
				headesetMbo.setValue("WAMIFACENAME","WAM_MXTOP6_WO_PC")
				headesetMbo.setValue("WAMSTATUS","NEW")
			#setting detail table
				headerDetailsetmbo = headesetMbo.getMboSet("WAMBATCHREL").add()
				headerDetailsetmbo.setValue("WAM_RECORDKEY",mbo.getString("WONUM"))
				headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",mbo.getString("WAMBUSINESSFUNCTION"))
				headerDetailsetmbo.setValue("WAMCOMMODITY",mbo.getString("WAMCOMMODITY"))
				headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
				headerDetailsetmbo.setValue("WAMSTATUS","NEW")
				headerDetailsetmbo.setValue("BATCHID",headesetMbo.getString("WAM_INT_BATCHID"))
				headesetMbo.getThisMboSet().save()
			else :
				headerDetailsetmbo = headerSet.getMbo(0).getMboSet("WAMBATCHREL").add()
				headerDetailsetmbo.setValue("WAM_RECORDKEY",mbo.getString("WONUM"))
				headerDetailsetmbo.setValue("WAMBUSINESSFUNCTION",mbo.getString("WAMBUSINESSFUNCTION"))
				headerDetailsetmbo.setValue("WAMCOMMODITY",mbo.getString("WAMCOMMODITY"))
				headerDetailsetmbo.setValue("WAMSITEID",mbo.getString("SITEID"))
				headerDetailsetmbo.setValue("WAMSTATUS","NEW")
				headerDetailsetmbo.setValue("BATCHID",headerSet.getMbo(0).getString("WAM_INT_BATCHID"))
				headerSet.getMbo(0).getThisMboSet().save()
			
				
						
		#server.lookup("MIC").exportData("WAM_MXTOP6_WO_PC", "WAM_PRIMAVERA_EX", "wonum='"+mbo.getString("WONUM")+"' and siteid='"+mbo.getString("SITEID")+"'", userInfo, 1)
maximoLogger.debug("WAM:::DEBUG:::WAM_OBJ_INTTRG_PRIMAVERA:::END:::")
