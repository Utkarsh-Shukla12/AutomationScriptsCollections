####################################################
# NAME: -> AUTOPOSTING_TO_SAP
# LANGUAGE: -> JYTHON
# DESCRIPTION: -> TO  POST  TO SAP
# Developer: -> Utkarsh Shukla
# Date Created: -> 28 May, 2019
# Version: -> 1.0
# Modified by: ->
# Reason for change: ->
# Launchpoint: Object-> On Save -> On Update
# ------------------------------------------------#

import java
from com.ibm.json.java import JSONObject, JSONArray
from java.io import BufferedReader, IOException, InputStreamReader
from java.lang import System, Class, String, StringBuffer
from java.nio.charset import Charset
from java.util import Date, Properties, List, ArrayList
from org.apache.commons.codec.binary import Base64
from org.apache.http import HttpEntity, HttpHeaders, HttpResponse, HttpVersion
from org.apache.http.client import ClientProtocolException, HttpClient
from org.apache.http.client.entity import UrlEncodedFormEntity
from org.apache.http.client.methods import HttpPost
from org.apache.http.entity import StringEntity
from org.apache.http.impl.client import DefaultHttpClient
from org.apache.http.message import BasicNameValuePair
from org.apache.http.params import BasicHttpParams, HttpParams, HttpProtocolParamBean


from  java.rmi import RemoteException
from  java.sql import Connection
from  java.sql import ResultSet
from  java.sql import SQLException
from  java.sql import Statement
from  psdi.security import ConnectionKey;
from  psdi.util import MXApplicationException;
from  psdi.util import MXException;
from  com.sun.rowset import CachedRowSetImpl;

from psdi.mbo import Mbo, MboRemote, MboSet, MboSetRemote, MboConstants
from psdi.security import UserInfo
from psdi.server import MXServer
from com.hccb.restclient.outbound import DefaultJsonClient
from sys import *

# Script Name: MATCONSM
# Post Material Consumed against WO/Process Order

# method for releasing the open client connection

def releaseConnection(client):
    if(client != None):
        client.getConnectionManager().shutdown()
        
# Method for returning material from line location to sap stores        

def returnMaterialToSAPStores():
    
    System.out.println('Starting Material Return 311')
    # Create JSON objects
    purOrder = JSONObject()
    header = JSONObject()
    contentHeader = JSONObject()
    polines = JSONArray()
    count = 0
    df = java.text.SimpleDateFormat("MM/dd/yyyy")
    today = MXServer.getMXServer().getDate()
    today = df.format(today) 
    
    isPostedSuccess=False
    System.out.println("Before mbo.getString" );
    currentWOActMbo= mbo.getThisMboSet()
    wonum= mbo.getString("PARENT");
    System.out.println("After mbo.getString" + wonum );
    woSet = mbo.getMboSet("$WO","WORKORDER","WONUM=" + "'" + wonum + "'")
    #woSet = mbo.getMboSet("PARENTWORKORDERSPEC")
    locSet = woSet.getMbo(0).getMboSet("LOCATION")
    lineLocationSAPCode = locSet.getMbo(0).getString("COCSAPCODE")
    
    processOrder=woSet.getMbo(0).getString("PROCESSORDERNUM")
    
    siteId= currentWOActMbo.getString("SITEID")
    
    System.out.println("Consume Materials" + currentWOActMbo.getName() + " ProcessOrder::" + processOrder)
    taskId=currentWOActMbo.getString("TASKID")
    
    woActivityNumber=currentWOActMbo.getString("WONUM")
    
   
    
    resultSet=getReturnedMaterials(woActivityNumber)
    
    System.out.println("woActivityNumber::" + taskId + "WONUM:" + str(woActivityNumber))
    
    
    while(resultSet.next()):
        siteId="HMAH"
        
        itemNumber= resultSet.getString("ITEMNUM")
        
        itemQty= resultSet.getString("3")
        
        
        
        matuseTransMboSet = mbo.getMboSet("$matusetrans","MATUSETRANS","refwo='" + woActivityNumber +"' AND COCINTBATCH='" + resultSet.getString("COCINTBATCH") + "'" )
        matuseTransMboSet.setWhere("COCINTBATCH=" + "'" + resultSet.getString("COCINTBATCH")+ "'")
        matuseTransMboSet.reset()
        
        
        
        location= matuseTransMboSet.getMbo(0).getString("STORELOC")
        
        internalBatchNumber=str(resultSet.getString("COCINTBATCH")).zfill(10)
        
        System.out.println("Totalqty:" + itemQty)
        transDate = MXServer.getMXServer().getDate();
        transFormat = java.text.SimpleDateFormat("MMddyyyyHHmmss")
        transDate = transFormat.format(transDate)
        transId= processOrder +transDate + str(count)
            
        System.out.println("TransactionId::" + str(transId))
        header.put("type","STOCK_ADJUSTMENT")
        header.put("action","C")
        header.put("movementType","311")
        header.put("Trans_Event","A101")
        header.put("RefDoc","R10")
        header.put("TransactionID",transId)
        System.out.println('Inside c : Header:  '+str(header))
        purOrder.put("header",header)
         
        #while (resultSet.next()):
                
        content = JSONObject()
        content.put("Plant",siteId)
        content.put("Doc_Date", today)
        content.put("PostingDate", today)
        content.put("DeliveryNote", "")
        content.put("BillOfLading","")        
        content.put("LRNumber", "")
        content.put("LRDate", "")
        content.put("VehicleNum", "")
        content.put("InvoiceNum", "")
        content.put("InvoiceDate","")  
        content.put("RoadPermitNum", "")
        content.put("CostCenter","")

        content.put("materialCodeFrom",itemNumber)
        content.put("materialCodeTo",itemNumber)
        content.put("Qty_UOE",itemQty)
        content.put("Qty_Dnote","")
        content.put("plantFrom",siteId)
        content.put("plantTo",siteId)
        content.put("storageLocationFrom",lineLocationSAPCode)
        
        System.out.println("upto storageLocation")
        content.put("storageLocationTo",getstoreRoomSAPStoreRoomCode(location))
        
        content.put("batchNumFrom",internalBatchNumber)
        content.put("batchNumTo",internalBatchNumber)
        content.put("vendorBatchNum","")
        content.put("MFG_Date","")
        content.put("EXP_Date","")
        content.put("itemOK","X")
        content.put("UOM","")
        content.put("Mvt_Ind","")
        purOrder.put("content",content)
        
        System.out.println("upto content")
        
        System.out.println("POST RETURN JSON to be sent " + str(purOrder))
        
        System.out.println("after ")
        responseJSON= httpPost(purOrder)
        
        System.out.println('POST CONSUMPTION JSON to be sent '+str(purOrder) + "--" + responseJSON.getResponse() )
        
        status=responseJSON.getStatusCode()
        
        #status=200
        if status == 200:
          System.out.println("Succussfully Posted Returns")
          saveMessageLog(str(woActivityNumber),"311-Material Return",status,transId,purOrder)
          
          #matConsumeMbo.setValue("COCPOSTED",1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
          UpdatePostReturnFlag(woActivityNumber,resultSet.getString("COCINTBATCH"))
          isPostedSuccess=True
          #funcDisplayInfo("Successfully Posted Returns")
        else:
          #System.out.println("Error Posting ::" + itemNumber + " MATUSETRANSID:" + matuseId) 
          DefaultJsonClient.logMessageToTable("COST_CENTER_TRANSFER",responseJSON.getStatusCode(),processOrder,responseJSON.getResponse())   
        count = count + 1   
        #matConsumeMbo=matConsumedSet.moveNext()





# method for creating the JSON string which is sent in http POST body
def postMaterialConsumption():
    System.out.println('Starting Material Consumption')
    # Create JSON objects
    purOrder = JSONObject()
    header = JSONObject()
    contentHeader = JSONObject()
    polines = JSONArray()
    
    df = java.text.SimpleDateFormat("MM/dd/yyyy")
    today = MXServer.getMXServer().getDate()
    today = df.format(today) 
    
    isPostedSuccess=False
    count=1;
    currentWOActMbo= mbo.getThisMboSet()
    wonum= mbo.getString("PARENT");
    
    woSet = mbo.getMboSet("$WO","WORKORDER","WONUM=" + "'" + wonum + "'")
    System.out.println("Parent Numb" + mbo.getString("PARENT")); 
    processOrder=woSet.getMbo(0).getString("PROCESSORDERNUM")
    siteId= currentWOActMbo.getString("SITEID")
    
    #System.out.println("Consume Materials" + currentWOActMbo.getName() + " ProcessOrder::" + processOrder)
    taskId=currentWOActMbo.getString("TASKID")
    System.out.println("woActivityNumber::" + taskId)
    woActivityNumber=currentWOActMbo.getString("WONUM")
    
    #userInfo=mbo.getUserInfo()
    #System.out.println("UserInfo::" + userInfo)
    matConsumedSet= MXServer.getMXServer().getMboSet("MATUSETRANS",mbo.getUserInfo())
    matConsumedSet.setWhere("REFWO=" + "'" + woActivityNumber + "'")
    matConsumeMbo = matConsumedSet.moveFirst()
    
    resultSet=getConsumedMaterials(woActivityNumber)
    
    while(resultSet.next()):
        siteId="HMAH"
        #System.out.println("matConsumeItem:" + resultSet.getString("ITEMNUM") + " ITEM-QTY:" + resultSet.getString("3") )
        #itemNumber= matConsumeMbo.getString("ITEMNUM")
        itemNumber= resultSet.getString("ITEMNUM")
        #itemQty= matConsumeMbo.getString("CURBAL")
        itemQty= resultSet.getString("3")
        location= matConsumeMbo.getString("LOCATION")
        #location= resultSet.getString("LOCATION")
        #matuseId= matConsumeMbo.getString("MATUSETRANSID")
        #matuseId= resultSet.getString("MATUSETRANSID")
        #internalBatchNumber=matConsumeMbo.getString("COCINTBATCH")
        internalBatchNumber=str(resultSet.getString("COCINTBATCH")).zfill(10)
        
        
        transDate = MXServer.getMXServer().getDate();
        transFormat = java.text.SimpleDateFormat("MMddyyyyHHmmss")
        transDate = transFormat.format(transDate)
        transId= processOrder + transDate + str(count)
            
        System.out.println("TransactionId::" + transId)
        header.put("type","STOCK_ADJUSTMENT")
        header.put("action","C")
        header.put("movementType","261")
        header.put("Trans_Event","A101")
        header.put("RefDoc","R10")
        header.put("TransactionID",transId)
        System.out.println('Inside c : Header:  '+str(header))
        purOrder.put("header",header)
         
        #while (resultSet.next()):
                
        content = JSONObject()
        content.put("Plant",siteId)
        content.put("DocNum", processOrder)
        content.put("Doc_Date", today)
        content.put("PostingDate", today)
        content.put("DeliveryNote", "")
        content.put("BillOfLading","")        
        content.put("LRNumber", "")
        content.put("LRDate", "")
        content.put("VehicleNum", "")
        content.put("InvoiceNum", "")
        content.put("InvoiceDate","")  
        content.put("RoadPermitNum", "")
        content.put("CostCenter","")

        content.put("materialCodeFrom",itemNumber)
        content.put("materialCodeTo","")
        content.put("Qty_UOE",itemQty)
        content.put("Qty_Dnote","")
        content.put("plantFrom",siteId)
        content.put("plantTo",siteId)
        content.put("storageLocationFrom",getstoreRoomSAPLocationCode(location))
        content.put("storageLocationTo","")
        content.put("batchNumFrom",internalBatchNumber)
        content.put("batchNumTo","")
        content.put("vendorBatchNum","")
        content.put("MFG_Date","")
        content.put("EXP_Date","")
        content.put("itemOK","X")
        content.put("UOM","")
        content.put("Mvt_Ind","")
        purOrder.put("content",content)
        
        responseJSON= httpPost(purOrder)
        
        System.out.println('POST CONSUMPTION JSON to be sent '+str(purOrder) + "--" + responseJSON.getResponse() )
        
        status=responseJSON.getStatusCode()
        #status=200
        if status == 200:
          System.out.println("Succussfully Posted Consumption")
          saveMessageLog(str(woActivityNumber),"261- consumption",status,transId,purOrder)
          
          #matConsumeMbo.setValue("COCPOSTED",1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
          UpdatePostConsumptionFlag(woActivityNumber,resultSet.getString("COCINTBATCH"))
          isPostedSuccess=True
          #funcDisplayInfo("Successfully Posted Consumption")
        else:
          #System.out.println("Error Posting ::" + itemNumber + " MATUSETRANSID:" + matuseId) 
          DefaultJsonClient.logMessageToTable("COST_CENTER_TRANSFER",responseJSON.getStatusCode(),processOrder,responseJSON.getResponse())
        count=count + 1   
           
        #matConsumeMbo=matConsumedSet.moveNext()
        
    #if(isPostedSuccess==True):
    #     funcDisplaySuccess("Successfully Posted Material to SAP")
    #    matConsumedSet.save()
    #    System.out.println("Saved Called")

def saveMessageLog(invuseid,service,response_code,transactionId,jsonObject):
     logSet = MXServer.getMXServer().getMboSet("COCMESSAGELOG",mbo.getUserInfo())
     logMbo = logSet.addAtEnd();
     
     logMbo.setValue("DESCRIPTION", str(invuseid),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
     logMbo.setValue("SERVICENAME",service,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
     logMbo.setValue("STATUSCODE",response_code,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
     logMbo.setValue("TRANSACTIONID",transactionId,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
     logMbo.setValue("MESSAGE",str(jsonObject),MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)
     logSet.save();
     logSet.commit();
     logSet.clear();
     logSet.close();    
            

def getConsumedMaterials(refWO):

    mxServer = MXServer.getMXServer()
    conKey = mxServer.getSystemUserInfo().getConnectionKey()
    con = mxServer.getDBManager().getConnection(conKey)
    
    try:
        stmt = con.createStatement();
        #rs = stmt.executeQuery("SELECT ITEMNUM, COCSITECODE, TOSTORELOC, COCINTBATCH, COCEXTBATCH FROM MAXIMO.MATRECTRANS WHERE PONUM ='" + poNumber + "' GROUP BY ITEMNUM, COCSITECODE, TOSTORELOC, COCINTBATCH, COCEXTBATCH");
        #rs = stmt.executeQuery("SELECT ITEMNUM,LOCATION,COCINTBATCH, SUM(CURBAL) FROM MAXIMO.MATUSETRANS WHERE REFWO=" + refWO + " AND COCITEMCONSUME=1 AND COCPOSTED=0 GROUP BY COCINTBATCH,ITEMNUM,LOCATION");
        rs = stmt.executeQuery("SELECT ITEMNUM,COCINTBATCH, SUM(COCQTY) FROM MAXIMO.COCACTUALBARCODE WHERE REFWO=" + refWO + " AND ISCONSUMED=1 AND ISPOSTED=0 GROUP BY COCINTBATCH,ITEMNUM");
        System.out.println("Stmt:: + executiing")
        
        # create CachedRowSet and populate
        crs = CachedRowSetImpl();
        crs.populate(rs);
    except:
                System.out.println( 'Error Occurred while send message:' +str(exc_info()[0]))
    finally:
        System.out.println("Closing Connection")
        rs.close();
        stmt.close();
        con.close();
        mxServer.getDBManager().freeConnection(conKey);
    
    return crs;


def getReturnedMaterials(refWO):
    
    mxServer = MXServer.getMXServer()
    conKey = mxServer.getSystemUserInfo().getConnectionKey()
    con = mxServer.getDBManager().getConnection(conKey)
    
    try:
        stmt = con.createStatement();
        
        #sql = "SELECT ITEMNUM,COCINTBATCH,STORELOC,SUM(ABS(QUANTITY)) FROM MAXIMO.MATUSETRANS WHERE REFWO=" + refWO + " AND issuetype='RETURN' GROUP BY COCINTBATCH,ITEMNUM,STORELOC"
        #System.out.println("Workorder Number:" + refWO + "  SQL:::" + sql)
        
        #rs = stmt.executeQuery("SELECT ITEMNUM,COCINTBATCH,STORELOC,SUM(ABS(QUANTITY)) FROM MAXIMO.MATUSETRANS WHERE REFWO=" + refWO + " AND issuetype='RETURN' GROUP BY COCINTBATCH,ITEMNUM,STORELOC");
        rs = stmt.executeQuery("SELECT ITEMNUM,COCINTBATCH,SUM(ABS(COCQTY)) FROM MAXIMO.COCACTUALBARCODE WHERE REFWO=" + refWO + " AND ISSUETYPE='RETURN' AND ISPOSTED=0 GROUP BY COCINTBATCH,ITEMNUM");
        System.out.println("Stmt:: + executiing")
        
        # create CachedRowSet and populate
        crs = CachedRowSetImpl();
        crs.populate(rs);
    except Exception,e:
                System.out.println( 'Error Occurred while send message:' +str(exc_info()[0]))
    finally:
        System.out.println("Closing Connection")
        rs.close();
        stmt.close();
        con.close();
        mxServer.getDBManager().freeConnection(conKey);
    
    return crs;


def getstoreRoomSAPLocationCode(LOC):
    locationSet = MXServer.getMXServer().getMboSet("LOCATIONS",mbo.getUserInfo()) 
    locationSet.setWhere("LOCATION=" + "'" + LOC + "'" + " and TYPE='OPERATING'")
    locationSAPCode= locationSet.getMbo(0).getString("COCSAPCODE");
    return(locationSAPCode)

def getstoreRoomSAPStoreRoomCode(storeRoom):
    storeRoomSet = MXServer.getMXServer().getMboSet("LOCATIONS",mbo.getUserInfo()) 
    storeRoomSet.setWhere("LOCATION=" + "'" + storeRoom + "'" + " and TYPE='STOREROOM'")
    storeRoomSAPCode= storeRoomSet.getMbo(0).getString("COCSAPCODE");
    return(storeRoomSAPCode)            

# method for http POST using the path, JSON body and token with bearer authorization
def httpPost(jsonstring):
    reference = None
    
    properties = MXServer.getMXServer().getConfig()
    host = properties.getProperty("HCCB.STAGING.OUTBOUND.HOST")
    path = properties.getProperty("HCCB.STAGING.OUTBOUND.STOCK_TRANSFER")
    uri = host + path
    System.out.println('POST_GOODS_RECEIVED: URI =' +uri)

    # get authentication header
    #authHeader = "Basic " + "U2FuYW5kVUFUOkdoamtpbEAxMm9scCM="
    authHeader = properties.getProperty("HCCB.STAGING.OUTBOUND.AUTHHEADER")

    jsonClient = DefaultJsonClient()
    response = jsonClient.execute(uri, authHeader, jsonstring)
    return response

def UpdatePostReturnFlag(refWO,internalBatchNum):

        mxServer = MXServer.getMXServer()
        conKey = mxServer.getSystemUserInfo().getConnectionKey()
        con = mxServer.getDBManager().getConnection(conKey)
        System.out.println("PO->" + str(refWO) + "InternalBatch->" + str(internalBatchNum))
        try:
            stmt = con.createStatement();
            updateCode = stmt.executeUpdate("UPDATE MAXIMO.COCACTUALBARCODE SET ISPOSTED=1 WHERE REFWO =" +"'" + refWO + "'" + " AND COCINTBATCH=" + "'" + internalBatchNum + "'" + " AND ISCONSUMED=1 AND ISSUETYPE='RETURN' ");
            System.out.println("Update Return Code:::" + str(updateCode))
            
        except:
                    System.out.println( 'Error Occurred while Updateing:' +str(exc_info()[0]))
        finally:
            System.out.println("Closing Connection")
            stmt.close();
            con.close();
            mxServer.getDBManager().freeConnection(conKey);

def UpdatePostConsumptionFlag(refWO,internalBatchNum):

        mxServer = MXServer.getMXServer()
        conKey = mxServer.getSystemUserInfo().getConnectionKey()
        con = mxServer.getDBManager().getConnection(conKey)
        System.out.println("PO->" + str(refWO) + "InternalBatch->" + str(internalBatchNum))
        try:
            stmt = con.createStatement();
            updateCode = stmt.executeUpdate("UPDATE MAXIMO.COCACTUALBARCODE SET ISPOSTED=1 WHERE REFWO =" +"'" + refWO + "'" + " AND COCINTBATCH=" + "'" + internalBatchNum + "'" + " AND ISCONSUMED=1 AND ISSUETYPE='ISSUE'");
            System.out.println("Update Return Code:::" + str(updateCode))
            
        except:
                    System.out.println( 'Error Occurred while Updateing:' +str(exc_info()[0]))
        finally:
            System.out.println("Closing Connection")
            stmt.close();
            con.close();
            mxServer.getDBManager().freeConnection(conKey);
        
def funcDisplaySuccess(errorMessage):
    global msggroup
    global msgkey
    global params
     
    msggroup = "COCSAP"
    msgkey = "MATCONSUMP"
    params=[errorMessage]
    return

def funcDisplayInfo(successMessage):
    global errorgroup
    global errorkey
    global params
    
    errorgroup ="coccustomgroup"
    errorkey ="coccustominfo"
    params=[successMessage]
    return

    
# method for creating Maximo company record as a current account in Logo 
def sendMessage():
    #jsonstr = createJSONstring()
    client = None
    System.out.println( 'POST Material Consumption: Send HTTP Message ')        
    postMaterialConsumption()
    returnMaterialToSAPStores()
    
# Main part
#System.out.println("AutoPosting: Entry")

if(mbo.isModified("STATUS") and mbo.getBoolean("istask")):
    if( mbo.getString("STATUS")=="COMP" ):
        sendMessage()
