#! /usr/bin/env python
# coding:utf-8

# inspiration: http://v3l0c1r4pt0r.tk/2014/06/01/how-to-download-from-dreamspark-bypassing-secure-download-manager/

__author__ = 'gulliver - Radek Simkanič'

#TODO rewrite to for Python3

import urllib2
import sys
import os
import shutil

#from urllib.parse import urlparse
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup as Soup
# or:
#from bs4 import BeautifulSoup as Soup
from soupselect import select
from lxml import etree

# constants
INFORMATION = 0;
WARNING = 1;
ERROR = 2;
EXCEPTION = 3;
DONE = 4;

def main() :
	argv = sys.argv
	if len(argv) < 2:
		message("SDX file is not included", ERROR)
		return 1
	d = Downloader()
	d.setSdx(argv[1])
	d.execute()

def message(text, type):
	if type == INFORMATION:
		print("Info: %s" % text)
	elif type == WARNING:
		print("\033[33mWarning:\033[0m %s" % text)
	elif type == ERROR:
		print("\033[31;1mError:\033[0m %s" % text)
	elif type == EXCEPTION:
		print("\033[41;1mEXCEPTION:\033[0m %s" % text)
	elif type == DONE:
		print("\033[32;1m %s \033[0m" % text)


class Downloader:
	sdxFile = ""
	html = ""
	oiop = []
	oiopu = []
	fileId = []
	fileName = []
	dlSelect = ""
	selected = 0
	domain = ""
	downloadedFiles = []

	def __init__(self):
		self.sdxFile = ""

	def setSdx(self, file):
		self.sdxFile = file

	def execute(self):
		if self.downloadMainPage() == False:
			return False

		if self.parse() == False:
			return False

		self.getList()

		if self.downloadFiles() == False:
			return False

		self.glue()
		message("SDC file is DONE!", DONE)
		return True


	def downloadMainPage(self):
		try:
			message("Opening SDX file", INFORMATION)
			file = open(self.sdxFile, 'r')
			url = file.readline()

			message("Parsing URL", INFORMATION)
			urlFragments = urlparse(url)
			if hasattr(urlFragments, 'netloc'):
				self.domain = urlFragments.netloc
			else:
				message("Bad URL", ERROR)
				return False

			message("Downloading main page", INFORMATION)
			response = urllib2.urlopen(url)
			html = response.read()
			self.html = html
			return True
		except ValueError:
			message(ValueError, EXCEPTION)
			return False

	def getList(self):
		i = 1
		print("Choose file:")

		if len(self.fileName) == 1:
			self.selected = 1
			return

		for name in self.fileName:
			print("\t#%i | %s" % (i, name))
			i += 1

		position = input("Please select file via number 1 - %i: " % (i-1))
		position = int(position)

		if position < 1 or position >= i:
			message("Bad choose!", WARNING)
			self.getList()
			return

		self.selected = position

	def parse(self):
		soup = Soup(self.html)
		edvCounter = 0
		edv = select(soup, '#edv')

		if len(edv) == 0:
			i = 1
			while(True):
				edvInput = '#edv' + str(i)
				oiopInput = '#oiop' + str(i)
				oiopuInput = '#oiopu' + str(i)
				fileIdInput = '#fileID' + str(i)
				fileNameInput = '#fileName' + str(i)

				edv = select(soup, edvInput)
				if len(edv) == 0:
					edvCounter = i-1
					message("Edv items founds: " + str(edvCounter), INFORMATION)
					break

				oiop = select(soup, oiopInput)
				oiopu = select(soup, oiopuInput)
				fileId = select(soup, fileIdInput)
				fileName = select(soup, fileNameInput)

				#print(len(oiop), len(oiopu), len(fileId), len(fileName))
				if len(oiop) == 0 or len(oiopu) == 0 or len(fileId) == 0 or len(fileName) == 0:
					message("Fragments is not found during parsing", ERROR)
					return False
				oiop = oiop[0]
				oiopu = oiopu[0]
				fileId = fileId[0]
				fileName = fileName[0]

				self.oiop.append( oiop.get('value') )
				self.oiopu.append( oiopu.get('value') )
				self.fileId.append( fileId.get('value') )
				self.fileName.append( fileName.get('value') )

				i += 1
		else:
			message("Edv is only one", INFORMATION)
			edvCounter = 1

		if edvCounter == 0:
			message("Edv is not found", ERROR)
			return False

		dlSelect = select(soup, '#dlSelect1')
		if len(dlSelect) == 0:
			message("dlSelect1 is not found", ERROR)
			return False

		dlSelect = dlSelect[0]
		self.dlSelect = dlSelect.get('value')

		message("Parsing done!", INFORMATION)

	def downloadFiles(self): #TODO
		message("Creating URL", INFORMATION)
		url = self.createUrl()

		message("Downloading page contains download link", INFORMATION)
		response = urllib2.urlopen(url)
		html = response.read()

		#remove CDATA
		e = etree.XML(html)
		html = etree.tostring(e)

		message("Parsing page", INFORMATION)
		soup = Soup(html)
		fileUrl = select(soup, 'fileurl')
		#fileUrl = soup.select('fileUrl')
		edv = select(soup, 'edv')

		if len(fileUrl) == 0:
			message("The page does not have a download link. ", ERROR)
			return False

		if len(edv) == 0:
			message("The page does not have 'edv' key", ERROR)
			return False

		name = self.fileName[self.selected-1]
		fileKeyName = "%s.key" % name

		message("Creating .key file", INFORMATION)
		edv = edv[0]
		print(edv)
		f = open(fileKeyName, 'w')
		f.write(edv.string)
		f.close
		message("Created", DONE)

		fileUrl = fileUrl[0]
		downloadUrl = fileUrl.string
		listUrl = downloadUrl.split('.')

		items = len(listUrl)
		iterationPosition = items - 2

		if items < 5 and len(listUrl[iterationPosition]) == 0 and len(listUrl[iterationPosition] > 2):
			message("URL is wrong. Actual URL is: %s" % fileUrl, ERROR)
			return False

		i = 1

		while(True):
			part = str(i)
			if i < 10:
				part = "0%i" % i

			listUrl[iterationPosition] = part
			fileName = "%s.part%s" % (name, part)
			url = ".".join(listUrl)
			if self.downloadFile(url, fileName) == False:
				break
			i += 1

		message("Downloaded.", INFORMATION)
		return True

	def createUrl(self):
		position = self.selected - 1
		url = "http://%s/WebStore/Account/SDMAuthorize.ashx?oiopu=%s&f=%s&oiop=%s&dl=%s" \
			  % (self.domain, self.oiopu[position], self.fileId[position], self.oiop[position], self.dlSelect)
		#print(url)
		return url

	def downloadFile(self, url, fileName):
		message("Testing download URL: %s" % url, INFORMATION)

		request = urllib2.Request(url)
		try:
			u = urllib2.urlopen(request)
			#print(u.getCode())
		except urllib2.URLError, e:
			return False

		f = open(fileName, 'wb')
		meta = u.info()
		#print(meta)
		fileSize = int(meta.getheaders("Content-Length")[0])
		print("Downloading: %s Bytes: %s" % (fileName, fileSize) )

		fileSizeDl = 0
		blockSize = 8192
		while True:
			buffer = u.read(blockSize)
			if not buffer:
				break

			fileSizeDl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (fileSizeDl, fileSizeDl * 100. / fileSize)
			status = status + chr(8)*(len(status)+1)
			print status,

		f.close()

		self.downloadedFiles.append(fileName)

		return True

	def glue(self):
		if len(self.downloadedFiles) == 1:
			os.rename(self.downloadedFiles[0], self.fileName[self.selected])
			return
		destination = open(self.fileName[self.selected-1], 'wb')
		for file in self.downloadedFiles:
			shutil.copyfileobj(open(file, 'rb'), destination)
			os.remove(file)
		destination.close()



if __name__ == '__main__':
	main()
