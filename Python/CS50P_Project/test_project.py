import pytest
from project import search_news, summarize, display_news

def test_search_news():
    results = search_news("CS50")
    assert isinstance(results, list)
    assert all(isinstance(article, dict) for article in results)
    assert all("title" in article and "link" in article for article in results)

def test_summarize():
    summary = summarize("https://www.thecrimson.com/article/2024/9/13/cs50-oxford-fall-malan/")
    assert isinstance(summary, str)

def test_display_news():
    articles = [{"title": "Harvard’s CS50 Course to be Offered at Oxford this Fall", "link": "https://www.thecrimson.com/article/2024/9/13/cs50-oxford-fall-malan/"}]
    display_news(articles)