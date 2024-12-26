# News Web Scraper and Summarizer

    #### Video Demo:  <URL HERE>
    #### Description:

This project is a Python-based application that fetches news articles from the web, summarizes their content using OpenAI’s GPT-3.5, and presents the user with a concise overview of the latest information about a topic of their choice.

The program begins by prompting the user for a topic of interest. The application then constructs a Google search URL for the chosen topic, appending search modifiers like "news" to focus on relevant articles. Using the `requests` library, the program sends a GET request to the search engine and retrieves the search results page's HTML. To parse the returned HTML, the project uses `BeautifulSoup` from the `bs4` library, which allows us to extract the desired content, such as article titles and links, using CSS class selectors.

Once the program identifies potential articles, it compiles a list of the top five articles, returning their titles and URLs. These articles are then processed one by one. For each article, the program uses the extracted URL to send another GET request to fetch the article’s HTML content. The first few paragraphs of text from the article are gathered and treated as input data. If no usable content can be extracted from the article, the program gracefully handles this by returning a could not find string.

The gathered content is then sent to OpenAI’s GPT-3.5 model for summarization. This is achieved by instructing the AI to condense the article into two to three sentences. The `openai.ChatCompletion` API is used to interact with the model, specifying parameters such as the prompt, token limits, and temperature (to control the randomness of the output). The result is a concise and readable summary of the article, highlighting key points or findings. Each summary is paired with its respective title and link, making it easy for the user to explore the original article if desired.

Each article's title, URL, and summary are printed to the console, separated by horizontal lines for better readability. This ensures that users can quickly scan through multiple articles and decide which ones are they interested in.

Functions like `search_news` and `summarize_article` are isolated, allowing for easy maintenance and reusability. The use of libraries like `requests` ensures robust and efficient HTTP requests, while `BeautifulSoup` provides a powerful toolset for navigating and extracting data from raw HTML. The integration of OpenAI’s API showcases the potential of GPT models in real-world applications, transforming unstructured article content into concise summaries.
