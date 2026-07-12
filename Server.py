
import websockets
try:
    import websockets
except ImportError as e:
    print(f"Error: {e}")
    exit(1)


MAX_CLUENTS=100

class Server:

    clients = set()

    async def handler(self, websocket):
        if len(Server.clients) >= MAX_CLUENTS:
            print("Server is full")
            return

        Server.clients.add(websocket)
        try:
            print(f"Client connected")
            async for message in websocket:
                print(f"message {message}")
                await websocket.send(message)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            Server.clients.remove(websocket)
            print(f"Client disconnected")

    async def run(self):
        try:
            async with websockets.serve(self.handler, "localhost", 8080) as server:
                print("Server started")
                await server.wait_closed()   
        except KeyboardInterrupt:       
            print("Server stopped")

    async def broadcast(self):
        for socket in Server.clients:
            message = {
                "name": "123"
            }
            print(f"send message to client...")
            await socket.send(message.__dict__)

