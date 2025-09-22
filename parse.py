import requests
from bs4 import BeautifulSoup
import zlib
from private import connection, cursor

def getSchedule(html) -> list[list[str]]:
    
    html = zlib.decompress(page['schedule']).decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')

    matrix = []
    y = 0

    for row in rows:
        cells = row.find_all('td')
        x = 0

        for cell in cells:
            rowspan = int(cell.get('rowspan', 1))
            colspan = int(cell.get('colspan', 1))

            while y < len(matrix) and x < len(matrix[y]) and matrix[y][x]:
                x += 1
            for dy in range(rowspan):
                rowY = y + dy
                while len(matrix) <= rowY:
                    matrix.append([])
                while len(matrix[rowY]) <= x + colspan - 1:
                    matrix[rowY].append(None)

                for dx in range(colspan):
                    matrix[rowY][x + dx] = cell

            x += colspan
        y += 1
    return matrix

cursor.execute("SELECT schedule FROM PageData")
page = cursor.fetchone()
if page: matrix = getSchedule(page['schedule'])


def getDate():
    global matrix
    
    months = {
        "янв": "01",
        "фев": "02",
        "мар": "03",
        "апр": "04",
        "мая": "05",
        "июн": "06",
        "июл": "07",
        "авг": "08",
        "сен": "09",
        "окт": "10",
        "ноя": "11",
        "дек": "12",
    }
    
    if matrix: return f"{matrix[0][0].text.split()[-1].split("(")[1].split(")")[0].capitalize()} {matrix[0][0].text.split()[1]}.{months[matrix[0][0].text.split()[2][0:3]]}:{matrix[0][0].text.split()[3]}"
print(getDate())

def getScheduleForStudents(group: str) -> list:
    global matrix
    group = group.upper()
    times, lessons, rooms = [], [], []
    if matrix:
        for row in range(len(matrix)):
            for cell in range(len(matrix[row])):
                if matrix[row][cell].text == group:
                    for i in matrix[row: row + 11]:
                        times.append(i[0].text)
                        lessons.append(i[cell].text)
                        rooms.append(i[cell + 1].text)
                        
    return [times, lessons, rooms]    
               


                
    
    


   


