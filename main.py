from typing import Optional
from bs4 import BeautifulSoup
import csv
import requests

import requests 

from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust this for production to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/scrape")
# def read_item(url: Optional[str] = None):
async def root(scrape_url: Optional[str] = None):
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    head = []
    rows = []
    def scrape_page(soup):
        rows_ele = soup.find_all('tr')
        for row in rows_ele:
            td = row.find_all('td')  # Find all <td> elements in the current row
            th = row.find_all('th')  # Find all <th> elements in the current row

            arr = []
            for cell in td:
                cell_text = cell.get_text(strip=True)
                arr.append(cell_text)
            rows.append(arr)

            for cell in th:
                head.append(cell.get_text(strip=True))
            

    # url = 'https://results.eci.gov.in/AcResultGenOct2024/partywisewinresult-834U08.htm'
    
    headers = {
        'User-Agent': 'curl/7.68.0'  # or the user agent used by curl
    }
    
    response = requests.get(scrape_url, verify=False, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print('page', soup) 
    scrape_page(soup)

    return {"message": "hello world", "columns": head, "rows": rows}