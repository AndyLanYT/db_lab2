import psycopg2
import csv
import time
import os


def validMark(string):
    if string != 'null' and string is not None:
        return float(string.replace(',', '.'))

def insert(tablename, cols, count):
    cols = str(cols).replace('\'', '')
    values = '%s' + ''.join([', %s' for _ in range(count-1)])
    return f'INSERT INTO {tablename} {cols} VALUES ({values}) ON CONFLICT DO NOTHING'


ZNO2019 = 'Odata2019File.csv'
ZNO2020 = 'Odata2020File.csv'

TABLES = ['tbl_regions', 'tbl_educationOrganizations', 'tbl_test', 'tbl_students', 'tbl_students_tests']


query = '''
SELECT data2019.EORegName, data2019.max2019, data2020.max2020
FROM
  (SELECT EORegName, MAX(testMark100) AS max2019
  FROM tbl_test
    INNER JOIN tbl_educationOrganizations ON tbl_test.EOName = tbl_educationOrganizations.EOName
    INNER JOIN tbl_students_tests ON tbl_test.testID = tbl_students_tests.testID
  WHERE year = 2019
  GROUP BY EORegName) AS data2019,
  (SELECT EORegName, MAX(testMark100) AS max2020
  FROM tbl_test
    INNER JOIN tbl_educationOrganizations ON tbl_test.EOName = tbl_educationOrganizations.EOName
    INNER JOIN tbl_students_tests ON tbl_test.testID = tbl_students_tests.testID
  WHERE year = 2020
  GROUP BY EORegName) AS data2020
WHERE data2019.EORegName = data2020.EORegName
'''


tries = 5
while tries:
    try:
        conn = psycopg2.connect(dbname='znodata', user='postgres', password='password', host='db', port='5432')

        print('Connected!!')

        with conn:
            cur = conn.cursor()

            # for tablename in TABLES:
                # cur.execute(f'DROP TABLE IF EXISTS {tablename} CASCADE')

            print('Tables were created!')

            for tablename in TABLES:
                cur.execute(f'ALTER TABLE {tablename} DISABLE TRIGGER ALL')

            cur.execute('SELECT COUNT(studentID) FROM tbl_students_tests WHERE year=2019')
            count = cur.fetchone()[0]

            print(count)

            start = time.time()

            with open(ZNO2019, 'r', encoding='windows-1251') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                headers = next(reader)

                # tbl_test
                testName = headers.index('engTest')
                testMark100 = headers.index('engBall100')
                testMark12 = headers.index('engBall12')
                testStatus = headers.index('engTestStatus')
                EONameTest = headers.index('engPTName')

                # tbl_regions
                regName = headers.index('REGNAME')
                areaName = headers.index('AREANAME')
                terTypeName = headers.index('TerTypeName')

                # tbl_educationOrganizations
                EOName = headers.index('EONAME')
                EOTypeName = headers.index('EOTYPENAME')
                EORegName = headers.index('EORegName')
                EOAreaName = headers.index('EOAreaName')

                # tbl_students
                outID = headers.index('OUTID')
                birth = headers.index('Birth')
                sexTypeName = headers.index('SEXTYPENAME')
                
                # tbl_students_tests
                year = 2019


                while count != 0:
                    row = next(reader)
                    if row[testName] == 'Англійська мова':
                        count -= 1
                
                for idx, row in enumerate(reader):
                    if row[testName] == 'Англійська мова':
                        cur.execute(insert('tbl_regions',
                                          ('regName',    'areaName',    'terTypeName'), 3),
                                          (row[regName], row[areaName], row[terTypeName]))
                        
                        cur.execute(insert('tbl_educationOrganizations',
                                          ('EOName',    'EOTypeName',    'EORegName',    'EOAreaName'), 4),
                                          (row[EOName], row[EOTypeName], row[EORegName], row[EOAreaName]))
                        
                        cur.execute(insert('tbl_test',
                                          ('testName',    'testMark100',               'testMark12',               'testStatus',    'EOName'), 5),
                                          (row[testName], validMark(row[testMark100]), validMark(row[testMark12]), row[testStatus], row[EONameTest]))
                        
                        cur.execute(insert('tbl_students',
                                          ('outID',    'birth',    'sexTypeName',    'EOName'), 4),
                                          (row[outID], row[birth], row[sexTypeName], row[EOName]))
                        
                        cur.execute('SELECT MAX(testID) FROM tbl_test')
                        testID = cur.fetchone()[0]

                        cur.execute(insert('tbl_students_tests',
                                          ('studentID', 'testID', 'year'), 3),
                                          (row[outID],  testID,    year))
                    
                    if idx % 10000 == 0:
                        conn.commit()
                
                conn.commit()

            cur.execute('SELECT COUNT(studentID) FROM tbl_students_tests WHERE year=2020')
            count = cur.fetchone()[0]

            print(count)
	    
            with open(ZNO2020, 'r', encoding='windows-1251') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                headers = next(reader)
                
                # tbl_test
                testName = headers.index('engTest')
                testMark100 = headers.index('engBall100')
                testMark12 = headers.index('engBall12')
                testStatus = headers.index('engTestStatus')
                EONameTest = headers.index('engPTName')

                # tbl_regions
                regName = headers.index('REGNAME')
                areaName = headers.index('AREANAME')
                terTypeName = headers.index('TerTypeName')

                # tbl_educationOrganizations
                EOName = headers.index('EONAME')
                EOTypeName = headers.index('EOTYPENAME')
                EORegName = headers.index('EORegName')
                EOAreaName = headers.index('EOAreaName')

                # tbl_students
                outID = headers.index('OUTID')
                birth = headers.index('Birth')
                sexTypeName = headers.index('SEXTYPENAME')
                
                # tbl_students_tests
                year = 2020


                while count != 0:
                    row = next(reader)
                    if row[testName] == 'Англійська мова':
                        count -= 1
                
                for idx, row in enumerate(reader):
                    if row[testName] == 'Англійська мова':
                        cur.execute(insert('tbl_regions',
                                          ('regName',    'areaName',    'terTypeName'), 3),
                                          (row[regName], row[areaName], row[terTypeName]))
                        
                        cur.execute(insert('tbl_educationOrganizations',
                                          ('EOName',    'EOTypeName',    'EORegName',    'EOAreaName'), 4),
                                          (row[EOName], row[EOTypeName], row[EORegName], row[EOAreaName]))
                        
                        cur.execute(insert('tbl_test',
                                          ('testName',    'testMark100',          'testMark12',         'testStatus', 'EOName'), 5),
                                          (row[testName], validMark(row[testMark100]), validMark(row[testMark12]), row[testStatus], row[EONameTest]))
                        
                        cur.execute(insert('tbl_students',
                                          ('outID',    'birth',    'sexTypeName',    'EOName'), 4),
                                          (row[outID], row[birth], row[sexTypeName], row[EOName]))
                        
                        cur.execute('SELECT MAX(testID) FROM tbl_test')
                        testID = cur.fetchone()[0]

                        cur.execute(insert('tbl_students_tests',
                                          ('studentID', 'testID', 'year'), 3),
                                          (row[outID],  testID,    year))
            
                    if idx % 10000 == 0:
                        conn.commit()
                
                conn.commit()
            
            print('All data successfuly inserted')
        
            for tablename in TABLES:
                cur.execute(f'ALTER TABLE {tablename} ENABLE TRIGGER ALL')

        print('Creating migration file!!')

        for idx, tablename in enumerate(TABLES):
            os.system(f'pg_dump --column-inserts --data-only --table={tablename} -h db -p 5432 -U postgres -F p znodata > flyway/sql/V2.{idx+1}__insert_into_{tablename}.sql')

        # os.system('pg_dump "host=db port=5432 dbname=znodata user=postgres password=password" > V1__data_2019_2020.sql')

        print(f'Execution time: {time.time() - start}')


        cur.execute(query)

        with open('ZNOdata.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([col[0] for col in cur.description])

            for row in cur:
                writer.writerow([str(el) for el in row])
        
        print('Created file ZNOdata.csv with statistics')
        
        tries = 0
    
    except psycopg2.OperationalError as err:
        tries -= 1
        print('OperationalError')
        # print(err)
        time.sleep(1.5)
    
    except FileNotFoundError as err:
        tries = 0
        print('FileNotFoundError')
        # print(f'File {err.filename} does not exist')
