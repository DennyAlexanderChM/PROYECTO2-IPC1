from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_cors import CORS
from Personas import Persona
from Medicamentos import Medicamentos
from Medicos import Medicos
from Citas import Citas
import json

app = Flask(__name__)
CORS(app)
app.secret_key = "mysecretkey"
# Variables globales
citas = []
carrito = []
usuarios = []
enfermeras = []
doctores = []
medicamentos = []
datos_login = []
login = False
id_medicamento = 1

# Buscar usuarios---Incio de sesion
@app.route('/login', methods=['POST'])
def searchUser():
    error = False
    global datos_login
    global usuarios, enfermeras, doctores, login
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['pass'] == '1234':
            datos_login = ['admin',True]
            login = True
            return render_template('Admin/admin.html')
        if not login and usuarios:
            for i in usuarios:
                if i.getUser() == request.form['user'] and i.getPassword() == request.form['pass']:
                    datos_login = ['user',i.getUser()]
                    login = True
                    return render_template('user/home.html', nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

        if not login and enfermeras:
            for i in enfermeras:
                if i.getUser() == request.form['user'] and i.getPassword() == request.form['pass']:
                    datos_login = ['nurse',i.getUser()]
                    login = True
                    return render_template('Enfermeras/home.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

        if not login and doctores:
            for i in doctores:
                if i.getUser() == request.form['user'] and i.getPassword() == request.form['pass']:
                    datos_login = ['doctor',i.getUser()]
                    login = True
                    return render_template('Medicos/home.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), especialidad = i.getEspecialidad(),tel=i.getPhone(), contra=i.getPassword())
        if not login:
            error = True
            return render_template('Home/login.html', error=True)

# añadir un nuevo usuario
@ app.route('/perfil', methods=['POST'])
def addUsser():
    global usuarios
    global datos_login
    global login
    sexo = 'No especificado'
    if request.method == 'POST':
        user_paciente = request.form['username']
        agregar = verificar_repetido(user_paciente)
        if agregar:
            nuevo = Persona(request.form['name'], request.form['lastname'], request.form['date'], request.form['sex'], request.form['username'], request.form['password'], request.form['tel'])
            usuarios.append(nuevo)
            datos_login = ['user',user_paciente]
            login = True
            return redirect(url_for('home_user',id_user = user_paciente))
        else:
            flash('Usuario existente')
            return render_template('check.html',nombre=request.form['name'], apellido=request.form['lastname'], fecha_nacimiento=request.form['date'], sexo=request.form['sex'], tel=request.form['tel'])

# Carga masiva de usuarios
@app.route('/usuario', methods=['POST'])
def AgregarUsuario():
    # Referencia a la lista global
    global usuarios
    temp_user = Persona(request.json['Nombre'], request.json['Apellido'], request.json['Fecha'], request.json['Sexo'],request.json['Usuario'], request.json['Contraseña'], request.json['Teléfono'])
    usuarios.append(temp_user)
    return jsonify('Agregado correctamente')

# Carga masiva enfermeras
@app.route('/enfermeras', methods=['POST'])
def Agregar_enfermera():
    # Referencia a la lista global
    global enfermeras
    temp_user = Persona(request.json['Nombre'], request.json['Apellido'], request.json['Fecha'], request.json['Sexo'],request.json['Usuario'], request.json['Contraseña'], request.json['Teléfono'])
    enfermeras.append(temp_user)
    return jsonify('Agregado correctamente')

# Carga masiva de medicos
@app.route('/medicos', methods=['POST'])
def Agregar_medicos():
    # Referencia a la lista global
    global doctores
    temp_user = Medicos(request.json['Nombre'], request.json['Apellido'], request.json['Fecha'], request.json['Sexo'],request.json['Usuario'], request.json['Especialidad'],request.json['Contraseña'], request.json['Teléfono'])
    doctores.append(temp_user)
    return jsonify('Agregado correctamente')

# Carga masiva de medicamentos
@app.route('/medicamentos', methods=['POST'])
def Agregar_medicamentos():
    # Referencia a la lista global
    global medicamentos
    global id_medicamento
    temp_medicine = Medicamentos(id_medicamento, request.json['Nombre'], request.json['Precio'], request.json['Descripción'], request.json['Cantidad'])
    medicamentos.append(temp_medicine)
    id_medicamento +=1
    return jsonify('Agregado correctamente')
    
'''
----------editar datos desde el admin--------------
'''
@app.route('/edit/user/<string:user_name>')
def page_user(user_name):
    global usuarios
    for i in usuarios:
        if user_name == i.getUser():
            return render_template('Admin/user.html', nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

@app.route('/edit/nurse/<string:user_name>')
def page_nurse(user_name):
    global enfermeras
    for i in enfermeras:
        if user_name == i.getUser():
            return render_template('Admin/nurse.html', nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

@app.route('/edit/medic/<string:user_name>')
def page_doctor(user_name):
    global doctores
    for i in doctores:
        if user_name == i.getUser():
            return render_template('Admin/doctor.html', especialidad = i.getEspecialidad(), nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

@app.route('/edit/medicine/<string:id>')
def page_medicine(id):
    global medicamentos
    for i in medicamentos:
        if int(id) == int(i.getId()):
            
            return render_template('Admin/medicine.html', id = i.getId(), nombre = i.getNombre(), descripcion = i.getDescripcion(), precio= i.getPrecio(), cantidad = i.getCantidad())

'''
----------borrar datos desde el admin--------------
'''
@app.route('/delete/user/<string:user_name>',methods = ['POST','GET'])
def delete_user(user_name):
    global usuarios
    for i in range(len(usuarios)):
        if user_name == usuarios[i].getUser():
            del usuarios[i]
            return redirect(url_for('tablas'))

@app.route('/delete/nurse/<string:user_name>', methods = ['POST','GET'])
def delete_nurse(user_name):
    global enfermeras
    for i in range(len(enfermeras)):
        if user_name == enfermeras[i].getUser():
            del enfermeras[i]
            return redirect(url_for('tablas'))

@app.route('/delete/medic/<string:user_name>', methods = ['POST','GET'])
def delete_doctor(user_name):
    global doctores
    for i in range(len(doctores)):
        if user_name == doctores[i].getUser():
            del doctores[i]
            return redirect(url_for('tablas'))

@app.route('/delete/medicine/<string:id>', methods = ['POST','GET'])
def delete_medicine(id):
    global medicamentos
    for i in range(len(medicamentos)):
        if int(id) == int(medicamentos[i].getId()):
            del medicamentos[i]
            return redirect(url_for('tablas'))

#Editar un usuario ----usuario---admin
@app.route('/edit/user/<string:user_name>', methods=['POST'])
def editUsser(user_name):
    global usuarios
    global datos_login
    new_user = request.form['username']
    for i in range(len(usuarios)):
        if user_name == usuarios[i].getUser():
            if usuarios[i].getUser() == new_user:
                usuarios[i].setNombre(request.form['nombre'])
                usuarios[i].setApellido(request.form['apellido'])
                usuarios[i].setDate(request.form['fecha'])
                usuarios[i].setPassword(request.form['pass'])
                usuarios[i].setPhone(request.form['telefono'])
                usuarios[i].setSexo(request.form['sexo'])
                flash('¡Cambios Guardados!')
                if datos_login[0] == 'admin':
                    return redirect(url_for('page_user', user_name = new_user))
                else:
                    return redirect(url_for('user_dates', id_user = new_user))
            else:
                agregar = verificar_repetido(new_user)
                if agregar:
                    usuarios[i].setUser(request.form['username'])
                    usuarios[i].setNombre(request.form['nombre'])
                    usuarios[i].setApellido(request.form['apellido'])
                    usuarios[i].setDate(request.form['fecha'])
                    usuarios[i].setPassword(request.form['pass'])
                    usuarios[i].setPhone(request.form['telefono'])
                    usuarios[i].setSexo(request.form['sexo'])
                    flash('¡Cambios Guardados!')
                    if datos_login[0] == 'admin':
                        return redirect(url_for('page_user', user_name = usuarios[i].getUser()))
                    else:
                        return redirect(url_for('user_dates', id_user = usuarios[i].getUser()))
                else:
                    flash('¡Usuario existente!')
                    if datos_login[0] == 'admin':
                        return redirect(url_for('page_user', user_name = user_name))
                    else:
                        return redirect(url_for('user_dates', id_user = user_name))
                    

#Editar enfermera
@app.route('/edit/nurse/<string:user_name>', methods=['POST'])
def editNurse(user_name):
    global enfermeras
    global datos_login
    new_user = request.form['username']
    for i in range(len(enfermeras)):
        if user_name == enfermeras[i].getUser():
            if enfermeras[i].getUser() == new_user:
                enfermeras[i].setNombre(request.form['nombre'])
                enfermeras[i].setApellido(request.form['apellido'])
                enfermeras[i].setDate(request.form['fecha'])
                enfermeras[i].setPassword(request.form['pass'])
                enfermeras[i].setPhone(request.form['telefono'])
                enfermeras[i].setSexo(request.form['sexo'])
                flash('¡Cambios Guardados!')
                if datos_login[0] == 'admin':
                    return redirect(url_for('page_nurse', user_name = new_user))
                else:
                    return redirect(url_for('nurse_dates', id_user = new_user))
            else:
                agregar = verificar_repetido(new_user)
                if agregar:
                    enfermeras[i].setUser(request.form['username'])
                    enfermeras[i].setNombre(request.form['nombre'])
                    enfermeras[i].setApellido(request.form['apellido'])
                    enfermeras[i].setDate(request.form['fecha'])
                    enfermeras[i].setPassword(request.form['pass'])
                    enfermeras[i].setPhone(request.form['telefono'])
                    enfermeras[i].setSexo(request.form['sexo'])
                    flash('¡Cambios Guardados!')
                    if datos_login[0] == 'admin':
                        return redirect(url_for('page_nurse', user_name = enfermeras[i].getUser()))
                    else:
                        return redirect(url_for('nurse_dates', id_user = enfermeras[i].getUser()))
                else:
                    flash('¡Usuario existente!')
                    if datos_login[0] == 'admin':
                        return redirect(url_for('page_nurse', user_name = user_name))
                    else:
                        return redirect(url_for('nurse_dates', id_user = user_name))
                    

#Editar un doctores
@app.route('/edit/medic/<string:user_name>', methods=['POST'])
def editDoctor(user_name):
    global doctores
    global datos_login
    global login
    new_user = request.form['username']
    for i in range(len(doctores)):
        if user_name == doctores[i].getUser():
            if doctores[i].getUser() == new_user:
                doctores[i].setNombre(request.form['nombre'])
                doctores[i].setApellido(request.form['apellido'])
                doctores[i].setDate(request.form['fecha'])
                doctores[i].setPassword(request.form['pass'])
                doctores[i].setPhone(request.form['telefono'])
                doctores[i].setSexo(request.form['sexo'])
                doctores[i].setEspecialidad(request.form['especialidad'])
                flash('¡Cambios Guardados!')
                if datos_login[0] == 'admin':
                    return redirect(url_for('page_doctor', user_name = new_user))
                else:
                    return redirect(url_for('medic_dates', id_user = new_user))
            else:
                agregar = verificar_repetido(new_user)
                if agregar:
                    doctores[i].setUser(request.form['username'])
                    doctores[i].setNombre(request.form['nombre'])
                    doctores[i].setApellido(request.form['apellido'])
                    doctores[i].setDate(request.form['fecha'])
                    doctores[i].setPassword(request.form['pass'])
                    doctores[i].setPhone(request.form['telefono'])
                    doctores[i].setSexo(request.form['sexo'])
                    doctores[i].setEspecialidad(request.form['especialidad'])
                    flash('¡Cambios Guardados!')
                    if datos_login[0] == 'admin':
                        return redirect(url_for('page_doctor', user_name = doctores[i].getUser()))
                    else:
                        return redirect(url_for('medic_dates', id_user = doctores[i].getUser()))
                else:
                    flash('¡Usuario existente!')
                    if datos_login[0] == 'admin':
                        return redirect(url_for('page_doctor', user_name = user_name))
                    else:
                        return redirect(url_for('medic_dates', id_user = user_name))

#Editar un medicamento
@app.route('/edit/medicine/<string:m_Id>', methods=['POST'])
def editMedicine(m_Id):
    global medicamentos
    for i in range(len(medicamentos)):
        if int(m_Id) == int(medicamentos[i].getId()):
            if medicamentos[i].getNombre() ==  request.form['nombre']:
                medicamentos[i].setPrecio(request.form['precio'])
                medicamentos[i].setCantidad(request.form['cantidad'])
                medicamentos[i].setDescripcion(request.form['descripcion'])
                flash('¡Cambios Guardados!')
                return redirect(url_for('page_medicine', id = m_Id))
            else:
                agregar = verificar_medicamento(request.form['nombre'])
                if agregar:
                    medicamentos[i].setNombre(request.form['nombre'])
                    medicamentos[i].setPrecio(request.form['precio'])
                    medicamentos[i].setCantidad(request.form['cantidad'])
                    medicamentos[i].setDescripcion(request.form['descripcion'])
                    flash('¡Cambios Guardados!')
                    return redirect(url_for('page_medicine', id = m_Id))
                else:
                    flash('¡Medicamento existente!')
                    return redirect(url_for('page_medicine', id = m_Id))

def verificar_medicamento(nombre_):
    global  medicamentos
    Agregar = True
    for i in medicamentos:
        if i.getNombre() == nombre_:
            Agregar = False
    return Agregar

#Método para verificar usuario existente
def verificar_repetido(nombre_usuario):
    global usuarios, enfermeras, doctores
    Agregar = True
    for i in usuarios:
        if i.getUser() == nombre_usuario:
            Agregar = False
    if Agregar:
        for i in enfermeras:
            if i.getUser() == nombre_usuario:
                Agregar = False
    if Agregar:
        for i in doctores:
            if i.getUser() == nombre_usuario:
                Agregar = False
    return Agregar

# PESTAÑAS DE HTML
# Pestaña de inicio
@app.route('/')
def home():
    return render_template('home.html')

# Inicio de sesión
@app.route('/login')
def login_():
    global login
    global datos_login
    if login == True:
        if datos_login[0]=='admin':
            return render_template('Admin/admin.html')
        elif datos_login[0] == 'user':
            return redirect(url_for('home_user', id_user = datos_login[1]))
        elif datos_login[0] == 'nurse':
            return redirect(url_for('home_nurse', id_user = datos_login[1]))
        elif datos_login[0] == 'doctor':
            return redirect(url_for('home_doctor', id_user = datos_login[1]))
    else:
        return render_template('/Home/login.html')

# cerrar sesión
@app.route('/salir')
def logout():
    global datos_login
    global login
    login = False
    datos_login = []
    return render_template('/Home/login.html')

# Mas informacion
@app.route('/about')
def about():
    return render_template('Home/about.html')

# Informacion de contactos
@app.route('/contact')
def contact():
    return render_template('Home/contact.html')

# Informacion del estudiante
@app.route('/student')
def student():
    return render_template('Home/student.html')

# Sobre la covid
@app.route('/covid')
def about_covid():
    return render_template('Home/covid.html')

# Crear cuenta
@app.route('/check')
def check():
    return render_template('check.html')


'''
------------------------------------SECCIÓN DE MEDICOS--------------------------------------
'''
@app.route('/medico/home/<string:id_user>')
def home_doctor(id_user):
    global doctores
    if doctores:
        for i in doctores:
            if i.getUser() == id_user:
                return render_template('Medicos/home.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), especialidad = i.getEspecialidad(),fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

# Perfil
@app.route('/medico/perfil/<string:id_user>')
def medic_dates(id_user):
    global doctores
    if doctores:
        for i in doctores:
            if i.getUser() == id_user:
                return render_template('Medicos/profile.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), especialidad = i.getEspecialidad(),fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#cita (menu)
@app.route('/medico/citas/<string:id_user>')
def menu_citasd(id_user):
    global doctores
    if doctores:
        for i in doctores:
            if i.getUser() == id_user:
                return render_template('Medicos/cita.html', nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), especialidad = i.getEspecialidad(),fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#citas (pendites)
@app.route('/medico/cita/pendientes/<string:id_user>')
def citas_penditesd(id_user):
    global doctores
    global citas
    global usuarios
    citas_ = []
    if citas:
        j=1
        for i in citas:
            if i.getEstado() == 'Pendiente':
                for k in usuarios:
                    if k.getUser() == i.getPaciente():
                        tmp = (j,k.getNombre(),k.getApellido(),i.getPaciente(),i.getFecha(),i.getHora(),i.getMotivo(),i.getEstado())
                        citas_.append(tmp)
                        j += 1
    if doctores:
        for i in doctores:
            if i.getUser() == id_user:
                return render_template('Medicos/pendientes.html', citas=citas_, nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), especialidad = i.getEspecialidad(),fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#Citas (confirmadas---->asignadas al medico)
@app.route('/medico/cita/confirmadas/<string:id_user>')
def citas_confirmadasd(id_user):
    global doctores
    global citas
    citas_ = []
    if citas:
        j=1
        for i in citas:
            if i.getEstado() == 'Confirmada':
                if i.getMedico() == id_user:
                    for k in usuarios:
                        if k.getUser()==i.getPaciente():
                            tmp = (j,k.getNombre(),k.getApellido(),i.getPaciente(),i.getFecha(),i.getHora(),i.getMotivo())
                            citas_.append(tmp)
                            j += 1
    if doctores:
        for i in doctores:
            if i.getUser() == id_user:
                return render_template('Medicos/confirmadas.html',citas = citas_, nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), especialidad = i.getEspecialidad(),fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#Confirmar cita
@app.route('/medico/cita/confirmar',methods=['POST'])
def confirmar_citad():
    global citas
    global usuarios
    datos = []
    temp_medic = request.json['medico']
    temp_user = request.json['usuario']
    if citas:
        for i in range(len(citas)):
            if temp_user == citas[i].getPaciente():
                citas[i].setEStado('Confirmada')
                citas[i].setMedico(temp_medic)

        for i in citas:
            if i.getEstado() == 'Pendiente':
                if usuarios:
                    for k in usuarios:
                        if k.getUser() == i.getPaciente():
                            temp = {
                                'Nombre': k.getNombre(),
                                'Apellido':k.getApellido(),
                                'Usuario': i.getPaciente(),
                                'Fecha': i.getFecha(),
                                'Hora': i.getHora(),
                                'Motivo':i.getMotivo(),
                            }
                            datos.append(temp)

        return(jsonify(datos))
    salida = {"Mensaje":"A ocurrido un error"}
    return(jsonify(salida))

#rechazar cita
@app.route('/medico/cita/rechazar',methods=['POST'])
def rechazar_citad():
    global citas
    global usuarios
    datos = []
    temp_user = request.json['usuario']
    if citas:
        for i in range(len(citas)):
            if temp_user == citas[i].getPaciente():
                citas[i].setEStado('Rechazada')

        for i in citas:
            if i.getEstado() == 'Pendiente':
                if usuarios:
                    for k in usuarios:
                        if k.getUser() == i.getPaciente():
                            temp = {
                                'Nombre': k.getNombre(),
                                'Apellido':k.getApellido(),
                                'Usuario': i.getPaciente(),
                                'Fecha': i.getFecha(),
                                'Hora': i.getHora(),
                                'Motivo':i.getMotivo(),
                            }
                            datos.append(temp)
        return(jsonify(datos))
    salida = {"Mensaje":"A ocurrido un error"}
    return(jsonify(salida))

#Generar Receta
@app.route('/medico/receta/generar/<string:id_medic>')
def generar_receta(id_medic):
    global doctores
    if doctores:
        for i in doctores:
            if i.getUser() == id_medic:
                return render_template('Medicos/receta.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), especialidad = i.getEspecialidad(),fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#cita completada
@app.route('/medico/cita/completada', methods=['POST'])
def cita_completada():
    global citas
    global doctores
    temp_user = request.json['usuario']
    temp_medic = request.json['medico']
    datos = []
    if citas:
        for i in range(len(citas)):
            if temp_user == citas[i].getPaciente():
                citas[i].setEStado('completada')

        for i in citas:
            if i.getEstado() == 'Confirmada':
                if i.getMedico() == temp_medic:
                    for k in usuarios:
                        if k.getUser()==i.getPaciente():
                            temp = {
                                'Nombre': k.getNombre(),
                                'Apellido':k.getApellido(),
                                'Usuario': i.getPaciente(),
                                'Fecha': i.getFecha(),
                                'Hora': i.getHora(),
                                'Motivo':i.getMotivo(),
                            }
                            datos.append(temp)
        return(jsonify(datos))
                            
    salida = {"Mensaje":"A ocurrido un error"}
    return(jsonify(salida))

'''
------------------------------------SECCIÓN DE ENFERMERAS--------------------------------------
'''
@app.route('/Enfermera/home/<string:id_user>')
def home_nurse(id_user):
    global enfermeras
    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_user:
                return render_template('Enfermeras/home.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())


# Perfil
@app.route('/enfermera/perfil/<string:id_user>')
def nurse_dates(id_user):
    global enfermeras
    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_user:
                return render_template('Enfermeras/profile.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#cita (menu)
@app.route('/enfermeras/citas/<string:id_user>')
def menu_citas(id_user):
    global enfermeras
    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_user:
                return render_template('Enfermeras/cita.html', nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#citas (pendientes)
@app.route('/enfermera/cita/pendientes/<string:id_user>')
def citas_pendites(id_user):
    global enfermeras
    global citas
    global usuarios
    citas_ = []
    if citas:
        j=1
        for i in citas:
            if i.getEstado() == 'Pendiente':
                for k in usuarios:
                    if k.getUser() == i.getPaciente():
                        tmp = (j,k.getNombre(),k.getApellido(),i.getPaciente(),i.getFecha(),i.getHora(),i.getMotivo(),i.getEstado())
                        citas_.append(tmp)
                        j += 1
    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_user:
                return render_template('Enfermeras/pendientes.html',citas = citas_, nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#Citas (confirmadas)
@app.route('/enfermera/cita/confirmadas/<string:id_user>')
def citas_confirmadas(id_user):
    global enfermeras
    global citas
    global usuarios
    citas_ = []
    if citas:
        j=1
        for i in citas:
            if i.getEstado() == 'Confirmada':
                for k in usuarios:
                    if k.getUser()==i.getPaciente():
                        tmp = (j,k.getNombre(),k.getApellido(),i.getPaciente(),i.getFecha(),i.getHora(),i.getMotivo(),i.getEstado())
                        citas_.append(tmp)
                        j += 1
    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_user:
                return render_template('Enfermeras/confirmadas.html',citas = citas_, nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#Confirmar cita---->menú
@app.route('/enfermera/cita/confirmar/<string:id_nurse>/<string:id_user>')
def confirmar_cita(id_nurse,id_user):
    global citas
    global enfermeras
    global doctores
    global usuarios
    temp=[]
    medicos_temp = []
    if citas:
        for i in citas:
            if i.getPaciente()==id_user:
                if i.getEstado()=='Pendiente':
                    for k in usuarios:
                        if k.getUser() == i.getPaciente():
                            temp_=(k.getNombre(),k.getApellido(),i.getPaciente(), i.getFecha(),i.getHora(),i.getMotivo())
                            temp.append(temp_)
    if doctores:
        for i in doctores:
            temp_ = (i.getNombre(),i.getApellido(),i.getUser())
            medicos_temp.append(temp_)

    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_nurse:
                return render_template('Enfermeras/confirmar.html',medicos=medicos_temp, usuario2=id_user, cita = temp,nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#Confirmar cita
@app.route('/enfermera/cita/confirmar/<string:id_nurse>/<string:id_user>',methods=['POST'])
def asignar_cita(id_nurse,id_user):
    global citas
    global enfermeras
    global doctores
    medico_asignar = request.form['medico']
    if citas:
        for i in range(len(citas)):
            if id_user == citas[i].getPaciente():
                citas[i].setEStado('Confirmada')
                citas[i].setMedico(medico_asignar)
    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_nurse:
                flash('Listo')
                return redirect(url_for('citas_pendites', id_user = id_nurse))

#rechazar cita
@app.route('/enfermera/cita/rechazar/<string:id_nurse>/<string:id_user>')
def rechazar_cita(id_nurse,id_user):
    global citas
    global enfermeras
    if citas:
        for i in range(len(citas)):
            if id_user == citas[i].getPaciente():
                citas[i].setEStado('Rechazada')
    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_nurse:
                return redirect(url_for('citas_pendites', id_user = id_nurse))

#Generar Factura
@app.route('/enfermera/factura/generar/<string:id_nurse>')
def facturar_cita(id_nurse):
    global enfermeras
    global doctores
    medicos_temp = []
    if doctores:
        for i in doctores:
            temp_ = (i.getNombre(),i.getApellido(),i.getUser())
            medicos_temp.append(temp_)

    if enfermeras:
        for i in enfermeras:
            if i.getUser() == id_nurse:
                return render_template('Enfermeras/facturar.html',medicos=medicos_temp, nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

'''
------------------------------------SECCIÓN DE PACIENTES--------------------------------------
'''
#Productos
@app.route('/tienda')
def tienda():
    return render_template('user/tienda.html')

#cita (menu)
@app.route('/cita/<string:id_user>')
def cita_medica(id_user):
    global usuarios
    if usuarios:
        for i in usuarios:
            if i.getUser() == id_user:
                return render_template('user/cita.html', nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#Citas nueva
@app.route('/cita/nueva/<string:id_user>')
def cita_nueva(id_user):
    global usuarios
    if usuarios:
        for i in usuarios:
            if i.getUser() == id_user:
                return render_template('user/Nueva.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#Citas agregar
@app.route('/cita/nueva/<string:id_user>',methods=['POST'])
def cita_crear(id_user):
    global citas
    Agregar_cita = True
    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        motivo = request.form['motivo']
        if citas:
            for i in citas:
                if i.getPaciente()==id_user:
                    if i.getEstado() == 'Pendiente' or i.getEstado() == 'Aceptada':
                         Agregar_cita = False

        if Agregar_cita:
            temp_ = Citas(id_user, 'ninguno',fecha, hora, motivo, 'Pendiente')
            citas.append(temp_)
            flash('¡Cita agendada!')
            return redirect(url_for('cita_nueva', id_user = id_user))
        else:
            flash('¡Ya tienes una cita pendiente')
            return redirect(url_for('cita_nueva', id_user = id_user))

#Citas ver
@app.route('/lista/citas/<string:id_user>')
def cita_lista(id_user):
    global citas
    global usuarios
    citas_=[]
    if citas:
        j=1
        for i in citas:
            if i.getPaciente() == id_user:
                tmp = (j,i.getPaciente(),i.getFecha(),i.getHora(),i.getMotivo(),i.getEstado())
                citas_.append(tmp)
                j += 1
    
    if usuarios:
        for i in usuarios:
            if i.getUser() == id_user:
                return render_template('user/estado.html', citas = citas_, nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

# Perfil
@app.route('/user/perfil/<string:id_user>')
def user_dates(id_user):
    global usuarios
    if usuarios:
        for i in usuarios:
            if i.getUser() == id_user:
                return render_template('user/profile.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#pagina de inicio
@app.route('/user/home/<string:id_user>')
def home_user(id_user):
    global usuarios
    if usuarios:
        for i in usuarios:
            if i.getUser() == id_user:
                return render_template('user/home.html',nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())

#tienda
@app.route('/user/tienda/<string:id_user>')
def tienda_user(id_user):
    global usuarios
    global medicamentos
    medicamentos_disponibles=[]
    value = 1
    if medicamentos:
        for i in medicamentos:
            if int(i.getCantidad()) > value:
                temp = (i.getNombre(),i.getDescripcion(),i.getPrecio(),i.getCantidad(), i.getId())
                medicamentos_disponibles.append(temp)
    if usuarios:
        for i in usuarios:
            if i.getUser() == id_user:
                return render_template('user/tienda.html',medicamentos = medicamentos_disponibles,nombre=i.getNombre(), apellido=i.getApellido(), usuario=i.getUser(), fecha_nacimiento=i.getDate(), sexo=i.getSexo(), tel=i.getPhone(), contra=i.getPassword())


'''
------------------------------------SECCIÓN DEL ADMIN--------------------------------------
'''
# Perfil-----OPCIONES
@app.route('/date/tables')
def tablas():
    global usuarios, enfermeras, medicamentos, doctores
    users = []
    enfermeras_ = []
    medicamentos_ = []
    doctores_ = []
    if usuarios:
        j = 1
        for i in usuarios:
            temp = (j, i.getNombre(), i.getApellido(), i.getDate(), i.getSexo(), i.getUser(), i.getPassword(), i.getPhone())
            users.append(temp)
            j += 1

    if enfermeras:
        j = 1
        for i in enfermeras:
            temp = (j, i.getNombre(), i.getApellido(), i.getDate(), i.getSexo(), i.getUser(), i.getPassword(), i.getPhone())
            enfermeras_.append(temp)
            j += 1

    if doctores:
        j = 1
        for i in doctores:
            temp = (j,i.getNombre(), i.getApellido(), i.getDate(), i.getSexo(), i.getUser(),i.getEspecialidad(), i.getPassword(), i.getPhone())
            doctores_.append(temp)
            j += 1

    if medicamentos:
        j = 1
        for i in medicamentos:
            temp = (j,i.getNombre(), i.getPrecio(), i.getDescripcion(),i.getCantidad(),i.getId())
            medicamentos_.append(temp)
            j += 1

    return render_template('Admin/tables.html', users=users, enfermeras=enfermeras_, medicos=doctores_, medicina=medicamentos_)

#Obtener datos Pacientes
@app.route('/admin/datos/pacientes')
def datos_pacientes():
    global usuarios
    datos = []
    if usuarios:
        for i in usuarios:

            temp = {
                'Nombre': i.getNombre(),
                'Apellido':i.getApellido(),
                'Fecha': i.getDate(),
                'Sexo': i.getSexo(),
                'Usuario': i.getUser(),
                'Contraseña':i.getPassword(),
                'Teléfono':i.getPhone()
                }
            datos.append(temp)
        
        return(jsonify(datos))      

    salida = {"Mensaje":"A ocurrido un error"}
    return(jsonify(salida))

#Obtener datos Enfermeras
@app.route('/admin/datos/enfermeras')
def datos_enfermeras():
    global enfermeras
    datos = []
    if enfermeras:
        for i in enfermeras:
            temp = {
                'Nombre': i.getNombre(),
                'Apellido':i.getApellido(),
                'Fecha': i.getDate(),
                'Sexo': i.getSexo(),
                'Usuario': i.getUser(),
                'Contraseña':i.getPassword(),
                'Teléfono':i.getPhone()
                }
            datos.append(temp)
        
        return(jsonify(datos))      

    salida = {"Mensaje":"A ocurrido un error"}
    return(jsonify(salida))

#Obtener datos medicos
@app.route('/admin/datos/medicos')
def datos_medicos():
    global doctores
    datos = []
    if doctores:
        for i in doctores:
            temp = {
                'Nombre': i.getNombre(),
                'Apellido':i.getApellido(),
                'Fecha': i.getDate(),
                'Sexo': i.getSexo(),
                'Usuario': i.getUser(),
                'Contraseña':i.getPassword(),
                'Teléfono':i.getPhone(),
                'Especialidad':i.getEspecialidad()
                }
            datos.append(temp)
        
        return(jsonify(datos))      

    salida = {"Mensaje":"A ocurrido un error"}
    return(jsonify(salida))

#Obtener datos medicamentos
@app.route('/admin/datos/medicamentos')
def datos_medicamento():
    global medicamentos
    datos = []
    if medicamentos:
        for i in medicamentos:
            temp = {
                'Nombre': i.getNombre(),
                'Precio':i.getPrecio(),
                'Cantidad': i.getCantidad(),
                'Descripción': i.getDescripcion()
                }
            datos.append(temp)
        
        return(jsonify(datos))      

    salida = {"Mensaje":"A ocurrido un error"}
    return(jsonify(salida))

#Carga masiva---Ventanainicial
@app.route('/admin/add')
def cargas_masivas():
    return render_template('Admin/admin.html')

if __name__ == '__main__':
    app.run(debug=True)  # modo de prueba
