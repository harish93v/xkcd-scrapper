xkcd-scrapper
=============

A simple python script to download images and its text from xkcd.com

Dependencies:
	BeautifulSoup4
	urllib2
	urllib
	lxml
	joblib
* Use pip to install dependencies (Install pip beforehand)
* Will be using to create a local mirror of the site.
* Rather than mirroring using curl or wget, this will consume less space as they use the same template through out the website :)
* Uses multiprocess to create paralleize the downloads

Usage: python xkcd.py <start> <end> <no_of_processes>
