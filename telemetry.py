from pathlib import Path

import fastf1


CACHE_DIR = Path("./cache")


def enable_fastf1_cache() -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))


def get_fastest_lap_telemetry(year: int, grand_prix: str, session_type: str, driver: str):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()

    driver_laps = session.laps.pick_drivers(driver)
    if driver_laps.empty:
        raise ValueError(f"Aucun tour trouve pour le pilote {driver}.")

    fastest_lap = driver_laps.pick_fastest()
    if fastest_lap is None:
        raise ValueError(f"Impossible de determiner le tour le plus rapide de {driver}.")

    telemetry = fastest_lap.get_car_data().add_distance()
    if telemetry.empty or "Speed" not in telemetry.columns or "Distance" not in telemetry.columns:
        raise ValueError("La telemetrie de vitesse/distance est indisponible pour ce tour.")

    return {
        "telemetry": telemetry[["Distance", "Speed"]].dropna(),
        "lap_time": fastest_lap.get("LapTime"),
        "lap_number": fastest_lap.get("LapNumber"),
    }
