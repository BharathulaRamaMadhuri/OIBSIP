import os
import shutil
import socket
import sys
import threading
from datetime import datetime
 
HOST = "127.0.0.1"   # localhost: server and clients run on the same machine
PORT = 5000
 
 
def timestamp():
    """Current time as HH:MM, used as the message prefix."""
    return datetime.now().strftime("%H:%M")
 
 
def replace_typed_line(text):
    """Erase the line the user just typed, so only the formatted message stays on screen."""
    if not sys.stdout.isatty():
        return
    width = shutil.get_terminal_size().columns
    lines_used = max(1, -(-len(text) // width))  # how many screen lines the typed text took
    for _ in range(lines_used):
        sys.stdout.write("\033[A\033[2K")  # move cursor up one line and clear it
    sys.stdout.flush()
 
 
def show_own_message(line):
    """Show the user's own message on the right side of the screen (like WhatsApp)."""
    if sys.stdout.isatty():
        width = shutil.get_terminal_size().columns
        print(line.rjust(width - 1))
    else:
        print(line)
 
 
def get_name():
    """Keep asking until the user enters a valid name."""
    while True:
        name = input("Enter your name: ").strip()
        if not name:
            print("Error: Name cannot be empty.")
            continue
        if len(name) > 20:
            print("Error: Name must be 20 characters or less.")
            continue
        return name
 
 
def receive_messages(sock, stop_event):
    """Runs in a separate thread: prints every message that arrives from the server."""
    reader = sock.makefile("r", encoding="utf-8")
    try:
        for line in reader:
            print(line.rstrip("\n"))
    except OSError:
        pass
    stop_event.set()
    print("Disconnected from the server. Press Enter to exit.")
 
 
def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
 
    os.system("")  # lets Windows terminals understand the screen-clearing codes used below
    print("=== Chat Client ===")
    name = get_name()
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, port))
    except OSError:
        print(f"Error: Could not connect to the server at {HOST}:{port}. Start server.py first.")
        return
 
    sock.sendall((name + "\n").encode("utf-8"))
 
    stop_event = threading.Event()
    thread = threading.Thread(target=receive_messages, args=(sock, stop_event), daemon=True)
    thread.start()
 
    print("Type your message and press Enter. Type /quit to leave.")
    try:
        while not stop_event.is_set():
            typed = input()
            text = typed.strip()
            if stop_event.is_set() or text == "/quit":
                break
            if not text:
                continue
            sock.sendall((text + "\n").encode("utf-8"))
            replace_typed_line(typed)
            show_own_message(f"[{timestamp()}] {name}: {text}")
    except (EOFError, KeyboardInterrupt, OSError):
        pass
    finally:
        sock.close()
        print("You left the chat.")
 
if __name__ == "__main__":
    main()