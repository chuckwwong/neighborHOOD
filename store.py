import json
import pymysql
connection = pymysql.connect(
                            host = 'localhost',
                            user = '//root//',
                            password = '//cs411//',
                            db = '//testmysql//')
try:
    with connection.cursor() as cursor:
        with open("crimetotal.json") as json_file:
            data = json.load(json_file)
            for crime in data["crimes"]:
                case_number = crime["case_number"]
                address     = crime["block"]
                ca          = crime["community_area"]
                date        = crime["date"]
                type        = crime["primary_type"]
                arrested   = crime["arrest"]
                command = "insert into //tablename// (case_number, address, community_area, date, type, arrested, verified, email) values (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(command, (case_number, address, ca, date, type, arrested, "True", "Null"))
                connection.commit()

finally:
    connection.close()
