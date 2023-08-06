import os
from decouple import config 

class Core():

    myBase = "POSTGRES"
    myCulture = "es-EC"
    myDecimalSeparator = ","
    myGroupSeparator = "."
    myDateSeparator = "/"
    myShortDate = "dd/mm/YY"
    myLongDate = "dd/mm/YYYY"
    myDecimalDigits = 2
    myVariables = None
    mySession = None
    myDb = None
    myApp = None

    def __init__(self, myApp):
        """Contructor de la clase Core

        Args:
            myApp (flask): Objeto de la aplicación Flask
        """        
        self.myApp = myApp
        self.myApp.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.myApp.config['DEBUG'] = True
        self.myApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.setVariables()
        self.setRegion()
        # self.setSession(session)

    """
       SETTERS


    """

    def setVariables(self):
        """Método para asignar variables del ENV al SO
        """        
        self.myVariables = os.environ.copy()
        env = dict(os.environ)
        for key in env:
            self.myApp.config[key] = env[key]

    def setDbCnx(self, cnx):
        """Método para asignar la conección de la base de datos a demanda para la aplicación Flask

        Args:
            cnx (str): Cadena de conexión de la base de datos
        """        
        self.myApp.config['SQLALCHEMY_DATABASE_URI'] = cnx
# TESTED

    def setRegion(self):
        """Método para asignar la configuración regional de la aplicación
        """        
        self.myCulture = self.getVariable("myCulture")
        self.myDecimalSeparator = self.getVariable("myDecimalSeparator")
        self.myGroupSeparator = self.getVariable("myGroupSeparator")
        self.myDateSeparator = self.getVariable("myDateSeparator")
        self.myShortDate = self.getVariable("myShortDate")
        self.myLongDate = self.getVariable("myLongDate")
        self.myDecimalDigits = self.getVariable("myDecimalDigits")

    def setSession(self, session):
        """Método para asignar la sesión de la aplicación

        Args:
            session (dict): Diccionario con la sesión de la aplicación
        """        
        self.mySession = session

    """
       GETTERS


    """

    def getVariable(self, key):
        """Método para obtener una variable del ENV

        Args:
            key (str): Llave de la variable del ENV

        Returns:
            any: Valor de la variable del ENV
        """        
        return config(str(key).upper())

    def getAllVariables(self):
        """Método para obtener todas las variables del ENV

        Returns:
            list: Lista con todas las variables del ENV
        """        
        return self.myVariables

    def getEnvTableName(self, table):
        """Mètodo para obtener el nombre de la tabla del archivo ENV

        Args:
            table (str): Nombre de la tabla

        Returns:
            str: valor de la tabla del archivo ENV
        """        
        tableAtDomain = self.getVariable(table)
        domain = str(tableAtDomain).split("@")[1]
        tbl = self.getVariable(domain)
        return tbl

    def getEnvCnx(self, table):
        """Mètodo para obtener la cadena de conexión de la tabla del archivo ENV

        Args:
            table (str): Nombre de la tabla
        """        
        tableAtDomain = self.getVariable(table)
        domain = str(tableAtDomain).split("@")[1]
        cnx = self.getVariable(domain)
        self.setDbCnx(cnx)
