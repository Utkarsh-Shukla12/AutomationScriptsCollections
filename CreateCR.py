from psdi.mbo import MboConstants

pmnum = mbo.getString("PMNUM")
siteid= mbo.getString("SITEID")
orgid= mbo.getString("ORGID")
owner=mbo.getThisMboSet().getParentApp()
if pmnum is not None :
	crset = mbo.getMboSet("$PLUSCA_NEW", "PLUSCA", "1=1"  )
	#crset.reset()
	cr = crset.add()
	NoCheck = MboConstants.NOVALIDATION_AND_NOACTION

	cr.setValue("DESCRIPTION", mbo.getString("DESCRIPTION"), NoCheck)
	cr.setValue("PLUSCATEGORY", "PREVENTIVE", NoCheck)
	cr.setValue("TARGETSTART", mbo.getDate("TARGSTARTDATE"), NoCheck)
	cr.setValue("TARGETFINISH", mbo.getDate("TARGCOMPDATE"), NoCheck)
	
	if mbo.getString("LOCATION") is not None:
		cr.setValue("LOCATION", mbo.getString("LOCATION"), NoCheck)
	elif mbo.getString("ASSETNUM") is not None:
		cr.setValue("ASSETNUM", mbo.getString("ASSETNUM"), NoCheck)
        cr.setValue("SITEID", siteid, NoCheck)
        cr.setValue("ORGID", orgid, NoCheck)
	#relwoset = crs
	crset.save()
	#crmbo = cr.getThisMboSet()
        crnum= cr.getString("TICKETID")
        relwoset = cr.getMboSet("$RELATEDWO","RELATEDRECORD","1=1")
        relwoset.reset()
        relwo = relwoset.add()
        relwo.setValue("CLASS", "CORRECT_ACT",  NoCheck)
        relwo.setValue("RELATEDRECKEY", mbo.getString("WONUM"), NoCheck)
        relwo.setValue("RELATEDRECCLASS", "WORKORDER", NoCheck )

        relwo.setValue("RECORDKEY", crnum, NoCheck)
        relwo.setValue ("RELATETYPE", "ORIGINATOR", NoCheck)
        relwo.setValue("SITEID", siteid, NoCheck)
        relwo.setValue("ORGID", orgid, NoCheck)
        relwo.setValue("RELATEDRECSITEID", siteid, NoCheck)
        relwo.setValue("RELATEDRECORGID", orgid, NoCheck)
        relwoset.save()
        relwoset.close()
        
        relpmset=cr.getMboSet("PLUSPMREFTICKET")
        relpm=relpmset.add()
        relpm.setValue("TICKETID", crnum, NoCheck)
        relpm.setValue("SITEID", siteid, NoCheck)
        relpm.setValue("PMNUM", mbo.getString("PMNUM"), NoCheck)
        relpmset.save()
        relpmset.close()
        crset.close()
