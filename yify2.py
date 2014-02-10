from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
import json

class yify2(object):
    url = 'http://yts.im'
    name = 'YIFY Torrents'
    
    supported_categories = {
        'all': 'All',
        #'movies': 'Comedy',
        'music': 'Music',
        'anime': 'Animation',
    }

    def __init__(self):
        pass

    def search(self, what, cat='all'):
        i = 1
        while True and i<11:
            results = []
            url = self.url+'/api/list.json?sort=seeds&limit=50&keywords=%s&set=%s&genre=%s'%(what, i, self.supported_categories[cat])
            json_data = retrieve_url(url)
            try:
                json_dict = json.loads(json_data)
            except:
                i += 1
                continue
            try:
                results = json_dict['MovieList']
            except KeyError:
                return
            else:
                for r in results:
                    res_dict = dict()
                    res_dict['name'] = r['MovieTitle']
                    res_dict['size'] = r['Size']
                    res_dict['seeds'] = r['TorrentSeeds']
                    res_dict['leech'] = r['TorrentPeers']
                    res_dict['link'] = r['TorrentUrl']
                    res_dict['desc_link'] = r['MovieUrl']
                    res_dict['engine_url'] = self.url
                    prettyPrinter(res_dict)
            i += 1
                    
if __name__ == "__main__":
    y = yify2()
    y.search('millers')
