import pymysql

conn = pymysql.connect( 
        host = "localhost", 
        port = 3306, 
        user = "root", 
        password = "RnfRjr123", 
        database = "unimate", 
        charset = 'utf8' 
    )

curs = conn.cursor()

def interests_delete():
    sql1 = "SET foreign_key_checks = 0"
    sql2 = "DROP TABLE IF EXISTS interests"
    sql3 = "SET foreign_key_checks = 1"
    
    curs.execute(sql1)
    curs.execute(sql2)
    curs.execute(sql3)
    conn.commit()
    
def interests_create():
    sql = """
    CREATE TABLE `interests` (
    `name` varchar(255) NOT NULL,
    PRIMARY KEY (`name`)
    )
    """
    
    curs.execute(sql)
    conn.commit()
    
def interests_insert():
    sql = """
    INSERT INTO `interests` VALUES
    ('여행'),
    ('영화'),
    ('음악'),
    ('뮤지컬'),
    ('노래듣기'),
    ('노래부르기'),
    ('춤'),
    ('독서'),
    ('요리'),
    ('사진'),
    ('운동'),
    ('헬스'),
    ('야구'),
    ('축구'),
    ('농구'),
    ('러닝'),
    ('수영'),
    ('자전거'),
    ('보드게임'),
    ('산책'),
    ('악기연주')
    """
    
    curs.execute(sql)
    conn.commit()
    
def chats_auto_increment():
    sql1 = "SET foreign_key_checks = 0"
    sql2 = """
    ALTER TABLE `chats` 
    CHANGE COLUMN `id` `id` INT NOT NULL AUTO_INCREMENT ;
    """
    sql3 = "SET foreign_key_checks = 1"
    
    curs.execute(sql1)
    curs.execute(sql2)
    curs.execute(sql3)
    conn.commit()
    
interests_delete()
interests_create()
interests_insert()

chats_auto_increment()
