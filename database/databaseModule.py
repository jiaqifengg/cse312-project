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
        create_user_info_table += "ID MEDIUMINT NOT NULL AUTO_INCREMENT, "
        create_user_info_table += "username VARCHAR(20) NOT NULL, "
        create_user_info_table += "password VARCHAR(20) NOT NULL, "
        create_user_info_table += "profile_pic_path VARCHAR(225) NOT NULL DEFAULT '0', "            
        create_user_info_table += "exist_status BOOLEAN DEFAULT TRUE"
        create_user_info_table += "PRIMARY KEY (ID, username)"
        create_user_info_table += "); "
        
        self.mycursor.execute(create_user_info_table)
        
        self.mysql.commit()            


    def print_table(self):
        sql = 'SELECT * FROM user_info'
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        for i in myresult:
            print(i)


    def check_username_exist(self,username):
        sql = 'SELECT * FROM user_info WHERE username=(%s)'
        val = (username,)
        self.mycursor.execute(sql, val)
        info = self.mycursor.fetchall()
        if len(info) != 0:
            return True 
        return False

   
    def register(self, username, password):            
        # register 
        # make sure that the username is not exist
        username_exist = self.check_username_exist(username)
        if username_exist == False:
            return [False, 'Username exists']

        # encrypt the username
        sql = "INSERT INTO user_info (username, password)"
        sql += "VALUES (%s, %s)"
        val = (username, password)
        self.mycursor.execute(sql, val)
        self.mysql.commit()
        return [True]


    def login(self, username, password):
        username_exist = self.check_username_exist(username)
        if username_exist == False:
            return [False, 'Username exists']
        
        sql = "SELECT password FROM user_info WHERE username=(%s) AND password=(%s);"
        val = (username, password)
        result = self.mycursor.execute(sql, val)
        if len(result) == 0:
            return [False, 'Incorrect password']
        return [True]


    def update_user_info(self, username, password):
        # update user information
        # make sure that the username is not exist
        username_exist = self.check_username_exist(username)
        if username_exist == False:
            return [False, 'Username exists']

        sql = "INSERT INTO user_info (username, password)"
        sql += "VALUES (%s, %s)"
        val = (username, password)
        self.mycursor.execute(sql, val)
        self.mysql.commit()
        return [True]


    def store_profile_pic_path(self, username, path):
        # update user information
        # make sure that the username is not exist
        username_exist = self.check_username_exist(username)
        if username_exist == False:
            return [False, 'Username exists']
        
        # store the new path 
        sql = "INSERT INTO user_info (path)"
        sql += "VALUES (%s)"
        val = (path,)
        self.mycursor.execute(sql, val)
        self.mysql.commit()




    
 

      