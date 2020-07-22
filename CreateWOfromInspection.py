
print "=============== EXECUTING CREATE WO SCRIPT ===============";
planned = False;
if (mbo.getString("REFERENCEOBJECT")=="WORKORDER" or  mbo.getString("REFERENCEOBJECT")=="WOACTIVITY") :
planned = True;
else:
planned = False;
# iterate through the responses 
resultSet = mbo.getMboSet("INSPFIELDRESULT");
for i in range(0,resultSet.count()):
currentResult = resultSet.getMbo(i);
# on the current response, check if it requires action (relationship INSPFIELDRESULTACT search on field options if the current response requires action)
requireActionSet = currentResult.getMboSet("INSPFIELDOPTIONACT");
requireAction=False;
if requireActionSet.count()>0:
  requireAction=True;
if requireAction:
  # for planned (with WO) inspections that does not have any follow up actions to its results yet
  questionDetailSet = currentResult.getMboSet("INSPQUESTION");
  desc = questionDetailSet.getMbo(0).getString("description") + " = " + currentResult.getString("TXTRESPONSE");
  if (planned and currentResult.getString("FUPOBJECT")==""):
   #This will create your follow up WO, it can be part of the WO/Task itself or you can relate them to the ParentWO that contains all results
   if mbo.getString("PARENT") is not None:
    woSet = mbo.getMboSet("PARENTWO");
   else:
    woSet = mbo.getMboSet("WORKORDER");
   wo = woSet.getMbo(0);
   # create a follow up work order
   newWO = wo.createWorkorder(); 
   #set WO desc based on the question response
   newWOSet = mbo.getMboSet("$NewWO","WORKORDER","wonum='" + newWO.getString("wonum") + "' and siteid= '" + newWO.getString("siteid") + "'");
   newWOSet.getMbo(0).setValue("description",desc);
   newWOSet.getMbo(0).setValue("location",mbo.getString("location"));
   newWOSet.getMbo(0).setValue("assetnum",mbo.getString("asset"));
   currentResult.setValue("FUPOBJECT","WORKORDER");
   currentResult.setValue("FUPOBJECTID",newWO.getString("wonum"));
   currentResult.setValue("DISPLAYMESSAGE","Workorder " + str(newWO.getString("wonum")) + " created");
   newWOSet.save();
  # if does not have a planning WO, will create a new WO and include each individual question that require action as a task   
  if (planned==False and currentResult.getString("FUPOBJECT")==""):
   woSet = mbo.getMboSet("WORKORDER");
   # if there is already a WO created for the result, just skip
   if mbo.getString("FUPOBJECT")=="":
   newWO = woSet.add();
    newWO.setValue("Description","Follow Up Work Order for Inspection " + str(mbo.getString("resultnum")));
    newWO.setValue("location",mbo.getString("location"));
    newWO.setValue("assetnum",mbo.getString("asset"));
    mbo.setValue("FUPOBJECT","WORKORDER");
    mbo.setValue("FUPOBJECTID",newWO.getString("wonum"));
    mbo.setValue("DISPLAYMESSAGE","Workorder " + str(newWO.getString("wonum")) + " created");
    print "Created WO " + str(newWO.getString("wonum"));
    woSet.save();
   woSet = mbo.getMboSet("FUPWORKORDER");
   newTask = woSet.getMbo(0).getMboSet("WOACTIVITY").add();
   newTask.setValue("PARENT",mbo.getString("FUPOBJECTID"));
   print "Created Task " + str(newTask.getString("taskid"));
   newTask.setValue("description",desc);
   currentResult.setValue("FUPOBJECT","WORKORDER");
   currentResult.setValue("FUPOBJECTID",newTask.getString("wonum"));
   currentResult.setValue("DISPLAYMESSAGE","Work Order " + mbo.getString("FUPOBJECTID") + " Task " + str(newTask.getString("taskid")) + " created"); 
   woSet.save();
resultSet.save();
print "=============== END CREATE WO SCRIPT ===============";
