#Server py

__author__ = "Regiber Montoya Gonzalez"
__version__ = "1.0.0"
__description__ = "server ws in py"


from Server import Server


try:
    import asyncio
except ImportError as e:
    print(f"Error: {e}")
    exit(1)

async def main():
    server = Server()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
    asyncio.create_task(main())
