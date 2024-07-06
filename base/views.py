from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import redirect

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

def login(request):

    if request.method == "POST":

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        email = request.POST.get("email")
        password = request.POST.get("password")

        cur.execute("SELECT * FROM users WHERE email = (?)", (email,))
        account = cur.fetchone()

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

        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (count + 1, first_name, last_name, 
                                                                 email, make_password(password1),))
        conn.commit()
        conn.close()
        return render(request, "login.html")

    return render(request, "signup.html")

# for showtables()
def get_tables():
    conn = sqlite3.connect('transport.db') #establish connection to the db
    cur = conn.cursor() #establish a cursor to execute sql statements/queries
    cur.execute("SELECT * FROM vehicles")
    vehicles = cur.fetchall()
    cur.execute("SELECT * FROM components")
    components = cur.fetchall()
    cur.execute("SELECT * FROM operators")
    operators = cur.fetchall()
    cur.execute("SELECT * FROM routes")
    routes = cur.fetchall()
    conn.close()
    return vehicles, components, operators, routes

def showtables(request):
    if 'user_id' in request.session:
        name = request.session['first_name']
        vehicles, components, operators, routes = get_tables()
        return render(request, "showtable.html", {"vehicles": vehicles, 
                                              "components": components,
                                              "operators": operators,
                                              "routes": routes,
                                              "name": name})
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
                cur.execute("SELECT * FROM routes ORDER BY route_length;")
                routes_length = cur.fetchall()
                conn.close()
                return render(request, "basic.html", {"routes_length": routes_length, "name":name})
            
            if 'route_end' == query:
                cur.execute("SELECT * FROM routes ORDER BY start_route, end_route;")
                routes_end = cur.fetchall()
                conn.close()
                return render(request, "basic.html", {"routes_end": routes_end, "name":name})
            
            if 'operators' == query:
                cur.execute("SELECT * FROM operators ORDER BY name_of_operator;")
                operators = cur.fetchall()
                conn.close()
                return render(request, "basic.html", {"operators": operators, "name":name})        

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
                cur.execute("SELECT start_route, COUNT(*) count FROM routes GROUP BY start_route HAVING count > 1 ORDER BY count DESC;")
                routes = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_1": routes, "name":name})
            
            if 'mod-2' == query:
                cur.execute("SELECT manufacturer, COUNT(*) count FROM vehicles GROUP BY manufacturer ORDER BY count DESC;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_2": vehicles, "name":name})
            
            if 'mod-3' == query:
                cur.execute("SELECT vehicle_type, COUNT(*) count FROM vehicles GROUP BY vehicle_type ORDER BY count DESC;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_3": vehicles, "name":name})    

            if 'mod-4' == query:
                cur.execute("SELECT manufacturer, ROUND(AVG(revenue), 2) average_revenue FROM vehicles GROUP BY manufacturer ORDER BY average_revenue DESC;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_4": vehicles, "name":name})     
            
            if 'mod-5' == query:
                cur.execute("SELECT vehicle_type, ROUND(AVG(revenue), 2) average_revenue FROM vehicles GROUP BY vehicle_type ORDER BY average_revenue DESC;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_5": vehicles, "name":name}) 
            
            if 'mod-6' == query:
                cur.execute("SELECT model, ROUND(AVG(revenue), 2) average_revenue FROM vehicles GROUP BY model ORDER BY average_revenue DESC;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_6": vehicles, "name":name}) 
            
            if 'mod-7' == query:
                cur.execute("SELECT vehicle_type, manufacturer, model, ROUND(AVG(revenue), 2) average_revenue FROM vehicles GROUP BY vehicle_type, manufacturer, model ORDER BY vehicle_type, manufacturer, model;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_7": vehicles, "name":name}) 
            
            if 'mod-8' == query:
                cur.execute("SELECT occupation, COUNT(*) count FROM operators GROUP BY occupation;")
                operators = cur.fetchall()
                conn.close()
                return render(request, "moderate.html", {"mod_8": operators, "name":name}) 

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
                cur.execute("SELECT o.operator_number, o.name_of_operator, o.no_of_operational_units, ROUND(SUM(v.revenue), 2) 'Total revenue' FROM operators o JOIN vehicles v ON o.operator_number = v.operator_number GROUP BY o.operator_number ORDER BY 'Total revenue' DESC;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "complex.html", {"mod_1": vehicles, "name":name})

            if 'mod-2' == query:
                operator_name = request.POST.get("operator_name")
                cur.execute("SELECT o.operator_number, r.route_id, r.start_route, r.end_route FROM operators o JOIN vehicles v ON v.operator_number = o.operator_number JOIN routes r ON r.route_id = v.route_id WHERE o.name_of_operator = (?);", (operator_name,))
                routes = cur.fetchall()
                conn.close()
                return render(request, "complex.html", {"mod_2": routes, "name":name})
            
            if 'mod-3' == query:
                cur.execute("SELECT v.plate_number, v.revenue,  ROUND((c.brake_system + c.clutch + c.tires + c.battery + c.bearings + c.belt + c.fuel_filter + c.piston_ring + c.lights + c.body + c.electrical_system), 2) 'Total maintenance cost' FROM vehicles v JOIN components c ON c.model = v.model ORDER BY revenue DESC;")
                vehicles = cur.fetchall()
                conn.close()
                return render(request, "complex.html", {"mod_3": vehicles, "name":name})    


        return render(request, "complex.html", {"name":name})

    else:
        return redirect('login') 

def userprofile(request):
    return render(request, "userprofile.html")