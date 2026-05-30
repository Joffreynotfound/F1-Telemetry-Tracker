from pathlib import Path

import fastf1
import matplotlib.pyplot as plt
import streamlit as st


CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))

YEARS = [2022, 2023, 2024, 2025]
GRANDS_PRIX = {
    "Bahrein": "Bahrain Grand Prix",
    "Djeddah": "Saudi Arabian Grand Prix",
    "Melbourne": "Australian Grand Prix",
    "Imola": "Emilia Romagna Grand Prix",
    "Monaco": "Monaco Grand Prix",
    "Montreal": "Canadian Grand Prix",
    "Silverstone": "British Grand Prix",
    "Spa": "Belgian Grand Prix",
    "Zandvoort": "Dutch Grand Prix",
    "Monza": "Italian Grand Prix",
    "Singapour": "Singapore Grand Prix",
    "Suzuka": "Japanese Grand Prix",
    "Austin": "United States Grand Prix",
    "Mexico": "Mexico City Grand Prix",
    "Interlagos": "Sao Paulo Grand Prix",
    "Las Vegas": "Las Vegas Grand Prix",
    "Abu Dhabi": "Abu Dhabi Grand Prix",
}
SESSION_TYPES = {
    "Course": "R",
    "Qualifications": "Q",
    "Essais libres 1": "FP1",
    "Essais libres 2": "FP2",
    "Essais libres 3": "FP3",
    "Sprint": "S",
    "Sprint Shootout": "SS",
}
DRIVERS = {
    "Max Verstappen": "VER",
    "Sergio Perez": "PER",
    "Lewis Hamilton": "HAM",
    "George Russell": "RUS",
    "Charles Leclerc": "LEC",
    "Carlos Sainz": "SAI",
    "Lando Norris": "NOR",
    "Oscar Piastri": "PIA",
    "Fernando Alonso": "ALO",
    "Lance Stroll": "STR",
}


st.set_page_config(
    page_title="F1 Telemetry Tracker",
    page_icon="F1",
    layout="centered",
)


@st.cache_data(show_spinner=False)
def load_fastest_lap_telemetry(year: int, grand_prix: str, session_type: str, driver: str):
    session = fastf1.get_session(year, grand_prix, session_type)
    session.load()

    driver_laps = session.laps.pick_drivers(driver)
    if driver_laps.empty:
        raise ValueError(f"Aucun tour trouvé pour le pilote {driver}.")

    fastest_lap = driver_laps.pick_fastest()
    if fastest_lap is None:
        raise ValueError(f"Impossible de déterminer le tour le plus rapide de {driver}.")

    telemetry = fastest_lap.get_car_data().add_distance()
    if telemetry.empty or "Speed" not in telemetry.columns or "Distance" not in telemetry.columns:
        raise ValueError("La télémétrie de vitesse/distance est indisponible pour ce tour.")

    lap_time = fastest_lap.get("LapTime")
    lap_number = fastest_lap.get("LapNumber")

    return {
        "telemetry": telemetry[["Distance", "Speed"]].dropna(),
        "lap_time": lap_time,
        "lap_number": lap_number,
    }


st.title("F1 Telemetry Tracker")

with st.sidebar:
    st.header("Paramètres")
    year = st.selectbox("Année", YEARS, index=1)
    grand_prix_label = st.selectbox("Grand Prix", list(GRANDS_PRIX), index=list(GRANDS_PRIX).index("Monza"))
    session_label = st.selectbox("Session", list(SESSION_TYPES))
    driver_name = st.selectbox("Pilote", list(DRIVERS))

    st.caption("R = course, Q = qualifications, FP = essais libres.")

grand_prix = GRANDS_PRIX[grand_prix_label]
session_type = SESSION_TYPES[session_label]
driver = DRIVERS[driver_name]

st.subheader(f"{driver_name} - {grand_prix_label} {year} ({session_type})")

try:
    with st.spinner("Chargement de la session FastF1 et de la télémétrie..."):
        lap_data = load_fastest_lap_telemetry(
            year=year,
            grand_prix=grand_prix,
            session_type=session_type,
            driver=driver,
        )
        telemetry = lap_data["telemetry"]

    lap_time = lap_data["lap_time"]
    lap_number = lap_data["lap_number"]
    if lap_time is not None:
        total_seconds = lap_time.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60
        st.metric("Tour le plus rapide", f"{minutes}:{seconds:06.3f}", f"Tour {int(lap_number)}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(telemetry["Distance"], telemetry["Speed"], color="#e10600", linewidth=1.8)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Vitesse (km/h)")
    ax.set_title("Vitesse en fonction de la distance")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)
    st.caption(f"{len(telemetry)} points de télémétrie chargés depuis FastF1.")
    st.download_button(
        "Télécharger la télémétrie CSV",
        data=telemetry.to_csv(index=False).encode("utf-8"),
        file_name=f"{year}_{grand_prix_label}_{session_type}_{driver}_telemetry.csv",
        mime="text/csv",
    )

except Exception as exc:
    st.error("Impossible de charger ou d'afficher les données sélectionnées.")
    st.info(
        "Vérifiez que la combinaison année, Grand Prix, session et pilote existe dans FastF1. "
        "Certaines sessions sprint ou certains pilotes peuvent ne pas être disponibles selon la saison."
    )
    with st.expander("Détail technique"):
        st.exception(exc)
