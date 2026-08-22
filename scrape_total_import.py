import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
url = 'https://tradestat.commerce.gov.in/ftpa/import_commodity_group_new'

session = requests.Session()

month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
year_list = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
list_total =[]
list_total_col=[]
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

        table_data_category = soup2.find_all('tr')
        list_category =[]
        for row in table_data_category:
            cell = row.find_all('td')
            #row_text = [''.join(cells.get_text().split())for cells in cell]
            #Since at line 87 we have use " " and not '' causes some commodity groups to be still there in the detailed csv
            row_text = [" ".join(cells.get_text().split())for cells in cell]
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

        df_total = df_category[df_category["Commodity"].str.contains("total", case=False, na=False)]
        for col in df_total.columns:
            if re.search(r'\d{4}', str(col)):
                value = pd.to_numeric(
                    df_total[col].str.replace(",", "", regex=False)
                ).iloc[0]

                list_total.append(value)
                list_total_col.append(col)

df_final = pd.DataFrame({
    "Value": list_total,
    "Column_Name": list_total_col
})
df_final = df_final.drop_duplicates(subset="Column_Name", keep="first")
df_final["Value"] = df_final["Value"].fillna(0.0)
filename = f"2total_import_outputCategory.csv"
df_final.to_csv(filename,index=False)