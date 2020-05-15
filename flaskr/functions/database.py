import mysql.connector
from datetime import datetime
import config
import mysql.connector
import pandas as pd
# from application import login_manager


# @login_manager.user_loader()
# def load_user(user_id):
#     query = "SELECT `user_id`, `fname`,`email`FROM `users` WHERE `user_id` LIKE {};".format(user_id)
#     result = run_in_database(quary=query, fetch='yes')
#     return False


def check_email_in_databace(email):
    query = "SELECT * FROM `users` WHERE `users`.`email` LIKE '{}';".format(email)
    result = run_in_database(quary=query, fetch='yes')
    if result:
        return result[0][1], result[0][5]  # returns firs name and email address.
    else:
        return False, False


def week_of_month(date_value):
    return date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1


def dashboard_bargraph_data(user_id, month=None, credit=False):
    if month:
        month_filter = "AND MONTH(date) LIKE {}".format(datetime.strptime(month, '%B').month)
    else:
        month_filter = " "

    if credit:
        credit_filter = "AND credit_debit_id LIKE {}".format(2)
    else:
        credit_filter = "AND credit_debit_id LIKE {}".format(1)
    quary = """SELECT 
    `expences`.`date`,DAY(`expences`.`date`), SUM(`expences`.`amount`) 
    FROM `expences` 
    WHERE `expences`.`user_id` LIKE {} {} {}
    GROUP BY `expences`.`date`
    ORDER BY DAY(`expences`.`date`) ASC""".format(user_id, credit_filter, month_filter)

    try:
        conn = mysql.connector.connect(host=config.host, user=config.user,
                                       password=config.password, database=config.database)
        mycursor = conn.cursor()
        mycursor.execute(quary)
        result = mycursor.fetchall()
        result = pd.DataFrame(result)
        result.columns = ["Date", "Date_n", "Amount"]
        amount_col = result["Amount"]
        com = [amount_col[0]]
        for i in range(1, len(amount_col)):
            com.append(com[-1] + amount_col[i])
        result["Amount_comm"] = com
        result["Week Name"] = list(map(week_of_month, result["Date"]))
        result["day"] = [x.strftime('%A') for x in result["Date"]]
        return result
    except Exception as e:
        print(e)
        return None


# print(dashboard_bargraph_data(5, month="March"))

def get_pie_chat_data():
    query = """SELECT `type`.`type`, SUM(`expences`.`amount`) 
    FROM `expences` 
    JOIN `type` ON
     `expences`.`type_id` = `type`.`type_id` 
     WHERE `expences`.`user_id` LIKE 5 AND credit_debit_id LIKE 2 AND MONTH(date) LIKE 3 
     GROUP BY `expences`.`type_id`"""
    try:
        conn = mysql.connector.connect(host=config.host, user=config.user,
                                       password=config.password, database=config.database)
        mycursor = conn.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = pd.DataFrame(result)
        result.columns = ["type", "Amount"]
        return result
    except Exception as e:
        print(e)
        return None


def get_pie_chat_data_subtype():
    query = """SELECT `sub_type`.`subtype`, SUM(`expences`.`amount`) 
    FROM `expences` 
    JOIN `sub_type` ON
     `expences`.`sub_type_id` = `sub_type`.`sub_type_id` 
     WHERE `expences`.`user_id` LIKE 5 AND credit_debit_id LIKE 2 AND MONTH(date) LIKE 3 AND `expences`.`type_id` LIKE 3
     GROUP BY `expences`.`sub_type_id`"""
    try:
        conn = mysql.connector.connect(host=config.host, user=config.user,
                                       password=config.password, database=config.database)
        mycursor = conn.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
        result = pd.DataFrame(result)
        result.columns = ["type", "Amount"]
        return result
    except Exception as e:
        print(e)
        return None


def get_savings_data():
    query_expense = """SELECT YEAR(`expences`.`date`) as SalesYear,
        MONTH(`expences`.`date`) as SalesMonth,
        SUM(`expences`.`amount`) AS TotalSales
        FROM `expences`
        WHERE `expences`.`user_id` LIKE  5 AND `expences`.`credit_debit_id` LIKE 2
        GROUP BY YEAR(`expences`.`date`), MONTH(`expences`.`date`)
        ORDER BY YEAR(`expences`.`date`), MONTH(`expences`.`date`)"""
    query_income = """SELECT YEAR(`expences`.`date`) as SalesYear,
        MONTH(`expences`.`date`) as SalesMonth,
        SUM(`expences`.`amount`) AS TotalSales
        FROM `expences`
        WHERE `expences`.`user_id` LIKE  5 AND `expences`.`credit_debit_id` LIKE 1
        GROUP BY YEAR(`expences`.`date`), MONTH(`expences`.`date`)
        ORDER BY YEAR(`expences`.`date`), MONTH(`expences`.`date`)"""
    # try:
    conn = mysql.connector.connect(host=config.host, user=config.user,
                                   password=config.password, database=config.database)
    mycursor = conn.cursor()
    mycursor.execute(query_expense)
    result_expense = pd.DataFrame(mycursor.fetchall())
    print(result_expense)
    mycursor.execute(query_income)
    result_income = pd.DataFrame(mycursor.fetchall())
    # result_income["date"] = result_income[[0, 1]].apply(lambda x: '-'.join(x), axis=1)
    print(result_income)
    result_income[2] = result_income[2] - result_expense[2]
    # df['period'] = df[['Year', 'quarter']].apply(lambda x: ''.join(x), axis=1)
    return result_income
    # except Exception as e:
    #     print(e)
    #     return None


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
