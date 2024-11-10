import requests
from collections import defaultdict
from bs4 import BeautifulSoup

def decode_message_from_url(doc_url):
    """
    Fetch and decode message from Google Docs URL.
    
    Args:
        doc_url: URL of the Google Doc containing the coordinate table
    """
    try:
        # Fetch content from URL
        response = requests.get(doc_url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find table data
        grid_by_row = defaultdict(dict)
        max_x = max_y = 0
        
        # Skip header row and process data rows
        rows = soup.find_all('tr')[1:]  # Skip header row
        for row in rows:
            # Extract cells from row
            cells = row.find_all('td')
            if len(cells) == 3:  # Ensure row has 3 columns
                try:
                    x = int(cells[0].text.strip())
                    char = cells[1].text.strip()
                    y = int(cells[2].text.strip())
                    
                    if char != '⬚':  # Only store filled positions
                        grid_by_row[y][x] = char
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {e}")
                    continue
        
        # Build and print grid
        for y in range(max_y + 1):
            row = ''
            for x in range(max_x + 1):
                row += grid_by_row[y].get(x, ' ')
            print(row)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching document: {e}")
    except Exception as e:
        print(f"Error processing document: {e}")

# Example usage
doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
decode_message_from_url(doc_url)