from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def scrape():
    executable_path = {'executable_path': 'C:\Program Files\chromedriver_win32\chromedriver.exe'}

    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://mars.nasa.gov/news/')
    news_title = BeautifulSoup(browser.html, 'html.parser').find('div', class_='content_title').text
    news_p = BeautifulSoup(browser.html, 'html.parser').find('div', class_='article_teaser_body').text
    browser.quit()

    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    feat_href = BeautifulSoup(browser.html, 'html.parser').find('a', class_='button fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + feat_href
    browser.quit()

    twitter_soup = BeautifulSoup(requests.get('https://twitter.com/marswxreport?lang=en').text, 'html.parser')
    tweet_string = twitter_soup.body.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    end_string = tweet_string.find('hPa') + 3
    mars_weather = tweet_string[:end_string].replace('\n', ' ')

    mars_df = pd.read_html('https://space-facts.com/mars/')[0].rename(columns={0:'description', 1:'value'}).set_index('description')

    mars_htmltable = mars_df.to_html().replace('\n', '')

    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    hemi_html = BeautifulSoup(browser.html, 'html.parser').find_all('div', class_='description')

    hemi_list = []
    img_list = []

    for x in range(len(hemi_html)):
        hemi_list.append(hemi_html[x].find('h3').text[:hemi_html[x].find('h3').text.find('Hemisphere')+len('Hemisphere')])
        img_list.append('https://astrogeology.usgs.gov' + hemi_html[x].find('a')['href'])

    for y in range(len(img_list)):
        browser.visit(img_list[y])
        img_list[y] = BeautifulSoup(browser.html, 'html.parser').find('div', class_='downloads').find('a')['href']

    browser.quit()

    hemisphere_image_urls = []
    for z in range(len(hemi_list)):
        hemisphere_image_urls.append({'title':hemi_list[z], 'img_url':img_list[z]})

    return {'news_title':news_title, 'news_p':news_p, 'featured_image_url':featured_image_url, 'mars_weather':mars_weather, 'mars_htmltable':mars_htmltable, 'hemisphere_image_urls':hemisphere_image_urls}