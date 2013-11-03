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
    # -- Append parameter for print friendly mode
    url = url[:url.find('?')] + "?pagewanted=print"
    # -- Must set Referer or we won't get print friendly page
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
    os.system('lpr tmp.pdf') # -- uses default printer 

if __name__ == '__main__':
    kickoff()


'''
To run every Sunday at 7:30am using cron:
30 7 * * Sun /path/to/me/main.py
'''

