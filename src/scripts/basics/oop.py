# creación de clases y herencia en python
class Casa:
    def __init__(self, color, precio):
        self.color = color
        self.precio = precio
        self.luz = 0
        self.agua = 0
    
    def timbre_de_casa(self):
        print('ring ring')
    
    def prender_luz(self):
        print('Luz prendida')
        self.luz += 1
    
    def apagar_luz(self):
        print('Luz apagada')
        self.luz -= 1
    
    def abrir_llave_de_agua(self):
        print('Agua abierta')
        self.agua += 1
    
    def cerrar_llave_de_agua(self):
        print('Agua cerrada')
        self.agua -= 1

clase = Casa('rojo', 1000000)

clase.prender_luz()
print(clase.luz)

# podemos heredar sin necesidad de hacer super init
class Mansion(Casa):
    def prender_luz(self):
        print('Luz prendida en la mansion')
        self.luz += 10


mansion = Mansion('azul', 1000000000)
mansion.prender_luz()

print(mansion.color)
print(mansion.luz)