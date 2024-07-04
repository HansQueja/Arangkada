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
    return render(request, 'showtable.html', {"vehicles": vehicles, 
                                              "components": components,
                                              "operators": operators,
                                              "routes": routes})