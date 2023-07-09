import pymysql
import yaml
with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file)
def execute(plan_id, days):
    # 连接到数据库
    conn = pymysql.connect(
        host=config_data['ip'],
        port=config_data['port'],
        user=config_data['user'],
        password=config_data['password'],
        database=config_data['database']
    )

    # 检查连接是否成功
    if conn is not None:
        print("连接成功！")
        # 创建游标对象
        cursor = conn.cursor()
        try:
            # 让用户输入要修改的用户邮箱
            email = input("请输入要修改的用户邮箱：")

            # 查询v2_user表中符合条件的记录数量
            count_query = f"SELECT COUNT(*) FROM v2_user WHERE plan_id = {plan_id} AND email = '{email}' AND expired_at > UNIX_TIMESTAMP()"
            cursor.execute(count_query)
            count_result = cursor.fetchone()
            user_count = count_result[0]
            print(f"符合条件且未过期的用户数量为: {user_count}")

            # 更新v2_user表中符合条件的记录的过期时间
            update_query = f"UPDATE v2_user SET expired_at = expired_at + {days * 86400} WHERE plan_id = {plan_id} AND email = '{email}' AND expired_at > UNIX_TIMESTAMP()"
            cursor.execute(update_query)
            conn.commit()
            print(f"已成功给用户 {email} 增加 {days} 天时间")

        except pymysql.Error as e:
            print(f"操作出错: {e}")
        finally:
            # 关闭游标对象和连接
            cursor.close()
            conn.close()
    else:
        print("连接失败！")
