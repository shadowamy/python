import pymysql
import time

def eegOprate(type, power):
    daytime = time.strftime('%H:%M', time.localtime(time.time()))
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    db = pymysql.connect("localhost", "root", "", "ssrbed")
    cursor = db.cursor()
    sql=''
    if(type == 'delta'):
        sql = "insert delta(Date, daytime, DeltaValue) values ('%s', '%s', '%s')" % (date, daytime, power)

    elif(type == 'theta'):
        sql = "insert theta(Date, daytime, ThetaValue) values ('%s', '%s', '%s')" % (date, daytime, power)

    elif (type == 'alpha'):
        sql = "insert alpha(Date, daytime, AlphaValue) values ('%s', '%s', '%s')" % (date, daytime, power)

    elif (type == 'beta'):
        sql = "insert beta(Date, daytime, BetaValue) values ('%s', '%s', '%s')" % (date, daytime, power)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()

        # 关闭数据库连接
    cursor.close()
    db.close()

#eegOprate('beta', 24)