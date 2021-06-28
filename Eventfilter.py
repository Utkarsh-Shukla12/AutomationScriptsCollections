# Owner: Utkarsh Shukla
# EventFilter for MXTOWEBPORT_METR_PC


from psdi.iface.mic import IntegrationContext
from psdi.util.logging import MXLoggerFactory	
logger = MXLoggerFactory.getLogger("maximo.autoscript")
logger.debug("::DEBUG:::PUBLISH.MXTOWEBPORT_METR_PC.EVENTFILTER:::START:::")
if (ifaceName=="WAM_MXTOWEBPORT_METR_PC"):
	context = IntegrationContext.getCurrentContext()
	# to check if the source type is not null
	if ((context is not None) and (context.getStringProperty("sourcetype") is not None)):
		evalresult = False
		
logger.debug("::DEBUG:::PUBLISH.WAM_MXTOWEBPORT_METR_PC.EVENTFILTER:::END:::")
