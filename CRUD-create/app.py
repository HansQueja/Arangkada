from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_tables():
    conn = sqlite3.connect('transportV1.db') #establish connection to the db
    conn.row_factory = sqlite3.Row
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


def get_record(table): #getting input for each attr for a specific table and returns it as a tuple
    match table:
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


def create_record(table, values): #setting values to the db with a query
    conn = sqlite3.connect('transportV1.db')
    conn.row_factory = sqlite3.Row #allows the db to be referenced by column names
    c = conn.cursor()
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
    query = f"INSERT INTO {table} {attributes[table]} VALUES {placeholders[table]}"
    c.execute(query, values)
    conn.commit()
    conn.close()


@app.route('/', methods=['POST', 'GET'])
def crud(): #for directory
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
        except sqlite3.IntegrityError as e: #not sure how to handle errors concerning duplicate pk's
            return f'Error with {e}'
        except Exception as e:
            return f'{e}'
    else:
        vehicles, components, operators, routes = get_tables() #for dropdown menu of foreign keys
        return render_template('create.html', vehicles=vehicles, components=components, operators=operators, routes=routes)
    

@app.route('/crud/update', methods=['POST', 'GET'])
def update():
    return render_template('update.html')


@app.route('/crud/delete', methods=['POST', 'GET'])
def delete():
    return render_template('delete.html')

#i'll add def read(); later

if __name__ == "__main__":
    app.run(debug=True)
    
