from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Cambia a tu usuario de MySQL
app.config['MYSQL_PASSWORD'] = ''  # Cambia a tu contraseña de MySQL
app.config['MYSQL_DB'] = 'municipio'  # Base de datos que creaste

mysql = MySQL(app)

# Ruta principal (ver ubicaciones y dispositivos)
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()

    cur.execute("SELECT * FROM devices")
    devices = cur.fetchall()

    return render_template('index.html', locations=locations, devices=devices)

# Ruta para agregar una nueva ubicación (lugar, oficina y encargado)
@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        place = request.form['place']
        office = request.form['office']
        manager = request.form['manager']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO locations (place, office, manager) VALUES (%s, %s, %s)", (place, office, manager))
        mysql.connection.commit()
        return redirect(url_for('index'))
    
    return render_template('add_location.html')

# Ruta para agregar un nuevo dispositivo (computadora o impresora)
@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        device_type = request.form['type']
        location_id = request.form['location_id']
        brand = request.form['brand']
        model = request.form['model']
        status = request.form['status']
        notes = request.form['notes']
        
        # Especificaciones de la computadora
        processor = request.form.get('processor')
        ram = request.form.get('ram')
        power_supply = request.form.get('power_supply')
        disk = request.form.get('disk')
        
        # Especificaciones de la impresora
        connection = request.form.get('connection')
        ip_address = request.form.get('ip_address') if connection == 'IP' else None

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO devices (type, location_id, brand, model, status, notes, processor, ram, power_supply, disk, connection, ip_address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (device_type, location_id, brand, model, status, notes, processor, ram, power_supply, disk, connection, ip_address))
        mysql.connection.commit()
        return redirect(url_for('index'))

    # Obtener las ubicaciones para mostrarlas en el formulario
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()

    return render_template('add_device.html', locations=locations)


if __name__ == '__main__':
    app.run(debug=True)
