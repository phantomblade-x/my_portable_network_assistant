"""
Serial console connection to Cisco IOS
"""

import serial
import time
import re
from typing import Optional


class CiscoConsole:
    def __init__(self, port: str = '/dev/ttyUSB0', baud: int = 9600, timeout: int = 2):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud, timeout=timeout)
        self.prompt_pattern = re.compile(r'[\w\-]+[#>]\s*$')
        self.hostname = None
        self._detect_prompt()
    
    def _detect_prompt(self):
        """Send empty line to detect current prompt"""
        self.ser.write(b'\n')
        time.sleep(0.5)
        output = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='ignore')
        match = re.search(r'([\w\-]+)[#>]', output)
        if match:
            self.hostname = match.group(1)
    
    def send_command(self, cmd: str, wait: float = 1.0) -> str:
        """Send a command and return output"""
        # Clear buffer
        self.ser.read(self.ser.in_waiting)
        
        # Send command
        self.ser.write(f"{cmd}\n".encode())
        time.sleep(wait)
        
        # Read response
        output = ""
        while True:
            chunk = self.ser.read(self.ser.in_waiting)
            if not chunk:
                break
            output += chunk.decode('utf-8', errors='ignore')
            time.sleep(0.1)
        
        # Remove the command echo and trailing prompt
        lines = output.split('\n')
        if lines and cmd in lines[0]:
            lines = lines[1:]
        if lines and self.prompt_pattern.search(lines[-1]):
            lines = lines[:-1]
        
        return '\n'.join(lines).strip()
    
    def enter_config_mode(self):
        """Enter global configuration mode"""
        self.send_command('configure terminal', wait=0.5)
    
    def exit_config_mode(self):
        """Exit to privileged exec mode"""
        self.send_command('end', wait=0.5)
    
    def close(self):
        """Close serial connection"""
        if self.ser and self.ser.is_open:
            self.ser.close()