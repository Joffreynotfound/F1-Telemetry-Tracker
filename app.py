from pathlib import Path

import fastf1
import matplotlib.pyplot as plt
import streamlit as st


CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))

YEARS = [2022, 2023]
GRANDS_PRIX = ["Monza", "Silverstone"]
SESSION_TYPES = ["R", "Q"]
DEFAULT_DRIVER = "VER"


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

    return telemetry[["Distance", "Speed"]].dropna()


st.title("F1 Telemetry Tracker")

with st.sidebar:
    st.header("Paramètres")
    year = st.selectbox("Année", YEARS, index=1)
    grand_prix = st.selectbox("Grand Prix", GRANDS_PRIX)
    session_type = st.selectbox("Session", SESSION_TYPES)

st.subheader(f"{DEFAULT_DRIVER} - {grand_prix} {year} ({session_type})")

try:
    with st.spinner("Chargement de la session FastF1 et de la télémétrie..."):
        telemetry = load_fastest_lap_telemetry(
            year=year,
            grand_prix=grand_prix,
            session_type=session_type,
            driver=DEFAULT_DRIVER,
        )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(telemetry["Distance"], telemetry["Speed"], color="#e10600", linewidth=1.8)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Vitesse (km/h)")
    ax.set_title("Vitesse en fonction de la distance")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)
    st.caption(f"{len(telemetry)} points de télémétrie chargés depuis FastF1.")

except Exception as exc:
    st.error("Impossible de charger ou d'afficher les données sélectionnées.")
    st.exception(exc)
