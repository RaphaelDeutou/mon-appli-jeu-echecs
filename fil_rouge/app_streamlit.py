"""Exo 2 : un tableau de bord pour choisir le prochain axe d'entraînement."""

import plotly.express as px
import streamlit as st

from data import familles, load_data, load_phases

st.set_page_config(
    page_title="Mon plan d'entraînement",
    page_icon="♟",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background: #f7f9fc;
        }
        .block-container {
            max-width: 1440px;
            padding-top: 1.7rem;
            padding-bottom: 3rem;
        }
        [data-testid="stSidebar"] {
            background: #f0f4f8;
            border-right: 1px solid #e3eaf1;
        }
        [data-testid="stMetric"] {
            min-height: 112px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 1rem 1.15rem;
            background: #ffffff;
            border: 1px solid #e3eaf1;
            border-radius: 16px;
            box-shadow: 0 5px 16px rgba(24, 49, 74, 0.05);
        }
        [data-testid="stMetricLabel"] p {
            color: #64748b;
            font-size: 0.9rem;
            font-weight: 600;
        }
        [data-testid="stMetricValue"] {
            color: #16344d;
            font-weight: 700;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #e3eaf1 !important;
            border-radius: 16px;
        }
        .hero {
            margin-bottom: 0.8rem;
            padding: 1.2rem 1.6rem;
            color: #ffffff;
            background: linear-gradient(115deg, #163b52 0%, #216b70 58%, #438a78 100%);
            border-radius: 20px;
        }
        .hero-kicker {
            margin-bottom: 0.45rem;
            color: #bde4d8;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .hero h1 {
            margin: 0;
            color: #ffffff;
            font-size: 1.9rem;
            letter-spacing: -0.035em;
        }
        .hero p {
            max-width: 760px;
            margin: 0.35rem 0 0;
            color: #e3f0ed;
            font-size: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def charger_donnees():
    return load_data(), load_phases()


def styliser_figure(figure, hauteur: int) -> None:
    figure.update_layout(
        template="plotly_white",
        height=hauteur,
        margin={"l": 12, "r": 24, "t": 12, "b": 30},
        font={"family": "Inter, Segoe UI, sans-serif", "size": 12, "color": "#475569"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hoverlabel={"bgcolor": "#ffffff", "font": {"color": "#16344d"}},
    )


def libelle_cadence(valeur: str) -> str:
    if valeur == "aucune":
        return "Sans cadence précisée"
    return valeur.capitalize()


df, phases = charger_donnees()

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Votre bilan d'entraînement</div>
        <h1>Vous stagnez aux échecs ? Vos parties ont la réponse.</h1>
        <p>Repérez en un regard l'ouverture à revoir et la phase où vous faites le plus de gaffes.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

date_min = df["date_jeu"].min().date()
date_max = df["date_jeu"].max().date()

with st.sidebar:
    st.markdown("### Affiner l'analyse")
    st.caption("Les indicateurs et graphiques se mettent à jour avec vos choix.")
    cadences = st.multiselect(
        "Cadences incluses",
        options=sorted(df["cadence"].unique()),
        default=[],
        format_func=libelle_cadence,
        placeholder="Toutes les cadences",
        help="Ajoutez les cadences à inclure. Sans sélection, toutes les cadences sont analysées.",
        key="cadences",
    )
    periode = st.date_input(
        "Période",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
        format="DD/MM/YYYY",
        help="Les dates des parties sont en UTC.",
        key="periode",
    )
    couleur = st.selectbox(
        "Couleur jouée",
        options=["Toutes", "Blancs", "Noirs"],
        key="couleur",
    )
    st.divider()
    st.caption("Score : victoire = 1, nulle = 0,5, défaite = 0.")

if not isinstance(periode, tuple) or len(periode) != 2:
    st.warning("Choisissez une date de début et une date de fin pour afficher l'analyse.")
    st.stop()

debut, fin = periode
masque = df["date_jeu"].dt.date.between(debut, fin)
if cadences:
    masque &= df["cadence"].isin(cadences)
if couleur == "Blancs":
    masque &= df["couleur"].eq("white")
elif couleur == "Noirs":
    masque &= df["couleur"].eq("black")

vue = df.loc[masque]
if vue.empty:
    st.warning("Aucune partie ne correspond à ces filtres. Élargissez la période ou changez un filtre.")
    st.stop()

score_moyen = vue["score"].mean()
score_global = df["score"].mean()
gaffes_moyennes = vue["gaffes_joueur"].mean()
gaffes_globales = df["gaffes_joueur"].mean()
nb_parties = f"{len(vue):,}".replace(",", " ")
cadences_resume = ", ".join(libelle_cadence(valeur) for valeur in cadences)
if not cadences_resume:
    cadences_resume = "Toutes les cadences"

phases_codes = ["opening", "middlegame", "endgame"]
noms_phases = {
    "opening": "Ouverture",
    "middlegame": "Milieu de partie",
    "endgame": "Finale",
}
phases_vue = phases.loc[
    phases["partie_id"].isin(vue["partie_id"]) & phases["phase"].isin(phases_codes)
]
par_phase = (
    phases_vue.groupby("phase", as_index=False)
    .agg(parties=("partie_id", "nunique"), gaffes=("gaffes_joueur", "sum"))
)
par_phase["gaffes_par_partie"] = par_phase["gaffes"] / par_phase["parties"]
par_phase["phase_nom"] = par_phase["phase"].map(noms_phases)
par_phase = par_phase.loc[par_phase["parties"] > 0].copy()
if par_phase.empty:
    st.warning("Aucune statistique de phase disponible pour les parties sélectionnées.")
    st.stop()

par_famille = familles(vue)
familles_a_afficher = par_famille.head(8).copy()
phase_prioritaire = par_phase.sort_values("gaffes_par_partie", ascending=False).iloc[0]
nb_parties_phase = f"{int(phase_prioritaire['parties']):,}".replace(",", " ")

st.caption(
    f"**{nb_parties} parties** · {cadences_resume} · "
    f"{debut:%d/%m/%Y} – {fin:%d/%m/%Y} · {couleur}"
)

with st.container(border=True):
    st.markdown("#### Votre priorité, en un regard")
    col_phase, col_famille = st.columns(2, gap="large")
    with col_phase:
        st.markdown(
            f"**Phase à travailler : {phase_prioritaire['phase_nom']}**  \n"
            f"{phase_prioritaire['gaffes_par_partie']:.2f} gaffes par partie "
            f"({nb_parties_phase} parties concernées)"
        )
    with col_famille:
        if familles_a_afficher.empty:
            st.markdown("**Ouverture à revoir**  \nPas assez de parties pour une comparaison fiable.")
        else:
            ouverture = familles_a_afficher.iloc[0]
            st.markdown(
                f"**Ouverture à revoir : {ouverture['famille']}**  \n"
                f"Score moyen {ouverture['score']:.0%} sur {int(ouverture['n'])} parties"
            )
    st.caption(
        "Pistes calculées sur la sélection ; les familles comptent au moins 30 parties."
    )

col_parties, col_score, col_gaffes = st.columns(3, gap="medium")
delta_score = (score_moyen - score_global) * 100
delta_score_label = f"{delta_score:+.1f} pts vs historique" if abs(delta_score) >= 0.05 else None
delta_gaffes = gaffes_moyennes - gaffes_globales
delta_gaffes_label = f"{delta_gaffes:+.2f} vs historique" if abs(delta_gaffes) >= 0.005 else None

with col_parties:
    st.metric(
        "Parties analysées",
        nb_parties,
        help="Nombre de parties correspondant aux filtres.",
    )
with col_score:
    st.metric(
        "Score moyen",
        f"{score_moyen:.1%}",
        delta=delta_score_label,
        help="Victoires valent 1 point, nulles 0,5 et défaites 0.",
    )
with col_gaffes:
    st.metric(
        "Gaffes par partie",
        f"{gaffes_moyennes:.2f}",
        delta=delta_gaffes_label,
        delta_color="inverse",
        help="Une valeur plus basse est préférable. La comparaison se fait avec tout l'historique.",
    )

st.markdown("### Où travailler en priorité")
col_familles, col_phases = st.columns(2, gap="large")

with col_familles, st.container(border=True):
    st.markdown("#### Ouvertures à réviser")
    st.caption("Score moyen par famille · les scores les plus faibles apparaissent en haut.")
    if familles_a_afficher.empty:
        st.info("Aucune famille ne compte au moins 30 parties dans cette sélection.")
    else:
        familles_a_afficher["score_label"] = familles_a_afficher["score"].map(
            lambda score: f"{score:.0%}"
        )
        score_min = max(0.0, float(familles_a_afficher["score"].min()) - 0.05)
        score_max = min(1.0, float(familles_a_afficher["score"].max()) + 0.05)
        figure_familles = px.bar(
            familles_a_afficher,
            x="score",
            y="famille",
            color="score",
            orientation="h",
            text="score_label",
            color_continuous_scale=["#dd6b5d", "#f0b65a", "#368978"],
            range_color=[score_min, score_max],
            hover_data={
                "score": ":.1%",
                "n": ":,",
                "gaffes": ":.2f",
                "score_label": False,
            },
        )
        figure_familles.update_traces(textposition="outside", cliponaxis=False)
        figure_familles.update_coloraxes(showscale=False)
        figure_familles.update_xaxes(
            range=[0, min(1.15, float(familles_a_afficher["score"].max()) + 0.16)],
            tickformat=".0%",
            title=None,
            gridcolor="#e8edf3",
            zeroline=False,
        )
        figure_familles.update_yaxes(autorange="reversed", title=None, automargin=True)
        styliser_figure(figure_familles, max(340, 36 * len(familles_a_afficher) + 100))
        st.plotly_chart(
            figure_familles,
            width="stretch",
            theme=None,
            config={"displayModeBar": False},
        )

with col_phases, st.container(border=True):
    st.markdown("#### Phases à surveiller")
    st.caption("Gaffes par partie ayant atteint la phase · comparaison normalisée.")
    par_phase["priorite"] = par_phase["phase_nom"].eq(phase_prioritaire["phase_nom"]).map(
        {True: "Priorité", False: "Autres phases"}
    )
    par_phase["taux_label"] = par_phase["gaffes_par_partie"].map(
        lambda taux: f"{taux:.2f}"
    )
    figure_phases = px.bar(
        par_phase,
        x="phase_nom",
        y="gaffes_par_partie",
        color="priorite",
        text="taux_label",
        color_discrete_map={
            "Priorité": "#dd6b5d",
            "Autres phases": "#3e788a",
        },
        hover_data={
            "parties": ":,",
            "gaffes": ":,",
            "gaffes_par_partie": ":.2f",
            "taux_label": False,
            "priorite": False,
        },
        category_orders={"phase_nom": list(noms_phases.values())},
    )
    figure_phases.update_traces(textposition="outside", cliponaxis=False)
    figure_phases.update_xaxes(title=None, showgrid=False)
    figure_phases.update_yaxes(
        title=None,
        rangemode="tozero",
        gridcolor="#e8edf3",
        zeroline=False,
    )
    styliser_figure(figure_phases, 380)
    st.plotly_chart(
        figure_phases,
        width="stretch",
        theme=None,
        config={"displayModeBar": False},
    )

st.caption(
    "Conseil : changez un filtre à la fois pour voir si une priorité dépend de la cadence, "
    "de la période ou de la couleur."
)
