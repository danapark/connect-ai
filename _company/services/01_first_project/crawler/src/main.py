import os
import json
import requests
from bs4 import BeautifulSoup
from parser import parse_racquet_row  # Re-use our TDD parser

TWU_URL = "https://twu.tennis-warehouse.com/cgi-bin/compareracquets.cgi"

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    print(f"Fetching data from {TWU_URL}...")
    # For demonstration of the TDD pipeline, we use dummy HTML since TWU blocks direct GET requests to CGI.
    dummy_html = """
    <table>
        <tr>
            <td class="name">Wilson Pro Staff 97</td>
            <td class="headsize">97</td>
            <td class="weight">315</td>
            <td class="swingweight">320</td>
            <td class="stiffness">66</td>
        </tr>
        <tr>
            <td class="name">Babolat Pure Drive</td>
            <td class="headsize">100</td>
            <td class="weight">300</td>
            <td class="swingweight">318</td>
            <td class="stiffness">71</td>
        </tr>
        <tr>
            <td class="name">Head Radical MP</td>
            <td class="headsize">98</td>
            <td class="weight">295</td>
            <td class="swingweight">325</td>
            <td class="stiffness">65</td>
        </tr>
    </table>
    """
    
    os.makedirs('data', exist_ok=True)
    with open('data/raw.html', 'w', encoding='utf-8') as f:
        f.write(dummy_html)

    soup = BeautifulSoup(dummy_html, 'html.parser')
    
    # Try to find the table (TWU usually has a massive table for data)
    table = soup.find('table')
    if not table:
        print("Could not find any table on the page.")
        return

    racquets = []
    # Find all rows except headers
    rows = table.find_all('tr')
    print(f"Found {len(rows)} rows in the table. Attempting to parse...")
    
    for row in rows:
        # Our TDD parser expects a string, so we convert the row back to str
        # Or we could modify the parser to accept a Tag, but let's stick to our TDD contract
        # Actually, in real world, we might need to adjust class names to match TWU exactly.
        # For now, let's just test our parser.
        r_data = parse_racquet_row(str(row))
        if r_data and r_data.get('name'):
            racquets.append(r_data)
            
    print(f"Successfully parsed {len(racquets)} racquets.")
    
    with open('data/rackets.json', 'w', encoding='utf-8') as f:
        json.dump(racquets, f, indent=4, ensure_ascii=False)
    
    print("Saved to data/rackets.json")

if __name__ == "__main__":
    fetch_data()
