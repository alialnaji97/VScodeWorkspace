from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import sys


client = OpenAI(api_key="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")


def main():

    topic = input("Enter a news topic to search for: ").strip()

    articles = search_news(topic)
    if not articles:
        sys.exit("No news articles found.")

    display_news(articles)



def search_news(topic):
    """
    Search for news articles with the given topic.

    Searches Google for news articles with the given topic, and returns
    the top 5 results as a list of dictionaries with keys "title" and "link".

    :param topic: The topic to search for.
    :return: A list of dictionaries with keys "title" and "link".
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(f"https://www.google.com/search?q={topic}+news&hl=en", headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for item in soup.select(".tF2Cxc"):  # Class for Google search result cards
        title = item.select_one("h3").text
        link = item.select_one("a")["href"]
        results.append({"title": title, "link": link})

    return results[:5]  # Return the top 5 results

def display_news(articles):
    """
    Displays the given list of news articles, with a summary for each.

    :param articles: A list of dictionaries with keys "title" and "link".
    """
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")

        summary = summarize(article["link"])
        print(f"Summary: {summary}")
        print("-" * 100)

def summarize(url):
    """
    Summarize a news article at the given URL in 2-3 sentences.

    Fetches the article content, extracts the first 5 paragraphs of text, and uses
    OpenAI GPT to generate a summary.

    Returns the summary as a string, or an error message if summarization fails.
    """

    try:
        # Fetch article content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract paragraphs of text
        paragraphs = soup.find_all("p")
        content = " ".join(p.get_text(strip=True) for p in paragraphs[:5])  # Limit to 5 paragraphs

        # Use OpenAI GPT to summarize
        if content:
            prompt = f"Summarize the following news article in 2-3 sentences:\n\n{content}"
            completion = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0)
            summary = completion.choices[0].message.content
            return summary.strip()

        return "Could not extract content for summarization."
    except Exception as e:
        return f"Error summarizing article: {e}"


if __name__ == "__main__":
    main()