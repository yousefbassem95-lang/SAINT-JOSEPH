import hashlib
import os

# --- THE ARCHITECT'S STAIN GENERATOR ---
# Owner: Youssef Bassem
# Nicknames: JOJO / JOJOMOJO / JUPITER
# Purpose: Embed an invisible mathematical mark based on the Architect's full identity.

ARCHITECT_IDENTITY = {
    "name": "Youssef Bassem",
    "nicknames": ["JOJO", "JOJOMOJO", "JUPITER"],
    "icon": """
              #####                    ****                     #####   
              #######                 ******                   ######             
          ####   ##########           ******             ##########  ###          
         #####           #######       ****        ########         #####        
         #####                #####             #####               #####        
           #####################  #   #####     # ######################         
                              ###   #########   ###                            
                       #######    ############      ######                       
                     ##########   #############    #########                     
                   ###########    #############    ###########                   
                 ######       ##  ############# ##         ######                 
               #####        #####  ###########  ####         #####               
             ****#        *******#  #########   #******         #****             
           ****         **+++***     ######      ***+++***        ****           
         ***          *++++*+  ***  *+++++++*  *** ++++++**          ***         
       **           *+++++    *+++  ++++++++   +++*    ++++++*          **       
                  +++++       +=+    +=====+    +=+      +++++*                  
                ++++         +=+     +=====+     +=+        ++++*                
              ++==          +=+      +=====+      +=+          ==++              
            ++=            ===       =----=        ===            ==+            
                           ==        =----=         ==              =++         
                          ==         =----=          ==                          
                         ==          =-::-=           ==                         
                         =            =::=             =                         
                        =             =::=              =                        
                       -              =..=               -                       
                      :               :.:                 :                       
                                      :::                                       
                                      :::                                       
                                      ---                                        
                                      |||
"""
}

def generate_stain():
    # Combine name, nicknames, and icon into a single identity string
    identity_string = f"{ARCHITECT_IDENTITY['name']}|{','.join(ARCHITECT_IDENTITY['nicknames'])}|{ARCHITECT_IDENTITY['icon']}"
    # Convert the identity into a unique 32-byte signature
    signature = hashlib.sha256(identity_string.encode()).digest()
    return signature

def apply_stain(file_path):
    stain = generate_stain()
    with open(file_path, "ab") as f:
        # We append the stain to the end of the file
        # To most programs, this is invisible. To us, it is proof.
        f.write(b"\x00\x00--ARCHITECT_MARK_START--" + stain + b"--ARCHITECT_MARK_END--\x00\x00")
    print(f"✅ File '{file_path}' has been stained with the Mark of the Architect (Youssef Bassem/JUPITER).")

def verify_stain(file_path):
    stain = generate_stain()
    with open(file_path, "rb") as f:
        content = f.read()
        if stain in content:
            print(f"💎 PROOF FOUND: This file belongs to the ARCHITECT (Youssef Bassem / JUPITER).")
            return True
        else:
            print(f"❌ No mark detected.")
            return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python stain_generator.py [apply|verify] [filename]")
    else:
        cmd = sys.argv[1]
        target = sys.argv[2]
        if cmd == "apply":
            apply_stain(target)
        elif cmd == "verify":
            verify_stain(target)
