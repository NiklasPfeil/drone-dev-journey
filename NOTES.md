 ## PX4-Parameter nach Airframe-Wechsel neu setzen

Diese Parameter werden bei einem Airframe-Wechsel in PX4 SITL zurückgesetzt
und müssen danach manuell neu gesetzt werden:

- `NAV_DLL_ACT=0` – deaktiviert die Reaktion auf Datalink-Verlust
- `COM_RC_IN_MODE=4` – hebt die Pflicht zu einem physischen RC-Sender auf

Setzen über die PX4-Shell:
    param set NAV_DLL_ACT 0
    param set COM_RC_IN_MODE 4
