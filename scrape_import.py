import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://tradestat.commerce.gov.in/ftpa/import_commodity_group_new'

session = requests.Session()

month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
year_list = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

for year in year_list:
    for month in month_list:
        
        response = session.get(url)
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            exit(1)

        soup = BeautifulSoup(response.text,'html.parser')
        if soup.find("html") is None:
            print("Invalid HTML received")
            exit(2)

        token = soup.find('input')
        token_value = token.get('value')
        if not token_value:
            print("CSRF token not found")
            exit(3)
        print(token_value)

        payload = {
            "_token": token_value,
            "IReportType": "2",
            "IMonth": month,
            "IYear": year,
            "IReport": "2"
        }
        response2 = session.post(
            url,
            data= payload
        )
        if not response2.ok:
            print(f"POST failed with status code {response2.status_code}")
            exit(4)
        else:
            print(f"Got response form server for {payload}")

        soup2 = BeautifulSoup(response2.text,'html.parser')
        if soup2.find("table") is None:
            print("No table found in response")
            exit(5)

        table_header = soup2.find_all('th')
        if not table_header:
            print("No table headers found")
            exit(6)

        header =[" ".join(head.get_text().split()) for head in table_header]
        header2 = header[2:]

        table_data_category = soup2.find_all('tr',style='font-weight: bold;')
        list_category =[]
        for row in table_data_category:
            cell = row.find_all('td')
            row_text = [''.join(cells.get_text().split())for cells in cell]
            if row_text:
                list_category.append(row_text)

        if not list_category:
            print("No category rows found")
            exit(7)

        df_category = pd.DataFrame(list_category,columns=header2)
        df_category['Commodity'] = df_category['Commodity'].str.lstrip('0123456789 ')

        table_data = soup2.find_all('td')
        if not table_data:
            print("No table data found")
            exit(8)

        list_new =[]
        current = []
        for rows in table_data:
            current.append(" ".join(rows.get_text().split()))
            if len(current)==5:
                list_new.append(current)
                current = []
        if current:
            list_new.append(current)

        df_detailed = pd.DataFrame(list_new,columns=header2)
        df_detailed['Commodity'] = df_detailed['Commodity'].str.lstrip('0123456789 ')
        df_detailed = df_detailed[~df_detailed['Commodity'].isin(df_category['Commodity'])].copy()
        
        filename = f"outputDetailed_{year}_{month}.csv"
        df_detailed.to_csv(filename,index=False)
        filename = f"outputCategory_{year}_{month}.csv"
        df_category.to_csv(filename,index=False)