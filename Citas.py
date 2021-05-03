class Citas:
    def __init__(self, id_paciente, id_medico, fecha, hora, motivo_cita, estado):
        self.id_medico = id_medico
        self.id_paciente = id_paciente
        self.fecha = fecha
        self.hora = hora
        self.motivo_cita = motivo_cita
        self.estado = estado
 
    def getPaciente(self):
        return self.id_paciente

    def getMedico(self):
        return self.id_medico

    def getFecha(self):
        return self.fecha

    def getHora(self):
        return self.hora

    def getMotivo(self):
        return self.motivo_cita

    def getEstado(self):
        return self.estado

    def setPaciente(self, id_paciente):
        self.id_paciente = id_paciente

    def setMedico(self, id_medico):
        self.id_medico = id_medico

    def setFecha(self, fecha):
        self.fecha = fecha

    def setHora(self, hora):
        self.hora = hora
    
    def setMotivo(self, motivo_cita):
        self.motivo_cita = motivo_cita

    def setEStado(self, estado):
        self.estado = estado