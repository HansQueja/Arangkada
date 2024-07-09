from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
from django.shortcuts import redirect

from base.helper import get_tables, get_record, create_record, update_record, get_pk, delete_record
from base.helper import basic_queries, moderate_queries, complex_queries

import sqlite3

# Create your views here.
def home(request):
    if 'user_id' in request.session:
        name = request.session['first_name']
        return render(request, 'index.html', {"name":name})
    else:
        return redirect('login')

def about(request):
    if 'user_id' in request.session:
        name = request.session['first_name']
        return render(request, 'aboutus.html', {"name":name})
    else:
        return redirect('login')
    
def userprofile(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        first_name = request.session['first_name']
        last_name = request.session['last_name']
        email = request.session['email']
        return render(request, 'userprofile.html', {"user_id": user_id, "first_name": first_name,
                                                    "last_name": last_name, "email": email, "name":first_name})
    else:
        return redirect('login')

def login(request):

    if request.method == "POST":

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        email = request.POST.get("email")
        password = request.POST.get("password")

        cur.execute("SELECT * FROM users WHERE email = (?)", (email,))
        account = cur.fetchone()
        print("here post")

        if account and check_password(password, account[4]):
            
            s = SessionStore()
            s['user_id'] = account[0]
            s['first_name'] = account[1]
            s['last_name'] = account[2]
            s['email'] = account[3]
        
            request.session = s
            print(request.session)
            conn.close()

            return redirect('home')
        else:
            context = {"response":"Your email or password is incorrect. Please check your credentials."}
            return render(request, "login.html", context)


    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('login')


def signup(request):

    if request.method == "POST":

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("confirm-password")
        
        cur.execute("SELECT email FROM users")
        db_email = [email[0] for email in cur.fetchall()]
        
        cur.execute("SELECT COUNT(*) FROM users")
        db_count = cur.fetchall()
        count = db_count[0][0]

        if email in db_email:
            context = {"response":"The email you've entered is already in use. Try a new email."}
            return render(request, "signup.html", context)

        if password1 != password2:
            context = {"response":"Your password and confirm password doesn't match. Please try again."}
            return render(request, "signup.html", context)

        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (count + 1, first_name, last_name, email, make_password(password1),))
        conn.commit()
        conn.close()
        return render(request, "login.html")

    return render(request, "signup.html")


def showtables(request):
    if 'user_id' in request.session:
        name = request.session['first_name']
        vehicles, components, operators, routes = get_tables()
        return render(request, "showtable.html", {"vehicles": vehicles, "components": components, "operators": operators,
                                                   "routes": routes, "name": name})
    else:
        return redirect('login')
    
# QUERIES BELOW
def basic(request):

    if 'user_id' in request.session:

        name = request.session['first_name']

        if request.method == "POST":

            query = request.POST.get("options")
            conn = sqlite3.connect('transport.db')
            cur = conn.cursor()

            if 'route_length' == query:
                cur.execute(basic_queries[0])
                routes_length = cur.fetchall()
                conn.close()
                return render(request, "basic.html", {"routes_length": routes_length, "name":name, "query":basic_queries[0]})
            
            if 'route_end' == query:
                cur.execute(basic_queries[1])
                routes_end = cur.fetchall()
                conn.close()
                return render(request, "basic.html", {"routes_end": routes_end, "name":name, "query":basic_queries[1]})
            
            if 'operators' == query:
                cur.execute(basic_queries[2])
                operators = cur.fetchall()
                conn.close()
                return render(request, "basic.html", {"operators": operators, "name":name, "query":basic_queries[2]})        

        return render(request, "basic.html", {"name":name})

    else:
        return redirect('login')

def moderate(request):

    if 'user_id' in request.session:
        name = request.session['first_name']

        if request.method == "POST":

            query = request.POST.get("options")
            conn = sqlite3.connect('transport.db')
            cur = conn.cursor()

            if 'mod-1' == query:
                cur.execute(moderate_queries[0])
                routes = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_1": routes, "name":name, "query":moderate_queries[0]})
            
            if 'mod-2' == query:
                cur.execute(moderate_queries[1])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_2": vehicles, "name":name, "query":moderate_queries[1]})
            
            if 'mod-3' == query:
                cur.execute(moderate_queries[2])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_3": vehicles, "name":name, "query":moderate_queries[2]})    

            if 'mod-4' == query:
                cur.execute(moderate_queries[3])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_4": vehicles, "name":name, "query":moderate_queries[3]})     
            
            if 'mod-5' == query:
                cur.execute(moderate_queries[4])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_5": vehicles, "name":name, "query":moderate_queries[4]}) 
            
            if 'mod-6' == query:
                cur.execute(moderate_queries[5])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_6": vehicles, "name":name, "query":moderate_queries[5]}) 
            
            if 'mod-7' == query:
                cur.execute(moderate_queries[6])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_7": vehicles, "name":name, "query":moderate_queries[6]}) 
            
            if 'mod-8' == query:
                cur.execute(moderate_queries[7])
                operators = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_8": operators, "name":name, "query":moderate_queries[7]}) 

        return render(request, "moderate.html", {"name":name})

    else:
        return redirect('login') 

def complex(request):

    if 'user_id' in request.session:

        name = request.session['first_name']

        if request.method == "POST":

            query = request.POST.get("options")
            conn = sqlite3.connect('transport.db')
            cur = conn.cursor()

            if 'mod-1' == query:
                cur.execute(complex_queries[0])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "complex.html", {"mod_1": vehicles, "name":name, "query":complex_queries[0]})

            if 'mod-2' == query:
                operator_name = request.POST.get("operator_name")
                cur.execute(complex_queries[1], (operator_name,))
                routes = cur.fetchall()
                conn.close()
                return render(request, "complex.html", {"mod_2": routes, "name":name, "operator_name":operator_name, "query":complex_queries[1]})
            
            if 'mod-3' == query:
                cur.execute(complex_queries[2])
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "complex.html", {"mod_3": vehicles, "name":name, "query":complex_queries[2]})    


        return render(request, "complex.html", {"name":name})

    else:
        return redirect('login') 


def database(request):
    if 'user_id' in request.session:

        name = request.session['first_name']

        return render(request, "crud.html", {"name": name})
    else:
        return redirect('login') 


def create(request):
    if 'user_id' in request.session:

        vehicles, components, operators, routes = get_tables()
        name = request.session['first_name']

        if request.method == "POST":
            table = request.POST.get('form_type')
            values = get_record(request, table)
            
            flag = create_record(table, values)
            if flag == -1:
                messages.error(request, "The primary key you've entered is already in the database. Enter a unique model.")
                return render(request, "create.html", {"vehicles": vehicles, "components": components, "operators": operators, "routes": routes, "name": name})
            
            messages.success(request, "Your record has been added to the database.")

        return render(request, "create.html", {"vehicles": vehicles, "components": components, "operators": operators, "routes": routes, "name": name})
    else:
        return redirect('login')    
    

def update(request):
    if 'user_id' in request.session:

        vehicles, components, operators, routes = get_tables()
        name = request.session['first_name']

        if request.method == "POST":
            table = request.POST.get('form_type')
            values = get_record(request, table)

            update_record(table, values)
            messages.success(request, "Your choosen record has been updated with new values.")

        return render(request, "update.html", {"vehicles": vehicles, "components": components, "operators": operators, "routes": routes, "name": name})
    else:
        return redirect('login')  
    

def delete(request):
    if 'user_id' in request.session:

        vehicles, components, operators, routes = get_tables()
        name = request.session['first_name']

        if request.method == "POST":
            table = request.POST.get('form_type')
            pk = get_pk(request, table)

            delete_record(table, pk)
            messages.success(request, f"Your choosen record '{pk}' has been deleted from the database.")

        return render(request, "delete.html", {"vehicles": vehicles, "components": components, "operators": operators, "routes": routes, "name": name})
    else:
        return redirect('login')  