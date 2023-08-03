# Web Scraper for TruyenFull.vn
This is a Python script for web scraping the website TruyenFull.vn to retrieve information on a specified number of pages of completed novels. The script utilizes the aiohttp and bs4 libraries to asynchronously request and parse the HTML content of each page. The retrieved information is then saved to an Excel file using the pandas library.

## How to Use


```
1. Clone the repository:
> git clone https://github.com/Tuanpluss02/Crawl-truyenfull.git

2. Change into the project directory:
> cd Crawl-truyenfull

3. Create a virtual environment:
> py -m venv venv

4. Activate the virtual environment:
> source venv/bin/activate (Linux)
> venv\Scripts\activate (Windows)

5. Install dependencies:
> pip install -r requirements.txt

6. Run the script:
> py main.py
```

Then input the number of pages of completed novels that you would like to retrieve information for.
The script will output a progress bar for each page being scraped and will save the results to an Excel file in the `output` folder.

**Note**: The script may take some time to complete depending on the number of pages being scraped. Additionally, the website may block your IP address if too many requests are made in a short period of time. To avoid this, the script has a delay of 1 second after every 50 pages scraped.
