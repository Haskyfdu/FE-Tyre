import pymysql


def sql_receiver_transport_pick1(sql):
    con = pymysql.connect(
        host='106.75.233.19',
        port=3307,
        user='aifuyi',
        passwd='1qaz2wsx',
        db='mw_transport'
    )    # 连接数据库
    cur = con.cursor()    # 获取游标
    cur.execute(sql)      # 执行sql
    rule_scope = []    # 新建空字典
    while True:
        i = 0
        receiver_transport = cur.fetchone()  # 获取一条数据 元组转列表
        if not receiver_transport:
            break  # 如果抓取的数据为None,退出循环
        if receiver_transport[5] is None or len(receiver_transport[5]) == 0:
            prov = ''
        elif receiver_transport[5][-1] == '省' or receiver_transport[5][-1] == '市':
            prov = receiver_transport[5][0:-1]
        else:
            prov = receiver_transport[5]
        if receiver_transport[6] is None or len(receiver_transport[6]) == 0:
            city = ''
        elif receiver_transport[6][-1] == '省' or receiver_transport[6][-1] == '市':
            city = receiver_transport[6][0:-1]
        else:
            city = receiver_transport[6]
        if receiver_transport[7] is None or len(receiver_transport[7]) == 0:
            dist = ''
        else:
            dist = receiver_transport[7]
        if receiver_transport[8] is None or len(receiver_transport[8]) == 0:
            street = ''
        else:
            street = receiver_transport[8]
        if int(receiver_transport[2]) <= 38:
            storage = '000003'
        elif int(receiver_transport[2]) <= 56:
            storage = '000010'
        elif int(receiver_transport[2]) <= 62:
            storage = '000011'
        elif int(receiver_transport[2]) <= 90:
            storage = '000008'
        elif int(receiver_transport[2]) <= 97:
            storage = '000014'
        else:
            storage = '000003'

        rule_scope.append({'prov': prov,
                           'city': city,
                           'dist': dist,
                           'street': street,
                           'pricing_id': receiver_transport[2],
                           'rule_id': receiver_transport[3],
                           'storage': storage})        # 将数据录入字典
    cur.close()  # 关闭游标
    con.close()  # 关闭连接
    return rule_scope


if __name__ == '__main__':

    data = sql_receiver_transport_pick1("SELECT * FROM mw_transport.mwt_contract_rule_scope;")
