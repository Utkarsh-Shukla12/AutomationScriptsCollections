#			itemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo());
#			itemSet.setWhere("ITEMNUM=" + ITEMNUM + " AND MANAGED=1")
#			itemSet.reset()
#			itemMbo=itemSet.getMbo(0)
#			numOfparts =3;
#			managed = itemMbo.getInt("ISMANAGED");
#			for i in numOfparts:
#			 addFokliftRecords(itemnum,refWO,binNumberInvBarcode,intBatch,count,assetnum,description,storeloc,boxBinQty,lotnum)# calling addFokliftRecords function
	
			
			
def addpartvaltoflapp ():
	itemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo());
	itemSet.setWhere("ITEMNUM=" + ITEMNUM + " AND ISMANAGED = 1")
	itemSet.reset()
	itemMbo = itemSet.getMbo(0)
	partnum = itemSet.getInt("IN23")
	managed = itemSet.getInt("ISMANAGED")
	while(itemMbo):
		
		