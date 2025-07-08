import pymysql
import pandas as pd
import sys

def sql(first_name, last_name):
    timeout = 10
    connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="banking",
    host="127.0.0.1",
    password="Dsci-551",
    read_timeout=timeout,
    port=3306,
    user="root",
    write_timeout=timeout,
    )
    cursor = connection.cursor()

    script = f"""select a.AccountID, AccountType, Balance from accounts a left join 
    (select CustomerID, FirstName, LastName from customers where FirstName = \'{first_name}\' and LastName = \'{last_name}\') as c
    on a.CustomerID = c.CustomerID
    where c.CustomerID is not null"""
    cursor.execute(script)
    df = pd.DataFrame(cursor.fetchall())
    arr =  df.to_numpy()
    result = "\n".join([",".join(list(map(lambda x: str(x), arr[i, :]))) for i in range(arr.shape[0])])
    cursor.close()
    connection.close()
    return result

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: python search_customer.py <first name> <last name>")
        sys.exit(1)

    first_name = sys.argv[1]
    last_name = sys.argv[2]
    print(sql(first_name, last_name))