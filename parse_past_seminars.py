from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re


def is_valid_date(date_str, date_format="%d/%m/%Y"):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def parse_paper_info(paper_str):
    # Example: 'Roman Novak, et al., "Sensitivity and generalization in neural networks: an empirical study", ICLR 2018'
    authors = None
    title = None
    venue = None
    year = None

    # Split authors and the rest
    parts = [p.strip() for p in paper_str.split(',', 1)]
    if len(parts) >= 2:
        authors = parts[0]
        rest = parts[1]

        # Extract title (enclosed in quotes)
        title_match = re.search(r'"(.*?)"', rest)
        if title_match:
            title = title_match.group(1)
            remaining = rest.replace(title_match.group(0), '').strip()

            # Extract venue and year (e.g., "ICLR 2018")
            venue_year_parts = remaining.split()
            if len(venue_year_parts) >= 2:
                venue = ' '.join(venue_year_parts[:-1])
                year = venue_year_parts[-1]
            else:
                venue = remaining
        else:
            # No title in quotes, assume rest is venue and year
            venue_year_parts = rest.split()
            if len(venue_year_parts) >= 2:
                venue = ' '.join(venue_year_parts[:-1])
                year = venue_year_parts[-1]
            else:
                venue = rest
    else:
        # No comma, assume entire string is authors or venue
        authors = paper_str

    return authors, title, venue, year


# Load the HTML file
with open('public/past_seminars.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <tr> entries
entries = soup.find_all('tr')

data = []

for entry in entries:
    # Extract date
    date_tag = entry.find('td', class_='date')
    if date_tag:
        date_str = date_tag.get_text(strip=True)
        if not is_valid_date(date_str):
            continue
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        formatted_date = date_obj.strftime('%Y-%m-%d')
    else:
        formatted_date = None

    # Extract presenter
    name_tag = entry.find('td', class_='name')
    presenter = name_tag.get_text(strip=True) if name_tag else None

    # Extract paper info (third <td>)
    paper_tag = entry.find_all('td')[2]
    paper_str = paper_tag.get_text(strip=True) if paper_tag else None
    authors, title, venue, year = parse_paper_info(
        paper_str) if paper_str else (None, None, None, None)

    # Extract materials (optional)
    materials_tag = entry.find('a')
    materials = materials_tag['href'] if materials_tag else None

    data.append({
        'Date': formatted_date,
        'Presenter': presenter,
        'Authors': authors,
        'Title': title,
        'Venue': venue,
        'Year': year,
        'Materials': materials
    })

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('public/past_seminars.csv', index=False)
