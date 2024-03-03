import scrapy
from chapterLiving.helpers.selenium_script import SeleniumHelper
from pymongo import MongoClient



class ChapterlivingSpider(scrapy.Spider):
    name = "chapterliving"
    allowed_domains = ["chapter-living.com"]
    start_urls = ["https://www.chapter-living.com/booking/"]
    
    def save_to_mongodb(self, data):
        # MongoDB connection parameters
        client = MongoClient("mongodb+srv://sachinsinghshah:sss12345@mongosss.0ynhdax.mongodb.net/")
        db = client.scrapy
        collection = db['Properties']  # Update with your collection name

        # Insert the data into MongoDB
        collection.insert_one(data)

    def parse(self, response):
        # Initialize SeleniumHelper
        selenium_helper = SeleniumHelper()

        # Trigger Selenium functionality and extract data
        extracted_data = selenium_helper.navigate_and_extract_data(response.url)
        
        print(extracted_data)

        selenium_helper.close_driver()
        for data in extracted_data:
            self.save_to_mongodb(data)
        
        
        
#     