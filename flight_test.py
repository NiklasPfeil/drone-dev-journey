import asyncio
from mavsdk_grpc import System

async def run():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    print("Warte auf Verbindung...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Verbunden mit Drohne!")
            break

    print("Warte auf Health-Check...")
    async for health in drone.telemetry.health_all_ok():
        if health:
            print("-- Health-Check OK")
            break

    print("Arming...")
    await drone.action.arm()
    print("-- Armed")

    print("Starte Takeoff...")
    await drone.action.takeoff()
    print("-- Takeoff kommandiert")

    await asyncio.sleep(10)

    print("Lande...")
    await drone.action.land()
    print("-- Landung kommandiert")

asyncio.run(run())
