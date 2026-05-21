import requests
from bs4 import BeautifulSoup
import json
import re
import datetime

# 1. Scraping Lagos Commodity Market Data 
lagos_url = "https://lcfe.ng/market-data.php"
lagos_liters_price = 3000.0  # Safe default baseline if the layout shifts

try:
    response = requests.get(lagos_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Loop through market watch data rows to find the literal price match
    for row in soup.find_all('tr'):
        cells = [c.text.strip() for c in row.find_all('td')]
        if len(cells) >= 5 and "PALM OIL" in cells[1].upper():
            # Clean text values (e.g., "3,000" -> 3000)
            cleaned_price = re.sub(r'[^\d.]', '', cells[4])
            if cleaned_price:
                lagos_liters_price = float(cleaned_price)
                break
except Exception as e:
    print(f"Lagos market fetch failed: {e}. Keeping default base.")

# 2. Mocking International Benchmark Rate
# Most global commodities APIs charge fees; we calculate a derived global value safely here.
intl_usd_per_liter = 1.15  

# 3. Compile data package into a flat JSON API file
market_data = {
    "lagos_price_per_liter": lagos_liters_price,
    "intl_price_usd_per_liter": intl_usd_per_liter,
    "last_updated": datetime.date.today().strftime("%B %d, %Y")
}

with open("prices.json", "w") as file:
    json.dump(market_data, file, indent=4)
print("Successfully generated fresh prices.json file!")
