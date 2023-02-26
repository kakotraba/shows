#####################################
#
#   import(s)
#
#####################################


from flask import redirect,render_template,request,session
from flask_app import app
from flask_app.models.show import Show
from flask_app.models import user



#####################################
#
#   @app.route(s)
#
#####################################


#list_shows...run 2 queries to gather data on current user(by id) and all shows(with poster data)
@app.route('/shows/list')
def list_shows():
    if 'user_id' not in session:
        print("   *!!!*!!!*!!!*   ACCESS DENIED - NOT IN SESSION   *!!!*!!!*!!!*   ")
        return redirect('/')
    return render_template("list_shows.html" , user = user.User.get_by_id(session['user_id']) , show_list = Show.get_all_shows_with_poster_data())


#new_show_page...render a page to enter new show data into a form
@app.route('/shows/new')
def new_show_page():
    if 'user_id' not in session:
        print("   *!!!*!!!*!!!*   ACCESS DENIED - NOT IN SESSION   *!!!*!!!*!!!*   ")
        return redirect('/')
    return render_template("new_show.html")


#save_show_to_db...parse form data into dictionary, run a classmethod to validate the entered data and save to the DB
@app.route("/shows/save_to_db", methods=['POST'])
def save_show_to_db(): 
    
    user_supplied_form_data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
        "user_id": session['user_id']
    } 
    valid_show = Show.save_valid_show(user_supplied_form_data)
    if not valid_show:
        print("   *!*!*!*!*!*!*   CREATE FAILED   *!*!*!*!*!*!*   ")
        return redirect("/shows/new")
    print("   *$*$*$*$*$*$*   SHOW POSTED SUCCESSFULLY    *$*$*$*$*$*$*   ")
    return redirect('/shows/list')


#edit_show_page...render a page to edit an existing show's data, pass in show id, run 2 queries to gather data on current user(by id) and one show(by show id, with poster data)
@app.route('/shows/edit/<int:show_id>')
def edit_show_page(show_id):
    if 'user_id' not in session:
        print("   *!!!*!!!*!!!*   ACCESS DENIED - NOT IN SESSION   *!!!*!!!*!!!*   ")
        return redirect('/')
    show_data ={"id":show_id}
    return render_template("edit_show.html" , show=Show.get_one_show_with_poster_data(show_data) , user = user.User.get_by_id(session['user_id']) )


#update_db...parse form data into dictionary, run a classmethod to validate the entered data and update the DB
@app.route('/shows/update_db', methods=['POST'])
def update_db():
    
    user_supplied_form_data = {
        "id": request.form['id'],
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
        "user_id": session['user_id']
    } 
    show_id = request.form['id']
    updated_show = Show.update_valid_show(user_supplied_form_data)
    if not updated_show:
        print("   *!*!*!*!*!*!*   UPDATE FAILED   *!*!*!*!*!*!*   ")
        return redirect (f'/shows/edit/{show_id}')
    print("   *$*$*$*$*$*$*   SHOW UPDATED SUCCESSFULLY    *$*$*$*$*$*$*   ")
    return redirect('/shows/list')


#view_show_page...render a page to view show details, pass in the show id, run 2 queries to gather data on current user(by id) and one show(by show id, with poster data)
@app.route('/shows/view/<int:show_id>')
def view_show_page(show_id):
    if 'user_id' not in session:
        print("   *!!!*!!!*!!!*   ACCESS DENIED - NOT IN SESSION   *!!!*!!!*!!!*   ")
        return redirect('/')
    show_data={"id":show_id}
    return render_template("view_show.html" , show = Show.get_one_show_with_poster_data(show_data) , user = user.User.get_by_id(session['user_id']))


@app.route('/shows/delete/<int:show_id>')
def delete_show(show_id):
    if 'user_id' not in session:
        print("   *!!!*!!!*!!!*   ACCESS DENIED - NOT IN SESSION   *!!!*!!!*!!!*   ")
        return redirect('/')
    show_data = {'id':show_id}
    Show.delete(show_data)
    return redirect('/shows/list')



#111