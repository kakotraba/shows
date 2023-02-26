#####################################
#
#   imports(s)
#
#####################################


from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash



#####################################
#
#   global variable(s)
#
#####################################


DB = "belt_shows"



#####################################
#
#   User class
#
#####################################


class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.poster_first = data['first_name']
        self.poster_last = data['last_name']
        self.poster_id = data['user_id']



#####################################
#
#   @class method(s)
#
#####################################


    @classmethod
    def get_all_shows_with_poster_data(cls):
        query = "SELECT * FROM shows JOIN users on shows.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        show_list = []
        for show_user_dictionary in results:
            show_class = cls(show_user_dictionary)
            show_list.append(show_class)
        return show_list


    @classmethod
    def save_valid_show(cls, request_form_data):
        if not cls.is_valid(request_form_data):
            print("   *!*!*!*!*!*!*   INVALID SHOW DATA   *!*!*!*!*!*!*   ")
            return False
        print("   *$*$*$*$*$*$*   SHOW DATA VALIDATED    *$*$*$*$*$*$*   ")
        query = """INSERT INTO shows 
                    (title, network, release_date, description, user_id)
                    VALUES
                    (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s)
                    """
        result = connectToMySQL(DB).query_db(query, request_form_data)
        return result


    @classmethod
    def update_valid_show(cls, request_form_data):
        if not cls.is_valid(request_form_data):
            print("   *!*!*!*!*!*!*   INVALID UPDATE DATA   *!*!*!*!*!*!*   ")
            return False
        print("   *$*$*$*$*$*$*   UPDATE DATA VALIDATED    *$*$*$*$*$*$*   ")
        query = """UPDATE shows 
                    SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s, updated_at=NOW() 
                    WHERE id=%(id)s;"""
        result = connectToMySQL(DB).query_db(query,request_form_data)
        print (result)
        if result == None:
            return True
        return False


    @classmethod
    def get_one_show_with_poster_data(cls,show_id):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id WHERE shows.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,show_id)
        #print(result[0])
        show_class = cls(result[0])
        print(show_class)
        return show_class


    @classmethod
    def delete(cls,show_id):
        query = "DELETE FROM shows WHERE id = %(id)s"
        result = connectToMySQL(DB).query_db(query,show_id)
        print(result)



#####################################
#
#   @static method(s)            
#
#####################################


    @staticmethod
    def is_valid(show):
        valid = True
        if len(show["title"]) < 3:
            valid = False
            flash("Title must be at least 3 characters.", "show")           
        if len(show["network"]) < 3:
            valid = False
            flash("Network must be at least 3 characters.", "show") 
        if len(show["release_date"]) < 1:
            valid = False
            flash("Date must not be blank.", "show") 
        if len(show["description"]) < 3:
            valid = False
            flash("Description must be at least 3 characters.", "show") 
        return valid
