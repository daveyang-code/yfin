import requests
from bs4 import BeautifulSoup
import argparse
import sys


def getWatchlists():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    url = "https://finance.yahoo.com/watchlists/category/section-popular"
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find(
        "table",
        {
            "class": "cwl-category-table W(100%) Pos(r) BdB Bdc($seperatorColor) Mb(30px)"
        },
    )
    rows = table.find_all("tr")

    watchlists = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            watchlist_name = cells[0].text.strip()
            watchlist_link = cells[0].find("a").get("href")
            watchlists.append([watchlist_name, watchlist_link])

    return watchlists


def getWatchlistItems(ext):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    url = "https://finance.yahoo.com"
    response = requests.get(url + ext, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find_all("table", {"class": "W(100%)"})[1]
    rows = table.find_all("tr")
    watchlist = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            watchlist.append(cells[0].text.strip())
    return watchlist


def getScreeners():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    url = "https://finance.yahoo.com/screener"
    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"class": "Tbl(f) W(100%) BdT Bdtc($seperatorColor)"})
    rows = table.find_all("tr")
    screeners = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            screener_name = cells[0].text.strip()
            screener_link = cells[0].find("a").get("href")
            screeners.append([screener_name, screener_link])

    return screeners


def getScreenerItems(ext):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    url = "https://finance.yahoo.com"
    response = requests.get(url + ext, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find_all("table", {"class": "W(100%)"})[0]
    rows = table.find_all("tr")
    screener = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            screener.append(cells[0].text.strip())
    return screener


def getTrending():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    url = "https://finance.yahoo.com/trending-tickers"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    section = soup.find("section", {"id": "yfin-list"})
    rows = section.find_all("tr")
    trending = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            trending.append(cells[0].text.strip())
    return trending


def getSP500():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable"})
    rows = table.find_all("tr")[1:]
    symbols = []
    for row in rows:
        columns = row.find_all("td")
        symbol = columns[0].text.strip()
        symbols.append(symbol)
    return symbols


def printMenu():
    print("[0] Watchlists\n[1] Screeners\n[2] Trending")


def printOptions(list):
    for i, l in enumerate(list):
        print(f"[{i}] {l[0]}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        help="watchlist",
    )
    parser.add_argument(
        "-s",
        help="screener",
    )
    parser.add_argument(
        "-t",
        action="store_true",
        help="trending",
    )
    parser.add_argument(
        "-S",
        action="store_true",
        help="S&P 500",
    )
    args = parser.parse_args()
    return args


def main():
    if len(sys.argv) > 1:
        inputs = parse_args()
        if inputs.w:
            watchlists = getWatchlists()
            print(watchlists[int(inputs.w)][0])
            print(getWatchlistItems(watchlists[int(inputs.w)][1]))
        if inputs.s:
            screeners = getScreeners()
            print(screeners[int(inputs.s)][0])
            print(getScreenerItems(screeners[int(inputs.s)][1]))
        if inputs.t:
            print("Trending")
            print(getTrending())
        if inputs.S:
            print("S&P 500")
            print(getSP500())

    else:
        printMenu()
        choice = input("Select option: ")
        if choice == "0":
            watchlists = getWatchlists()
            printOptions(watchlists)
            choice = input("Select option: ")
            print(getWatchlistItems(watchlists[int(choice)][1]))
        elif choice == "1":
            screeners = getScreeners()
            printOptions(screeners)
            choice = input("Select option: ")
            print(getScreenerItems(screeners[int(choice)][1]))
        elif choice == "2":
            print(getTrending())


if __name__ == "__main__":
    main()
