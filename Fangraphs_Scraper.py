#Make sure to install the libraries if you haven't already:
#bash
#pip install beautifulsoup4
#pip install pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.fangraphs.com/leaders/major-league?pos=all&stats=pit&type=8"

request_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Make te request
response = requests.get(url, headers=request_headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    
    # Create an array to save the stats
    stats = []

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the pitcher information
    div = soup.find('div', {'class': 'table-scroll'})
    
    table = div.find_next("table")

    tbody = div.find_next("tbody")
    
    # Iterate through each row in the table
    for row in tbody.find_all('tr'):
        
        # Extract pitcher details: name, team, ERA, FIP, and WAR
        rank = row.find('td', {'class': 'fixed'}).get_text()
        pitcher_name = row.find('td', {'data-col-id': 'Name'}).get_text()
        team = row.find('td', {'data-col-id': 'Team'}).get_text()
        era = row.find('td', {'data-col-id': 'ERA'}).get_text()
        fip = row.find('td', {'data-col-id': 'FIP'}).get_text()
        war = row.find('td', {'data-col-id': 'WAR'}).get_text()

        # Save the data inside the array
        stats.append([rank,
                     pitcher_name,
                     era,
                     fip,
                     war
        ])

        # Print the extracted information (for debugging purposes)
        #print(f'{rank}. {pitcher_name} - Team: {team}, ERA: {era}, FIP: {fip}, WAR: {war}')
else:
    print(f"Failed to retrieve the page. Status Code:", {response.status_code})


# Create the dataframe for the stats
df = pd.DataFrame(stats, columns=['rank', 'pitcher_name', 'era', 'fip', 'war'])

# Print the dataframe with the data
print(df)