from database.user_auth import *
import MySQLdb.cursors

class database:
    def __init__(self, mysql):
        self.mysql = mysql

        self.mycursor = cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        create_user_info_table = "CREATE TABLE IF NOT EXISTS account ("
        create_user_info_table += "ID MEDIUMINT NOT NULL AUTO_INCREMENT, "
        create_user_info_table += "username VARCHAR(50) NOT NULL, "
        create_user_info_table += "hashed_password BLOB NOT NULL, "
        create_user_info_table += "profile_pic_path VARCHAR(225) NOT NULL DEFAULT '', "  
        create_user_info_table += "hashed_token_binary BLOB DEFAULT NULL, "
        create_user_info_table += "exist_status BOOLEAN DEFAULT TRUE"
        create_user_info_table += "PRIMARY KEY (ID, username)"
        create_user_info_table += "); "
        
        self.mycursor.execute(create_user_info_table)
        
        self.mysql.commit()            


    def print_table(self):
        sql = 'SELECT * FROM account'
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        for i in myresult:
            print(i)


    def check_username_exist(self, username):
        sql = 'SELECT * FROM account WHERE username=(%s)'
        val = (username,)
        self.mycursor.execute(sql, val)
        info = self.mycursor.fetchall()
        if len(info) != 0:
            return True 
            # if the input user name exists
        return False

   
    def register(self, username, password): 
        # make sure to check if the username exist before using this function
        sql = "INSERT INTO account (username, password)"
        sql += "VALUES (%s, %s)"
        hashed_password = hash_password(password.encode('utf-9'))
        val = (username, hashed_password)
        self.mycursor.execute(sql, val)
        self.mysql.commit()


    def login(self, username, password):
        # make sure to check if the username exist before using this function        
        sql = "SELECT password FROM account WHERE username=(%s);"
        val = (username, )
        self.mycursor.execute(sql, val)
        hashed_password = self.mycursor.fetchall()[0][0]
        if check_password(password.encode('utf-8'), hashed_password):
            return True
        return False
        


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




    
 

      