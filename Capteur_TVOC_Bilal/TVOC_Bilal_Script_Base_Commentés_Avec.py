import time
from pinpong.board import I2C,Board

# code de base supprimés (import pigpio import time)
 

# Identification(id) du capteur CCS811. 
# Pour trouver cela faire i2cdetect -y 4 sur un terminal en putty ssh.

# Tous les parametrès de bases n'ont pas été touché. 
# Elle sont de base de l'auteur Sasa Saftic (Sparkfuns éditeur de base Nathan Seidle) 
#----------------------------#
CCS811_ADDR = 0x5A  
CSS811_STATUS = 0x00
CSS811_MEAS_MODE = 0x01
CSS811_ALG_RESULT_DATA = 0x02
CSS811_RAW_DATA = 0x03
CSS811_ENV_DATA = 0x05
CSS811_NTC = 0x06
CSS811_THRESHOLDS = 0x10
CSS811_BASELINE = 0x11
CSS811_HW_ID = 0x20
CSS811_HW_VERSION = 0x21
CSS811_FW_BOOT_VERSION = 0x23
CSS811_FW_APP_VERSION = 0x24
CSS811_ERROR_ID = 0xE0
CSS811_APP_START = 0xF4
CSS811_SW_RESET = 0xFF
#-----------------------------#

# Une classe de base sous le nom de CCS811.
class CCS811:
 
    # Méthode Construcuteur (démmare premièrement).
    def __init__(self):

        """ self.pi = pigpio.pi()  """
        # Initialise la carte UNIHIKER.
        Board("UNIHIKER").begin()
        # Pour initialiser un objet I2C.
        self.i2c = I2C()

        # Ces lignes assignent la valeur 0 à l'attribut tVOC et à l'attribut CO2.
        self.tVOC = 0
        self.CO2 = 0
        


# Pour gérer les erreurs lors de la communication I2C (affichages des erreurs).
    def print_error(self):
       
       """  error = self.pi.i2c_read_byte_data(self.device, CSS811_ERROR_ID) """

        error = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_ERROR_ID, 1)[0]
        message = 'Error: '

        if error & 1 << 5:
            message += 'HeaterSupply '
        elif error & 1 << 4:
            message += 'HeaterFault '
        elif error & 1 << 3:
            message += 'MaxResistance '
        elif error & 1 << 2:
            message += 'MeasModeInvalid '
        elif error & 1 << 1:
            message += 'ReadRegInvalid '
        elif error & 1 << 0:
            message += 'MsgInvalid '

        print(message)

# Permet de vérifier si une erreur est présente dans le capteur CCS811
    def check_for_error(self):

        """ value = self.pi.i2c_read_byte_data(self.device, CSS811_STATUS) """

        value = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return value & 1 << 0

# La fonction app_valid est utilisée pour vérifier si l'application du capteur CCS811 est valide.
    def app_valid(self):

        """ value = self.pi.i2c_read_byte_data(self.device, CSS811_STATUS) """
        value = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return value & 1 << 4

# Utiliser pour configurer le mode de fonctionnement du capteur CCS811.
    def set_drive_mode(self, mode):
        if mode > 4:
            mode = 4

""" setting = self.pi.i2c_read_byte_data(self.device, CSS811_MEAS_MODE) """
        setting = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_MEAS_MODE, 1)[0]
        setting &= ~(0b00000111 << 4)
        setting |= (mode << 4)
        """ self.pi.i2c_write_byte_data(self.device, CSS811_MEAS_MODE, setting) """
        self.i2c.writeto_mem(CCS811_ADDR, CSS811_MEAS_MODE,setting)
        
# Cette méthode fait partie d'une classe Python utilisée pour interagir avec le capteur CCS811. 
# Un capteur de qualité de l'air capable de mesurer le CO2 et les composés organiques volatils totaux (TVOC).
    def configure_ccs811(self):
       """  hardware_id = self.pi.i2c_read_byte_data(self.device, CSS811_HW_ID) """
        hardware_id = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_HW_ID, 1)[0]


        if hardware_id != 0x81:
            raise ValueError('CCS811 not found. Please check wiring.')

        if self.check_for_error():
            self.print_error()
            raise ValueError('Error at Startup.')

        if not self.app_valid():
            raise ValueError('Error: App not valid.')

        """ self.pi.i2c_write_byte(self.device, CSS811_APP_START) """
        self.i2c.writeto(CCS811_ADDR, bytes([CSS811_APP_START]))

        if self.check_for_error():
            self.print_error()
            raise ValueError('Error at AppStart.')

        self.set_drive_mode(1)

        if self.check_for_error():
            self.print_error()
            raise ValueError('Error at setDriveMode.')

# La fonction setup du capteur CCS811 est. 
# Conçue pour initialiser le capteur et obtenir la valeur de référence (baseline).
    def setup(self):
        print('Starting CCS811 Read')
        self.configure_ccs811()

        result = self.get_base_line()

        print("baseline for this sensor: 0x")
        if result < 0x100:
            print('0')
        if result < 0x10:
            print('0')
        print(result)

# Lire une valeur de baseline à partir d'un capteur CCS811 via l'interface I²C.
    def get_base_line(self):
        """ a, b = self.pi.i2c_read_i2c_block_data(self.device, CSS811_BASELINE, 2) """
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_BASELINE, 2)
        baselineMSB = data[0]
        baselineLSB = data[1]
        baseline = (baselineMSB << 8) | baselineLSB
        return baseline

# Vérifier si de nouvelles données sont disponibles à partir du capteur CCS811.
    def data_available(self):
        """ value = self.pi.i2c_read_byte_data(self.device, CSS811_STATUS) """
        value = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_STATUS, 1)[0]
        return value & 1 << 3

# Conçue pour configurer le capteur.
# Et lire en continu les résultats de qualité de l'air, tels que les niveaux de CO2 et de TVOC.

    def run(self):
        self.setup()

        while True:
            if self.data_available():
                self.read_logorithm_results()
                print("CO2[%d] tVOC[%d]" % (self.CO2, self.tVOC))
            elif self.check_for_error():
                self.print_error()

            time.sleep(1)
# Utilisée pour lire les résultats d'algorithme du capteur CCS811. 

    def read_logorithm_results(self):
        """ b, d = self.pi.i2c_read_i2c_block_data(self.device, CSS811_ALG_RESULT_DATA, 4) """
        data = self.i2c.readfrom_mem(CCS811_ADDR, CSS811_ALG_RESULT_DATA, 4)

        co2MSB = data[0]
        co2LSB = data[1]
        tvocMSB = data[2]
        tvocLSB = data[3]

        self.CO2 = (co2MSB << 8) | co2LSB
        self.tVOC = (tvocMSB << 8) | tvocLSB


# Utilisée pour déterminer si un fichier Python est exécuté en tant que script principal 
# Ou s'il est importé en tant que module dans un autre fichier.
if __name__ == "__main__" :

# Crée une instance de la classe ccs811
    c = CCS811()

# Cette méthode est appelée sur l'instance c de la classe ccs811.
    c.run() 
 

""" 
Ceci était pour ne pas faire de boucle en permanance un resultat pour une seule fois. 
    c.read_logorithm_results()
    print(c.CO2)
    print(c.tVOC) """
