from flask_mysqldb import MySQL
from config import Config 

class database:
    def __init__(self, app):
        app.config['MYSQL_HOST'] = Config.DATABASE_CONFIG['host']
        app.config['MYSQL_USER'] = Config.DATABASE_CONFIG['user']
        app.config['MYSQL_PASSWORD'] = Config.DATABASE_CONFIG['password']
        app.config['MYSQL_DB'] = Config.DATABASE_CONFIG['database']

        self.mysql = MySQL(app)

        self.mycursor = self.mysql.connection.cursor()

        create_user_info_table = "CREATE TABLE IF NOT EXISTS user_info ("
        create_user_info_table += "ID MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
        create_user_info_table += "username VARCHAR(20) NOT NULL, "
        create_user_info_table += "password VARCHAR(20) NOT NULL, "
        create_user_info_table += "email VARCHAR(225) NOT NULL, "
        create_user_info_table += "profile_pic_id MEDIUMINT NOT NULL DEFAULT 0, "               # profile pic need to be update at profile_pic_infor before here
        create_user_info_table += "exist_status BOOLEAN DEFAULT TRUE"
        create_user_info_table += "FOREIGN KEY (profile_pic_id) REFERENCES profile_pic_info(profile_pic_id)"
        create_user_info_table += "); "
        
        self.mycursor.execute(create_user_info_table)

        create_profile_pic_table = "CREATE TABLE IF NOT EXISTS profile_pic_info ("
        create_profile_pic_table += "profile_pic_id MEDIUMINT NOT NULL PRIMARY KEY, "
        create_profile_pic_table += "path "
        create_profile_pic_table += "); "
        
        self.mysql.commit()                             # commit my code


    def print_table(self, table):
        sql = 'SELECT * FROM ' + table
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        for i in myresult:
            print(i)

    def inser_user_info_log_in(self):                                                                     # is not allow to upload profile pic when log in  
        sql = "INSERT INTO user_info "
 

      