from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
import re
from urllib import quote

torrent_pattern = re.compile(r'''<div class="torrentName">?\s*<a href="/sub/(?P<cat_id>\d+)/0/" class=".*" title=".*">?\s*</a>?\s*<h3 class="org">?\s*<a href="(?P<desc_link>.+)" class="org">(?P<name>.+)</a>?\s*</h3>?\s*<div class="clr">?\s*</div>?\s*</div>?\s*<span class="seed">(?P<seeds>.+)</span>?\s*<span class="leech">(?P<leech>.+)</span>?\s*<span class="size">(?P<size>.+)</span>''')
download_pattern = re.compile(r'''<a href="(?P<link>.+)?" onclick''')
tag = re.compile(r'<.*?>')                          

class x1337(object):
	url = 'http://1337x.org'
	name = '1337x.org'
	supported_categories = {'all': '',
		'movies': [1, 2, 3, 4, 9, 42, 54, 55, ],
		'tv': [5, 6, 7, 41, ],
		'music': [22, 23, 24, 25, 26, 27, 53, ],
		'games': [10, 11, 12, 13, 14, 15, 16, 17, 43, 44, 45, 46, ],
		'anime': [28, ],
		'software': [18, 19, 20, 21, ],
		'pictures': [37, ],
		'books': [34, 36, 39, 52, ],
	}
	# CATEGORIES = ('all', 'movies', 'tv', 'music', 'games', 'anime', 'software', 'pictures', 'books')

	def __init__(self):
		pass
		
	def download_torrent(self, info):
		info_page = retrieve_url(info)
		link = download_pattern.findall(info_page)[0]
		print download_file(link)

	def search_page(self, what, cat, start):
		# html = retrieve_url(self.url+'/sort-tag/%s/seeders/desc/%s/' % s(quote(what), start))
		html = retrieve_url(self.url+'/search/%s/%s/'%(quote(what), start))
		for el in torrent_pattern.finditer(html):
			d = el.groupdict()
			d['desc_link'] = self.url + d['desc_link']
			d['engine_url'] = self.url
			d['name'] = tag.sub('', d['name'])
			d['link'] = d['desc_link']
			d['cat_id'] = int(d['cat_id'])
			# exclude xxx videos from the result
			if d['cat_id'] in [48, 49, 50, 51]:
				continue
			if cat != 'all':
				if d['cat_id'] in self.supported_categories[cat]:
					yield d
			else:
				yield d

	def search(self, what, cat='all'):
		start = 0
		f = True
		while f and start < 51:
			f = False
			for d in self.search_page(what, cat, start):
				prettyPrinter(d)
				f = True
			start += 1
