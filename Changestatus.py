from psdi.mbo import MboConstants

Asset_new = mbo.getString("ASSETNUM")

if (Asset_new == "11300"):
 mbo.setValue("WORKTYPE", "CM", MboConstants.NOVALIDATION_AND_NOACTION)

#Author : Utkarsh Shukla
#Modified : 26th December, 2019
#Purpose: Change WorkType for the given asset