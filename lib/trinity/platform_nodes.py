import time, os
from subprocess import call

class WINDOWS_NODE:
    def __init__(self, debug=False, task=''):

        ascii_logo = '''                                             
                                °°                             
                              °@@@@@@°                          
                            *@@@@@@@@@@°                        
                          @@@@@@@@@@@@@@                       
                        °@@@@@@@oo@@@@@@@°                     
                        °@@@@@@@    @@@@@@@°                    
                        @@@@@@#      #@@@@@@                    
                      #@@@@@@        @@@@@@#                   
                      @@@@@@O@@@@@@@@@@@@@@@                   
                      .@@@@@@O@@@@@@@@@@@@@@@o                  
                  *@@O@@@@@@O@@@@@@@@@@@@@@@@@@*               
                o@@@@@O@@@@@@       .@@@@@@@@@@@@o             
              .@@@@@@@*@@@@@@@      @@@@@@@@@@@@@@@.           
              *@@@@@@@°  @@@@@@@.  .@@@@@@@  °@@@@@@@*          
            *@@@@@@#    .@@@@@@@*#@@@@@@@     #@@@@@@*         
            @@@@@@o       O@@@@@@@@@@@@O       o@@@@@@         
            #@@@@@@O**°°°*o#@@@@@@@@@@@@Oo*°°°**O@@@@@@O        
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
            °#@@@@@@@@@@@@@@@@@@#*.o@@@@@@@@@@@@@@@@@@#°        
                °*OO#####O*°          °*O#####OO*°             
                
                [Mind] --> [Computer] --> [Machine]
    '''

        print("Welcome to Trinity v0.12!")
        print(ascii_logo)
        start = input("Press <ENTER> to start!\n")
        
        #############################################################
        if debug:
            currentDirectory = os.getcwd()
            print("CURRENT DIRECTORY >> "+ str(currentDirectory))
        #############################################################

        time.sleep(1)

        print("Now opening Communications Client, please hold ...\n")

        # TODO: Insert logic to specify board

        os.system('start "Client" cmd /k "python client.py"')

        time.sleep(1)

        # TODO: Insert logic to specifc metric and other features of signal processing

        print("Now opening Signal Filtering and Processing Relay , please hold ...\n")

        time.sleep(2)

        os.system('start "SFPR" cmd /k "python sfpr.py"')

        time.sleep(1)

        # TODO: Insert logic to select which program should listen to SFPR

        print("Now opening Concentration output , please hold ...\n")

        time.sleep(1)

        os.system('start "Concentration OUT" cmd /k "python out.py"')

        exit = input("Press <ENTER> again to exit")


class LINUX_NODE:

    def __init__(self, debug=False, task=''):

        ascii_logo = '''                                             
                                °°                             
                              °@@@@@@°                          
                            *@@@@@@@@@@°                        
                          @@@@@@@@@@@@@@                       
                        °@@@@@@@oo@@@@@@@°                     
                        °@@@@@@@    @@@@@@@°                    
                        @@@@@@#      #@@@@@@                    
                      #@@@@@@        @@@@@@#                   
                      @@@@@@O@@@@@@@@@@@@@@@                   
                      .@@@@@@O@@@@@@@@@@@@@@@o                  
                  *@@O@@@@@@O@@@@@@@@@@@@@@@@@@*               
                o@@@@@O@@@@@@       .@@@@@@@@@@@@o             
              .@@@@@@@*@@@@@@@      @@@@@@@@@@@@@@@.           
              *@@@@@@@°  @@@@@@@.  .@@@@@@@  °@@@@@@@*          
            *@@@@@@#    .@@@@@@@*#@@@@@@@     #@@@@@@*         
            @@@@@@o       O@@@@@@@@@@@@O       o@@@@@@         
            #@@@@@@O**°°°*o#@@@@@@@@@@@@Oo*°°°**O@@@@@@O        
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
            °#@@@@@@@@@@@@@@@@@@#*.o@@@@@@@@@@@@@@@@@@#°        
                °*OO#####O*°          °*O#####OO*°             
                
                [Mind] --> [Computer] --> [Machine]
    '''

        print("Welcome to Trinity v0.12 [for linux]!")
        print(ascii_logo)
        start = input("Press <ENTER> to start!\n")

        board = ''
        metric = ''

        # get current working directory

        current_directory = os.getcwd()
        os.system(f"cd {current_directory}")
        print(f"Current directory: {current_directory}\n")

        time.sleep(1)

        print("Now opening Communications Client, please hold ...\n")

        # TODO: ADD logic to specify which board we want!
        # chooseBoards()

        call(['gnome-terminal', '-e', "python3 client.py"])

        time.sleep(1)

        # TODO: ADD logic to specify metric we want to look for
        # chooseMetric()

        print("Now opening Signal Filtering and Processing Relay , please hold ...\n")

        time.sleep(2)

        call(['gnome-terminal', '-e', "python3 sfpr.py"])

        time.sleep(1)

        print("Now opening Concentration output , please hold ...\n")

        time.sleep(1)

        call(['gnome-terminal', '-e', "python3 out.py"])

        exit = input("Press <ENTER> again to exit")