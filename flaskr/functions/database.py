import mysql.connector
import config
import mysql.connector


def week_of_month(date_value):
    return date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1


def run_in_database(quary, fetch='no', commit='no'):
    try:
        conn = mysql.connector.connect(host=config.host, user=config.user,
                                       password=config.password, database=config.database)
        mycursor = conn.cursor()
        mycursor.execute(quary)
        result = True
        if fetch == 'yes':
            result = mycursor.fetchall()
        if commit == 'yes':
            conn.commit()
        mycursor.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        return False
