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
