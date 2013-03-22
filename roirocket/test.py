'''This is the test file to test the class
'''

from roirocket import ROIRocket
from datetime import datetime

import logging
from pandora.utils import enable_console_logging

log = logging.getLogger(__name__)
enable_console_logging(log)

if __name__ == '__main__':
    affiliate_id = '<YOUR-AFFILIATE-ID>'
    api_key = '<YOUR-API-KEY>'
    start_date = datetime.strptime('2013-03-01', '%Y-%m-%d')
    end_date = datetime.strptime('2013-03-20', '%Y-%m-%d')

    log.info('start_date: %s' %(start_date.strftime('%Y-%m-%d')))
    log.info('end_date: %s' %(end_date.strftime('%Y-%m-%d')))
    roi = ROIRocket(affiliate_id = affiliate_id, api_key = api_key,
	    start_date = start_date, end_date = end_date)
    log.info(roi.get())
