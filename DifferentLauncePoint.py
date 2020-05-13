from psdi.util.logging import MXLoggerFactory
maximoLogger = MXLoggerFactory.getLogger("maximo")
maximoLogger.debug("WAM:::LOGGING:::WAM_ATTR_PLUSDTASKTYPE:::ENTER:::")
taskType=mbo.getString("PLUSDTASKTYPE")
#Checking for Task Type input
if taskType<>"" :
   matrixSet=mbo.getMboSet("WAMCUTASKTYPE")
   #Fetching related record from Matrix table based on Task Type
   if matrixSet.getMbo(0):
      matrixTaskType=matrixSet.getMbo(0).getString("WAMTASKTYPE")
      #Sets TaskType
      mbo.setValue("WAMTASKTYPE",matrixTaskType)
#Script to Crossover parent workorder to child workorder	  
if launchPoint=="WAM_OBJ_WOAPTASKTYPE" and onadd:
	ownerWo=mbo.getOwner()		
	if ownerWo is not None:				
		mbo.setValue("WAMCOMMODITY",ownerWo.getString("WAMCOMMODITY"))
		mbo.setValue("WAMBUSINESSFUNCTION",ownerWo.getString("WAMBUSINESSFUNCTION"))
		mbo.setValue("WAMENTITY",ownerWo.getString("WAMENTITY"))						
		mbo.setValue("WAMSUBWORKTYPE",ownerWo.getString("WAMSUBWORKTYPE"))
		mbo.setValue("WAMAREAWORKCENTER",ownerWo.getString("WAMAREAWORKCENTER"))
		mbo.setValue("WAMTERRITORY",ownerWo.getString("WAMTERRITORY"))
		mbo.setValue("WAMREGION",ownerWo.getString("WAMREGION"))
		mbo.setValue("WAMPRIORITYWO",ownerWo.getString("WAMPRIORITYWO"))
		mbo.setValue("WAMTOWN",ownerWo.getString("WAMTOWN"))
		mbo.setValue("FINCNTRLID",ownerWo.getString("FINCNTRLID"))
		mbo.setValue("SNECONSTRAINT",ownerWo.getString("SNECONSTRAINT"))
		mbo.setValue("FNLCONSTRAINT",ownerWo.getString("FNLCONSTRAINT"))
		mbo.setValue("TARGSTARTDATE",ownerWo.getString("TARGSTARTDATE"))
		mbo.setValue("TARGCOMPDATE",ownerWo.getString("TARGCOMPDATE"))
