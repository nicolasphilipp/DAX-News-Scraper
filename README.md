## IMPORTANT: outdated and probably not working anymore

This repository contains 3 crawlers/scrapers to find relevant links to articles providing information about price movements of the DAX performance index.

## Usage

### 1. Linkcrawler

Run the following command to extract links and save them to a JSON file:

```bash
scrapy crawl Linkcrawler -o outputLinks.json
```

#### Output (outputLinks.json):
```json
[
  {"link_url": "https://finanzmarktwelt.de/dax-daily-die-devise-an-den-aktienmaerkten-lautet-to-the-moon-190317/"},
  {"link_url": "https://www.boerse-online.de/nachrichten/ressort/maerkte/dax-chartanalyse-anstieg-wird-sich-verlangsamen-1030044819"},
  {"link_url": "https://www.boerse-daily.de/boersen-nachrichten/insight-dax-ruhiger-handel-vor-us-leitzinsentscheid-34490"},
  {"link_url": "https://www.godmode-trader.de/analyse/dax-tagesausblick-weiterer-sprunghafter-kursanstieg,9290831"}
]
```

---

### 2. Contentcrawler

To crawl and process content from the previously extracted links, use the following command:

```bash
scrapy crawl Contentcrawler -a inputfile=outputLinks.json
```

#### Output Example:
```text
...
2021-03-20 15:19:53 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://admiralmarkets.com/de/analysen/dax30-tages-updates> (referer: None)
['Der Dax ging gestern morgen bei 14.725 Punkten in den vorbörslichen Handel. ...', 'Kann sich der Dax über der 14.680 Punkte Marke halten, so könnte es weiter aufwärts an unsere nächsten Anlaufziele bei 14.689/91, bei 14.702/04, bei 14.711/13 und dann bei 14.723/25 Punkten gehen. Kommt es hier zu keinen Rücksetzern, so könnte sich die Aufwärtsbewegung weiter fortsetzen. ', 'Rutscht der Dax unter die 14.680 Punkte, so könnte er zunächst unsere nächsten Anlaufziele bei 14.669/67, bei 14.651/49 und dann bei 14.636/34 Punkten erreichen. Kommt es hier zu keinen Erholungen, so könnten sich die Abgaben weiter fortsetzen. ', '14.763 Punkte bis 14.635 Punkte ist die heute von uns erwartete Tagesrange. ']
...
```

---

### 3. Libertexcrawler

Run the following command to crawl specific data from Libertex:

```bash
scrapy crawl Libertexcrawler
```

#### Output Example:
```text
...
2021-03-01 15:10:41 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://app.libertex.com/products/indexes/FDAX/#modal_news_5711895_FDAX> (referer: https://app.libertex.com/products/indexes/FDAX/)
2021-03-01 15:10:42 [selenium.webdriver.remote.remote_connection] DEBUG: Finished Request http://127.0.0.1:52305/session/43c18f59a13ba90527cd707167860bfe/url {"url": "https://app.libertex.com/products/indexes/FDAX/#modal_news_5711895_FDAX"}
...
['Kaufposition über 13830,00 mit Kurszielen von 14010,00 & 14070,00. ', 'Pivot-Punkt: 13830,00. ', 'Unsere Meinung: Kaufposition über 13830,00 mit Kurszielen von 14010,00 & 14070,00. ', '...']
...
```
