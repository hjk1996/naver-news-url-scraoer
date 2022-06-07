from bs4 import BeautifulSoup
import requests
from lxml import etree
from lxml.etree import _Element

from model import NewsOverview

class NaverNewsUrlScraper:
    SORTS = {"relate": 0, "new": 1, "old": 2}
    URL_TEMPLATE = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort={}&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start={}"
    
    NEWS_LIST_ITEM_XPATH = '//*[@class="bx"]'
    NAVER_NEWS_LINK_XPATH = './/div/div/div/div[2]/a'
    PRESS_NAMES_XPATH = './div/div/div/div[2]/a/span'
    TITLE_XPATH = './div/div/a'
    

    def __init__(self, keyword: str, sort: str, start_page: int, target_amount: int) -> None:
        if sort not in self.SORTS.keys():
            raise ValueError("Invalid sort value")
        
        self._parser = etree.HTMLParser()
        self._sort = self.SORTS[sort]
        self._keyword = keyword
        self._current_page = start_page
        self._target_amount = target_amount
        self._data = set()

    def scrape(self):

        while True:
            url = self.URL_TEMPLATE.format(self._keyword, self._sort, self._current_page * 10 - 9)
            dom = self._get_dom_from_url(url)
            page_data, is_last_page = self._extract_data_from_dom(dom)
            self._data.update(page_data)
    
            if self._should_break or is_last_page:
                break
            
            self._current_page += 1
            


    def _get_dom_from_url(self, url: str) -> _Element:
        res = requests.get(url)
        html = BeautifulSoup(res.text, "html.parser")
        return etree.HTML(str(html))

    def _extract_data_from_dom(self, dom: _Element) -> tuple[set[NewsOverview], bool]:
        is_last_page = False
        news_item_elements: list[_Element] = dom.xpath(self.NEWS_LIST_ITEM_XPATH)

        if len(news_item_elements) < 10:
            is_last_page = True

        filtered_news_item_elements = self._filter_news_list(news_item_elements)

        press_names = self._extract_press_names(filtered_news_item_elements)
        news_links = self._extract_news_links(filtered_news_item_elements)
        news_titles = self._extract_news_titles(filtered_news_item_elements)

        return self._make_news_overview_objects(press_names, news_links, news_titles), is_last_page

    @staticmethod
    def _make_news_overview_objects(press_names: list[str], news_links: list[str], news_titles: list[str]) -> set[NewsOverview]:
        overviews = set()
        for press, link, title in zip(press_names, news_links, news_titles):
            overviews.add(NewsOverview(press, link, title))
        return overviews

    def _extract_press_names(self, news_list: list[_Element]) -> list[str]:
        return [element.find(self.PRESS_NAMES_XPATH).tail.strip() for element in news_list]

    def _extract_news_links(self, news_list: list[_Element]) -> list[str]:
        return [element.findall(self.NAVER_NEWS_LINK_XPATH)[-1].attrib['href'] for element in news_list]

    def _extract_news_titles(self, news_list: list[_Element]) -> list[str]:
        return [element.find(self.TITLE_XPATH).attrib['title'].strip() for element in news_list]

    def _filter_news_list(self, news_list: list[_Element]) -> list[_Element]:
        return [element for element in news_list if self._is_naver_news(element)]

    def _is_naver_news(self, element: _Element) -> bool:
        return len(element.findall(self.NAVER_NEWS_LINK_XPATH)) == 2
    
    @property
    def _should_break(self) -> bool:
        if self._current_page > 400:
            return True
        
        if len(self._data) >= self._target_amount:
            return True
        
        return False

    @staticmethod
    def _is_beyond_end_page(html: str) -> bool:
        pass
        

        
        