import argparse
from core.brain import Brain
import subprocess
import sys
import os

def check_integrity():
    print("[*] Performing integrity check...")
    wd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "integrity_watchdog.py"))
    result = subprocess.run([sys.executable, wd_path, "check"], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print("[!] Integrity check FAILED. Potential unauthorized modifications detected.")
        sys.exit(1)
    print("[+] Integrity check PASSED.")


def main():
    banner = r"""
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
    check_integrity()
    print(banner)
    print("                 Cerebrum Excidium - The Mind of Destruction")
    print("                           --- SHADOWHacker-GOD ---")
    print("\n[+] Initializing Core Systems...\n")


    parser = argparse.ArgumentParser(description="Cerebrum Excidium - Autonomous Hacking AI")
    parser.add_argument('--target', help="Initial target URL or IP address")
    parser.add_argument('--mode', choices=['recon', 'full_attack', 'social'], default='recon', help="Operation mode")
    
    args = parser.parse_args()

    print(f"[*] AI Core instantiated. Target: {args.target} | Mode: {args.mode}")
    ai_brain = Brain(target=args.target, mode=args.mode)
    
    try:
        ai_brain.run()
    except KeyboardInterrupt:
        print("\n[!] Operation manually terminated by Master of Command.")
    except Exception as e:
        print(f"\n[!!!] A critical error occurred in the AI Core: {e}")

if __name__ == "__main__":
    main()
