#!/usr/bin/python

import xml.sax
import urllib2
import socket
import threading

class StopSaxException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class NotXMLException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    

class Podcast():
    def __init__(self):
        self.nome=u""
        self.feedUrl=u""
        self.descricao=u""
        self.imgUrl=u""
        
    def __unicode__(self):
        return u"Nome: " + self.nome + "\nDescricao: " + self.descricao + "\nFeed: " + self.feedUrl + "\nImagem: " + self.imgUrl + "\n"

class OPMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.urls = [];
        
    def startElement(self, tag, attributes):
        if tag == "outline":
            urlString = attributes["xmlUrl"];
            if urlString:
                self.urls.append(urlString);
                


class PodcastHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentTag = ""
        self.podcast = Podcast()
        self.salvarPodcast = True
    
    def startElement(self, tag, attributes):
        self.CurrentTag=tag;
        
        if tag == "itunes:image":
            self.podcast.imgUrl=attributes["href"];
        
        elif tag == "item":
            raise StopSaxException("Todos os dados carregados")
            
        elif tag == "html":
            raise NotXMLException("Arquivo esta em HTML")
            
    def characters(self, content):
        if self.CurrentTag=="title":
            if not self.podcast.nome:
                self.podcast.nome=content
        elif self.CurrentTag=="description":
            if not self.podcast.descricao:
                self.podcast.descricao=content
        elif self.CurrentTag=="url":
            self.podcast.imgUrl=content;
    
    def endElement(self, tag):
        self.CurrentTag=""


def handlePodcastUrl(podcastHandler, url):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(podcastHandler)
    
           
    try:
        #print "url: ", url
        parser.parse(opener.open(url))
    except xml.sax.SAXParseException, e:
        podcastHandler.salvarPodcast=False
        print "SAXParseException:", e
    except IOError as ioe:
        podcastHandler.salvarPodcast=False
        print "IOError:", url, "ERRO:", ioe
    except NotXMLException:
        podcastHandler.salvarPodcast=False
        print "NotXMLException:", url
    except StopSaxException:
        pass
    except Exception:
        podcastHandler.salvarPodcast=False
    
    podcastHandler.podcast.feedUrl = url
    
                
if ( __name__ == "__main__"):
    
    
    socket.setdefaulttimeout(10)
    
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    
    opmlHandler = OPMLHandler()
    parser.setContentHandler(opmlHandler)
    parser.parse("/home/murilo/Dropbox/podkicker_backup.opml");
    
    podcasts = [];
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')]
    
    podcastHandlers = []
    podThreads = []
    
    for url in opmlHandler.urls:
        podcastHandler = PodcastHandler()
        podcastHandlers.append(podcastHandler)

        podThreads.append(threading.Thread(target=handlePodcastUrl, args=(podcastHandler, url)))
        
    
    for t in podThreads:
        t.start()
    
    for t in podThreads:
        t.join()
            
        
    for podcastHandler in podcastHandlers:
        if podcastHandler.salvarPodcast:
            podcast = podcastHandler.podcast
            podcasts.append(podcast)    
        
        
    for podcast in podcasts:
        print "Nome:", podcast.nome
        print "Descricao:", podcast.descricao
        print "Feed:", podcast.feedUrl
        print "Imagem:", podcast.imgUrl
        print "\n"
        
    print "Podcasts regisgrados", len(podcasts)
    
        
    
    
    
    
