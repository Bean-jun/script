import pymysql


try:
    import mysql_settings
except ImportError :
    pass


if __name__ == '__main__':
    try:
        client = pymysql.connect(host=mysql_settings.HOST,
                                user=mysql_settings.USER,
                                password=mysql_settings.PASSWORD,
                                database=mysql_settings.DATABASE,
                                charset='utf8')
    except NameError as e:
        print("数据库配置一下",e)
    
    else:
        cursor = client.cursor()

        cursor.execute("""select content from blog_note""")

        all_result = cursor.fetchall()
        number = 0
        for res in all_result:
            number += len(res[0])
        print(number)

        cursor.close()
        client.close()
