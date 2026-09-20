import asyncio
from mavsdk_grpc import System
from mavsdk_grpc.offboard import PositionNedYaw, OffboardError
from mavsdk_grpc.telemetry import LandedState


async def wait_for_landing(drone):
    async for state in drone.telemetry.landed_state():
        if state == LandedState.ON_GROUND:
            print("-- Landung bestätigt (ON_GROUND)")
            break


async def watch_connection(drone, status):
    async for state in drone.core.connection_state():
        if not state.is_connected:
            print("!! Verbindung zur Drohne verloren!")
            status["connected"] = False
            break


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

    status = {"connected": True}
    watcher = asyncio.create_task(watch_connection(drone, status))

    print("Armiere...")
    await drone.action.arm()

    print("Starte Takeoff...")
    await drone.action.takeoff()
    await asyncio.sleep(8)

    print("Setze initialen Setpoint...")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -2.5, 0.0))

    print("Starte Offboard-Modus...")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Offboard-Start fehlgeschlagen: {error}")
        await drone.action.land()
        return

    async for flight_mode in drone.telemetry.flight_mode():
        print(f"Aktueller Flugmodus: {flight_mode}")
        break

    print("Position vor Bewegung:")
    async for position in drone.telemetry.position():
        print(f"  lat={position.latitude_deg:.6f}, lon={position.longitude_deg:.6f}")
        break

    print("-- Offboard aktiv, fliege 3 m nach Norden...")
    for _ in range(80):
        if not status["connected"]:
            print("Abbruch: Verbindung verloren, stoppe Setpoints.")
            break
        await drone.offboard.set_position_ned(PositionNedYaw(3.0, 0.0, -2.5, 0.0))
        await asyncio.sleep(0.1)

    print("Position nach Bewegung:")
    async for position in drone.telemetry.position():
        print(f"  lat={position.latitude_deg:.6f}, lon={position.longitude_deg:.6f}")
        break

    print("Stoppe Offboard...")
    await drone.offboard.stop()

    print("Lande...")
    await drone.action.land()

    print("Warte auf Landebestätigung...")
    try:
        await asyncio.wait_for(wait_for_landing(drone), timeout=30)
    except asyncio.TimeoutError:
        print("Timeout: keine Landebestätigung nach 30s")

    watcher.cancel()
    try:
        await watcher
    except asyncio.CancelledError:
        pass


asyncio.run(run())
