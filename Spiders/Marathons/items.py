# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class DublinItem(scrapy.Item):
    Name = Field()
    Age = Field()
    AgeCategory = Field()
    Hometown = Field()
    OverallPlace = Field()
    Category = Field()
    CategoryPlace = Field()
    GenderPlace = Field()
    Gender = Field()
    Ten_Kilometer_Split = Field()
    Half_Split = Field()
    Thirty_Kilometer_Split = Field()
    Clock_Time = Field()
    Net_Time = Field()
    RunnerID = Field()
    RaceID = Field()

class DisneyItem(scrapy.item):
    Name = Field()
    Hometown = Field()
    Age = Field()
    Bib = Field()
    GenderPlace = Field()
    CategoryPlace = Field()
    Five_Mile_Split = Field()
    Ten_Mile_Split = Field()
    Fifteen_Mile_Split = Field()
    Twenty_Mile_Split = Field()
    Clock_Time = Field()
    Net_Time = Field()
