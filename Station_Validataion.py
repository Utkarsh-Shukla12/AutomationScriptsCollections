#####################
############################################################################################################################
# Name: WAM_ATTR_STATIONLOCATION
# Launch Point: Attribute
# Event: Validate
#
# Script to validate Locations in CU
#              
############################################################################################################################
# Developer                      Version Date            launchPoint       Remarks                              
#--------------------------------------------------------------------------------------------------------------------------
#
#Utkarsh Shukla 1.0     04/06/2019        WAM_ATTR_STATIONLOCATION      Script to validate Locations in CU
#
############################################################################################################################*/

estimatEntity=0
cuLocation = mbo.getString("LOCATION")
cuParentSpec=mbo.getMboSet("PLUSDESTCONTROLSTATIONREL")
if cuParentSpec is not None and cuParentSpec.getMbo(0) is not None:
    estimatEntity=cuParentSpec.getMbo(0).getString("WAMENTITY")
if estimatEntity==0:
    errorkey='WAMSAVEMSG'
    errorgroup='WAMESTIMATE'
else:
    LocMboSet = mbo.getMboSet("$StationLocation", "LOCATIONS", "LOCATION ='"+cuLocation+"' and WAMENTITY='"+estimatEntity+"'")

    if LocMboSet.getMbo(0) is None:
        params=[str(estimatEntity)]
        errorkey='INVALIDSTATIONLOCATON'
        errorgroup='WAMPLUSDCUEST'
