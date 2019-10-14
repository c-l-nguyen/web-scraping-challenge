# web-scraping-challenge

A Flask application created by web scraping the latest Mars news, facts, and images and storing in/pulling from a Mongo database.

## Contents
* **/Mission_to_Mars**
  * **/templates**: contains template HTML file for Flask application
  * app.py: Flask application
  * mission_to_mars.ipynb: web scraping Mars news, facts, and images in Jupyter Notebook from various websites
  * scrape_mars.py: web scraping in Python function form for use in Flask application
  
## Description
The latest Mars news, facts, and space images are continually updated. To keep up with that, a web scraping script was created using BeautifulSoup and Splinter in Python. The resulting contents are summarized in a Flask application webpage in this project. 

The following websites were scraped and data obtained:
* [NASA Mars News Site](https://mars.nasa.gov/news/): latest Mars News Title and associated Paragraph Text
* [JPL Featured Space Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars): image url for the current Featured Mars Image
* [Mars Weather twitter account](https://twitter.com/marswxreport?lang=en): latest Mars weather tweet
* [Mars Facts webpage](https://space-facts.com/mars/): facts table about the Mars including Diameter, Mass, etc.
* [USGS Astrogeology site](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars): high resolution images for each of Mar's hemispheres

This data was then stored in a MongoDB collection. This collection is accessed in a Flask app and HTML template (using Jinja) to create the resulting webpage:
