from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

attributes = {'components': ('model', 'brake_system', 'clutch', 'tires', 'battery', 'bearings', 'belt', 'fuel_filter', 'piston_ring', 'lights', 'body', 'electrical_system'),
                'operators': ('operator_number', 'name_of_operator', 'address', 'occupation', 'no_of_operational_units', 'age', 'contact_number'),
                'vehicles': ('plate_number', 'vehicle_type', 'manufacturer', 'model', 'year', 'revenue', 'engine_condition', 'seat_capacity', 'operation_times', 'operator_number', 'route_id'),
                'routes': ('route_id', 'start_route', 'end_route', 'route_length', 'base_fare') 
                } #for matching attributes with values
placeholders = {'components': '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    'operators': '(?, ?, ?, ?, ?, ?, ?)',
                    'vehicles': '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    'routes': '(?, ?, ?, ?, ?)' 
                    } #for placeholder where the tupled values go
                      #might separate these dicts in a diff function/make it global, if it would be used for other crud operations


def get_tables():
    conn = sqlite3.connect('transport.db') #establish connection to the db
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
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


def get_record(table):
    match table: #getting input for each attr for a specific table
        case 'components': 
            model = request.form.get('model')
            brake_system = request.form.get('brake_system')
            clutch = request.form.get('clutch')
            tires = request.form.get('tires')
            battery = request.form.get('battery')
            bearings = request.form.get('bearings')
            belt = request.form.get('belt')
            fuel_filter = request.form.get('fuel_filter')
            piston_ring = request.form.get('piston_ring')
            lights = request.form.get('lights')
            body = request.form.get('body')
            electrical_system = request.form.get('electrical_system')
            values = (model, brake_system, clutch, tires, battery, bearings, belt, fuel_filter, piston_ring, lights, body, electrical_system)
        case 'operators':
            operator_number = request.form.get('operator_number')
            name_of_operator = request.form.get('name_of_operator')
            address = request.form.get('address')
            occupation = request.form.get('occupation')
            no_of_operational_units = request.form.get('no_of_operational_units')
            age = request.form.get('age')
            contact_number = request.form.get('contact_number')
            values = (operator_number, name_of_operator, address, occupation, no_of_operational_units, age, contact_number)
        case 'vehicles':
            plate_number = request.form.get('plate_number')
            vehicle_type = request.form.get('vehicle_type')
            manufacturer = request.form.get('manufacturer')
            model = request.form.get('model')
            year = request.form.get('year')
            revenue = request.form.get('revenue')
            engine_condition = request.form.get('engine_condition')
            seat_capacity = request.form.get('seat_capacity')
            operation_times = request.form.get('operation_times')
            operator_number = request.form.get('operator_number')
            route_id = request.form.get('route_id')
            values = (plate_number, vehicle_type, manufacturer, model, year, revenue, engine_condition, seat_capacity, operation_times, operator_number, route_id)
        case 'routes':
            route_id = request.form.get('route_id')
            start_route = request.form.get('start_route')
            end_route = request.form.get('end_route')
            route_length = request.form.get('route_length')
            base_fare = request.form.get('base_fare')
            values = (route_id, start_route, end_route, route_length, base_fare)
    return values


def create_record(table, values):
    conn = sqlite3.connect('transport.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    conn.row_factory = sqlite3.Row #allows the db to be referenced by column names
    c = conn.cursor()
    
    query = f"INSERT INTO {table} {attributes[table]} VALUES {placeholders[table]}"
    c.execute(query, values)
    conn.commit()
    conn.close()
    
    
def get_pk(table):
    match table: #getting input for each attr for a specific table
        case 'components': 
            pk = request.form.get('model')
        case 'operators':
            pk = request.form.get('operator_number')
        case 'vehicles':
            pk = request.form.get('plate_number')
        case 'routes':
            pk = request.form.get('route_id')
    return pk
    
    
def delete_record(table, pk_value):
    primary_key = {'components': 'model','operators': 'operator_number', 'vehicles': 'plate_number', 'routes': 'route_id'}
    conn = sqlite3.connect('transport.db')
    conn.execute('PRAGMA foreign_keys = ON;')
    c = conn.cursor()
    query = f"DELETE FROM {table} WHERE {primary_key[table]}=?"
    c.execute(query, (pk_value,))
    conn.commit()
    conn.close()


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


    
@app.route('/')
def index():
    return redirect('/crud')

@app.route('/crud', methods=['POST', 'GET'])
def crud():
    return render_template('crud.html')


@app.route('/showtables')
def show_tables():
    vehicles, components, operators, routes = get_tables()
    return render_template('showtables.html', vehicles=vehicles, components=components, operators=operators, routes=routes)


@app.route('/crud/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        table = request.form.get('form_type')
        values = get_record(table)
        try:
            create_record(table, values)
            return redirect('/crud/create')
        except sqlite3.IntegrityError as e:
            return f'Error with {e}'
        except Exception as e:
            return f'{e}'
    else:
        vehicles, components, operators, routes = get_tables() #for dropdown menu of foreign keys
        return render_template('create.html', vehicles=vehicles, components=components, operators=operators, routes=routes)
    

@app.route('/crud/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        table = request.form.get('form_type')
        values = get_record(table)
        try:
            update_record(table, values)
            return redirect('/crud/update')
        except Exception as e:
            return f'{e}'
    else:
        vehicles, components, operators, routes = get_tables() #for dropdown menu of foreign keys
        return render_template('update.html', vehicles=vehicles, components=components, operators=operators, routes=routes)


@app.route('/crud/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        table = request.form.get('form_type')
        pk = get_pk(table)
        try:
            delete_record(table, pk)
            return redirect('/crud/delete')
        except Exception as e:
            return f'{e}'
    else:
        vehicles, components, operators, routes = get_tables() #for dropdown menu of foreign keys
        return render_template('delete.html', vehicles=vehicles, components=components, operators=operators, routes=routes)

if __name__ == "__main__":
    app.run(debug=True)
    