#!/usr/bin/env python

import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # ## NASA Mars News

    nasa_mars_url = "https://mars.nasa.gov/news/"

    browser = init_browser()
    browser.visit(nasa_mars_url)
    soup = BeautifulSoup(browser.html, 'html.parser')

    news_title = soup.find_all("div", class_="content_title")[0].get_text()
    news_paragraph = soup.find_all("div", class_="article_teaser_body")[0].get_text()

    # close browser after scraping
    browser.quit()


    # ## JPL Mars Space Images - Featured Image

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser = init_browser()
    browser.visit(jpl_url)

    browser.click_link_by_partial_text(news_title)
    browser.click_link_by_partial_text("Full image and caption")
    browser.click_link_by_partial_text(".jpg")

    featured_image_url = browser.url

    # close browser after scraping
    browser.quit()


    # ## Mars Weather

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    twitter_page = requests.get(twitter_url)

    soup = BeautifulSoup(twitter_page.content, 'html.parser')

    first_tweet = soup.find_all("div", class_="js-tweet-text-container")[0]
    mars_weather_tweet = first_tweet.find("p").get_text()


    # ## Mars Facts

    mars_facts_url = "https://space-facts.com/mars/"

    browser = init_browser()
    browser.visit(mars_facts_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_facts_table = soup.find_all("table", id="tablepress-p-mars")[0]

    # get the types of facts
    topics = []
    for row in mars_facts_table.find_all("td",class_="column-1"):
        topic_text = row.get_text().replace(":","")
        topics.append(topic_text)

    # get the measurements of the facts
    measurements = []
    for row in mars_facts_table.find_all("td",class_="column-2"):
        measurements.append(row.get_text())

    # combine topics and measurements into single dictionary
    mars_facts_dict = {}

    for i in range(len(topics)):
        mars_facts_dict[topics[i]] = measurements[i]

    # close browser after scraping
    browser.quit()


    # ## Mars Hemispheres

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser = init_browser()
    browser.visit(usgs_url)

    hemispheres = ["Cerberus","Schiaparelli","Syrtis","Valles"]
    hemisphere_image_urls = []

    # loop through each hemisphere and scrape the data
    for hemi in hemispheres:
        new_dict = {}

        browser.click_link_by_partial_text(hemi)
        usgs_html = browser.html
        soup = BeautifulSoup(usgs_html, 'html.parser')
        new_dict["title"] = soup.find("h2").get_text().replace("Enhanced","").strip()
        new_dict["img_url"] = soup.find_all("div", class_="downloads")[0].find_all("a")[0]["href"]
        hemisphere_image_urls.append(new_dict)
        
        # go back to original page with all the hemispheres
        browser.back()

    # close browser after scraping
    browser.quit()

    mars_data = {
        "nasa_mars":{"title":news_title, "paragraph":news_paragraph},
        "jpl_image":featured_image_url,
        "mars_latest_tweet": mars_weather_tweet,
        "mars_facts":mars_facts_dict,
        "mars_hemisphere":hemisphere_image_urls
    }

    return mars_data

if __name__ == "__main__":
    print(scrape())