#!/usr/bin/python
 # -*- coding: utf-8 -*-

import urllib2
import urlparse
import re
import locale, datetime, time
from BeautifulSoup import BeautifulSoup

# @TODO: some documentation about the config dict
# @TODO: try/catch opslag i configdict

class Articlescrape:
	def __init__(self, url, configdict):
		self.url = url
		host = urlparse.urlparse(self.url).hostname
		self.config = configdict[host]
		self.soup = self._downloadurl()

	def _downloadurl(self):	
		html = ""	
		# Get HTML

		response = urllib2.urlopen(self.url)
		html = response.read()

		# Prepare for DOM-manipulation
		soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
		return soup

	def gettextlist(self):

		# Container
		articlehtml = self.soup.find(self.config["text"]["find"][0], { "class" : re.compile(self.config["text"]["find"][1]) })

		# Extract
		for tag in self.config["text"]["extract"]:
			if(tag[1]):
				[s.extract() for s in self.soup(tag[0], { "class" : tag[1] } )]
			else:
				[s.extract() for s in self.soup(tag[0])]
		
		text = ''.join(articlehtml.findAll(text=True))

		rgx = re.compile("[\w']+", re.UNICODE)
		textlist = rgx.findall(text)
		return textlist
"""
	def getdate(self):
		#print self.config
		dateelement = self.soup.find(self.config["date"]["find"][0], { "class" : re.compile(self.config["date"]["find"][1]) })
		if dateelement:
			
			datestring = dateelement.findAll(text=True)[0]
			locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8') 
			date = datetime.datetime.strptime(datestring, self.config["date"]["format"]).date()

			return date #should be: return date
		else:
			return None
"""




