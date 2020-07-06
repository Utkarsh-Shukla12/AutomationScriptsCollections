############################################################################################################################
# Name:  Script_Missing_Components_from_ValidationScript.py
#
# This script is to check the Master DD MXLoader for various components and prepare the report by comparing it with Script_validates_ConsolidatedComponents.sql. It gives the list of values which are not included in validation script.
#               
############################################################################################################################
# Developer                      Version	Date            Remarks				      									                              
#-------------------------------------------------------------------------------------------------------------------------- 
#
# Utkarsh Shukla                1.0     25/06/2020	     It gives the list of values which are not included in validation script for Conditions, Domains, Relationships, Messages, Indexes, Maxattributes 	                      
#
############################################################################################################################*/	

import xlwings as xw
import logging


LOG_FILENAME = 'ScriptLog.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.debug('Script_Missing_Components_from_ValidationScript Started')

def textCheck(Value,lineText,SheetName):
	with open('Script_validates_ConsolidatedComponents.sql') as f :
		datafile = f.readlines()
	
	for line in datafile :
		if SheetName=='02 DD WAMObj-woDom(Add)' :
			if Value in line :
				return  True
		
		else:
			if lineText in line:
				if Value in line :
					return  True

app = xw.App(visible=False) # IF YOU WANT EXCEL TO RUN IN BACKGROUND

xlwb = xw.Book('C:\Utkarsh\Task\Validation Scripts\Script to automate\ESE_WAM_R2_01_Data Dictionary MxLoader_Master.xlsm')

xlws = {}
file1 = open("ExceptionReport.txt","w")
column='A'
lineText=''
falseValueArray=[]

SheetNames= ['01 Conditional Expression ALL','04 Table & CrossOver Domain', '06 MaxRelationship ALL', '08 MaxMessages ALL', '09 Indexes', '02 DD WAMObj-woDom(Add)']

for k in range(len(SheetNames)):
	
	logging.debug('SheetName ' +SheetNames[k])

	xlws['ws1'] = xlwb.sheets[SheetNames[k]]
	rowNum = xlws['ws1'].range(1,1).end('down').row
	
	if SheetNames[k]== '09 Indexes' :
		column='AB'
		lineText='INDEXES as component'
		Component='INDEXES'
	else:
		if SheetNames[k]== '01 Conditional Expression ALL' :
			lineText='CONDITIONNUM as component'
			Component='CONDITIONS'
		if SheetNames[k]== '04 Table & CrossOver Domain' :
			lineText='domainid as component'
			Component='DOMAINS'
		if SheetNames[k]== '06 MaxRelationship ALL' :
			Component='RELATIONSHIPS'
			lineText='a.name as component'
		if SheetNames[k]== '08 MaxMessages ALL' :
			Component='MESSAGES'
			lineText='MSGKEY as component'
		if SheetNames[k]== '02 DD WAMObj-woDom(Add)' :
			column='B'
			lineText='attributename as component'
			Component='MAXATTRIBUTES'
	
	
	j=''
	m=''
	falseValueArray=[]
	
	file1.write('\n----------------------\n'+Component+'\n----------------------\n') 
	
	logging.debug('Full range ' +str(rowNum))

	for i in range(3,rowNum+1):
		
		if SheetNames[k]== '02 DD WAMObj-woDom(Add)' :
			j=column+str(i)
			m='AT'+str(i)
			Value=str(xlws['ws1'].range(j).value)+' - '+str(xlws['ws1'].range(m).value)
		else:
			j=column+str(i)
			Value=xlws['ws1'].range(j).value
		
				
		textChk =textCheck(Value,lineText,SheetNames[k])
		
		if textChk !=True:
			if Value not in falseValueArray:
				falseValueArray.append(Value)
				logging.debug('Text Found false: Updating the .txt file withe the value ' +Value)
				file1.write(Value+'\n')
	logging.debug('textCheck final falsevalueArray= ' +str(falseValueArray))				
			 
					

file1.close() #to change file access modes 
xlwb.close()
######################## Updated Script #############################
############################################################################################################################
# Name:  Script_Missing_Components_from_ValidationScript.py
#
# This script is to check the Master DD MXLoader for various components and prepare the report by comparing it with Script_validates_ConsolidatedComponents.sql. It gives the list of values which are not included in validation script.
#               
############################################################################################################################
# Developer                      Version	Date            Remarks				      									                              
#-------------------------------------------------------------------------------------------------------------------------- 
#
# Utkarsh                  1.0     25/06/2020	     It gives the list of values which are not included in validation script for Conditions, Domains, Relationships, Messages, Indexes, Maxattributes 	                      
#
############################################################################################################################*/	

import xlwings as xw
import logging


LOG_FILENAME = 'ScriptLog.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.debug('Script_Missing_Components_from_ValidationScript Started')

def textCheck(Value,lineText,SheetName):
	with open('Script_validates_ConsolidatedComponents.sql') as f :
		datafile = f.readlines()
	
	for line in datafile :
		if SheetName=='02 DD WAMObj-woDom(Add)' :
			if Value in line :
				return  True
		
		else:
			if lineText in line:
				if Value in line :
					return  True

def packageExportFileCheck(whereClauseValue,lineText,Component,appName,falseArray):
			
	whereClauseComponents= whereClauseValue.split(',')
	
	
	for l in range(len(whereClauseComponents)):
		whereClauseComponent=whereClauseComponents[l].strip("'")
		whereClauseComponent=whereClauseComponent.strip('\n\n\n\n'+"('")
		whereClauseComponent=whereClauseComponent.strip(" '")
		
		if Component=='SIG OPTIONS':
			whereClauseComponent=appName+' - '+whereClauseComponent
			
		logging.debug(Component+' : ' +str(whereClauseComponent))
		
		if Component=='AUTOMATION SCRIPTS':
			ScriptstoExclude=['PUBLISH.WAM_MXTOPMV_PC.EVENTFILTER','PUBLISH.WAM_MXTOPV_WO_PC.USEREXIT.OUT.BEFORE','PUBLISH.WAM_PVERA_TSKASG_PC.EVENTFILTER','PUBLISH.WAM_PVERA_TSKASG_PC.USEREXIT.OUT.BEFORE','SYNC.WAM_C2TOMX_ES.EXTEXIT.IN','WAM_ACT_PUSHCLICKWO','WAM_ACT_PUSHCONVERSIONWO','WAM_ATTR_FAILURECODE','WAM_ATTR_WAMPROJSEGNO','WAM_OBJ_WAMFORMDATA','WAMPROJECTIDRESTRICT','WAMRULEVALIDATE']
			if whereClauseComponent in ScriptstoExclude:
				return
		
		
		textChk =textCheck(whereClauseComponent,lineText,'PackageExport')
		if textChk !=True:
			if whereClauseComponent not in falseArray:
				falseArray.append(whereClauseComponent)
				logging.debug('Text Found false: Updating the .txt file withe the value ' +whereClauseComponent)
				file1.write(whereClauseComponent+'\n')

app = xw.App(visible=False) # IF YOU WANT EXCEL TO RUN IN BACKGROUND

xlwbMxLoader = xw.Book('C:\Madhu\EverSource\Task\Validation Scripts\Script to automate\ESE_WAM_R2_01_Data Dictionary MxLoader_Master.xlsm')
xlwbPackageExport = xw.Book('C:\Madhu\EverSource\Task\Validation Scripts\Script to automate\Package_export.xlsx')


xlws = {}
file1 = open("ExceptionReport.txt","w")
column='A'
lineText=''
falseValueArray=[]

xlwsPackageExport = {}
xlwsPackageExport['ws1'] = xlwbPackageExport.sheets['Export Worksheet']
PackageExportrowNum = xlwsPackageExport['ws1'].range(1,1).end('down').row
logging.debug('Full range PackageExport ' +str(PackageExportrowNum))

SheetNames= ['01 Conditional Expression ALL','04 Table & CrossOver Domain', '06 MaxRelationship ALL', '08 MaxMessages ALL', '09 Indexes', '02 DD WAMObj-woDom(Add)']

for k in range(len(SheetNames)):
	
	logging.debug('SheetName ' +SheetNames[k])

	xlws['ws1'] = xlwbMxLoader.sheets[SheetNames[k]]
	rowNum = xlws['ws1'].range(1,1).end('down').row
	
	if SheetNames[k]== '09 Indexes' :
		column='AB'
		lineText='INDEXES as component'
		Component='INDEXES'
	else:
		if SheetNames[k]== '01 Conditional Expression ALL' :
			lineText='CONDITIONNUM as component'
			Component='CONDITIONS'
		if SheetNames[k]== '04 Table & CrossOver Domain' :
			lineText='domainid as component'
			Component='DOMAINS'
		if SheetNames[k]== '06 MaxRelationship ALL' :
			Component='RELATIONSHIPS'
			lineText='a.name as component'
		if SheetNames[k]== '08 MaxMessages ALL' :
			Component='MESSAGES'
			lineText='MSGKEY as component'
		if SheetNames[k]== '02 DD WAMObj-woDom(Add)' :
			column='B'
			lineText='attributename as component'
			Component='MAXATTRIBUTES'
	
	
	j=''
	m=''
	falseValueArray=[]
	
	file1.write('\n----------------------\n'+Component+'\n----------------------\n') 
	
	logging.debug('Full range ' +str(rowNum))

	for i in range(3,rowNum+1):
		
		if SheetNames[k]== '02 DD WAMObj-woDom(Add)' :
			j=column+str(i)
			m='AT'+str(i)
			Value=str(xlws['ws1'].range(j).value)+' - '+str(xlws['ws1'].range(m).value)
		else:
			j=column+str(i)
			Value=xlws['ws1'].range(j).value
		
				
		textChk =textCheck(Value,lineText,SheetNames[k])
		
		if textChk !=True:
			if Value not in falseValueArray:
				falseValueArray.append(Value)
				logging.debug('Text Found false: Updating the .txt file withe the value ' +Value)
				file1.write(Value+'\n')
	logging.debug('textCheck final falsevalueArray= ' +str(falseValueArray))
	
heading=''
falseASArray=[]
falseEscArray=[]
falseExtSysArray=[]
falseESArray=[]
falsePCArray=[]
falseActArray=[]
falseSOArray=[]
	 
for i in range(2,PackageExportrowNum+1):	
	j='D'+str(i)
	k='E'+str(i)
	
	
	CFGObjValue=xlwsPackageExport['ws1'].range(j).value
	whereClauseValue=xlwsPackageExport['ws1'].range(k).value
	
	if CFGObjValue=='DMSCRIPT' and 'autoscript' in whereClauseValue.lower():
		lineText='autoscript as component'
		Component='AUTOMATION SCRIPTS'
		
		if heading!='AutomationScript':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='AutomationScript'
		
		whereClauseValue=whereClauseValue.upper().strip('AUTOSCRIPT IN (')
		whereClauseValue=whereClauseValue.upper().strip('AUTOSCRIPT IN(')
		whereClauseValue=whereClauseValue.upper().strip('AUTOSCRIPT=')
		whereClauseValue=whereClauseValue.upper().strip('AUTOSCRIPT= ')
		whereClauseValue=whereClauseValue.upper().strip('AUTOSCRIPT = ')
		whereClauseValue=whereClauseValue.upper().strip('AUTOSCRIPT =')
		whereClauseValue=whereClauseValue.strip(')')
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falseASArray)
					
	if CFGObjValue=='DMESCALATION' and 'escalation' in whereClauseValue.lower():
		lineText='escalation as component'
		Component='ESCALATIONS'
		
		if heading!='ESCALATIONS':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='ESCALATIONS'
		
		whereClauseValue=whereClauseValue.strip('escalation in (')
		whereClauseValue=whereClauseValue.strip(')')
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falseEscArray)
						
	if CFGObjValue=='DMMAXEXTSYSTEM' and 'extsysname' in whereClauseValue.lower():
		lineText='extsysname as component'
		Component='EXTERNAL SYSTEMS'
		
		if heading!='EXTERNALSYSTEMS':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='EXTERNALSYSTEMS'
		
		whereClauseValue=whereClauseValue.upper().strip('EXTSYSNAME IN (')
		whereClauseValue=whereClauseValue.upper().strip('EXTSYSNAME =') 
		whereClauseValue=whereClauseValue.strip(')')
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falseExtSysArray)
						
	if CFGObjValue=='DMMAXIFACEIN' and 'ifacename' in whereClauseValue.lower():
		lineText="'Enterprise Services' as type"
		Component='ENTERPRISE SERVICES'
		
		if heading!='ENTERPRISESERVICES':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='ENTERPRISESERVICES'
		
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME IN (')
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME IN(')
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME =') 
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME=')
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME= ')
		whereClauseValue=whereClauseValue.strip(')')
		if " AND INTOBJECTNAME='WAMCSDSTRTDRCTRY_OS'" in whereClauseValue.upper():
			whereClauseValue=whereClauseValue.replace(" AND INTOBJECTNAME='WAMCSDSTRTDRCTRY_OS'",'')
			
		if "LIKE 'DC2%'" in whereClauseValue.upper():	
			whereClauseValue=whereClauseValue.upper().strip("LIKE 'DC2%'")
			
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falseESArray)
		
		
					
	if CFGObjValue=='DMMAXIFACEOUT' and 'ifacename' in whereClauseValue.lower():
		lineText="'Publish Channel' as type"
		Component='PUBLISH CHANNEL'
		
		if heading!='PUBLISHCHANNEL':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='PUBLISHCHANNEL'
		
		whereClauseValue=whereClauseValue.strip('ifacename in (')
		whereClauseValue=whereClauseValue.strip('ifacename in(')
		whereClauseValue=whereClauseValue.strip('ifacename =') 
		whereClauseValue=whereClauseValue.strip('ifacename=')
		whereClauseValue=whereClauseValue.strip('ifacename = ')
		whereClauseValue=whereClauseValue.strip(')')
			
		if "IFACENAME LIKE 'DC2%'" in whereClauseValue.upper():	
			whereClauseValue=whereClauseValue.replace("IFACENAME LIKE 'DC2%'",'')
			
		
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falsePCArray)
		
	if (CFGObjValue=='DMACTION' or CFGObjValue=='DMACTIONGROUP') and 'action' in whereClauseValue.lower():
		lineText='ACTION as component'
		Component='ACTIONS'
		
		if heading!='Action':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='Action'
		
		whereClauseValue=whereClauseValue.upper().strip('ACTION IN (')
		whereClauseValue=whereClauseValue.upper().strip('ACTION IN(')
		whereClauseValue=whereClauseValue.upper().strip('ACTION IN  (')
		whereClauseValue=whereClauseValue.upper().strip('ACTION=')
		whereClauseValue=whereClauseValue.strip(')')
		if 'SELECT ACTION' in whereClauseValue.upper():	
			if 'ES_WOPRGEN' in whereClauseValue.upper():	
				whereClauseValue="'1137','ES_WOPRGEN'"
			if 'ES_DELLOBBY' in whereClauseValue.upper():
				whereClauseValue="'1133','ES_DELLOBBY'"
		
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falseActArray)
		
	if CFGObjValue=='DMSIGOPTION' and ('app' in whereClauseValue.lower() or 'optionname' in whereClauseValue.lower()):
		lineText='optionname from dual'
		Component='SIG OPTIONS'
		appName=''
		if heading!='Sigoption':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='Sigoption'
			
		whereClauseValue=whereClauseValue.upper()
		whereClauseValue=whereClauseValue.replace('OPTIONNAME IN (','')
		whereClauseValue=whereClauseValue.replace('OPTIONNAME IN(','')
		whereClauseValue=whereClauseValue.replace(')','')
		if "APP IN ('WAMLOCATION' AND " in whereClauseValue:
			whereClauseValue=whereClauseValue.replace("APP IN ('WAMLOCATION' AND ",'')
			appName='WAMLOCATION'
		if "WAMWOTRKG" in whereClauseValue:
			whereClauseValue="'WAMCLAIMREQ','WAMDISPBILLLINE','WAMBILLLINEREADONLY','WAMCANCELBILL','WAMSENDBILL','CUCREATED','WAMCANTASK','WAMBCNTCTTYPE'"
			appName='WAMWOTRKG'
		if "AND APP IN ('WAMWORKMATRIX'" in whereClauseValue:
			whereClauseValue=whereClauseValue.replace("AND APP IN ('WAMWORKMATRIX'",'')
			appName='WAMWORKMATRIX'
		if "APP IN('WAMWOTRKE' AND " in whereClauseValue: 
			whereClauseValue=whereClauseValue.replace("APP IN('WAMWOTRKE' AND ",'')
			appName='WAMWOTRKE'
		if "APP='WAMMASTERPM' AND " in whereClauseValue: 
			whereClauseValue=whereClauseValue.replace("APP='WAMMASTERPM' AND ",'')
			appName='WAMMASTERPM'
		if "APP = 'WAMPM' AND " in whereClauseValue: 
			whereClauseValue=whereClauseValue.replace("APP = 'WAMPM' AND ",'')
			appName='WAMPM'	
		if "APP IN ('PLUSDACTVT' AND " in whereClauseValue: 
			whereClauseValue=whereClauseValue.replace("APP IN ('PLUSDACTVT' AND ",'')
			appName='PLUSDACTVT'	
		if "APP IN('WAMFINCNTRL' AND " in whereClauseValue: 
			whereClauseValue=whereClauseValue.replace("APP IN('WAMFINCNTRL' AND ",'')
			appName='WAMFINCNTRL'
		if "APP='WAMWOLITE' " in whereClauseValue: 
			whereClauseValue="'WAMBCNTCTTYPE','WAMBUSFUNC','WAMCOMMBUSF','WAMCOMMODITY','WAMDISPAPTSEC','WAMDISPASSETNUM','WAMDISPAWC','WAMDISPBILLTYPE','WAMDISPCLEAR','WAMDISPCOMMENTS','WAMDISPENTITY','WAMDISPLOCATION','WAMDISPMETERTYPE','WAMDISPPFRCNCTDTS','WAMDISPPRJID','WAMDISPSCNBYPASS','WAMDISPSCNSEC','WAMDISPSUBWORKTYPE','WAMDISPTOWN','WAMDISPWOF','WAMDISPWORKTYPE','WAMEDITAPMNTDT','WAMEDITCOMNTSAPP','WAMEDITCOMNTSPER','WAMEDITCOMNTSSCN','WAMEDITFUNDPRJ','WAMEDITVALUE','WAMHIDE','WAMHIDEWOF','WAMREQAWC','WAMSFLEAD','WAMWRMETERINFOR'"
			appName='WAMWOLITE'
		if "APP IN ('WAMPLUSDCUEST" in whereClauseValue: 
			whereClauseValue="'WAMALNVALUERO','WAMDISPAREAWORKCENTER','WAMDISPBUSFUN','WAMDISPCUEVER','WAMDISPCUNAME','WAMDISPENTITY','WAMDISPFLDINST','WAMDISPLOOKUP','WAMDISPSTATION','WAMHIDE','WAMHIDENEWROW','WAMNUMVALUE','WAMTABLEVALUE','WAMTERCOND','WAMDISPCOMMODITY','WAMHIDEELEC','WAMHIDEGAS'"
			appName='WAMPLUSDCUEST'	
		if "APP='WAMPLUSDCULIB'" in whereClauseValue: 
			whereClauseValue="'WAMHIDE','WAMSELECTENTITY'"
			appName='WAMPLUSDCULIB'
		if "APP='WAMPLUSDORG" in whereClauseValue: 
			whereClauseValue='None'
			appName='WAMPLUSDORG'
		if "APP IN ('WAMSTDPRQ'" in whereClauseValue: 
			whereClauseValue="'WAMBYPASSTATUS'"
			appName='WAMSTDPRQ'
		if "WAMROUTEADMIN" in whereClauseValue:
			appName='WAMROUTES'
			
		
		packageExportFileCheck(whereClauseValue,lineText,Component,appName,falseSOArray)		

falsePCPRArray=[]
falseESPRArray=[]
for i in range(2,PackageExportrowNum+1):	
	j='D'+str(i)
	k='E'+str(i)
	
	
	CFGObjValue=xlwsPackageExport['ws1'].range(j).value
	whereClauseValue=xlwsPackageExport['ws1'].range(k).value

	if CFGObjValue=='DMMAXIFACEOUT' and 'ifacename' in whereClauseValue.lower():
		lineText="ProcessName from dual"
		Component='PROCESSING RULES missing from PUBLISH CHANNEL'
		
		if heading!='PC-PR':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='PC-PR'
		
		whereClauseValue=whereClauseValue.strip('ifacename in (')
		whereClauseValue=whereClauseValue.strip('ifacename in(')
		whereClauseValue=whereClauseValue.strip('ifacename =') 
		whereClauseValue=whereClauseValue.strip('ifacename=')
		whereClauseValue=whereClauseValue.strip('ifacename = ')
		whereClauseValue=whereClauseValue.strip(')')
			
		if "IFACENAME LIKE 'DC2%'" in whereClauseValue.upper():	
			whereClauseValue=whereClauseValue.replace("IFACENAME LIKE 'DC2%'",'')
			
		
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falsePCPRArray)

	if CFGObjValue=='DMMAXIFACEIN' and 'ifacename' in whereClauseValue.lower():
		lineText="'Enterprise Service - Processing Rules' as type"
		Component='PROCESSING RULES missing from ENTERPRISE SERVICES'
		
		if heading!='ES-PR':
			file1.write('\n----------------------\n'+Component+'\n----------------------\n')
			heading='ES-PR'
		
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME IN (')
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME IN(')
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME =') 
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME=')
		whereClauseValue=whereClauseValue.upper().strip('IFACENAME= ')
		whereClauseValue=whereClauseValue.strip(')')
		if " AND INTOBJECTNAME='WAMCSDSTRTDRCTRY_OS'" in whereClauseValue.upper():
			whereClauseValue=whereClauseValue.replace(" AND INTOBJECTNAME='WAMCSDSTRTDRCTRY_OS'",'')
			
		if "LIKE 'DC2%'" in whereClauseValue.upper():	
			whereClauseValue=whereClauseValue.upper().strip("LIKE 'DC2%'")
			
		packageExportFileCheck(whereClauseValue,lineText,Component,'',falseESPRArray)
					
file1.close() #to change file access modes 
xlwbMxLoader.close()
xlwbPackageExport.close()
