import Automation3270Library
import time

# delayTime = 2 # -1 uses the terminal pause (to see the program traverse though)
# userName = 'HERC01'
# password = 'CUL8TR'
# hostNamePort = '192.168.176.1:3270' #host name:port number
screenPath = 'Hercules\\'
screenrows = []
fileToRead = 'Hercules\\RandomFile.txt'



class Automation:
    """
        Automation Methods
        use x3270 (visible=True) to see terminal
        use s3270 (visible=False) to not see terminal
    """
    def __init__(self, userName, password, hostNamePort, visible=True, delayTime=0):
        # use x3270 (visible=True) to see terminal
        # use s3270 (visible=False) to not see terminal
        self.my3270 = Automation3270Library.Emulator(visible=visible)
        self.delayTime = delayTime
        self.userName = userName
        self.password = password
        self.hostNamePort = hostNamePort

    def login(self):
        """
            Logs in with supplied credentials
        """
        #connects to mainframe through hostname and port
        self.my3270.connect(self.hostNamePort)
        self.my3270.pause(self.delayTime)
        if not self.my3270.is_connected:
            print("Mainframe not connected!")
            exit(1)

        #Looks for the Login prompt
        loginTry=0
        while not self.my3270.string_found(23, 1, 'Logon ===>'):
            if loginTry > 2:
                print("Login not found")
                self.my3270.terminate()
            self.my3270.send_enter()
            loginTry += 1
            self.my3270.pause(self.delayTime)

        #Enters username credentials
        self.my3270.send_string(self.userName)
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()

        #Check is user is already logged in
        self.my3270.wait_for_field()
        if self.my3270.string_found(1, 12, 'LOGON REJECTED'):
            print('User {} is already logged in'.format(self.userName))
            self.my3270.terminate()
            exit(1)

        #Check is user is valid
        if self.my3270.string_found(1, 12, 'INVALID USERID'):
            print('User {} is not a valid user'.format(self.userName))
            self.my3270.terminate()
            exit(1)

        #Enters password credentials
        self.my3270.send_string(self.password)
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()
        
        #Goes to the menu screen
        self.my3270.wait_for_field()
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()
        self.my3270.wait_for_field()
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()

    def logout(self):
        """
            Logs out of session and terminates the terminal
        """
        while not self.my3270.string_found(5, 2, 'READY'):
            self.my3270.wait_for_field()
            self.my3270.send_pf3()
            time.sleep(.1)
            self.my3270.pause(self.delayTime)

        #Sends command to log user off
        self.my3270.gateway(5, 2, 'READY')
        self.my3270.wait_for_field()
        self.my3270.send_string('logoff')
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()
        self.my3270.pause(self.delayTime)
        
        #Terminates wc3270 program
        if self.my3270.string_found(23, 1, 'Logon ===>'):
            self.my3270.terminate()

    def view_dataset_list(self):
        """
            Traverses through the terminal to set the Data-set list for HERC01
        """
        #Checks that program is at the main menu
        # while not my3270.string_found(5, 2, 'Option ===>'):
        #     my3270.send_pf3()
        #     print('PF3 sent in test nav')
        #     my3270.pause(delayTime)

        #Enters "SPF like" productivity tool
        self.my3270.wait_for_field()
        self.my3270.gateway(5, 2, 'Option ===>')
        self.my3270.delete_field()
        self.my3270.pause(self.delayTime)
        self.my3270.send_string('2', ypos=5, xpos=14)
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()
        
        #Enters Utility menu
        self.my3270.wait_for_field()
        self.my3270.gateway(2, 2, 'Option  ===>')
        self.my3270.delete_field()
        self.my3270.pause(self.delayTime)
        self.my3270.send_string('3', ypos=2, xpos=15)
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()
        
        #Enters Dataset List
        self.my3270.wait_for_field()
        self.my3270.gateway(2, 2, 'Option  ===>')
        self.my3270.delete_field()
        self.my3270.pause(self.delayTime)
        self.my3270.send_string('4', ypos=2, xpos=15)
        self.my3270.pause(self.delayTime)
        self.my3270.send_enter()
        
        #Shows Dataset List
        self.my3270.wait_for_field()
        self.my3270.gateway(2, 2, 'Option ===>')
        self.my3270.send_enter()
        self.my3270.pause(self.delayTime)
        self.my3270.pause(self.delayTime)
        self.my3270.pause(self.delayTime)
        self.my3270.pause(self.delayTime)

