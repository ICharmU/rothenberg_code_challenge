from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import os
from bs4 import BeautifulSoup
import json

download_dir = Path("data")
download_fp = os.path.join(download_dir, "data.json")

if not os.path.exists(download_dir):
    os.makedirs(download_dir)


# specify driver version, otherwise program can't requires path variables.
options = webdriver.ChromeOptions()
options.browser_version = "145.0.7632.76" 

driver = webdriver.Chrome(options=options)

financials_url = r"https://data.sec.gov/api/xbrl/companyfacts/CIK0000055785.json"
driver.get(financials_url)
raw_html = driver.page_source
driver.quit()

if "pre" not in raw_html:
    raise Exception("HTML not fully loaded. It is recommended to wait longer before the page loads.")

soup = BeautifulSoup(raw_html, features="html.parser")
json_string = soup.find("pre").text

data_dict = json.loads(json_string)
with open(Path("data") / "CIK0000055785.json", "w") as f:
    json.dump(data_dict, f)
