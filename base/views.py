from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
import sqlite3

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'aboutus.html')

def login(request):

    return render(request, 'login.html')

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
    vehicles, components, operators, routes = get_tables()
    return render(request, "showtable.html", {"vehicles": vehicles, 
                                              "components": components,
                                              "operators": operators,
                                              "routes": routes})

# QUERIES BELOW
def basic(request):

    if request.method == "POST":
        query = request.POST.get("options")
        conn = sqlite3.connect('transport.db')
        cur = conn.cursor()

        if 'route_length' == query:
            cur.execute("SELECT * FROM routes ORDER BY route_length;")
            routes_length = cur.fetchall()
            conn.close()
            return render(request, "basic.html", {"routes_length": routes_length})
        
        if 'route_end' == query:
            cur.execute("SELECT * FROM routes ORDER BY start_route, end_route;")
            routes_end = cur.fetchall()
            conn.close()
            return render(request, "basic.html", {"routes_end": routes_end})
        
        if 'operators' == query:
            cur.execute("SELECT * FROM operators ORDER BY name_of_operator;")
            operators = cur.fetchall()
            conn.close()
            return render(request, "basic.html", {"operators": operators})        

    return render(request, "basic.html")


def userprofile(request):
    return render(request, "userprofile.html")