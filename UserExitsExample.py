# Owner: Trishala Thakur
# Created date: 25 April, 2022
# Version: 1.0
# Description: Custom Script for Adding all the Values for ATLAS Notice Sent
# LANGUAGE:PYTHON
# Script: PUBLISH.WPD_ATLASNOTICE_SENDEXT.USEREXIT.OUT.BEFORE
#
# Version History##
#
###------------------------------------------------------------------------------------------------------------
# Version Developer Date Modified Reason for modifiaction Developer Comments
###------------------------------------------------------------------------------------------------------------
#
# Intial Draft Utkarsh Shukla 25 April ,2022 Original script Created
#
#--------------------------------------------------------------------------------------------------------------

###-------------------------------------------------------------------------------------------------------------
# Import Librarires
###-------------------------------------------------------------------------------------------------------------

from psdi.server import MXServer
from psdi.iface.mic import StructureData
from psdi.iface.migexits import UserExit

###------------------------------------------------------------------------------------------------------------------
# Define your Variables WPD_ADDCONT
###------------------------------------------------------------------------------------------------------------------

configData = MXServer.getMXServer().getConfig()
mbo=irData.getCurrentMbo()

WrcoordSet=mbo.getMboSet("WPD_WRCOORDINATES")
wrcoordmbo=WrcoordSet.getMbo(0)
Woset=mbo.getMboSet("WPD_WI")
wombo=Woset.getMbo(0)
CompSet=wombo.getMboSet("WPD_ATLSNS")
compmbo=CompSet.getMbo(0)
purchSet=wombo.getMboSet("WPD_WOPURCHVIEW")
purchmbo=purchSet.getMbo(0)
###------------------------------------------------------------------------------------------------------------------
# Define your Functions
###------------------------------------------------------------------------------------------------------------------

###------------------------------------------------------------------------------------------------------------------
# Main program
###------------------------------------------------------------------------------------------------------------------

irData.setCurrentData("WPD_ADDCONT",configData.getProperty("WPD_Promoter_Name"))
irData.setCurrentData("WPD_ADDCONTNUM",configData.getProperty("WPD_company_telephone_number"))
irData.setCurrentData("WPD_ADDCONTADDR1",configData.getProperty("WPD_ADDCONTADDR1"))
irData.setCurrentData("WPD_ADDCONTADDR2",configData.getProperty("WPD_ADDCONTADDR2"))
irData.setCurrentData("WPD_ADDCONTADDR3",configData.getProperty("WPD_ADDCONTADDR3"))
irData.setCurrentData("WPD_ADDCONTADDR4",configData.getProperty("WPD_ADDCONTADDR4"))
irData.setCurrentData("WPD_ADDCONTADDR5",configData.getProperty("WPD_ADDCONTADDR5"))
irData.setCurrentData("WPD_ADDPOSTCODE",configData.getProperty("WPD_ADDPOSTCODE"))
irData.setCurrentData("WPD_APPTYPE",'0200')
#irData.setCurrentData("WPD_DNOID",7003)

irData.setCurrentData("WPD_WORKCATEGORY",mbo.getInt("WPD_WORKCATEGORY"))
irData.setCurrentData("WPD_EXCAVATIONTYPE",mbo.getInt("WPD_EXCAVATIONTYPE"))
irData.setCurrentData("WPD_COLLTYPE",mbo.getInt("WPD_COLLTYPE")) #WPD_COLLTYPE
irData.setCurrentData("WPD_CARRIAGEWAYRESTYPE",mbo.getInt("WPD_CARRIAGEWAYRESTYPE")) #WPD_CARRIAGEWAYRESTYPE
irData.setCurrentData("WPD_CLOSEFOOT",mbo.getInt("WPD_CLOSEFOOT"))
irData.setCurrentData("WPD_WORKCATEGORY",mbo.getInt("WPD_WRKTYPE"))
irData.setCurrentData("WPD_PARKINGSUS",mbo.getInt("WPD_PARKINGSUS"))
irData.setCurrentData("WPD_OUTSIDEWORKINGHOURS",mbo.getBoolean("WPD_OUTSIDEWORKINGHOURS"))

if compmbo is not None:
    irData.setCurrentData("WPD_ADDRESS1",compmbo.getString("ADDRESS1"))
    irData.setCurrentData("WPD_ADDRESS2",compmbo.getString("ADDRESS2"))
    irData.setCurrentData("WPD_ADDRESS3",compmbo.getString("ADDRESS3"))
    irData.setCurrentData("WPD_ADDRESS4",compmbo.getString("ADDRESS4"))

if purchmbo is not None:
    irData.setCurrentData("WPD_CONTRACTNUM",purchmbo.getString("CONTRACTNUM"))
    #irData.setCurrentData("WPD_CONTACT",purchmbo.getString("CONTACT"))
    irData.setCurrentData("WPD_CONTACT",'Vendor1')
    irData.setCurrentData("WPD_STARTDATE",purchmbo.getDate("STARTDATE"))

if wrcoordmbo is not None:
    irData.setCurrentData("WPD_DNOID",wrcoordmbo.getString("WPD_SWA"))
    irData.setCurrentData("WPD_WORKSTREAMPREFIX",wrcoordmbo.getString("WPD_WRKSTRM"))
    irData.setCurrentData("WPD_STREETDESCRIPTOR",wrcoordmbo.getString("WPD_STREETDESCRIPTOR"))
    irData.setCurrentData("WPD_COORDINATETYPE",wrcoordmbo.getInt("WPD_COORDINATETYPE"))
    #raise TypeError(wrcoordmbo.getString("WPD_COORDINATETYPE"))
    irData.setCurrentData("WPD_USRN",wrcoordmbo.getInt("WPD_USRN"))
    irData.setCurrentData("WPD_LATITUDE",wrcoordmbo.getFloat("WPD_LATITUDE"))
    irData.setCurrentData("WPD_LONGITUDE",wrcoordmbo.getFloat("WPD_LONGITUDE"))
    irData.setCurrentData("WPD_SECWORKCOORDX",wrcoordmbo.getFloat("WPD_SECWORKCOORDX"))
    irData.setCurrentData("WPD_SECWORKCOORDY",wrcoordmbo.getFloat("WPD_SECWORKCOORDY"))
