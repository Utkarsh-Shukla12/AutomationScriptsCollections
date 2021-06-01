#########################################################################
# Script: ITG_PROCSTEPS
#
# Launch Point: OBJECT "ITG_PROCSTEPS" (Procedure and Steps Update for Corrigo)
#
# Author: Utkarsh Shukla
# Revision:
# Date        User          Comment
# 10/29/2020 Utkarsh Shukla Initial Version
#
########################################################################

from psdi.mbo import Mbo;
from psdi.mbo import MboSetRemote;
from java.lang import String;
from psdi.util.logging import FixedLoggerNames
from psdi.util.logging import MXLogger
from psdi.util.logging import MXLoggerFactory
from psdi.util import MXApplicationException
from psdi.mbo import MboConstants
from psdi.server import MXServer

status=mbo.getString("STATUS")
siteId=mbo.getString("SITEID")
woNum=mbo.getString("WONUM")

if(status is not None and woNum is not None):
server = MXServer.getMXServer()
userInfo = server.getSystemUserInfo()
whereClause = "WONUM='"+ woNum+"' and SITEID='INTEGUK'"
if mbo.isModified("OBSERVATION"):
server.lookup("MIC").exportData("ITG_PROCSTEPSPC","ITG_CORRIGO_EXTSYS", whereClause, userInfo, 1000)
