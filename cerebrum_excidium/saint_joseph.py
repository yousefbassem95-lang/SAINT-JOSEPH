#!/usr/bin/env python3
import sys
import time
import argparse
from core.brain import Brain

class SaintJosephBot:
    def __init__(self):
        self.brain = Brain()
        self.running = True

    def display_banner(self):
        # ANSI Colors
        PURPLE = '\033[38;5;129m' # True Purple
        RESET = '\033[0m'

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

   _____  ___  _____  _   __ _____        ___  _____  _____  _____ ______  _   _ 
  /  ___|/ _ \|_   _|| \ | ||_   _|      |_  ||  _  |/  ___||  ___|| ___ \| | | |
  \ `--./ /_\ \ | |  |  \| |  | |  ______  | || | | |\ `--. | |__  | |_/ /| |_| |
   `--. \  _  | | |  | . ` |  | | |______| | || | | | `--. \|  __| |  __/ |  _  |
  /\__/ / | | |_| |_ | |\  |  | |      /\__/ /\ \_/ //\__/ /| |___ | |    | | | |
  \____/\_| |_/\___/ \_| \_/  \_/      \____/  \___/ \____/ \____/ \_|    \_| |_/
                                                                                 
              .
             / \
            /   \
           /_____\
          (  o o  )
           )  _  (
          /  |_|  \
         /   | |   \
        /    | |    \
       (     |_|     )
        \    | |    /
         \   | |   /
          )  | |  (
         /   | |   \
        |    | |    |
        |____|_|____|
       (_____) (_____)

                                made by J0J0M0J0
        """
        print(PURPLE + banner + RESET)

    def print_menu(self):
        print("\n=== COMMAND CENTER ===")
        print("1. Scan Target (Recon)")
        print("2. Analyze Target (Vulnerability Check)")
        print("3. Attack Target (Exploit)")
        print("4. Status Report")
        print("5. Toggle Self-Protection (Tor)") 
        print("6. Generate Mission Report")
        print("7. Exit")
        print("======================")

    def start(self):
        self.display_banner()
        print("\n[+] SAINT-JOSEPH Online. Awaiting commands.")
        
        while self.running:
            try:
                cmd = input("\nSAINT-JOSEPH> ").strip().lower()
                
                if cmd in ['help', 'menu', '?']:
                    self.print_menu()
                
                elif cmd in ['exit', 'quit', '7']:
                    print("[*] Shutting down SAINT-JOSEPH...")
                    self.running = False
                    
                elif cmd.startswith('scan') or cmd == '1':
                    target = input("Target Hostname/IP: ").strip()
                    if target:
                        print(f"[*] Initiating Recon on {target}...")
                        self.brain.interactive_recon(target)
                        
                elif cmd == '2':
                    target_id = input("Target ID to Analyze (leave empty for auto): ").strip()
                    print(f"[*] Starting Analysis...")
                    self.brain.interactive_analysis(target_id)

                elif cmd == '3':
                    target_id = input("Target ID to Attack (leave empty for auto): ").strip()
                    print(f"[*] AUTHORIZED. Launching Exploitation...")
                    self.brain.interactive_exploitation(target_id)

                elif cmd == '4':
                     self.brain.print_status()

                elif cmd == '5':
                    current = self.brain.toggle_protection()
                    print(f"[*] Self-Protection Mode: {'ENABLED (Tor)' if current else 'DISABLED'}")
                    
                elif cmd == '6':
                    self.brain.generate_report()

                else:
                    # Provide a "chat" like response or fallback
                    print(f"[*] Chatbot: I processed '{cmd}'. Unknown command. Type 'help' for options.")
            
            except KeyboardInterrupt:
                print("\n[!] Interrupted. Exiting.")
                self.running = False

if __name__ == "__main__":
    bot = SaintJosephBot()
    bot.start()
