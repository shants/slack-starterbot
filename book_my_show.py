#!/usr/bin/python
#
# Screen scraper based API for BookMyShow.

import re
#import urllib2
import requests

class BookMyShowClient(object):
  NOW_SHOWING_REGEX = '{"event":"productClick","ecommerce":{"currencyCode":"INR","click":{"actionField":{"list":"Filter Impression:category\\\/now showing"},"products":\[{"name":"(.*?)","id":"(.*?)","category":"(.*?)","variant":"(.*?)","position":(.*?),"dimension13":"(.*?)"}\]}}}'
  COMING_SOON_REGEX = '{"event":"productClick","ecommerce":{"currencyCode":"INR","click":{"actionField":{"list":"category\\\/coming soon"},"products":{"name":"(.*?)","id":"(.*?)","category":"(.*?)","variant":"(.*?)","position":(.*?),"dimension13":"(.*?)"}}}}'

  def __init__(self, location = 'Bengaluru'):
    self.__location = location.lower()
    self.__url = "https://in.bookmyshow.com/%s/movies" % self.__location
    self.__html = None

  def __download(self):
    req = requests.get(self.__url) 
    #urllib2.Request(self.__url, headers={'User-Agent' : "Magic Browser"})
    html = req.text #urllib2.urlopen(req).read()
    return html

  def get_now_showing(self):
    if not self.__html:
      self.__html = self.__download()
    now_showing = re.findall(self.NOW_SHOWING_REGEX, self.__html)
    return now_showing
    #return self.__html

  def get_coming_soon(self):
    if not self.__html:
      self.__html = self.__download()
    coming_soon = re.findall(self.COMING_SOON_REGEX, self.__html)
    return coming_soon

if __name__ == '__main__':
  # Test code.
  bms_client = BookMyShowClient('Bengaluru')
  now_showing = bms_client.get_now_showing()
  for m in now_showing:
    print(m) 	 
#print(now_showing.status_code) 
# print(now_showing.content) 
