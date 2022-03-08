import  sys
import unicodedata
import re
from string import ascii_uppercase
import json



# ----------------- Enigma parametre initial -----------------
rotors = ("I","II","III")
ringSettings ="ABC" # nous permettra d'obtenir la clé de chiffre de chacun rotors
ringPositions = "DEF"# definie la postion init sur chaque rotor
rotatA = "Q" # rotation Sur I
rotatB = "E"
rotatC ="V"
alphabet = list(ascii_uppercase) # alphabet en majuscule





def RemoveAcents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
    

def LectureMessage(file):
    fs = open(file, 'r',encoding ='utf8')
    text = fs.read()
    if text == '':
        print("is empty")    
    texts = RemoveAcents(text.upper())
    move = re.sub(r"\s+", "" , texts)
    print('\n message IN : \t' + move )
    fs.close()
    return str(move)
    
        





def caesarShift(str, key):
	output = ""
    
	for i in range(0,len(str)):
		letter = str[i]
		code = ord(letter)
		if ((code >= 65) and (code <= 90)):
			letter = chr(((code - 65 + key) % 26) + 65)
		output = output + letter
	
	return output

def SauvegardeMessage(file, message):
    fs = open(file, 'w') 
    print("\nMessage enregistrer avec succes!!! \n ")
    fs.write(message)
    fs.close()
    
    
menu_options = {
    1: 'LectureMessage',
    2: 'EnregistreMessage',
    3: 'Cryptage et decryptage',
    4: 'Quitter',
    
    }

def Menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])    
    


 
def Egnima(rotors_file,rotors, messageIN):
   
    f = open(rotors_file, 'r')
    # Lecture du rotors et reflecteur dans le json
    json_object = json.load(f)
    rotors1 = json_object['rotors']
    reflector = json_object['reflecteurs']
    rotorsA = rotors1['RA']
    rotorsB = rotors1['RB']
    rotorsC = rotors1['RC']
    reflectorB  =  reflector['RFA']
    reflectorC  =  reflector['RFB']
    # liste contenant tous les rotors
    rotorDict = {"I":rotorsA,"II":rotorsB,"III":rotorsC}
    # liste contant la rotation initial sur chaque rotor
    rotorInitDict = {"I":rotatA,"II":rotatB,"III":rotatC}  
    
    rotationA = False
    rotationB = False
    rotationC = False
    
    if reflector=="UKW-B":
      reflectorDict = reflectorB
    else:
      reflectorDict = reflectorC
    
   # lecture des rotos
    rotorA = rotorDict[rotors[0]] # gauche
    rotorB = rotorDict[rotors[1]] # rotor du milieu
    rotorC = rotorDict[rotors[2]] # celui de droite
    # rotation 
    rotationA = rotorInitDict[rotors[0]]
    rotationB = rotorInitDict[rotors[1]]
    rotationC = rotorInitDict[rotors[2]]
    # il est important de savoir la postion initial de chaque rotors
    # sa nous permettra de tester if(rotation à change?)
    ALetter = ringPositions[0] # il est sur Q
    BLetter = ringPositions[1] # E
    CLetter = ringPositions[2]
    
    rotorASetting = ringSettings[0]
    keyA = alphabet.index(rotorASetting)
    rotorBSetting = ringSettings[1]
    keyB = alphabet.index(rotorBSetting)
    rotorCSetting = ringSettings[2]
    keyC = alphabet.index(rotorCSetting)
    
    rotorA = caesarShift(rotorA,keyA)
    rotorB = caesarShift(rotorB,keyB)
    rotorC = caesarShift(rotorC,keyC)
    

    messageOUT = ""
    

    
    plaintext = messageIN
    for letter in plaintext:
      encryptedLetter = letter  
      
      if letter in alphabet:
          Trigger = False
          if CLetter == rotationC:
            Trigger = True 
            CLetter = alphabet[(alphabet.index(CLetter) + 1) % 26]
          if Trigger:
              Trigger = False
              if BLetter == rotationB:
                  Trigger = True 
                  BLetter = alphabet[(alphabet.index(BLetter) + 1) % 26]
    
          #Check if rotorA needs to rotate
          if (Trigger):
              Trigger = False
              ALetter = alphabet[(alphabet.index(ALetter) + 1) % 26]
        		 
          else:
            #Check for double step sequence!
            if BLetter == rotationB:
              BLetter = alphabet[(alphabet.index(BLetter) + 1) % 26]
              ALetter = alphabet[(alphabet.index(ALetter) + 1) % 26]
          
          
            #Rotors & Reflector Encryption
            offsetA = alphabet.index(ALetter)
            offsetB = alphabet.index(BLetter)
            offsetC = alphabet.index(CLetter)
    
            # Wheel 3 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorC[(pos + offsetC)%26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetC +26)%26]
            
            # Wheel 2 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorB[(pos + offsetB)%26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetB +26)%26]
            
            # Wheel 1 Encryption
            pos = alphabet.index(encryptedLetter)
            let = rotorA[(pos + offsetA)%26]
            pos = alphabet.index(let)
            encryptedLetter = alphabet[(pos - offsetA +26)%26]
            
            # Reflector encryption!
            if encryptedLetter in reflectorDict.keys():
              if reflectorDict[encryptedLetter]!="":
                encryptedLetter = reflectorDict[encryptedLetter]
            
            #Back through the rotors 
            # Wheel 1 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetA)%26]
            pos = rotorA.index(let)
            encryptedLetter = alphabet[(pos - offsetA +26)%26] 
            
            # Wheel 2 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetB)%26]
            pos = rotorB.index(let)
            encryptedLetter = alphabet[(pos - offsetB +26)%26]
            
            # Wheel 3 Encryption
            pos = alphabet.index(encryptedLetter)
            let = alphabet[(pos + offsetC)%26]
            pos = rotorC.index(let)
            encryptedLetter = alphabet[(pos - offsetC +26)%26]
        
        

            messageOUT = messageOUT + encryptedLetter
    print("\n message OUT: \n " + messageOUT)
    return messageOUT

        


    
    
if __name__ == '__main__':
    rotors_file = 'rotors.json'

    while(1):
        Menu()
        option = ''
        try:
            option = int(input('entrer votre choix ...'))
        except:
            print('mauvais choix. ')
        
        if option == 1:
           LectureMessage('message.txt')          
        elif option == 2:
           messageIN = LectureMessage('message.txt') 
           message = Egnima(rotors_file, rotors, messageIN)
           SauvegardeMessage('sauvegarde.txt', message)
        elif option == 3:
            messageIN = LectureMessage('message.txt')
            Egnima(rotors_file, rotors, messageIN)
        elif option == 4:
            print('merci de mavoir utiliser bye..')
            sys.exit()
        else:
            print('option invalide')
 
    
    
    