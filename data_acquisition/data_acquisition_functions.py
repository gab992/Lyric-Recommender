import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
import requests
import time, os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen

def get_artist_album_lists():
    '''Returns 2 lists, albums and artists, from the pitchform list of the top 200 albums of the 2010s'''
    # Opens driver window on albumoftheyear.org
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://pitchfork.com/features/lists-and-guides/the-200-best-albums-of-the-2010s/')

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    albums_html = soup.find_all('h2')
    artists = []
    albums = []
    for album_h in albums_html:
        al = album_h.prettify().splitlines()
        artist = al[1].strip()
        artist = artist[:len(artist)-1]
        artists.append(artist)
        album = al[3].strip()
        albums.append(album)
    driver.close()

    return artists, albums

def get_links(artists, albums):
    '''Returns a list of page links to songs from the albums in the pitchfork top 200 albums of the 2010s list'''
    page_links=[]
    driver = webdriver.Chrome(chromedriver)
    driver.get('https://genius.com')
    for ind, album in enumerate(albums):
        try:
            print(album)
            time.sleep(3)
            search = driver.find_element_by_xpath("//form[@action='/search']")
            term = search.find_element_by_xpath("./input[@name='q']")
            typed = term.send_keys(artists[ind]+' '+album, Keys.ENTER)
            time.sleep(5)
            album_box = driver.find_elements_by_xpath("//a[@class='vertical_album_card']")
            album_box[-1].click()
            time.sleep(4)
            tracks = driver.find_elements_by_xpath("//a[@href]")
            for track in tracks:
                try:
                    link = track.get_attribute('href')
                    if link[(len(link)-6):] == 'lyrics':
                        page_links.append(link)
                except:
                    pass
            home = driver.find_element_by_xpath("//a[@href='https://genius.com/']")
            home.click()
            time.sleep(3)
        except:
            pass
    driver.close()
    return page_links

def get_json(link):
    '''gets json file with lyrics from a genius.com url'''
    # For ignoring SSL certificate errors

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Input from user
    url = link
    #input('Enter Genius song lyrics Url- ')

    # Making the website believe that you are accessing it using a mozilla browser
    req = Request(url, headers = { 'User-Agent' : 'Mozilla/5.0' })
    webpage = urlopen(req).read()

    # Creating a BeautifulSoup object of the html page for easy extraction of data.

    soup = BeautifulSoup(webpage, 'html.parser')
    html = soup.prettify('utf-8')
    song_json = {}
    song_json["Lyrics"] = [];
    song_json["Comments"] = [];

    #Extract Title of the song
    for title in soup.findAll('title'):
      song_json["Title"] = title.text.strip()

    # Extract the release date of the song
    for span in soup.findAll('span', attrs = {'class': 'metadata_unit-info metadata_unit-info--text_only'}):
      song_json["Release date"] = span.text.strip()

    # Extract the Comments on the song
    for div in soup.findAll('div', attrs = {'class': 'rich_text_formatting'}):
      comments = div.text.strip().split("\n")
      for comment in comments:
          if comment!="":
              song_json["Comments"].append(comment);

    #Extract the Lyrics of the song
    for div in soup.findAll('div', attrs = {'class': 'lyrics'}):
      song_json["Lyrics"].append(div.text.strip().split("\n"));

    #Save the json created with the file name as title + .json
    with open(song_json["Title"] + '.json', 'w') as outfile:
      json.dump(song_json, outfile, indent = 4, ensure_ascii = False)
