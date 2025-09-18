import requests
from bs4 import BeautifulSoup

def getSchedule(url: str, response):
    # try:
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text

            soup = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
            table = soup.find('table')
            rows = table.find_all('tr')

            matrix = []

            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = []
                for cell in cells:
                    # rowspan = int(cell.get('rowspan', 1))
                    colspan = int(cell.get('colspan', 1))
                    for _ in range(colspan):
                        row_data.append(cell)
                matrix.append(row_data)

            return matrix
    # except Exception as e:
    #     print(f"Ошибка: {e}")
    #     return []

# def getDate():
#     matrix = getSchedule("https://www.vgtk.by/schedule/lessons/day-tomorrow.php")
#     year = matrix[0][0].get_text().split()[-1]
#     months
#     return date

# print(getDate())


