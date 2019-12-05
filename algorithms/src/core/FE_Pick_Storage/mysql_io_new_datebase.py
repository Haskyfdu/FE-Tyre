import pymysql
import json


def sql_rule_scope(sql):
    con = pymysql.connect(
        host='106.75.233.19',
        port=3307,
        user='aifuyi',
        passwd='1qaz2wsx',
        db='mw_transport'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    rule_scope_dict = []    # 新建空字典
    while True:
        rule_scope = cur.fetchone()  # 获取一条数据 元组转列表
        if not rule_scope:
            break  # 如果抓取的数据为None,退出循环
        if rule_scope[5] is None:
            prov = '无'
        else:
            prov = rule_scope[5]
        if rule_scope[6] is None:
            city = '无'
        else:
            city = rule_scope[6]
        rule_scope_dict.append({'prov': prov, 'city': city,
                                'pricing_id': rule_scope[2],
                                'rule_id': rule_scope[3]})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return rule_scope_dict


def sql_pricing_id(sql):
    con = pymysql.connect(
        host='106.75.233.19',
        port=3307,
        user='aifuyi',
        passwd='1qaz2wsx',
        db='mw_transport'
    )  # 连接数据库
    cur = con.cursor()  # 获取游标
    cur.execute(sql)  # 执行sql
    pricing_id_dict = {}  # 新建空字典
    while True:
        pricing_id = cur.fetchone()  # 获取一条数据 元组转列表
        if not pricing_id:
            break  # 如果抓取的数据为None,退出循环
        pricing_id_dict.update({pricing_id[3]: {'id': pricing_id[2],
                                                'prov': pricing_id[7]}})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return pricing_id_dict


def sql_pricing_rule(sql):
    con = pymysql.connect(
        host='106.75.233.19',
        port=3307,
        user='aifuyi',
        passwd='1qaz2wsx',
        db='mw_transport'
    )  # 连接数据库
    cur = con.cursor()  # 获取游标
    cur.execute(sql)  # 执行sql
    pricing_rule_dict = []  # 新建空字典
    while True:
        pricing_rule = cur.fetchone()  # 获取一条数据 元组转列表
        if not pricing_rule:
            break  # 如果抓取的数据为None,退出循环
        pricing_rule_dict.append({'desc': pricing_rule[7],
                                  'type_id': pricing_rule[8],
                                  'algorithms': pricing_rule[9],
                                  'cond': pricing_rule[10],
                                  'val': pricing_rule[11],
                                  'fee': pricing_rule[12],
                                  'fee_least': pricing_rule[13],
                                  'fee_information': pricing_rule[14],
                                  'fee_delivery': pricing_rule[15],
                                  'fee_receipt': pricing_rule[16]})
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return pricing_rule_dict


if __name__ == '__main__':

    pass
