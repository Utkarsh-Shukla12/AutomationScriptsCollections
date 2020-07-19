WAMOVAPIPELEN, WAMEXISTINGINFRA
Domain
WAMOVAPIPELEN, WAMCLKEXISTINFRA
-----------------------------------------
(worktype='CUST' and siteid='ESSITE' and ownergroup in (select persongroup from persongroupteam where resppartygroup=:&USERNAME& )) or 





(worktype='CUST' and siteid='ESSITE' and owner in (select resppartygroup from persongroupteam where persongroup in (select persongroup from persongroupteam where resppartygroup=:&USERNAME& )))
-----------------------------------------
((worktype in('EM','DG','CP','CM') and siteid='ESSITE' and ownergroup in (select persongroup from persongroupteam where resppartygroup= :&USERNAME&   )) or 

(worktype in('EM','DG','CP','CM') and siteid='ESSITE' and owner in (select resppartygroup from persongroupteam where persongroup in (select persongroup from persongroupteam where resppartygroup= :&USERNAME& )))  and wamcommodity='ELECTRIC' and (wambusinessfunction is null or wambusinessfunction in (select wa.wambusinessfunction from wamuserauth wa join groupuser gu on wa.groupname = gu.groupname where wa.wamauthtype = 'BUSUNIT' and gu.userid =  :&USERNAME& )) and (wamentity is null or wamentity in (select wa.wamentity from wamuserauth wa join groupuser gu on wa.groupname = gu.groupname where wa.wamauthtype = 'ENTITY' and gu.userid = :&USERNAME& )))

-------------------------------------
(exists (select 1 from PLUSDESTCONTROL where masterwonum = :wonum))

-------------------------------------
(plusdisprereq=1 and siteid='ESSITE' and ((owner=:USER) or (ownergroup in (select persongroup from persongroupteam where respparty= :USER ))) and status in ('WAPPR','READY','INPRG','COMP','CANCEL') and wamcommodity in (select wa.wamcommodity from wamuserauth wa join groupuser gu on wa.groupname = gu.groupname where wa.wamauthtype = 'COMMODITY' and gu.userid =  :&USERNAME& ) and wamterritory in (select wa.wamterritory from wamuserauth wa join groupuser gu on wa.groupname = gu.groupname where wa.wamauthtype = 'TERRITORY' and gu.userid =  :&USERNAME& ) and wambusinessfunction in (select wa.wambusinessfunction from wamuserauth wa join groupuser gu on wa.groupname = gu.groupname where wa.wamauthtype = 'BUSUNIT' and gu.userid = :&USERNAME& )) order by STATUS desc

------------------------------------

select * from WOACTIVITY Where plusdisprereq=1 and siteid='ESSITE' and ((owner=:USER) or (ownergroup in (select persongroup from persongroupteam where respparty= :USER ))) and wonum in (select wo.wonum from WOACTIVITY woa join WORKORDER wo on woa.wonum = wo.wonum where wo.status not in ('RDISP')) and WAMSTDPRQNO in (select woa.WAMSTDPRQNO from WOACTIVITY woa join WAMSTRPRQ pq on woa.WAMSTDPRQNO = pq.WAMSTDPRQNO where pq.WAMKEYPREREQUISITE  = 'COMP')


-------------------------------------
(historyflag = 0 and siteid = 'ESSITE')
-------------------------------------
select woa.status from WOACTIVITY woa join WORKORDER wo on woa.wonum = wo.wonum where wo.status not in ('RDISP') and woa.status = 'COMP'
-------------------------------------
select woa.WAMSTDPRQNO from WOACTIVITY woa join WAMSTRPRQ pq on woa.WAMSTDPRQNO = pq.WAMSTDPRQNO where pq.WAMKEYPREREQUISITE  = 'COMP'

------------------------------------
select * from WORKORDER where status not in ('RDISP') and ((owner=:USER) or (ownergroup in (select persongroup from persongroupteam where respparty= :USER ))) and wonum in (select woa.wonum from WOACTIVITY woa join WAMSTRPRQ pq on woa.WAMSTDPRQNO = pq.WAMSTDPRQNO where pq.WAMKEYPREREQUISITE  = 'COMP');

----------------------------------

select *
from maximo.workorder
where
    woclass = 'WORKORDER'
    and siteid = 'ESSITE'
    and historyflag=0 
    and istask=0 
    and (wambusinessfunction in (select wa.wambusinessfunction from maximo.wamuserauth wa join maximo.groupuser gu on wa.groupname = gu.groupname where wa.wamauthtype = 'BUSUNIT' and gu.userid = :&USERNAME& ))
    and (wamentity in (select wa.wamentity from maximo.wamuserauth wa join maximo.groupuser gu on wa.groupname = gu.groupname where wa.wamauthtype = 'ENTITY' and gu.userid = :&USERNAME& ))
    
    and wonum in 
        (
        select parent 
        from maximo.woactivity 
        where
            woclass='ACTIVITY'
            and plusdisprereq = 1
            and istask = 1
            and historyflag = 0
            and status in ('READY', 'INPRG')
            and wamstdprqno = 'PRE536'
            and ((owner= :&USERNAME&) or (ownergroup in (select persongroup from maximo.persongroupteam where respparty= :&USERNAME&)))
        )
        
    and wonum in
        (
        select parent
        from maximo.WAMBILLINGQUOTE
        
        where
            (BILLAMOUNT * 0.98) <= WAMPAIDAMOUNT
            
        )


------------------------------------
