from django.shortcuts import render
import sqlite3

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'aboutus.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
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

        if 'route_length' in request.POST:
            conn = sqlite3.connect('transport.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM routes ORDER BY route_length;")
            routes_length = cur.fetchall()
            
            return render(request, "basic.html", {"routes_length": routes_length})
        
        if 'route_end' in request.POST:
            conn = sqlite3.connect('transport.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM routes ORDER BY start_route, end_route;")
            routes_end = cur.fetchall()
            
            return render(request, "basic.html", {"routes_end": routes_end})
        

    return render(request, "basic.html")


def userprofile(request):
    return render(request, "userprofile.html")