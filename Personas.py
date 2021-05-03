class Persona:
    def __init__(self, nombre, apellido, date, sexo, user, password, phone):
        self.nombre = nombre
        self.apellido = apellido
        self.date = date
        self.sexo = sexo
        self.user = user
        self.password = password
        self.phone = phone

    # METODOS GET
    # Creamos nuestros metodos para obtener la informacion, usando self

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
    # Creamos nuestros metodos para setear la informacion, usando el self y el parametro
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
