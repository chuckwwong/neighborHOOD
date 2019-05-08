import json
import pymysql
connection = pymysql.connect(
                            host = 'localhost',
                            user = 'neighborhood_root',
                            password = 'neighborhood',
                            db = 'neighborhood_testdb')
try:
    with connection.cursor() as cursor:
        with open("crimetotal.json") as json_file:
            data = json.load(json_file)
            used = set()
            for crime in data["crimes"]:
                case_number = crime["unique_key"]
                address     = crime["block"]
                loc_desc    = crime["location_description"]
                ca          = crime["community_area"]
                date        = crime["date"]
                type        = crime["primary_type"]
                domestic    = crime["domestic"]
                #email       = "benpopo@police.com"
                lat         = crime["latitude"]
                long        = crime["longitude"]
                arrest      = crime["arrest"]
                #command = "insert into users_crime (case_number, location, location_desc, community_area, date, type_crime, domestic,  email_id, latitude, longitude) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                #cursor.execute(command, (case_number, address, loc_desc, ca, date, type, domestic, "benpopo@police.com", lat, long))
                command  = "insert into users_verify (case_number_id, arrested, email_id) values (%s, %s, %s)"
                cursor.execute(command, (case_number, arrest ,"benpopo@police.com"))
                connection.commit()

finally:
    connection.close()
