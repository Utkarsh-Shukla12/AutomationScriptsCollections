#############################
# Script -> BATCHNUMSET
# Description -> Validating SFG2FGTRACE's Quantity
# Developer: -> Utkarsh Shukla
# Language : -> Python
# launchpoint -> Attribute -> Validate
# Credated date: -> 19 May, 2020
# Version: -> 1.4
# Modified by: ->
# Reason for change: ->
#############################


from  psdi.util import MXApplicationException;
from  psdi.util import MXException;
from  com.sun.rowset import CachedRowSetImpl;

from psdi.mbo import Mbo, MboRemote, MboSet, MboSetRemote, MboConstants
from psdi.security import UserInfo
from psdi.server import MXServer
from psdi.util.logging import MXLogger
from psdi.util.logging import MXLoggerFactory


logger=MXLoggerFactory.getLogger("maximo.script")
logger.debug("==Quantity Validation." + launchPoint + ": START ==")


wonum = mbo.getString("WONUM")
logger.debug("=Wonum: ===" + wonum)

worktype = mbo.getString("WORKTYPE")
logger.debug("=Wotype: ===" + worktype)

PoSet = mbo.getMboSet("$WORKORDER", "WORKORDER", "WONUM = :Wonum and WORKTYPE =:WORKTYPE");

PoSet.reset()
PoMbo = PoSet.moveFirst();

poqty = PoMbo.getInt("POQUANTITY");
poqty1 = PoMbo.getInt("POQUANTITY");

logger.debug("=POQUANTITY: ===" +str( poqty))

enqty = mbo.getDouble("QUANTITY")
logger.debug("=EnteredQUANTITY: ===" + str(enqty))
qty = 0

spo = mbo.getString("SOURCEPO");

#SyrupbatchSet = mbo.getMboSet("$COCSFG2FGTRACE", "COCSFG2FGTRACE", "SOURCEPO=:SOURCEPO")
SyrupbatchSet = mbo.getThisMboSet();

#SyrupbatchSet.reset()
#SyrupbatchSet.moveFirst();

SyrupCount = SyrupbatchSet.count();
logger.debug("=Count in COCSFG2FGTRACE: ===" +str( SyrupCount))
if (SyrupCount == 1):
	newqtyMbo = SyrupbatchSet.getMbo(0)
	if enqty > poqty:
        
		params=["Entered Quantity is greater than Process order Quantity "]
		errorgroup= "QuantitySyrp"
		errorkey= "Qty"
		warnparams = [params]

else:
	for i in range (SyrupCount):
	#for i in range (newqtyMbo = SyrupbatchSet.getMbo(i) != None):
		newqtyMbo = SyrupbatchSet.getMbo(i)
		qty = qty + newqtyMbo.getInt("QUANTITY")
		#newqty = poqty - qty
		logger.debug("=Total Entered QUANTITY: ===" + str(qty))
		#logger.debug("=Total Required QUANTITY: ===" + str(newqty))
		
		if qty > poqty :
			logger.debug("=Entered Qty is greater than Process order Quantity : ===" +str( qty)+ "<" +  str(enqty) )
			params=["Entered Quantity is greater than Process order Quantity "]
			errorgroup= "QuantitySyrp"
			errorkey= "Qty"
			warnparams = [params]
		
"""if qty == poqty:
	logger.debug("=Entered Qty is Equal to Process order Quantity : ===" +str( poqty)+ "=" +  str(qty) )
	params=["No more Quantity left in this Process Order"]
	errorgroup= "QuantitySyrp"
	errorkey= "Qty"
	warnparams = [params]
	
	poqty = PoMbo.getInt("POQUANTITY");
		
	

			
	elif enqty > poqty:
        
	params=["Entered Quantity is greater than Process order Quantity "]
  	errorgroup= "QuantitySyrp"
	errorkey= "Qty"
	warnparams = [params]"""
