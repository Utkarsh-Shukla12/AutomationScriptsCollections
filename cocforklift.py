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
from java.lang import Exception
import sys
from sys import *

#Script Name: COCMATUSETRANSTOFORKLIFT
# Group Material from Matusetrans and save it to Forklift table.
#


def forkLiftOPMaterial():
    System.out.println("Starting forklift")
    wonum =mbo.getString("REFWO")
    System.out.println("REFWO::" + wonum)
    #siteid= mbo.getString(siteid)
    resultSet= getIssueMaterial(wonum,"SANAND")
    
    
    #if(checkExistingRefWO(wonum)==False):
    while(resultSet.next()): # for every row in Wonum
	#calling getBoxCount function
           Qty = getBoxCount(resultSet.getString("ITEMNUM"),resultSet.getString("COCINTBATCH"),resultSet.getString("LOTNUM"),resultSet.getDouble("QTYREQUESTED"),resultSet.getString("REFWO"),resultSet.getString("ASSETNUM"),resultSet.getString("DESCRIPTION"),resultSet.getString("STORELOC"))
           if(Qty > 0 ):# calling function updateMatusetrans
               updateMatusetrans(wonum,resultSet.getString("LOTNUM"),resultSet.getString("MATUSETRANSID"))
           else: # calling function funcDisplayError
               funcDisplayError("Mismatch of Box Quantity Vs Mentioned Quantity")
            
                
def addFokliftRecords(itemnum,refwo,binnum,intbatch,noOfBox,assetnum,description,storeloc,actualBoxQty,lotnum):# setting values from matuseTrans to cocforklift
    forkliftset= MXServer.getMXServer().getMboSet("COCFORKLIFT", mbo.getUserInfo());
    fork=forkliftset.addAtEnd();
    fork.setValue("ITEMNUM",itemnum)
    fork.setValue("COCWONUM",refwo)
    fork.setValue("COCBINNUM",binnum)
    
    fork.setValue("COCINTBATCH",intbatch)
    fork.setValue("COCQUANTITY",noOfBox)
    fork.setValue("COCTOTQTY",noOfBox)
    
    fork.setValue("COCREMQTY",actualBoxQty)
    
    fork.setValue("ASSETNUM",assetnum)
    fork.setValue("DESCRIPTION",description)
    fork.setValue("STORE",storeloc)
    fork.setValue("LOTNUM",lotnum)
    System.out.println("ITEMNUM" + itemnum)
    
    #System.out.println("Count::" + resultSet.getString("10"))
    forkliftset.save()
    forkliftset.commit()
         


def funcDisplayError(errorMessage): # Display error function with params = 'Mismatch of Box Quantity Vs Mentioned Quantity'
    global errorgroup
    global errorkey
    global params
    
    errorgroup = "CocBarcodeMiss"
    errorkey = "Barcodemissmatch"
    params=[errorMessage]

    
def getBoxCount(itemnum,intBatch,lotnum,positiveQty,refWO,assetnum,description,storeloc):
    System.out.println("itemnum:"+ itemnum)
    System.out.println("intBatch:"+ intBatch)
    System.out.println("lotnum:" + lotnum)
    System.out.println("positiveQty:" + str(positiveQty))
    System.out.println("refWO" + refWO)
    System.out.println("assetnum:" + assetnum)
    System.out.println("description:" + description)
    System.out.println("storeloc:" + storeloc)
    
    cocInvBarcodeSet = MXServer.getMXServer().getMboSet("COCINVBARCODE", mbo.getUserInfo());
    cocInvBarcodeSet.setWhere("LOTNUM=" + lotnum + " AND COCINTBATCH=" + "'" + intBatch + "'" + " AND COCBOXCONSUME=0")
    cocInvBarcodeSet.setOrderBy("COCBIN")
    cocInvBarcodeSet.setOrderBy("COCQTY")
    cocInvBarcodeSet.reset()
    cocInvBarcodeMbo = cocInvBarcodeSet.moveFirst();
    System.out.println("in getBoxcount")
    System.out.println("ReqQty:" + str(positiveQty))
    boxQty=0.00
    boxBinQty=0.0
    count=0;
    current=1
    while(cocInvBarcodeMbo): #for every row in cocInvBarcode   
        System.out.println("BQ:" + str(cocInvBarcodeMbo.getDouble("COCQTY")))
        
        if(current == 1):
            binNumberInvBarcode = cocInvBarcodeMbo.getString("COCBIN") # setting value of cocbin in binNumberInvBarcode
            System.out.println("Firsttime Bin:" + binNumberInvBarcode)
            current=0;
        
        if( binNumberInvBarcode != cocInvBarcodeMbo.getString("COCBIN")): # create a new entry for every COCBIN
            #Create a new Entry to forklift 
            System.out.println("previousBin:" + binNumberInvBarcode)
            System.out.println("CurrentBin:" +cocInvBarcodeMbo.getString("COCBIN"))
            addFokliftRecords(itemnum,refWO,binNumberInvBarcode,intBatch,count,assetnum,description,storeloc,boxBinQty,lotnum)# calling addFokliftRecords function
            boxBinQty=0.0
            
            binNumberInvBarcode = cocInvBarcodeMbo.getString("COCBIN") # Setting binNumberInvBarcode = COCBIN
            count=0
        
        boxQty = boxQty + cocInvBarcodeMbo.getDouble("COCQTY") # total number of boxes
        boxBinQty=boxBinQty + cocInvBarcodeMbo.getDouble("COCQTY");# total number of bin boxes
        
        System.out.println("BoxQty:" + str(boxQty))
        System.out.println("Count ==" + str(count))
        
        pQty = positiveQty # QTYREQUESTED
        System.out.println("float_Qty:" + str(pQty))
        System.out.println("Type::" + str(type(pQty)))
        System.out.println("TypeBox::" + str(type(boxQty)))
        
        if pQty <= boxQty:
            System.out.println("Count in If" + str(count))
            count = count + 1
            binNumberInvBarcode = cocInvBarcodeMbo.getString("COCBIN")# Setting binNumberInvBarcode = COCBIN
            addFokliftRecords(itemnum,refWO,binNumberInvBarcode,intBatch,count,assetnum,description,storeloc,boxBinQty,lotnum) # calling addFokliftRecords function
            return(count)
        else:
            count= count + 1
            System.out.println("Count in else" + str(count))
        cocInvBarcodeMbo = cocInvBarcodeSet.moveNext();
    
    return(0)


def checkExistingRefWO(refWO):
    forkSet= MXServer.getMXServer().getMboSet("COCFORKLIFT", mbo.getUserInfo());
    forkSet.setWhere("COCWONUM=" + "'" + refWO + "'")#where work order = entered wo
    
    if( forkSet.count() > 0):
        return(True)
    else:
        return(False)
    
def RemoveZeroQtyRec():
    removeForkliftSet= MXServer.getMXServer().getMboSet("COCFORKLIFT", mbo.getUserInfo());
    removeForkliftSet.setWhere("COCQUANTITY=0.00")
    removeForkliftMbo = removeForkliftSet.moveFirst()
    while(removeForkliftMbo):
        removeForkliftSet.remove(removeForkliftMbo)
        removeForkliftMbo = removeForkliftSet.moveNext()
        
    removeForkliftSet.save()
    
def updateMatLotNum(refWO,lotnum):
    matuseTransSet=MXServer.getMXServer().getMboSet("MATUSETRANS", mbo.getUserInfo());
    matuseTransSet.setWhere("REFWO=" + "'" + refWO + "'" + " AND LOTNUM=" + "'" + lotnum + "'") 
    
    matuseTransSet.getMbo(0).setValue("COCFLSENT",1,MboConstants.NOACCESSCHECK | MboConstants.NOVALIDATION_AND_NOACTION)# setting value of  cocflsent=1
    matuseTransSet.save()
    matuseTransSet.commit()   
    
def updateMatusetrans(refWO,lotnum,matid):# updating the Matusetrans table
    mxServer = MXServer.getMXServer()
    conKey = mxServer.getSystemUserInfo().getConnectionKey()
    con = mxServer.getDBManager().getConnection(conKey)
    System.out.println ("updateMatusetrans RefWO::" + refWO + " lotnum::" + lotnum)
    try:
        stmt = con.createStatement();
        #rs = stmt.executeQuery("SELECT ITEMNUM, COCSITECODE, TOSTORELOC, COCINTBATCH, COCEXTBATCH FROM MAXIMO.MATRECTRANS WHERE PONUM ='" + poNumber + "' GROUP BY ITEMNUM, COCSITECODE, TOSTORELOC, COCINTBATCH, COCEXTBATCH");
        updateCode = stmt.executeUpdate("UPDATE MAXIMO.MATUSETRANS SET COCFLSENT=1 WHERE REFWO=" + "'" + refWO + "'" + " AND LOTNUM=" + "'" + lotnum + "' AND MATUSETRANSID=" +  "'" + matid + "'")
        System.out.println("Update Return Code:::" + str(updateCode))
    except:
                System.out.println( 'SQL Exeception:' +str(exc_info()[0]))
    finally:
        System.out.println("Closing Connection")
        stmt.close();
        con.close();
        mxServer.getDBManager().freeConnection(conKey);
    
       


def getIssueMaterial(refWO,siteid):

    mxServer = MXServer.getMXServer()
    conKey = mxServer.getSystemUserInfo().getConnectionKey()
    con = mxServer.getDBManager().getConnection(conKey)
    
    try:
        stmt = con.createStatement();
        #rs = stmt.executeQuery("SELECT ITEMNUM, COCSITECODE, TOSTORELOC, COCINTBATCH, COCEXTBATCH FROM MAXIMO.MATRECTRANS WHERE PONUM ='" + poNumber + "' GROUP BY ITEMNUM, COCSITECODE, TOSTORELOC, COCINTBATCH, COCEXTBATCH");
        rs = stmt.executeQuery("SELECT ITEMNUM,DESCRIPTION,STORELOC,REFWO,ASSETNUM,COCINTBATCH,QTYREQUESTED,LOTNUM, MATUSETRANSID,COUNT(COCINTBATCH)  FROM MAXIMO.MATUSETRANS WHERE REFWO ='" + refWO + "'" + " AND COCFLSENT=0 AND ISSUETYPE='ISSUE' GROUP BY ITEMNUM,REFWO,ASSETNUM,DESCRIPTION,STORELOC,COCINTBATCH,QTYREQUESTED,LOTNUM,MATUSETRANSID");
              
        # create CachedRowSet and populate
        crs = CachedRowSetImpl();
        crs.populate(rs);
    except:
                System.out.println( 'SQL Exeception:' +str(exc_info()[0]))
    finally:
        System.out.println("Closing Connection")
        rs.close();
        stmt.close();
        con.close();
        mxServer.getDBManager().freeConnection(conKey);
    
    return crs;

#Main 
forkLiftOPMaterial()#Inisilizing the program