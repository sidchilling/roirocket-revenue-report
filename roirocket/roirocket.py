'''roirocket: Python library to exctract revenue data from ROI Rocket for a publisher
'''

__version__ = '1.0'
__author__ = 'Siddharth Saha (sidchilling@gmail.com)'

import requests
from BeautifulSoup import BeautifulSoup

class ROIRocket(object):

    URL = 'http://tracking.roirocket.com/affiliates/api/2/reports.asmx/CampaignSummary'
    
    affiliate_id = None # Required
    api_key = None # Required
    start_date = None # The start date from which commission data is required
    end_date = None # The end date till which comission data is required - This date is not included

    def __init__(self, affiliate_id, api_key, start_date, end_date):
	assert affiliate_id and api_key and start_date and end_date, 'missing args'
	self.affiliate_id = affiliate_id
	self.api_key = api_key
	self.start_date = start_date.strftime('%Y-%m-%d')
	self.end_date = end_date.strftime('%Y-%m-%d')
    
    def _make_data(self):
	# This method makes the data dict which needs to be sent with the request
	return {
		'affiliate_id' : self.affiliate_id,
		'api_key' : self.api_key,
		'start_date' : self.start_date,
		'end_date' : self.end_date,
		'start_at_row' : 1,
		'row_limit' : 0
	    }

    def get(self):
	'''This method is to be called to get the commission data. The data will be returned
	in the following format - 
	{
	    '<advertiser-id>' : {
			'commission-amount' : <amount-in-cents>,
			'advertiser-name' : <advertiser-name>
			    }
	}
	'''
	res = {} # This is the return dict in the above format
	r = requests.post(url = self.URL, data = self._make_data())
	if r.ok:
	    soup = BeautifulSoup(r.content)
	    if soup.find('success').renderContents().strip() == 'true':
		cmp_list = soup.find('campaigns').findAll('campaign')
		for cmp in cmp_list:
		    res[cmp.find('offer_id').renderContents()] = {
			    'advertiser-name' : cmp.find('offer_name').renderContents(),
			    'commission-amount' : int(float(cmp.find('revenue').renderContents()) * 100)
			    }
		return res
	    else:
		raise Exception('%s' %(soup.find('message').renderContents().strip()))
	else:
	    raise Exception('Could not connect to the URL')
