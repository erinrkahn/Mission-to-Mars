#!/usr/bin/env python
# coding: utf-8

# In[41]:


# Import Splinter and BeautifulSoup
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


# In[42]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[43]:


# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[44]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[45]:


slide_elem.find('div', class_='content_title')


# In[46]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[47]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[48]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[49]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[50]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[51]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[52]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[53]:


df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[54]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[89]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[90]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
base_path ='https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'
browser.visit(url)
html = browser.html
img_soup = soup(html, 'html.parser')


# In[91]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
description_divs = img_soup.find_all('div', class_='description')

for desc_div in description_divs:
    atag = desc_div.find('a', class_="itemLink product-item")
    planet_url = base_path+atag['href']
    browser.visit(planet_url)
    planet_soup = soup(browser.html, 'html.parser')
    full_image_url = base_path + planet_soup.find('img',class_='wide-image').get('src')
    full_image_title = planet_soup.find('h2',class_='title').text
    hemispheres = {}
    hemispheres['image_url'] = full_image_url
    hemispheres['title'] = full_image_title
    hemisphere_image_urls.append(hemispheres)


# In[92]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[93]:


# 5. Quit the browser
browser.quit()


# In[ ]:




