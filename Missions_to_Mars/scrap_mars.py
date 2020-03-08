from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time
import pymongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)


    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title=soup.find('div',class_="list_text").find('div',class_="content_title").text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Display scrapped data 
    print(news_title)
    print(news_p)

# Find the image URL for Mars
    # Visit Mars Space Images through splinter module
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)


    # Set HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Add website URL
    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Retrieve the element that contains the url of image from the style
    featured_image_url=soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Print full link to featured image
    print(featured_image_url)


    # Mars Weather


    # Visit Mars Weather URL through splinter module
    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)



    # Set HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    # Print the html out to check where to find the tweet contect
    soup = bs(html, 'html.parser')
    tweet_html_content = requests.get(tweet_url).text
    soup = bs(tweet_html_content, "lxml")

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display only weather related words 
    latest_tweets = soup.find_all('div', class_="js-tweet-text-container")
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass

    # Mars Facts

    fact_url='https://space-facts.com/mars/'

    tables = pd.read_html(fact_url)
    tables

    # Print the tabe that needs to be transformed into dataframe 
    tables[0]

    fact_df=tables[0]
    fact_df.columns = ['Description','Value']
    fact_df.set_index('Description',inplace=True)
    fact_df

    # Convert Data frame to HTML
    html_table = fact_df.to_html()


    # Strip unwanted newlines to clean up the table
    html_table.replace('\n', '')

    # Save the html file to local folder
    fact_table=fact_df.to_html()

    # Mars Hemispheres
    # Find each url for all four links 
    cerberus_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    schiaparelli_url="https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    syrtis_major="https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    valles_marineris="https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
   
    list_urls=[cerberus_url,schiaparelli_url,syrtis_major,valles_marineris]
    hemisphere_image_urls_list=[]

    for img_url in list_urls:
        browser.visit(img_url)
        html=browser.html
        soup=bs(html, 'html.parser')
        original_title=soup.find('h2',class_='title').text
        title=original_title.strip('Enhanced')
        
        img=soup.find('img',class_='wide-image')["src"]
        img_url=f'https:astrogeology.usgs.gov{img}'
        
        hemisphere_image_urls={}
        hemisphere_image_urls['title']=title
        hemisphere_image_urls['img_url']=img_url    
        hemisphere_image_urls_list.append(hemisphere_image_urls)
       
    hemisphere_image_urls_list
    

    
    # Store data in a dictionary
    mars_data={
        "mars_title":news_title,  
        "mars_news":news_p,
        "mars_img":featured_image_url,
        "mars_weather":weather_tweet,
        "mars_fact":html_table,
        "mars_hemisphere":hemisphere_image_urls_list
    }

    # close the browser 
    browser.quit()

    #return results
    return mars_data




