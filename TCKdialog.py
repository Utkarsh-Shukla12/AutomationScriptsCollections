##==============================================================================
#*   NAME: TCKDialog
#* 
#*   PURPOSE: To set value on click of OK button Enter ASSET POS dialouge
#*   REVISIONS:
#*   Ver        Date              Author                             Description
#*   ---------  ---------- ---  ---------- ---------------  -----------------------------------
#*   
#*	 1.0		21/12/20	    Utkarsh    	to set value on ok button  of TCKPOSHIS Enter Asset Position dialouge DEVOPS - 217827 MX27E			  
#* 2.0		08/01/21		    Utkarsh	Changed Relation Ship as TCKMOSTRECENTASTPOSITION to fix for bug 230746- MX27E	
#*3.0		13/01/21		    Utkarsh	Changed Relation Ship as TCKASSETPOSDATANEWROW to fix for bug 230708- MX27E	
#*4.0       25/01/21            Utkarsh    Changed maxmessage from invalidreadingdate to AsOfPOSDateNotValid Bug -235456
#*5.0       16/04/21            Utkarsh      Changed service.error("ASSET","AsOfPOSDateNotValid") to errorgroup = "ASSET" and errorkey = "AsOfPOSDateNotValid" because New Component Position is taking null when we are using service.error  method  and POS Value null check has been removed
#***************************** End Standard Header ****************************
from psdi.mbo import MboConstants
from psdi.common.context import UIContext
from psdi.webclient.system.controller import SessionContext, Utility, WebClientEvent
from psdi.util.logging import MXLogger
from psdi.util.logging import MXLoggerFactory
from psdi.server import MXServer
from psdi.security import UserInfo



if( mbo.getName()=="TCKPOSHIS"):
   mxServer = MXServer.getMXServer()
   securityflag = mxServer.getSecurityContext()
   mxServer.setSecurityCheck(mxServer.SecurityContextFlag.DISABLED) 
   initDate=MXServer.getMXServer().getDate()
   ownerMbo=mbo.getOwner()
   tckAssetnum=ownerMbo.getString("ASSETNUM")
   orgID=ownerMbo.getString("ORGID")
   siteID=ownerMbo.getString("SITEID")
   #check if user has not eneterd valuse in POS Date 
   #As per feature MX27H POS Value null check has been removed
   if((mbo.getDate("TCKNEWPOSDATE") is not None)):
     assetPOSSet=ownerMbo.getMboSet("TCKASSETPOSDATANEWROW")
     assetPOSSet.setOrderBy("TCKNEWPOSDATE desc")
     assetPOSSet.reset()
     #assetPOSSet above will always return 1 row which get created during asset creation
     #
     # Added tempAssetPOSSet to get latest NEWPOSDATE 
     tempAssetPOSSet=ownerMbo.getMboSet("TCKMOSTRECENTASTPOSITION")
     tempAssetPOSSet.setFlag(MboConstants.DISCARDABLE, True)
     tempAssetPOSSet.setOrderBy("TCKNEWPOSDATE desc")
     tempAssetPOSSet.reset()
     tckAssetPOSDaate=None
     if(not tempAssetPOSSet.isEmpty()):
      tckAssetPOSDaate=tempAssetPOSSet.getMbo(0).getDate("TCKNEWPOSDATE")
      
     if((None is tckAssetPOSDaate) or (mbo.getDate("TCKNEWPOSDATE")>tckAssetPOSDaate)): 
      assetPOSLineRemote=assetPOSSet.add(MboConstants.NOACCESSCHECK)
      assetPOSLineRemote.setValue("TCKASSETNUM",mbo.getString("TCKASSETNUM"))
      assetPOSLineRemote.setValue("TCKNEWPLUSTPOS",mbo.getString("TCKNEWPLUSTPOS"))
      assetPOSLineRemote.setValue("TCKNEWPOSDATE",mbo.getDate("TCKNEWPOSDATE"))        
      assetPOSLineRemote.setValue("TCKENTERDATE",initDate,2L)
      assetPOSLineRemote.setValue("TCKENTERDBY",user,2L)
      assetPOSLineRemote.setValue("TCKORGID",mbo.getString("TCKORGID"))
      assetPOSLineRemote.setValue("tcksiteid",mbo.getString("tcksiteid"))
      if(ownerMbo.getName()=="ASSET"):     
       ownerMbo.setValue("PLUSTPOS",mbo.getString("TCKNEWPLUSTPOS"))
      ownerMbo.getThisMboSet().save(MboConstants.NOACCESSCHECK) 
      #if change is made from workorder app
      if(ownerMbo.getName()=="WORKORDER"):
       userP=MXServer.getMXServer().getUserInfo(user)
       assetSet = MXServer.getMXServer().getMboSet("ASSET", userP)
       assetSet.setWhere("assetnum ='"+tckAssetnum+"' and siteid ='"+siteID+"' and ORGID = '"+orgID+"'")
       assetSet.reset()
       assetSet.getMbo(0).setValue("PLUSTPOS",mbo.getString("TCKNEWPLUSTPOS"),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION|MboConstants.NOACTION)
       assetSet.save()
       assetSet.close()
     else:
       # MX27H - changed service.error("ASSET","AsOfPOSDateNotValid") to errorgroup = "ASSET" and errorkey = "AsOfPOSDateNotValid" because New Component Position is taking null when we are using service.error method
       errorgroup = "ASSET"
       errorkey = "AsOfPOSDateNotValid"       
      
     context = UIContext.getCurrentContext()
     if context:
      wcs = context.getWebClientSession()
      Utility().sendEvent(WebClientEvent("dialogcancel", wcs.getCurrentPageId(), None, SessionContext(wcs)))
   
   else: 
      context = UIContext.getCurrentContext()
      if context:
       wcs = context.getWebClientSession()
       Utility().sendEvent(WebClientEvent("dialogok", wcs.getCurrentPageId(), None, SessionContext(wcs)))
   mxServer.setSecurityCheck(securityflag)
