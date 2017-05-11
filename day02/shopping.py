#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""By xuzhigui"""

import time


class MoneyException(Exception):
    pass


class ShopException(Exception):
    pass


def login_getmoney(username, password):
    with open('db', 'r') as f:
        users_info = f.readlines()
        for user_info in users_info:
            user_name = user_info.split('|')[0].strip()
            user_pass = user_info.split('|')[1].strip()
            all_money = user_info.split('|')[-1].strip()
            if username == user_name and password == user_pass:
                return True, int(all_money)
            else:
                return False, int(all_money)


def get_sales(pagesize="all"):
    with open('shopping_list', 'r') as f:
        if pagesize == "all":
            sales = [i for i in f.readlines() if i.strip()]
            return sales
        else:
            pagesize = int(pagesize)
            start = (pagesize - 1) * 10
            stop = pagesize * 10
            sales = [i for i in f.readlines() if i.strip()]
            sales = sales[start:stop]
            return sales


def gen_shopping_list(shop_sales):
    somedict = {}
    for sale in shop_sales:
        k = sale.split()[0].strip()
        v = [i.strip() for i in sale.split()]
        v.pop(0)
        somedict.update(dict([(k, v)]))
    return somedict


def check_is_shop_success(last_money, shop_num):
    try:
        shop_price = int(all_sales_shop[shop_num][1])
        if last_money >= shop_price:
            last_money -= shop_price
            return (last_money, True)
        else:
            raise MoneyException("money not enough !")
    except KeyError:
        raise ShopException("product not exist !")


def log(userName, msg):
    times = time.strftime("%Y-%m-%d %X", time.localtime())
    msg = "{0}----{1}----{2}\n".format(times, userName, msg)
    with open('./shopping_history.log', 'a+') as f:
        f.write(msg)

if __name__ == "__main__":
    print("\n欢迎使用购物系统！\n")
    username = input("请输入用户名: ")
    upasswd = input("请输入密码: ")
    money = login_getmoney(username, upasswd)
    money_wait_replace = money[1]
    if money[0]:
        tmp_sales = get_sales("all")
        all_sales_shop = gen_shopping_list(tmp_sales)
        already_shop = []
        print("\nWelcone Shopping, your money is", int(money[1]))
        user_result = input("\n购物请输入s 查询请输入 q, 其他退出: ")
        if user_result == "s":
            while True:
                pagenum = input("请输入你想看查看的商品的页码数: ")
                if pagenum.isdecimal() and int(pagenum) > 0:
                    sales = get_sales(pagenum)
                    if sales:
                        for sale in sales:
                            sale = ' '.join(sale.split())
                            print(sale.strip())
                        is_continue_brow = input("继续浏览其他页商品 ? (Y/N): ")
                        if is_continue_brow.strip().upper() == "Y":
                            continue
                        else:
                            break
                    else:
                        print("没有此页的商品")

            while True:
                shop_num = input("请输入你要购买的商品序号: ")
                try:
                    try:
                        money = money[1]
                    except TypeError:
                        money = money
                    money, status = check_is_shop_success(money, shop_num)
                    if status:
                        already_shop.append(all_sales_shop[shop_num][0])
                        log(username, all_sales_shop[shop_num][0])
                        print("恭喜，购买成功， 您购买的商品是: %s" % all_sales_shop[shop_num][0])
                        print("当前余额为 %s" % money)
                        is_continue_shop = input("是否需要继续购买 (Y/N): ")
                        if is_continue_shop.strip().upper() != "Y":
                            break
                except ShopException as e:
                    print("商品不存在，请重新输入商品序号")
                except MoneyException as e:
                    print("Money不够，请充值！")
                    break

            # 写回余额
            with open("db", 'r') as f:
                a = f.readlines()
                print(a)
                for i, c in enumerate(a):
                    if username in c:
                        a[i] = c.replace(str(money_wait_replace), str(money))

            with open('db', 'w') as f1:
                f1.truncate()
                f1.writelines(a)

        elif user_result == "q":
            keywords = input("请输入你要查询的关键字, 输入all查看之前购买的所有商品: ")
            with open("./shopping_history.log", 'rU') as f:
                all = f.readlines()
                if keywords.strip().upper() == "ALL":
                    results = []
                    for i in all:
                        if username in i:
                            print(i.strip())
                            results.append(i.strip())
                    if len(results):
                        print("历史购买记录中找到 %s 个记录" % len(results))
                        for result in results:
                            print(result.strip())
                    else:
                        print("在你已购买的商品列表中没有找到你想要搜索的商品")

                else:
                    results = []
                    for one in all:
                        if keywords in one and username in one:
                            results.append(one.strip())

                    if results:
                        print("历史购买记录中找到 %s 个记录" % len(results))
                        for result in results:
                            print(result.strip())
                    else:
                        print("在你已购买的商品列表中没有找到你想搜索的商品")
        else:
            print("\nGoodBye !!!")
            exit(0)
    else:
        print("登录失败")
