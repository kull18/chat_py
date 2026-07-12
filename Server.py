
try:
    import websockets
except ImportError as e:
    print(f"Error: {e}")
    exit(1)

try:
    import asyncio
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

    async def send_to_all(self, message):
        while True:
            await asyncio.sleep(10)


            for client in Server.clients.copy():
                try:
                    message = f"Server: {message}"
                    await client.send(message)
                except Exception as e:
                    print(f"Error: {e}")
                    Server.clients.remove(client)