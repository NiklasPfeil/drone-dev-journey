 ## PX4-Parameter nach Airframe-Wechsel neu setzen

Diese Parameter werden bei einem Airframe-Wechsel in PX4 SITL zurückgesetzt
und müssen danach manuell neu gesetzt werden:

- `NAV_DLL_ACT=0` – deaktiviert die Reaktion auf Datalink-Verlust
- `COM_RC_IN_MODE=4` – hebt die Pflicht zu einem physischen RC-Sender auf

Setzen über die PX4-Shell:
    param set NAV_DLL_ACT 0
    param set COM_RC_IN_MODE 4

## Offboard-Positionierung: 

- `drone.telemetry.position()` (globale lat/lon) zeigt kleine lokale Bewegungen in diesem
  Setup nicht zuverlässig an. Für Verifikation lieber PX4s eigene `vehicle_local_position`
  (PX4-Shell: `listener vehicle_local_position`) oder MAVSDKs `position_velocity_ned()`
  verwenden.
- Die Position der Drohne bleibt zwischen Skript-Durchläufen bestehen, solange SITL
  durchläuft. `set_position_ned()` ist ein absolutes Ziel relativ zum Startpunkt — ein
  Folgelauf mit demselben Ziel bewegt die Drohne dann nicht mehr, weil sie schon dort
  steht. Für reproduzierbare Tests: SITL neu starten oder Ziel pro Lauf variieren.
