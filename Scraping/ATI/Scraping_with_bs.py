# Importing html getter, parser, and Kerberos authenticator
import requests
from bs4 import BeautifulSoup #parser
from requests_kerberos import HTTPKerberosAuth #OUR LORD AND SAVIOR KERBEROS

# Requesting access with KERBEROS authentication to web page
url = 'http://info.ati-ia.com/Inventive/Products/ViewRoutingSteps.aspx?ItemID=9120-011T-A15-000'
response = requests.get(url, auth=HTTPKerberosAuth())
# print(response) #response Status Code (200 = good, 4XX = client error response, 5XX = server error response)

# Parsing html and getting table from the page
soup = BeautifulSoup(response.content, 'html.parser')
stat_table = soup.find_all('table', id="ctl00_ContentPlaceHolder1_Routing_Steps1_gvRouting")
# print(type(stat_table)) #class should be bs4.element.ResultSet
# print(len(stat_table))  #should be non-zero
stat_table = stat_table[0]  #extracting table from ResultSet format
# print(type(stat_table)) #class should be bs4.element.Tag

with open('RoutingSteps.txt', 'w') as r:
    for row in stat_table.find_all('tr'):
        for bell in row.find_all('th'):
            r.write(bell.text.ljust(50))
        for cell in row.find_all('td'):
            r.write(cell.text.ljust(50))
        r.write('\n')