/* ###########################
# Developer: Utkarsh Shukla
# Script Name: CALCUALTE_EUR
# Desciption:Calculate EUR on click of button
# Language: Javascript
# Launchpoint: Action -> Click of button
############################# */

// Import libraries and modules

importPackage(Packages.psdi.server);
importPackage(Packages.psdi.mbo);
importPackage(Packages.psdi.iface.mic);
importPackage(Packages.java.io);
importPackage(Packages.java.util);
importPackage(Packages.psdi.util);
importPackage(Packages.com.ibm.json.java);
importPackage(Packages.org.apache.http);
importPackage(Packages.org.apache.http.client.methods);
importPackage(Packages.org.apache.http.impl.client);
importPackage(Packages.org.apache.http.entity);
importPackage(Packages.org.apache.http.message);
importClass(Packages.psdi.util.logging.MXLogger);
importClass(Packages.psdi.util.logging.MXLoggerFactory);
importClass(Packages.java.text.SimpleDateFormat);
importClass(Packages.com.hccb.restclient.outbound.DefaultJsonClient);


var logger=MXLoggerFactory.getLogger("maximo.script");
var maximo = MXServer.getMXServer();


function getLastHourReading(meter)
{
	var reading = 0;
	var meterReadingSet = maximo.getMboSet("MEASUREMENT", mbo.getUserInfo());
	meterReadingSet.setWhere("METERNAME='" + meter + "'");
	meterReadingSet.reset();
	if (!meterReadingSet.isEmpty())
	{
		reading = meterReadingSet.moveFirst().getDouble("MEASUREMENTVALUE");
		
		logger.info(meter +  " Latest Reading:" + reading);
	}
	var lhreading = 0;
	var lhmeterReadingSet = maximo.getMboSet("MEASUREMENT", mbo.getUserInfo());
	lhmeterReadingSet.setWhere("METERNAME='" + meter + "' AND MEASUREDATE IN (SELECT MAX(MEASUREDATE) FROM MEASUREMENT WHERE METERNAME=:METERNAME AND MEASUREDATE BETWEEN SYSDATE - 2 HOUR AND SYSDATE - 1 HOUR)");
	lhmeterReadingSet.reset();
	if (!lhmeterReadingSet.isEmpty())
	{
		lhreading = lhmeterReadingSet.moveFirst().getDouble("MEASUREMENTVALUE");
		
		logger.info(meter + " Last Reading:" + reading);
	}
	
	meterReadingSet.cleanup();
	lhmeterReadingSet.cleanup();
	
	return (reading - lhreading);
}





var totalElecEnergyUnit = getLastHourReading("PCC-1-TRANS01IC-ACT_ENG_DEL") + getLastHourReading("PCC-2-TRANS2OF-ACT_ENG_DEL") + getLastHourReading("UTIL-SOLARIN-ACT_ENG_DEL") + getLastHourReading("PCC-1-DGIC-ACT_ENG_DEL") + getLastHourReading("PCC-2-DG2-1500KVAIC-ACT_ENG_DEL") + getLastHourReading("PCC-2-DG3-500KVAIC-ACT_ENG_DEL");

var actDiesel =  getLastHourReading("SAU1BO130073");
var actCng =  getLastHourReading("SAU1BO130075");

var totalEnergy = (totalElecEnergyUnit * 3.6) + (actDiesel * 39) + (actCng * 50);

var totalEUR = totalEnergy / 200 ;

logger.info("TotalEUR:" + totalEUR)
