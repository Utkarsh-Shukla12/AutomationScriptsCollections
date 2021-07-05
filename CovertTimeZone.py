from psdi.server import MXServer
from psdi.security import UserInfo
from psdi.mbo import MboConstants
from java.util import Date
from psdi.util import MXFormat
from java.util import Calendar
from java.text import SimpleDateFormat
from java.util import TimeZone
from java.text import DateFormat
from java.time import ZoneId
from java.time import ZonedDateTime
from java.sql import Timestamp
from java.time.format import DateTimeFormatter
from java.text import SimpleDateFormat


# Get MST Time from Report Date
zoneId = ZoneId.of("Canada/Mountain")

reportedDateInUTC= mbo.getDate("REPORTDATE")
reportedDateInMST = ZonedDateTime.ofInstant(reportedDateInUTC.toInstant(),zoneId);
#reportedDateInMSTFormated=reportedDateInMST.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)
timestamp = Timestamp.valueOf(reportedDateInMST.toLocalDateTime())

reportedTime = timestamp.getTime()

#Get MST Time from current Date

cal = Date()
currentDateInUTC= cal
currentDateInMST = ZonedDateTime.ofInstant(currentDateInUTC.toInstant(),zoneId);
#reportedDateInMSTFormated=reportedDateInMST.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)
currenTimestamp = Timestamp.valueOf(currentDateInMST.toLocalDateTime())

currentTime = currenTimestamp.getTime()
