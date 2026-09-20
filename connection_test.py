
import asyncio
from mavsdk_grpc import System

async def run():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Warte auf Verbindung...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Verbunden mit Drohne!")
            break

asyncio.run(run())
