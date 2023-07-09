import pymysql
import yaml
from datetime import datetime
with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file)
def execute(reg_date, last_login_date):
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
            # 将日期字符串转换为 datetime 对象
            reg_datetime = datetime.strptime(reg_date, "%Y/%m/%d")
            last_login_datetime = datetime.strptime(last_login_date, "%Y/%m/%d")

            # 查询v2_user表中符合条件的僵尸号的email字段和数量
            zombie_email_query = "SELECT email FROM v2_user WHERE ((plan_id IS NULL AND t < {} AND created_at < {}) OR (plan_id IS NOT NULL AND expired_at < {} AND t < {} AND created_at < {}))".format(
                int(last_login_datetime.timestamp()), int(reg_datetime.timestamp()), int(datetime.now().timestamp()), int(last_login_datetime.timestamp()), int(reg_datetime.timestamp()))
            cursor.execute(zombie_email_query)
            zombie_emails = cursor.fetchall()

            zombie_count = len(zombie_emails)

            print("符合条件的僵尸号数量为：{}".format(zombie_count))

            with open("僵尸号.txt", "w") as file:
                for email in zombie_emails:
                    file.write(email[0] + "\n")

            print("符合条件的僵尸号的email字段已保存到僵尸号.txt文件中。")

            # 询问用户是否需要清理账号
            answer = input("是否需要清理这些僵尸账号？(y/n): ")
            if answer.lower() == 'y':
                # 清理账号的代码
                delete_query = "DELETE FROM v2_user WHERE email IN ({})".format(','.join(['"{}"'.format(email[0]) for email in zombie_emails]))
                cursor.execute(delete_query)
                conn.commit()
                print("僵尸账号已成功清理。")
            else:
                print("取消清理账号操作。")

        except pymysql.Error as e:
            print("操作出错: {}".format(e))
        finally:
            # 关闭游标对象和连接
            cursor.close()
            conn.close()
    else:
        print("连接失败！")

# 输入日期
reg_date = input("请输入要统计的注册时间之前的日期（格式：yyyy/mm/dd）：")
last_login_date = input("请输入要统计的最后登录时间之前的日期（格式：yyyy/mm/dd）：")

# 执行统计操作
execute(reg_date, last_login_date)
