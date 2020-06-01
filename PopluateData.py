# Integraton to populate street Address-CSD to Maximo(146)

from java.lang import String
from psdi.server import MXServer
from psdi.mbo import MboSetRemote
from psdi.mbo import MboSet
from psdi.mbo import Mbo
from psdi.mbo import MboRemote
from java.util import Calendar;
cal = Calendar.getInstance();
date=cal.getTime();
#==================================Breaking structure data ======================================
erData.breakData();
#==================================Defaulting the variable =======================================
maximo = MXServer.getMXServer();
userInfo = maximo.getSystemUserInfo();

###
# Get Variables
###

prefix = ""
addressStreet=""
addressType=""
suffix= ""
city=""
stateProvince=""
csdStatus=""
commodity=""
entity=""
businessFunction=""
externalrefid=""
streetAddress=""
formattedAddress=""

###
# Setting Integration Variables
###

if(erData.getCurrentData("WAMEXTERNALREFID") is not None):
	externalrefid=erData.getCurrentData("WAMEXTERNALREFID");
	
if(erData.getCurrentData("STADDRDIRPRFX") is not None):
	prefix=erData.getCurrentData("STADDRDIRPRFX");
	
if(erData.getCurrentData("STADDRSTREET") is not None):
	addressStreet=erData.getCurrentData("STADDRSTREET");
	
if(erData.getCurrentData("STADDRSTTYPE") is not None):
	addressType=erData.getCurrentData("STADDRSTTYPE");
	
if(erData.getCurrentData("STADDRDIRSFX") is not None):
	suffix=erData.getCurrentData("STADDRDIRSFX");
	
if(erData.getCurrentData("CITY") is not None):
	city=erData.getCurrentData("CITY");
	
if(erData.getCurrentData("WAMCSDSTATUS") is not None):
	csdStatus=erData.getCurrentData("WAMCSDSTATUS");

if(erData.getCurrentData("STATEPROVINCE") is not None):
	stateProvince=erData.getCurrentData("STATEPROVINCE");
	
if(erData.getCurrentData("WAMCSDBUSINESSCODE") is not None):
	businessFunction=erData.getCurrentData("WAMCSDBUSINESSCODE")
else:
	businessFunction=""
	
if(erData.getCurrentData("STATEPROVINCE") is not None):
	territoryValue=erData.getCurrentData("STATEPROVINCE")
else:
	territoryValue=""		
		
###
# Determine Business Function & Entity based on Inputs
###
	
if businessFunction is not None and territoryValue is not None:
	if businessFunction=="CE" and territoryValue=="CT":		
		commodity="ELECTRIC"
		businessFunction="D"
		entity="11"
		territoryValue="CT"		
	if businessFunction=="EN" and territoryValue=="MA":
		commodity="ELECTRIC"
		businessFunction="D"
		entity="21"
		territoryValue="MA"		
	if businessFunction=="ME" and territoryValue=="MA":
		commodity="ELECTRIC"
		businessFunction="D"
		entity="41"
		territoryValue="MA"		
	if businessFunction=="NE" and territoryValue=="NH":
		commodity="ELECTRIC"
		businessFunction="D"
		entity="06"
		territoryValue="NH"		
	if businessFunction=="CG"  and territoryValue=="CT":
		commodity="GAS"
		businessFunction="D"
		entity="71"
		territoryValue="CT"		
	if businessFunction=="GN" and territoryValue=="MA":
		commodity="GAS"
		businessFunction="D"
		entity="2Y"
		territoryValue="MA"		
	if businessFunction=="XM" and territoryValue=="CT":
		commodity="ELECTRIC"
		businessFunction="T"
		entity="1T"
		territoryValue="CT"		
	if businessFunction=="XM" and territoryValue=="MA":
		commodity="ELECTRIC"
		businessFunction="T"
		entity="4T"
		territoryValue="MA"		
	if businessFunction=="XM" and territoryValue=="NH":
		commodity="ELECTRIC"
		businessFunction="T"
		entity="6T"
		territoryValue="NH"


###
# Formatting fields
###

	if (prefix):
		streetAddress = streetAddress + prefix+" "
		formattedAddress = formattedAddress + prefix+" "
	if (addressStreet):
		streetAddress = streetAddress + addressStreet+" "
		formattedAddress = formattedAddress + addressStreet+" "
	if (addressType):
		streetAddress = streetAddress + addressType+" "
		formattedAddress = formattedAddress + addressType+" "		
	if (suffix):
		streetAddress = streetAddress + suffix+" "
		formattedAddress = formattedAddress + suffix+" "			
	if (city):
		formattedAddress = formattedAddress + city+" "
	if (stateProvince):
		formattedAddress = streetAddress + stateProvince+" "


	#streetAddress=prefix+" "+addressStreet+" "+addressType+" "+suffix

	#formattedAddress=prefix+" "+addressStreet+" "+addressType+" "+suffix+" "+city+" "+stateProvince
	
	locDescription=commodity+" | "+businessFunction+" | "+entity+" | "+formattedAddress
	
	SaDescription = "CSD Street: " + formattedAddress
	

###
# Setting Integration Fields
###
	
	erData.setCurrentData("FORMATTEDADDRESS",formattedAddress)
	erData.setCurrentData("DESCRIPTION",SaDescription[:70])
	erData.setCurrentData("STREETADDRESS",streetAddress)
	
###
# Dealing with Locations & Setting Status
###

	locationsSet = maximo.getMboSet("LOCATIONS",userInfo)
	locationsSet.setWhere("EXTERNALREFID='"+externalrefid+"' and TYPE='STREET' and SOURCESYSID='CSD'")
	locationsSet.reset()
	
	locationMbo = locationsSet.moveFirst()
	while (locationMbo):
		updateLocDescription=locationMbo.getString("WAMCOMMODITY")+" | "+locationMbo.getString("WAMBUSINESSFUNCTION")+" | "+locationMbo.getString("WAMENTITY")+" | "+formattedAddress

#Defect-5978: Changes CSDSTATUS = 1: Location status OPERATING, CSDSTATUS= 0:  Location Status CSDDELETED
		if csdStatus=="1" and locationMbo.getString("STATUS")!='OPERATING':	
			locationMbo.changeStatus("OPERATING",MXServer.getMXServer().getDate(), "CSD Status Change", True, False,True, False, False, False)
			updateLocDescription = updateLocDescription + "- Operating"
		elif csdStatus=="0" and locationMbo.getString("STATUS")!='CSDDELETED':
			locationMbo.changeStatus("CSDDELETED",MXServer.getMXServer().getDate(), "CSD Status Change", True, False,True, False, False, False)
			updateLocDescription = updateLocDescription + "- Retired"
			
		
		locationMbo.setValue("DESCRIPTION",updateLocDescription[:140])		
		locationMbo = locationsSet.moveNext()

	locationsSet.save()
	
###
# Create New Location
###

	serviceAddressSet=maximo.getMboSet("SERVICEADDRESS",userInfo)
	serviceAddressSet.setWhere("WAMEXTERNALREFID='"+externalrefid+"'")
	serviceAddressSet.reset()
	
	
	locationsSet.setWhere("EXTERNALREFID='"+externalrefid+"' and TYPE='STREET' and SOURCESYSID='CSD' and WAMENTITY='"+entity+"' and WAMCOMMODITY='"+commodity+"' and WAMBUSINESSFUNCTION='"+businessFunction+"'")
	locationsSet.reset()

	if locationsSet.getMbo(0) is None and businessFunction is not None and territoryValue is not None and businessFunction!="" and territoryValue!="":
		newlocation=locationsSet.add()
		newlocation.setValue("WAMCOMMODITY",commodity)
		newlocation.setValue("WAMBUSINESSFUNCTION",businessFunction)
		newlocation.setValue("WAMENTITY",entity)		
		newlocation.setValue("WAMTERRITORY",territoryValue)
		newlocation.setValue("DESCRIPTION",locDescription[:140])
		newlocation.setValue("TYPE",'STREET')	
		newlocation.setValue("EXTERNALREFID",externalrefid)
		newlocation.setValue("SOURCESYSID","CSD")
		if serviceAddressSet.getMbo(0) is not None:
			serviceAddress=serviceAddressSet.getMbo(0).getString("ADDRESSCODE")
			newlocation.setValue("SADDRESSCODE",serviceAddress)
	locationsSet.save()
