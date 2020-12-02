
import cx_Oracle

db=cx_Oracle.connect("yourOracleAddress")
cursor = db.cursor()

sql = "select * from laptop"
cursor.execute(sql) #laptopOS의 이름이 너무 길다 maximum:20

for row in cursor:
    for i in range(len(row)):
        #if i==3:
            #if(row[3] != None):
                #description = row[3].read()
        print(row[i],end="  ")
    print()

cursor.close()
db.close()