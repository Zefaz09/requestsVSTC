import requests
from bs4 import BeautifulSoup
import zlib
from private import connection, cursor

def getSchedule(html) -> list[list[str]]:
    
    soup = BeautifulSoup(zlib.decompress(html), 'html.parser')
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

def getScheduleForStudents(group: str) -> list:
    group = group.upper()
    cursor.execute("SELECT schedule FROM PageData")
    schedule = cursor.fetchone()
    times, lessons, rooms = [], [], []
    if schedule:
        page = getSchedule(schedule['schedule'])
        for row in range(len(page)):
            for cell in range(len(page[row])):
                if page[row][cell].text == group:
                    for i in page[row: row + 11]:
                        times.append(i[0].text)
                        lessons.append(i[cell].text)
                        rooms.append(i[cell + 1].text)
                        
    return [times, lessons, rooms]    
               


                
    
    


   


