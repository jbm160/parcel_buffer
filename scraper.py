# This is a template for a Python scraper on Morph (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries. You can use whatever libraries are installed
# on Morph for Python (https://github.com/openaustralia/morph-docker-python/blob/master/pip_requirements.txt) and all that matters
# is that your final data is written to an Sqlite database called data.sqlite in the current working directory which
# has at least a table called data.

import scraperwiki
import lxml.html
import lxml.etree
import json
import re
import resource
import xlrd
import cookielib, urllib2
import requests

def getBufferParcels(parcelID,distance):
    try:
        # get feature object based on parcel ID
        pageURL = "http://maps.nashville.gov/MetGIS/rest/services/Basemaps/Parcels/MapServer/0/query"
        params = {'where': "STANPAR='" + parcelID + "'", 'f':"json", 'outFields': "*", 'spatialReference': {"wkid" : 2274}, 'returnGeometry': true}
        r = requests.get(pageURL, params)
        print r.text
        
getBufferParcels("11714006400",250)      
      
def getAppraisal(propID,parcelID):
    try:
    # print "propID = " + propID + "."
        pageURL = "http://www.padctnwebpro.com/WebproNashville/searchResults.asp?cboSearchType=Parcel&SearchVal1=" + propID
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        html = lxml.html.parse(opener.open(pageURL)).getroot()
    # print html.text_content()
        links = html.cssselect('a')
        newURL = "http://www.padctnwebpro.com/WebproNashville/" + links[0].get('href')

#summary-bottom.asp?A1=2337573&A2=1
        record = lxml.html.parse(opener.open(newURL.replace("Summary","summary-bottom"))).getroot()
        fields = record.cssselect('td')
        neighborhood = fields[49].text_content().strip()
        apprData = {'parcelID': parcelID,
            'neighborhood': neighborhood}
        scraperwiki.sqlite.save(unique_keys=["parcelID"], data=apprData, table_name="Districts")
    except:
        print "Could not get appraisal info for parcelID " + parcelID + " at " + address
            
    # owner, street, parcelID, lastsaleprice, lastsaledate, totalval, landval, impval, acres, sqft, year, foundation, siding, rooms, bedrooms, fullbaths, halfbaths, fixtures


