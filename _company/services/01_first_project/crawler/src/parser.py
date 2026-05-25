from bs4 import BeautifulSoup

def parse_racquet_row(html_row: str) -> dict:
    soup = BeautifulSoup(html_row, 'html.parser')
    row = soup.find('tr')
    
    if not row:
        return {}

    def extract_int_or_none(class_name):
        td = row.find('td', class_=class_name)
        if td and td.text.strip() and td.text.strip().isdigit():
            return int(td.text.strip())
        return None

    name_td = row.find('td', class_='name')
    name = name_td.text.strip() if name_td else None

    return {
        "name": name,
        "headsize": extract_int_or_none('headsize'),
        "weight": extract_int_or_none('weight'),
        "swingweight": extract_int_or_none('swingweight'),
        "stiffness": extract_int_or_none('stiffness')
    }
