import socket
import sys
import threading
from datetime import datetime
 
HOST = "127.0.0.1"   # localhost: server and clients run on the same machine
PORT = 5000
MAX_USERS = 2        # this is a two-user chat
 
clients = []         # list of (connection, name) for the users who are connected
lock = threading.Lock()  # protects the clients list because many threads use it
 
 
def timestamp():
    """Current time as HH:MM, used as the message prefix."""
    return datetime.now().strftime("%H:%M")
 
 
def send_line(conn, text):
    """Send one line of text to a client. Ignore errors if the client is gone."""
    try:
        conn.sendall((text + "\n").encode("utf-8"))
    except OSError:
        pass
 
 
def find_other(conn):
    """Return (connection, name) of the other user, or None if nobody else is connected."""
    for other_conn, other_name in clients:
        if other_conn is not conn:
            return other_conn, other_name
    return None
 
 
def handle_client(conn, address):
    """Runs in its own thread for every connected client."""
    reader = conn.makefile("r", encoding="utf-8")
    name = ""
    registered = False
    try:
        # The first line a client sends is its name.
        name = reader.readline().strip()
        if not name:
            return
 
        with lock:
            if len(clients) >= MAX_USERS:
                full = True
            else:
                full = False
                clients.append((conn, name))
                registered = True
                other = find_other(conn)
 
        if full:
            send_line(conn, "SERVER: The chat is full. Only 2 users are allowed. Try again later.")
            return
 
        print(f"[{timestamp()}] {name} connected from {address[0]}:{address[1]}")
 
        if other:
            other_conn, other_name = other
            send_line(conn, f"[{timestamp()}] SERVER: You are now connected with {other_name}. Start chatting!")
            send_line(other_conn, f"[{timestamp()}] SERVER: {name} joined the chat. Start chatting!")
        else:
            send_line(conn, "SERVER: Waiting for another user to join...")
 
        # Keep reading messages from this client and pass them to the other client.
        for line in reader:
            message = line.rstrip("\n")
            if not message:
                continue
            with lock:
                other = find_other(conn)
            if other:
                send_line(other[0], f"[{timestamp()}] {name}: {message}")
            else:
                send_line(conn, "SERVER: No one else is connected yet. Message not delivered.")
    except OSError:
        pass  # the client closed the connection suddenly
    finally:
        # Graceful disconnection: tell the other user that this user has left.
        other = None
        with lock:
            if registered:
                clients.remove((conn, name))
                other = find_other(conn)
        if registered:
            print(f"[{timestamp()}] {name} disconnected")
            if other:
                send_line(other[0], f"[{timestamp()}] SERVER: {name} has left the chat.")
        try:
            conn.close()
        except OSError:
            pass
 
 
def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, port))
    except OSError:
        print(f"Error: Could not start the server on port {port}. The port may already be in use.")
        return
    server.listen()
    print(f"=== Chat Server ===")
    print(f"Server is listening on {HOST}:{port}")
    print("Waiting for clients to connect... (press Ctrl + C to stop)")
 
    try:
        while True:
            conn, address = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, address), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()
 
 
if __name__ == "__main__":
    main()