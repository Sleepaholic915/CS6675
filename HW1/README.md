# CS6675 HW1 Summer 2025
## Summer Li (ali385)

## Project Summary

The option I chose was Problem 1 Option 1.1. The web crawler I used is Scrapy, with my main crawler spider file being spider.py and crawled data saved in crawl_data.json. The seed url I chose was the Georgia Tech College of Computing website. I successfully crawled 1,000+ web pages, extracted keywords, and plotted data respectively.

## How to Execute the Crawler

- Step 1: Setup
  
    Open terminal in project directory
  
    Navigate to webcrawler folder: cd webcrawler

- Step 2: Run Crawler
  
    python -m scrapy crawl spider
  
   (will take 30+ minutes for 1000+ pages)

- Step 3: View Results
  
    Check crawl_data.json for raw data
  
    Open Excel files and graphs in Excel and Plots/ folder for analysis


## File Structure

├── webcrawler/spiders/spider.py    # Main crawler code

├── crawl_data.json                 # Raw crawled data    

├── Excel and Plots/                # Required excel sheets and plots

└── README.MD

## Key Results

Pages Crawled: 1,000+

Crawl Speed: 3.2 URLs per minute

Keywords Extracted: 9,500+ total

Average Keywords per Page: 9.5

Success Rate: 95%+


## Experience & Lessons Learned
This web crawling project was my first-ever experience with large-scale data collection, and it was quite challenging for me. I decided to go with the Scrapy framework because I had prior Python experience, and I found Scrapy very friendly to new users. I found this project very good for structured crawling and it can handle errors automatically, but I also learned there is always a difficult balance between being respectful to websites and getting good performance. I decided to set 2-second delays between requests and follow robots.txt rules to make sure I don't cause problems for the server, but this made my crawler very slow - only 3.2 URLs per minute. I was also surprised to discover that different pages have very different content quality - the early academic pages I crawled had around 15+ keywords each, but later when my crawler found navigation and directory pages, they only had about 9.5 keywords on average. The most shocking part for me was when I calculated the scaling numbers: with my current crawl speed, it would take 595 years to crawl 1 billion pages. It gives me new insights on how real-world search engines would require massively distributed architectures with thousands of concurrent crawlers to return immediate results.
Overall, I think this project taught me a lot about web crawling basics and also showed me how much difference there is between what we can do in school projects versus what real companies need to build, giving me good knowledge about web scraping ethics, Python programming, and why single-computer approaches cannot work for very large data collection.
