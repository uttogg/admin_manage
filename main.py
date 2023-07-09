import sys

def input_plan_id():
    while True:
        plan_id = input("请输入要修改的套餐ID（输入0返回上一步）：")
        if plan_id == '0':
            return None
        elif plan_id.isdigit():
            return int(plan_id)
        else:
            print("无效的输入，请重新输入！")

def input_option():
    while True:
        option = input("请输入选项(1: 批量添加时间, 2: 指定用户添加时间, 3:清理僵尸号，输入0返回上一步)：")
        if option == '0':
            return None
        elif option in ['1', '2', '3']:
            return int(option)
        else:
            print("无效的选项，请重新输入！")

def input_days():
    while True:
        days = input("请输入要增加的天数（输入0返回上一步）：")
        if days == '0':
            return None
        elif days.isdigit():
            return int(days)
        else:
            print("无效的输入，请重新输入！")

# 让用户选择要执行的功能
while True:
    option = input("请输入要执行的功能(1: 批量添加时间, 2: 指定用户添加时间，3: 清理僵尸号，输入0退出)：")
    if option == '0':
        sys.exit(0)
    elif option == '1':
        import bulk_add_time
        plan_id = input_plan_id()
        if plan_id is None:
            continue
        days = input_days()
        if days is None:
            continue
        bulk_add_time.execute(plan_id, days)
    elif option == '2':
        import specify_user_add_time
        plan_id = input_plan_id()
        if plan_id is None:
            continue
        days = input_days()
        if days is None:
            continue
        specify_user_add_time.execute(plan_id, days)
    elif option == '3':
        import clean_zombie_accounts
        reg_date = input("请输入要清理的注册时间之前的日期（格式：yyyy/mm/dd）：")
        last_login_date = input("请输入最后登录时间之前的日期（格式：yyyy/mm/dd）：")
        clean_zombie_accounts.execute(reg_date, last_login_date)


    else:
        print("无效的选项，请重新输入！")
