#!/usr/bin/python

import xml.sax
import urlparse
import httplib
import urllib

class MyUrlOpener(urllib.FancyURLopener):
    version='User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'



if ( __name__ == "__main__"):
    url="http://feeds.feedburner.com/TransmissaoFantasma"
    
    urllib._urlopener = MyUrlOpener()
    
    '''opener = urllib.URLopener()
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')]
    
    f = opener.open(url)'''
    

    f = urllib.urlopen(url)
    
    print f.read()
    
    
    print urllib.__version__
    
    '''parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        
        podcastHandler = PodcastHandler()
        parser.setContentHandler(podcastHandler)

        try:
            print "url: ", url
            url = resolve_http_redirect(url)
            
            f = urllib.urlopen(url)
            
            parser.parse(f)
        except xml.sax.SAXParseException, e:
            print "SAXParseException:", e
        except IOError:
            print "IOError:", url
        except Exception:
            pass
        
        podcast = podcastHandler.podcast
        podcast.feedUrl = url
        podcasts.append(podcast)'''
