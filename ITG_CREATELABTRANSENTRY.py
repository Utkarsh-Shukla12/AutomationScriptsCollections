#
# Owner: Utkarsh Shukla
# Created date: 26 June, 2021
# Version: 1.0
# Description: Custom Script for Adding Negative and Positive entries in LabTrans table and Custom Table
# LANGUAGE: JYTHON
# Script: ITG_CREATELABTRANSENTRY
#
# Version History##
#
###------------------------------------------------------------------------------------------------------------
# Version       Developer          Date Modified          Reason for modifiaction       Developer Comments            
###------------------------------------------------------------------------------------------------------------
#
# Intial Draft  Utkarsh Shukla     26 June,2021            Original script                  Created                   
#
#--------------------------------------------------------------------------------------------------------------

###-------------------------------------------------------------------------------------------------------------
# Import Librarires
###-------------------------------------------------------------------------------------------------------------
import java
from psdi.server import MXServer
from psdi.mbo import MboSet
from psdi.mbo import Mbo
from psdi.mbo import MboRemote
from psdi.mbo import MboConstants
from psdi.common.context import UIContext
from psdi.webclient.system.controller import SessionContext, Utility, WebClientEvent
###------------------------------------------------------------------------------------------------------------------
# Define your Variables
###------------------------------------------------------------------------------------------------------------------
#siteid = mbo.getString("siteid")
currentDate = MXServer.getMXServer().getDate()
currentApp = service.webclientsession().getCurrentApp()

WO = currentApp.getDataBean("MAINRECORD");
ITG_laborBean = currentApp.getDataBean("1623340097764");
ITG_transferDetailsMbo = currentApp.getDataBean("1624956965612").getMboSet().moveFirst();
ITG_MatSerLabTransSet = mbo.getMboSet("$ITG_MATSERVLABTRANSFER", "ITG_MATSERVLABTRANSFER", "1=2")
labtransSet =  mbo.getMboSet("$LABTRANS", "LABTRANS", "1=2")
LaborSelectedRecords = currentApp.getDataBean("selectlaborofwo").getMboSet().getSelection()
selectedRecordsSize = LaborSelectedRecords.size()
ORGID = WO.getString("ORGID")
SITEID = WO.getString("SITEID")
WONUM = WO.getString("WONUM")
isTransfer = ITG_transferDetailsMbo.getBoolean("IS_TRANSFER")
destinationWonum = ITG_transferDetailsMbo.getString("ITG_DEST_WONUM")
transferDescription = ITG_transferDetailsMbo.getString("ITG_TRANSFER_DESCRIPTION")
    

#raise TypeError("Fetched the Transfer details -> " + str(ITG_transferDetailsMbo.getBoolean("IS_TRANSFER")))
###------------------------------------------------------------------------------------------------------------------
# Define your Functions 
###------------------------------------------------------------------------------------------------------------------
def addToITG_MATSERVLABTRANSFER(ITG_MatSerLabTransSet, laborMbo):
    ITG_MatSerLabTransMbo = ITG_MatSerLabTransSet.add(11L)
    ITG_MatSerLabTransMbo.setValue("ITG_LABORCODE", laborMbo.getString("LABORCODE"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_SOURCEWO", WO.getString("WONUM"), 11L)
    ITG_MatSerLabTransMbo.setValue("itg_linetype", 'Labor', 11L)
    ITG_MatSerLabTransMbo.setValue("itg_orgid", WO.getString("ORGID"), 11L)
    ITG_MatSerLabTransMbo.setValue("itg_siteid", WO.getString("SITEID"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_TRANSDES", ITG_transferDetailsMbo.getString("ITG_TRANSFER_DESCRIPTION"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_DESTINATIONWO", ITG_transferDetailsMbo.getString("ITG_DEST_WONUM"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_REGULARHRS", laborMbo.getDouble("REGULARHRS"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_REVERSALID", laborMbo.getString("LABTRANSID"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_PAYRATE", laborMbo.getDouble("PAYRATE"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_STARTDATE", laborMbo.getDate("STARTDATE"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_CRAFT", laborMbo.getString("CRAFT"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_SKILL", laborMbo.getString("SKILLLEVEL"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_LOCATION", laborMbo.getString("LOCATION"), 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_DATETIMESTAMP", currentDate, 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_USERSTAMP", user, 11L)
    ITG_MatSerLabTransMbo.setValue("ITG_ISTRANSFER", True, 11L)
    
def addNegativeEntryInLabTrans(labtransSet,ORGID,SITEID, WONUM):
    negativeLabor = labtransSet.add(11L)
    negativeLabor.setValue("ENTERBY",user,11L)
    negativeLabor.setValue("CRAFT",laborMbo.getString("CRAFT"),11L)
    negativeLabor.setValue("LABORCODE",laborMbo.getString("LABORCODE"),11L)
    negativeLabor.setValue("ENTERDATE",currentDate,11L)
    negativeLabor.setValue("LINECOST",(-1 * laborMbo.getDouble("LINECOST")),11L)
    negativeLabor.setValue("REGULARHRS",(-1 * laborMbo.getDouble("REGULARHRS")),11L)
    negativeLabor.setValue("ORGID",ORGID,11L)
    negativeLabor.setValue("SITEID",SITEID,11L)
    negativeLabor.setValue("REFWO",WONUM,11L)
    negativeLabor.setValue("PAYRATE",laborMbo.getDouble("PAYRATE"),11L)
    negativeLabor.setValue("STARTDATE",laborMbo.getDate("STARTDATE"),11L)
    negativeLabor.setValue("STARTDATEENTERED",laborMbo.getDate("STARTDATEENTERED"),11L)
    negativeLabor.setValue("TRANSDATE",laborMbo.getDate("TRANSDATE"),11L)
    negativeLabor.setValue("TRANSTYPE",laborMbo.getString("TRANSTYPE"),11L)
    negativeLabor.setValue("LOCATION",laborMbo.getString("LOCATION"),11L)
    negativeLabor.setValue("ASSETNUM",laborMbo.getString("ASSETNUM"),11L)
    negativeLabor.setValue("SKILLLEVEL",laborMbo.getString("SKILLLEVEL"),11L)
    
def addPositveEntryInLabTrans(labtransSet,ORGID,SITEID):
    positiveLabor = labtransSet.add(11L)
    positiveLabor.setValue("ENTERBY",user,11L)
    positiveLabor.setValue("CRAFT",laborMbo.getString("CRAFT"),11L)
    positiveLabor.setValue("LABORCODE",laborMbo.getString("LABORCODE"),11L)
    positiveLabor.setValue("ENTERDATE",currentDate,11L)
    positiveLabor.setValue("LINECOST", laborMbo.getDouble("LINECOST"),11L)
    positiveLabor.setValue("REGULARHRS", laborMbo.getDouble("REGULARHRS"),11L)
    positiveLabor.setValue("ORGID",ORGID,11L)
    positiveLabor.setValue("SITEID",SITEID,11L)
    positiveLabor.setValue("REFWO",ITG_transferDetailsMbo.getString("ITG_DEST_WONUM"),11L)
    positiveLabor.setValue("PAYRATE",laborMbo.getDouble("PAYRATE"),11L)
    positiveLabor.setValue("STARTDATE",laborMbo.getDate("STARTDATE"),11L)
    positiveLabor.setValue("STARTDATEENTERED",laborMbo.getDate("STARTDATEENTERED"),11L)
    positiveLabor.setValue("TRANSDATE",laborMbo.getDate("TRANSDATE"),11L)
    positiveLabor.setValue("TRANSTYPE",laborMbo.getString("TRANSTYPE"),11L)
    positiveLabor.setValue("LOCATION",laborMbo.getString("LOCATION"),11L)
    positiveLabor.setValue("ASSETNUM",laborMbo.getString("ASSETNUM"),11L)
    positiveLabor.setValue("SKILLLEVEL",laborMbo.getString("SKILLLEVEL"),11L)
    
def throwError(errorMessage):
    params = [errorMessage]
    service.error("COST","Cost_Transfer",params)
def validateUserInputs():
    if selectedRecordsSize == 0:
        throwError('Please Select any record to process')
    if transferDescription == '':
        throwError('Before Proceeding, Please Enter the Transfer Description')
    if isTransfer and destinationWonum == '':
        throwError('Please Enter the Destination Work Order, where Labor Records will be Transferd or Uncheck the Transfer Check box')
    
###------------------------------------------------------------------------------------------------------------------
# Main Program
###------------------------------------------------------------------------------------------------------------------

''' Fetch ITG_MatSerLabTransSet and Selected records by user'''
    
#raise TypeError("Fetched the Selected records " + str(ITG_MatSerLabTransSet.add(11L)))
validateUserInputs()
if isTransfer:
    for record in range(selectedRecordsSize):
        laborMbo = LaborSelectedRecords.get(record)
        addToITG_MATSERVLABTRANSFER(ITG_MatSerLabTransSet, laborMbo)
        addNegativeEntryInLabTrans(labtransSet,ORGID,SITEID, WONUM)
        addPositveEntryInLabTrans(labtransSet,ORGID,SITEID)
        
else:
     for record in range(selectedRecordsSize):
        laborMbo = LaborSelectedRecords.get(record)
        addToITG_MATSERVLABTRANSFER(ITG_MatSerLabTransSet, laborMbo)
        addNegativeEntryInLabTrans(labtransSet,ORGID,SITEID, WONUM)
                     
        
#raise TypeError(" Selected records WONUM" + WO.getString("WONUM") + " Orgid " + WO.getString("ORGID")+" Siteid " + WO.getString("SITEID"))
context = UIContext.getCurrentContext()
if context:
    wcs = context.getWebClientSession()
    Utility().sendEvent(WebClientEvent("dialogclose", wcs.getCurrentPageId(), None, SessionContext(wcs)))

ITG_MatSerLabTransSet.save(11L)
ITG_laborBean.getMboSet().reset()
ITG_laborBean.refreshTable()
WO.getMboSet().reset()
WO.refreshTable()
WO.getMboSet().save(11L)
