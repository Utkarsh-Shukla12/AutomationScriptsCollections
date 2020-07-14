# Variables
# ARCHIVEDAYS (Int 60)
#   Days to maintain audit records. Leave 0 for Unlimited
# EMAILERROR 
#   List of Comma Separated Values to Email On Error
# EMAILSUCCESS
#   Comma Separated List of Email Addresses to Send on Success

from psdi.server import MXServer
import sys
from psdi.mbo import SqlFormat,MaxSequence,DBShortcut
from com.sun.rowset import CachedRowSetImpl
from psdi.util.logging import MXLoggerFactory
from java.util import Calendar

projetechLogger = MXLoggerFactory.getLogger("maximo")
maxServer = MXServer.getMXServer()
clientURL = str(maxServer.getProperty("mxe.hostname"))
conKey = runAsUserInfo.getConnectionKey() # Get Unique Connection Key
dummyMbo=maxServer.getMboSet("DUMMY_TABLE",runAsUserInfo).moveFirst()
connect = dummyMbo.getMboServer().getDBConnection(conKey) # Get Connection (Used to get EAUDITTRANSID)

strTransID = str(MaxSequence.generateKey(connect,'EAUDIT','TRANSID'))
dbPlatform = maxServer.getMaximoDD().getDBPlatform() # Returns 1 for Oracle, 2 for SQL Server, 3 for DB2
    
def executeQuery(query,parameters):
    errorMessage=""
    resultSet=CachedRowSetImpl()
    try:
        dbShortcut = DBShortcut()
        dbShortcut.connect(conKey)
        sqfQuery = SqlFormat(query)
        count=0
        for parameter in parameters:
            count+=1
            sqfQuery.setObject(count,parameter["datatype"],parameter["value"])
        query = sqfQuery.format()
        projetechLogger.debug("Query:" + query)
        resultSet.populate(dbShortcut.executeQuery(query))
    except:
        errorMessage = "Error: " + str(sys.exc_info()[0]) + ". Message: " + str(sys.exc_info()[1])
    finally:
        dbShortcut.close()
        
    return errorMessage,resultSet
    
def executeNonQuery(sqf):
    conKey = runAsUserInfo.getConnectionKey()
    dbShortcut = DBShortcut()
    dbShortcut.connect(conKey)    
    dbShortcut.execute(sqf)
    
    # Commit
    dbShortcut.commit()
def EmailError(strErrorMessage):
    projetechLogger.error("Error occurred during Inventory Audit. Error Message: " + strErrorMessage)
    maxServer.sendEMail(EMAILERROR,"DoNotReply@emaximo.com",clientURL + " Inventory Audit Error", str(strErrorMessage))
    service.error("emx","inventoryAuditFailed")
    
def EmailSuccess():
    maxServer.sendEMail(EMAILSUCCESS,"DoNotReply@emaximo.com",clientURL + " Inventory Audit Completed", "The Inventory Audit was successfully completed.")
    
def GetAuditTable(strTable):
    parameters=[]
    parameters.append({"datatype":"ALN","value":strTable})
    strAuditQuery = "SELECT eaudittbname FROM maxtable WHERE tablename=:1"
    strAuditTable = ""
    errorMessage,rsAuditTable = executeQuery(strAuditQuery,parameters)
    
    while(rsAuditTable.next()):
        strAuditTable = rsAuditTable.getString(1)
        
    return strAuditTable

def getWhereClause(table):
    whereClause=""
    
    if table=="INVENTORY":
        whereClause=" WHERE exists(SELECT 1 FROM locations WHERE locations.location=inventory.location and locations.siteid=inventory.siteid )"
    elif table=="INVCOST":
        whereClause=" WHERE exists(SELECT 1 FROM locations WHERE locations.location=invcost.location and locations.siteid=invcost.siteid )"
    elif table=="INVBALANCES":
        whereClause=" WHERE exists(SELECT 1 FROM locations WHERE locations.location=invbalances.location and locations.siteid=invbalances.siteid )"
    return whereClause
    
def PopulateTable(strTable,strAuditTable):
    try:
        parameters=[]
        parameters.append({"datatype":"ALN","value":strTable})
        strSQLQueryFields="SELECT columnname FROM maxattribute WHERE objectname=:1 and persistent=1 and attributename!='EMXINVENTORYDATE'"
        strFields=""
        
        errorMessage,rsFields = executeQuery(strSQLQueryFields,parameters)
        while(rsFields.next()):
            strFields=strFields + rsFields.getString(1) + ","
        
        strInsertStatement="INSERT INTO " + strAuditTable + "(" + strFields + "eauditusername,eaudittype,eaudittransid,eaudittimestamp,EMXINVENTORYDATE) SELECT " + strFields+"'MAXADMIN','I',"+strTransID+","
        
        if(dbPlatform==1): # Oracle
            strInsertStatement = strInsertStatement + "TRUNC(sysdate),TRUNC(sysdate) FROM " + strTable
        elif(dbPlatform==2): # SQL Server
            strInsertStatement = strInsertStatement + "CAST(getdate() AS date),CAST(getdate() AS date) FROM " + strTable
        strInsertStatement+=getWhereClause(strTable)
        sqfInsert = SqlFormat(strInsertStatement)
        executeNonQuery(sqfInsert)
    except: 
        strErrorMessage = "An unexpected error occurred. Exception: " + str(sys.exc_info()[0]) + ". Message: " + str(sys.exc_info()[1])
        EmailError(strErrorMessage)

    return True

def RemoveRecords(strAuditTable):
    try:
        strDeleteStatement="DELETE FROM " + strAuditTable + " WHERE "
        
        if(dbPlatform==1): # Oracle
            strDeleteStatement += " (TRUNC(sysdate) - TRUNC(EMXINVENTORYDATE)) >" + str(ARCHIVEDAYS) + " AND TO_CHAR(EMXINVENTORYDATE, 'DD') !='01'"
        elif(dbPlatform==2): # SQL Server
            strDeleteStatement += "EMXINVENTORYDATE<getdate()-" + str(ARCHIVEDAYS)+ " AND DATEPART(DAY,EMXINVENTORYDATE) != 1 "
        
        sqfDelete = SqlFormat(strDeleteStatement)
        executeNonQuery(sqfDelete)
    except:
        strErrorMessage = "An unexpected error occurred. Exception: " + str(sys.exc_info()[0]) + ". Message: " + str(sys.exc_info()[1])
        EmailError(strErrorMessage)
    return True
    
# End Functions

# Enter Main
if(dbPlatform==3):
    EmailError("DB2 isn't currently supported by this automation script. SQL Statements need to be adjusted to handle the additional platform.")
else:
    # Verify it hasn't run in the past hour (various bugs have caused duplicate runs). Each run should be substantially less than 1 hour.
    cal=Calendar.getInstance()
    cal.add(Calendar.HOUR,-1)
    # instanceName is an implict variable set by Maximo for cron task that is a combination of crontaskname.instancename. 
    # So while one would assume instanceName matches the instanceName, it's actually the unique combination and thus we have to split.
    cronName=instanceName.split(".")
    # CRONTASKHISTORY is created when the instance starts. When that happens the starttime will equal the end time. If a different execution occurred, the times will be different.
    relationship="crontaskname=:1 and instancename=:2 and activity='ACTION' and starttime>:3 and starttime!=endtime"
    sqf = SqlFormat(relationship)
    sqf.setObject(1,"ALN",cronName[0])
    sqf.setObject(2,"ALN",cronName[1])
    sqf.setTimestamp(3,cal.getTime())
    historySet=dummyMbo.getMboSet("$EMXINVENTORAUDIT_HIST","CRONTASKHISTORY",sqf.format())
    historySet.reset()
    if not historySet.isEmpty():
        EmailError("Cron task history shows this cron task has already executed so we're skipping this execution.")
        
    # Hardcoded list of tables now as we have special logic and order that is required.
    lstTables = ["ITEM","INVBALANCES","INVENTORY","INVCOST"]
    for table in lstTables:
        auditTable = GetAuditTable(table)
        PopulateTable(table,auditTable)
    
    # Wait to do deletes until the end. If an issue occurs, this is the least important part. Getting data loaded is time sensitive
    if(ARCHIVEDAYS!=0):
        for table in lstTables:
            auditTable = GetAuditTable(table)
            RemoveRecords(auditTable)
        
    EmailSuccess()

# End Main
