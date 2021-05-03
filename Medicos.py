class Medicos:
    def __init__(self, nombre, apellido, date, sexo, user, especialidad,  password, phone):
        self.nombre = nombre
        self.apellido = apellido
        self.date = date
        self.sexo = sexo
        self.user = user
        self.password = password
        self.phone = phone
        self.especialidad= especialidad

    # METODOS 
    def getEspecialidad(self):
        return self.especialidad
    
    def getNombre(self):
        return self.nombre

    def getApellido(self):
        return self.apellido

    def getDate(self):
        return self.date

    def getSexo(self):
        return self.sexo

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password

    def getPhone(self):
        return self.phone

    # METODOS SET
    def setEspecialidad(self, especialidad):
        self.especialidad = especialidad

    def setNombre(self, nombre):
        self.nombre = nombre

    def setApellido(self, apellido):
        self.apellido = apellido

    def setDate(self, date):
        self.date = date

    def setSexo(self, sexo):
        self.sexo = sexo

    def setUser(self, user):
        self.user = user

    def setPassword(self, password):
        self.password = password

    def setPhone(self, phone):
        self.phone = phone