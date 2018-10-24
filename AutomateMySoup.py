import requests
from bs4 import BeautifulSoup
import time
import re

stat_type = {
    0 : 'passing',
    1 : 'rushing',
    2 : 'receiving',
    3 : 'scoring',
    4 : 'returning',
    5 : 'kicking',
    6 : 'defense',
}



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

for x in stat_type:

    num = 1
    url = 'http://www.espn.com/nfl/statistics/player/_/stat/{}/count/{}'.format(stat_type[x],num)

    print("Testing: {}".format(url))

    with open ('{}_stats.txt'.format(stat_type[x]), 'w') as r:
        r.write('Football {} Table\n'.format(stat_type[x]))

    response = requests.get(url, headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    number_of_stats = soup.find('div', class_='totalResults').text
    number_of_stats = int(re.search(r'\d+',number_of_stats).group())


    print("Preparing to Scrape {} results".format(number_of_stats))

    while num < number_of_stats:
        url = 'http://www.espn.com/nfl/statistics/player/_/stat/{}/count/{}'.format(stat_type[x],num)

        time.sleep(1)
        response = requests.get(url, headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            stat_table = soup.find_all('table', class_ = 'tablehead')
            if len(stat_table)<2:
                stat_table = stat_table[0]
                with open ('{}_stats.txt'.format(stat_type[x]),'a') as r:
                    for row in stat_table.find_all('tr'):
                        for cell in row.find_all('td'):
                            r.write(cell.text.ljust(35))
                        r.write('\n')
            else:
                print("Too many tables")
        else:
            print('No Response')
            print(num)



        num+=40
