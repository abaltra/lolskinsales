# looskinsales
Scraper and API for lol skin sales

# Installation
requires python2.7, pip, pymongo, requests, scrapy and flask

# API
The app has a simple public API with sales data, it has 3 endpoints (for now) as follows:

 - api.lolskinsales.com -> Full list of current sale items
 - api.lolskinsales.com/championName/:champ_name -> Current sale info for champ named :champ_name. If the champ isn't on sale, it'll return an error
 - api.lolskinsales.com/championId/:champ_id -> Current sale info for champ with id :champ_name as shown in Riot's API. If the champ isn't on sale, it'll return an error 
