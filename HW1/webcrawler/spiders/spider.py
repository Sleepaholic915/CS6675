import scrapy
import re
from urllib.parse import urljoin, urlparse
import time
from collections import Counter

class GatechSpider(scrapy.Spider):
    name = 'gatech'
    allowed_domains = ['cc.gatech.edu']
    start_urls = ['https://cc.gatech.edu']
    
    crawled_count = 0
    max_pages = 1500  
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2, 
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1, 
        'ROBOTSTXT_OBEY': True,
        'FEEDS': {
            'crawl_data.json': {
                'format': 'jsonlines',
                'overwrite': True,
        }
    }
}
    
    def __init__(self):
        self.start_time = time.time()
        print(f"[START] Crawl begins at {time.ctime()}")

    def parse(self, response):
        if self.crawled_pages >= self.max_pages:
            self.logger.info(f"Reached page limit: {self.max_pages}")
            return

        if self.crawled_pages % 50 == 0:
            self._log_progress()

        yield self._extract_page_info(response)

        for href in response.css('a::attr(href)').getall():
            if self.crawled_pages >= self.max_pages:
                break

            full_url = urljoin(response.url, href)
            if self._should_follow(full_url):
                yield response.follow(full_url, callback=self.parse)

    def _extract_page_info(self, response):
        self.crawled_pages += 1
        text_blocks = []
        selectors = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'span', 'li']
        for sel in selectors:
            text_blocks.extend(response.css(f"{sel}::text").getall())


        raw_text = ' '.join(text_blocks)
        clean_text = self._clean_text(raw_text)
        keywords = self._extract_keywords(clean_text)

        return {
            'url': response.url,
            'title': response.css('title::text').get(default='').strip(),
            'text_content': clean_text[:2000],
            'keywords': keywords,
            'keyword_count': len(keywords),
            'word_count': len(clean_text.split()),
            'link_count': len(response.css('a::attr(href)').getall()),
            'crawl_timestamp': time.time(),
            'crawl_order': self.crawled_pages,
            'status_code': response.status,
            'page_size': len(response.body),
        }

    def _clean_text(self, text):
        if not text:
            return ""
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        return ' '.join(cleaned.split()).lower()
    

    def _extract_keywords(self, text, min_len=4, max_keywords=15):
        if not text:
            return []

        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'can', 'this', 'that', 'these', 'those', 'a', 'an', 'as', 'if',
            'each', 'how', 'which', 'who', 'when', 'where', 'why', 'what', 'there', 'here',
            'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

        words = [
            word for word in text.split()
            if len(word) >= min_len and word.isalpha() and word not in stop_words
        ]

        freq = Counter(words)
        return [word for word, _ in freq.most_common(max_keywords)]


    def _should_follow(self, url):
        try:
            parsed = urlparse(url)
        except:
            return False

        if parsed.scheme not in {'http', 'https'}:
            return False

        if not any(domain in parsed.netloc for domain in self.allowed_domains):
            return False

        if url.lower().endswith((
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.tar', '.gz', '.jpg', '.jpeg', '.png', '.gif',
            '.mp4', '.avi', '.mov', '.mp3', '.wav', '.css', '.js'
        )):
            return False

        if url.startswith(('mailto:', 'javascript:', 'tel:')):
            return False

        return True


    def _log_progress(self):
        elapsed = time.time() - self.start_time
        rate = self.crawled_pages / (elapsed / 60) if elapsed else 0
        self.logger.info(
            f"Crawled {self.crawled_pages} pages in {elapsed/60:.1f} min "
            f"({rate:.1f} pages/min)"
        )


    def closed(self, reason):
        elapsed = time.time() - self.start_time
        rate = self.crawled_pages / (elapsed / 60) if elapsed else 0

        print(f"\n[END] Crawl finished. Reason: {reason}")
        print(f"Total pages: {self.crawled_pages}")
        print(f"Duration: {elapsed / 60:.1f} minutes")
        print(f"Avg rate: {rate:.1f} pages/minute")
        print("Results saved to: crawl_data.json")

        if rate:
            est_10m_days = (10_000_000 / rate) / 60 / 24
            est_1b_days = (1_000_000_000 / rate) / 60 / 24
            print(f"\n[Projection]")
            print(f"~10M pages: {est_10m_days:.1f} days")
            print(f"~1B pages: {est_1b_days:.0f} days")