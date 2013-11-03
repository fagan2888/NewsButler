import os
import pdfkit
import requests
import feedparser

num_articles = None

def kickoff():
    source = 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    data = feedparser.parse(source)
    articles = data['entries']
    if num_articles:
        articles = articles[:num_articles]

    for article in articles:
        title = article['title']
        print "Printing:", title
        url = article['link']
        grab_article(url)

def grab_article(url):
    origUrl = url
    url = url[:url.find('?')] + "?pagewanted=print"
    headers = {'Referer': origUrl}
    print "Sending HTTP req..."
    page = requests.get(url, headers=headers)
    html = page.content
    tmpFile = open('tmp.html', 'w')
    tmpFile.write(html)
    tmpFile.close()
    print "Making pdf..."
    pdfkit.from_file('tmp.html', 'tmp.pdf')
    print "Printing..." 
    # os.system('lpr tmp.pdf') # -- uses default printer 

if __name__ == '__main__':
    kickoff()


'''
Run every saturday at 7:30am
30 7 * * Sat /usr/bin/find
'''

