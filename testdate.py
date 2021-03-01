# -*- coding:utf-8 -*-  

from datetime import datetime
#from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

now = datetime.now()

#yestoday = now - timedelta(days=1)
#print yestoday.replace(hour=0, minute=0, second=0)

relative = now + relativedelta(days=-1)
print relative