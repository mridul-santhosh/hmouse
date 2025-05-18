import btfpy

def callback(clientnode,operation,cticn):

  if(operation == btfpy.LE_CONNECT):
    # clientnode has just connected
    print("Connected")
  elif(operation == btfpy.LE_READ):
    # clientnode has just read local characteristic index cticn
    pass
  elif(operation == btfpy.LE_WRITE):
    # clientnode has just written local characteristic index cticn
    pass
  elif(operation == btfpy.LE_DISCONNECT):
    # clientnode has just disconnected
    # uncomment next line to stop LE server when client disconnects
    # return(btfpy.SERVER_EXIT)
    # otherwise LE server will continue and wait for another connection
    # or operations from other clients that are still connected
    print("Disconnected")
    return(btfpy.SERVER_EXIT)
  elif(operation == btfpy.LE_TIMER):
    # The server timer calls here every timerds deci-seconds 
    # clientnode and cticn are invalid
    # This is called by the server not a client    
    pass
  elif(operation == btfpy.LE_KEYPRESS):
    # Only active if Keys_to_callback(btfpy.KEY_ON,0) has been called before Le_server()
    # clientnode is invalid
    # cticn = key code
    #       = ASCII code of key (e.g. a=97) OR
    #         btferret custom code for other keys such as Enter, Home, PgUp
    #         Full list in keys_to_callback() section
    pass
    
  return(btfpy.SERVER_CONTINUE)  


if btfpy.Init_blue("devices.txt") == 0:
  exit(0)

print()
print("The local device must be the first entry in devices.txt")
print("(My Pi) that defines the LE characteristics")  
print("Connection/pairing problems? See notes in le_server.py")

  # Set My data (index 1) value  
btfpy.Write_ctic(btfpy.Localnode(),1,"Hello world",0)    


# ********* CONNECTION/PAIRING problems ********
# If you have connection problems - especially from
# Android/iOS/Windows, uncomment these four commands
# to use a random address. This creates a new identity
# for the server, with a different Bluetooth address.
# Choose 6 bytes for random address
# 2 hi bits of the 1st byte must be 1

#randadd  = [0xD3,0x56,0xDB,0x24,0x32,0xA0]
#btfpy.Set_le_random_address(randadd)
#btfpy.Set_le_wait(5000)     # wait 5 seconds for connection/pairing                                         
#btfpy.Le_pair(btfpy.Localnode(),btfpy.JUST_WORKS,0)  # Easiest option, but if client requires
                                                     # passkey security - remove this command  
  
#******** end CONNECTION problems *******


btfpy.Le_server(callback,0)   # timerds=0
    
btfpy.Close_all()
