#
# Owner: Utkarsh Shukla
# Created date: 15 May, 2021
# Version: 1.0
# Description: Custom Script for Changing Status for Work Schedule Application & Copy WA and SR to COC_SCHEDRECS
# LANGUAGE: JYTHON
# Script: COC_WORKSCHE_CNG_STATUS
#
# Version History##
#
###------------------------------------------------------------------------------------------------------------
# Version       Developer          Date Modified          Reason for modifiaction       Developer Comments            
###------------------------------------------------------------------------------------------------------------
#
# Intial Draft  Utkarsh Shukla     15 May,2021            Original script                  Created                   
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
###------------------------------------------------------------------------------------------------------------------
# Define your Variables
###------------------------------------------------------------------------------------------------------------------
siteid = mbo.getString("siteid")
SCHEDNUM = mbo.getString("SCHEDNUM")
StartDate = mbo.getDate("STARTDATE")
endDate = mbo.getDate("ENDDATE")
noCheck = MboConstants.NOACCESSCHECK
###------------------------------------------------------------------------------------------------------------------
# Define your Functions 
###------------------------------------------------------------------------------------------------------------------
def addToCOC_SCHEDRECS(schedRecsSet,classs, SCHEDNUM,RecordID, SITEID):
    #schedRecsSet = mbo.getMboSet("$COC_SCHEDRECS", "COC_SCHEDRECS", "1=2")
    schedRec = schedRecsSet.add(11L);
    schedRec.setValue("CLASS",classs, 11L);
    schedRec.setValue("SCHEDNUM",SCHEDNUM, 11L);
    schedRec.setValue("RECORDKEY",RecordID, 11L);
    schedRec.setValue("SITEID",SITEID, 11L);
    
# For Thorwing Errors with Custom Message

def throwError(errorMessage):
    params = [errorMessage] 
    service.error("COC_WORKSCHD", "COC_STATUS_CHANGE_ERROR", params)
    
# For WO Status Change    

def woChnageStatus(woSet):
    if (not woSet.isEmpty()):
        wo = woSet.moveFirst()
        while(wo):
            wo.setValue("STATUS","WASGN")
            wo = woSet.moveNext()
        woSet.save(11L)
        
# For Making record READONLY for 

def setFlags():
    mbo.setFieldFlag("DESCRIPTION", MboConstants.READONLY, True)
    mbo.setFieldFlag("CREW", MboConstants.READONLY, True)
    mbo.setFieldFlag("CREWTPE", MboConstants.READONLY, True)
    mbo.setFieldFlag("ENDDATE", MboConstants.READONLY, True)
    mbo.setFieldFlag("STARTDATE", MboConstants.READONLY, True)
###------------------------------------------------------------------------------------------------------------------
# Main Program
###------------------------------------------------------------------------------------------------------------------
'''------------------------------------ For Appr Custom Code and Change Status---------------------------------------'''
if launchPoint == "COC_WORKSCHE_APPR":
    if mbo.getString("STATUS") == "RAPPR" or "DRAFT":
        if StartDate < endDate:
            mbo.setValue("STATUS", "APPR", noCheck)
            setFlags()
           
           # workAssignmentSet = mbo.getMboSet("$WORKORDER", "WORKORDER","wonum in (select wonum from ASSIGNMENT where wonum in (select wonum from workorder where status in ('WSCH', 'WASGN', 'ASGND', 'INPRG') and siteid = :siteid and TARGSTARTDATE is null or TARGSTARTDATE < :ENDDATE and istask = 0))")
            #raise TypeError('is EMPTY of workAssignmentSet is ' + str(not workAssignmentSet.isEmpty()) + ' Count is:'+ str(workAssignmentSet.count()))
            #sr311Set = mbo.getMboSet("$SR", "SR","STATUS in ('QUEUED', 'INPROG') and TARGETSTART is null or TARGETSTART < :ENDDATE")
            
           
            schedRecsSet = mbo.getMboSet("$COC_SCHEDRECS", "COC_SCHEDRECS", "1=2")
            
            #woSet = mbo.getMboSet("$WORKORDER", "WORKORDER", "status = 'WSCH' and wonum in (select RECORDKEY from COC_SCHEDRECS where class='WO' and SCHEDNUM=:SCHEDNUM)")
# For Siteid = 'WT' or 'WWT'  
            if (siteid == 'WT' or siteid == 'WWT'):
                workAssignmentSet = mbo.getMboSet("$WORKORDER", "WORKORDER","wonum in (select wonum from ASSIGNMENT where wonum in (select wonum from workorder where status in ('WSCH', 'WASGN', 'ASGND', 'INPRG') and siteid = :siteid and TARGSTARTDATE is null or status in ('WSCH', 'WASGN', 'ASGND', 'INPRG') and siteid = :siteid and TARGSTARTDATE < :ENDDATE and istask = 0))")
                #raise TypeError('is EMPTY of workAssignmentSet is ' + str(not workAssignmentSet.isEmpty()) + ' Count is:'+ str(workAssignmentSet.count()))
                if (not workAssignmentSet.isEmpty()):
                    #raise TypeError('is EMPTY of workAssignmentSet is ' + str(not workAssignmentSet.isEmpty()) + ' Count is:'+ str(workAssignmentSet.count()))
                    workAssignment = workAssignmentSet.moveFirst()
                    while(workAssignment):
                        addToCOC_SCHEDRECS(schedRecsSet, 'WO', SCHEDNUM, workAssignment.getString("WONUM"), siteid)
                        workAssignment = workAssignmentSet.moveNext()

# For Siteid ='FLD'               
                
            elif (siteid == 'FLD'):
                sr311Set = mbo.getMboSet("$SR", "SR","siteid = :siteid and STATUS in ('QUEUED', 'INPROG') and TARGETSTART is null or STATUS in ('QUEUED', 'INPROG') and TARGETSTART < :ENDDATE")
                if (not sr311Set.isEmpty()): 
                    sr = sr311Set.moveFirst()
                    
                    while(sr):
                        addToCOC_SCHEDRECS(schedRecsSet, 'SR', SCHEDNUM, sr.getString("TICKETID"), siteid)
                        sr = sr311Set.moveNext()
                    workAssignmentSet = mbo.getMboSet("$WORKORDER", "WORKORDER","wonum in (select wonum from ASSIGNMENT where wonum in (select wonum from workorder where status in ('WSCH', 'WASGN', 'ASGND', 'INPRG') and siteid = :siteid and TARGSTARTDATE is null or status in ('WSCH', 'WASGN', 'ASGND', 'INPRG') and TARGSTARTDATE < :ENDDATE and siteid = :siteid and istask = 0))")    
                if (not workAssignmentSet.isEmpty()):
                    workAssignment = workAssignmentSet.moveFirst()
                    
                    while(workAssignment):
                        addToCOC_SCHEDRECS(schedRecsSet, 'WO', SCHEDNUM, workAssignment.getString("WONUM"), siteid)
                        workAssignment = workAssignmentSet.moveNext()

            WA1B = service.webclientsession().getCurrentApp().getDataBean("MAINRECORD")
            WA1B.save()
            #WA1BSet = WA1B.getMboSet()
            #WA1BSet.reset()
            WA1B.getMboSet().reset()
            WA1B.refreshTable()
            
            #woChnageStatus(woSet)
            
        else:
            throwError('The Status can not be changed, End Date should be greater than Start Date')
    else:
        throwError('The Status can not be changed to Approved it should be in Ready for Review/Approval')

        
        
        
#------------------------------------------------ For Change Status Only --------------------------------------------#
if launchPoint == "COC_WORKSCHE_RAPPR":
    if mbo.getString("STATUS") == "DRAFT":
        if StartDate < endDate:
            mbo.setValue("STATUS", "RAPPR", noCheck)
            setFlags()
           
        else:
            throwError('The Status can not be changed, End Date should be greater than Start Date')

    else:
        throwError('The Status can not be changed to Ready for Review/Approval it should be in Draft')

if launchPoint == "COC_WORKSCHE_FNSHD":
    if mbo.getString("STATUS") == "APPR":
        if StartDate < endDate:
            mbo.setValue("STATUS", "FNSHD", noCheck)
            
            
        else:
            throwError('The Status can not be changed, End Date should be greater than Start Date')
    else:
        throwError('The Status can not be changed to Finished it should be in Approved')

if launchPoint == "COC_WORKSCHE_DRAFT":
    if mbo.getString("STATUS") == "RAPPR":
        if StartDate < endDate:
            mbo.setValue("STATUS", "DRAFT", noCheck)
            
        else:
            throwError('The Status can not be changed, End Date should be greater than Start Date')
    else:
        throwError('The Status can not be changed to Draft it should be in Ready for Review/Approval')
