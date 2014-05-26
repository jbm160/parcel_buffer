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


def queryBuffer(buff):
        qparams = {}
        qparams['f'] = "json"
        qparams['geometry'] = buff
        qparams['returnGeometry'] = True;
        qparams['outFields'] = ["OBJECTID","STANPAR","OWNER","MAIL_ADDR","MAIL_CITY","MAIL_STATE","MAIL_ZIP","PROP_ADDR","PROP_CITY","PROP_ZIP"]
        qparams['outSR'] = 2274
        qparams['returnCountOnly'] = True
        queryURL = "http://maps.nashville.gov/MetGIS/rest/services/Basemaps/Parcels/MapServer/0/query"
        r3 = requests.get(queryURL, params=qparams)
        features = json.loads(r3.text)
        print "Number of parcels returned: " + r
        

def getGeoBuffer(geom,dist):
        bparams = {}
        bparams['geometries'] = geom
        bparams['distances'] = dist
        #bparams['unit'] = "UNIT_FOOT"
        bparams['unit'] = 9002
        bparams['bufferSR'] = 2274
        bparams['outSR'] = 2274
        bparams['inSR'] = 2274
        bparams['f'] = "json"
        buffURL = "http://maps.nashville.gov/MetGIS/rest/services/Geometry/GeometryServer/buffer"
        r2 = requests.get(buffURL, params=bparams)
        print r2.text
        buff = json.loads(r2.text)
        queryBuffer(buff[0])

def getParcelFeature(parcelID,distance):
    #try:
        # get feature object based on parcel ID
        spatialRef = {"wkid":2274}
        pageURL = "http://maps.nashville.gov/MetGIS/rest/services/Basemaps/Parcels/MapServer/0/query"
        params = {'where': "STANPAR='" + parcelID + "'", 'f':"json", 'outFields': "*", 'spatialReference': spatialRef, 'returnGeometry': True}
        r1 = requests.get(pageURL, params=params)
        feat = json.loads(r1.text)
        if len(feat['features']) == 0:
            print "No features were found"
        else:
            getGeoBuffer(feat['features'][0]['geometry'],distance)
#        print r.text
    #except:
#        print "error occurred"


getParcelFeature("11714006400",250)      
      
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


