from django.shortcuts import render

import sqlite3


attributes = {
            'components': ('model', 'brake_system', 'clutch', 'tires', 'battery', 'bearings', 'belt', 'fuel_filter', 'piston_ring', 'lights', 'body', 'electrical_system'),
            'operators': ('operator_number', 'name_of_operator', 'address', 'occupation', 'no_of_operational_units', 'age', 'contact_number'),
            'vehicles': ('plate_number', 'vehicle_type', 'manufacturer', 'model', 'year', 'revenue', 'engine_condition', 'seat_capacity', 'operation_times', 'operator_number', 'route_id'),
            'routes': ('route_id', 'start_route', 'end_route', 'route_length', 'base_fare') 
            } #for matching attributes with values

placeholders = {
                'components': '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                'operators': '(?, ?, ?, ?, ?, ?, ?)',
                'vehicles': '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                'routes': '(?, ?, ?, ?, ?)' 
                } #for placeholder where the tupled values go
                      #might separate these dicts in a diff function/make it global, if it would be used for other crud operations

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


# <----------------------------------------- For Create Function --------------------------------------------->

def get_record(request, table): #getting input for each attr for a specific table and returns it as a tuple
    
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    
    match table:
        case 'components': 

            model = request.POST.get('model')
            brake_system = request.POST.get('brake_system')
            clutch = request.POST.get('clutch')
            tires = request.POST.get('tires')
            battery = request.POST.get('battery')
            bearings = request.POST.get('bearings')
            belt = request.POST.get('belt')
            fuel_filter = request.POST.get('fuel_filter')
            piston_ring = request.POST.get('piston_ring')
            lights = request.POST.get('lights')
            body = request.POST.get('body')
            electrical_system = request.POST.get('electrical_system')
            values = (model, brake_system, clutch, tires, battery, bearings, belt, fuel_filter, piston_ring, lights, body, electrical_system)
        case 'operators':

            operator_number = request.POST.get('operator_number')
            name_of_operator = request.POST.get('name_of_operator')
            address = request.POST.get('address')
            occupation = request.POST.get('occupation')
            no_of_operational_units = request.POST.get('no_of_operational_units')
            age = request.POST.get('age')
            contact_number = request.POST.get('contact_number')
            values = (operator_number, name_of_operator, address, occupation, no_of_operational_units, age, contact_number)
        case 'vehicles':

            plate_number = request.POST.get('plate_number')
            vehicle_type = request.POST.get('vehicle_type')
            manufacturer = request.POST.get('manufacturer')
            model = request.POST.get('model')
            year = request.POST.get('year')
            revenue = request.POST.get('revenue')
            engine_condition = request.POST.get('engine_condition')
            seat_capacity = request.POST.get('seat_capacity')
            operation_times = request.POST.get('operation_times')
            operator_number = request.POST.get('operator_number')
            route_id = request.POST.get('route_id')
            values = (plate_number, vehicle_type, manufacturer, model, year, revenue, engine_condition, seat_capacity, operation_times, operator_number, route_id)
        case 'routes':

            route_id = request.POST.get('route_id')
            start_route = request.POST.get('start_route')
            end_route = request.POST.get('end_route')
            route_length = request.POST.get('route_length')
            base_fare = request.POST.get('base_fare')
            values = (route_id, start_route, end_route, route_length, base_fare)

    conn.close()
    return values


def create_record(table, values): #setting values to the db with a query
    conn = sqlite3.connect('transport.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    conn.row_factory = sqlite3.Row #allows the db to be referenced by column names
    c = conn.cursor()

    query = f"INSERT INTO {table} {attributes[table]} VALUES {placeholders[table]}"
    try:
        c.execute(query, values)
    except sqlite3.IntegrityError:
        return -1
    conn.commit()
    conn.close()

# <---------------------------- UPDATE Function ---------------------------------------->
def update_record(table, values):
    pk_value = values[0]#get pk value
    values = values[1:] #remove pk from the values
    
    active_attr = attributes[table] #get the attributes of the table to be updated
    pk_name = active_attr[0] #get pk attribute
    active_attr = active_attr[1:] #remove pk attribute
    
    val_list = [element for element in values if element != ''] #strip the input values tuple of ' '(skipped) inputs
    attr_list = [attr for attr, val in zip(active_attr, values) if val !=''] #remove attributes that has no corresponding input values
    zipped_values = zip(attr_list, val_list) #match the attribute to the value
    
    conn = sqlite3.connect('transport.db')
    c = conn.cursor()
    for attr, val in zipped_values: #loop through each attribute-value to update
        query = f"UPDATE {table} SET {attr} = ? WHERE {pk_name} = ?"
        c.execute(query, (val, pk_value))
    conn.commit()
    conn.close()

# <--------------------------- DELETE Function ---------------------------------------->
def get_pk(request, table):
    match table: #getting input for each attr for a specific table
        case 'components': 
            pk = request.POST.get('model')
        case 'operators':
            pk = request.POST.get('operator_number')
        case 'vehicles':
            pk = request.POST.get('plate_number')
        case 'routes':
            pk = request.POST.get('route_id')
    return pk

def delete_record(table, pk_value):
    primary_key = {'components': 'model','operators': 'operator_number', 'vehicles': 'plate_number', 'routes': 'route_id'}
    conn = sqlite3.connect('transport.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    c = conn.cursor()

    query = f"DELETE FROM vehicles WHERE {primary_key[table]}=?"
    c.execute(query, (pk_value,))
    conn.commit()
    
    query = f"DELETE FROM {table} WHERE {primary_key[table]}=?"
    c.execute(query, (pk_value,))
    conn.commit()
    conn.close()