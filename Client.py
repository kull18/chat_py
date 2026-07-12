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

class Client:
    def __init__(self, uri="ws://localhost:8080", heartbeat_interval=10, reconnect_delay=5):
        self.uri = uri
        self.heartbeat_interval = heartbeat_interval
        self.reconnect_delay = reconnect_delay

    async def _heartbeat(self, websocket):
        try:
            while True:
                await asyncio.sleep(self.heartbeat_interval)
                try:
                    await websocket.ping()
                    print("Heartbeat: ping sent")
                except Exception as e:
                    print(f"Heartbeat error: {e}")
                    break
        except asyncio.CancelledError:
            pass

    async def _receive_loop(self, websocket):
        try:
            async for message in websocket:
                print(f"Received: {message}")
        except Exception as e:
            print(f"Receive loop error: {e}")

    async def read_server_message(self, websocket):
        try:
            async for message in websocket:
                print(f"Received from server: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")

    async def connect(self):
        # Persistent connect + automatic reconnect on failure
        while True:
            try:
                # disable automatic pinging to manage heartbeats manually
                async with websockets.connect(self.uri, ping_interval=None) as websocket:
                    print(f"Connected to server at {self.uri}")
                    try:
                        await websocket.send("Hello, Server!")
                        print("Sent greeting to server")
                    except Exception as e:
                        print(f"Send error: {e}")

                    hb_task = asyncio.create_task(self._heartbeat(websocket))
                    recv_task = asyncio.create_task(self.read_server_message(websocket))

                    _, pending = await asyncio.wait(
                        [hb_task, recv_task], return_when=asyncio.FIRST_EXCEPTION
                    )

                    for task in pending:
                        task.cancel()
            except Exception as e:
                print(f"Connection error: {e}")

            print(f"Reconnecting in {self.reconnect_delay} seconds...")
            await asyncio.sleep(self.reconnect_delay)

async def main():
    client = Client()
    await client.connect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())