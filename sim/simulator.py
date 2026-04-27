import json
import random
import os

# ---------- CONFIG ----------
SIMULATIONS = 100000
NR_PROBABILITY = 0.06   # 6% chance of no result

BASE_ELO = {
    "CSK": 1600,
    "MI": 1620,
    "RCB": 1630,
    "KKR": 1580,
    "RR": 1610,
    "SRH": 1590,
    "PBKS": 1580,
    "DC": 1570,
    "GT": 1600,
    "LSG": 1580
}

K_FACTOR = 20

# ---------- LOAD DATA ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    with open(os.path.join(BASE_DIR, "data", "teams.json")) as f:
        teams = json.load(f)

    with open(os.path.join(BASE_DIR, "data", "fixtures.json")) as f:
        fixtures = json.load(f)

    return teams, fixtures


# ---------- ELO PROBABILITY ----------
def win_probability(t1, t2, elo):
    r1 = elo[t1]
    r2 = elo[t2]
    return 1 / (1 + 10 ** ((r2 - r1) / 400))


# ---------- ELO UPDATE ----------
def update_elo(winner, loser, elo):
    expected = win_probability(winner, loser, elo)

    elo[winner] += K_FACTOR * (1 - expected)
    elo[loser] -= K_FACTOR * (1 - expected)


# ---------- SIMULATION ----------
def run_simulations():
    teams, fixtures = load_data()

    top4 = {t: 0 for t in teams}
    top2 = {t: 0 for t in teams}
    points_range = {t: [100, 0] for t in teams}

    for _ in range(SIMULATIONS):

        teams_copy = {t: teams[t].copy() for t in teams}
        elo = BASE_ELO.copy()

        for t1, t2 in fixtures:

            # ---------- NR CHECK ----------
            if random.random() < NR_PROBABILITY:
                teams_copy[t1]["points"] += 1
                teams_copy[t2]["points"] += 1
                continue  # no ELO update

            # ---------- NORMAL MATCH ----------
            prob = win_probability(t1, t2, elo)

            # small randomness
            prob = max(0.1, min(0.9, prob + random.uniform(-0.05, 0.05)))

            if random.random() < prob:
                winner, loser = t1, t2
            else:
                winner, loser = t2, t1

            # points
            teams_copy[winner]["points"] += 2

            # NRR impact (small random)
            teams_copy[winner]["nrr"] += random.uniform(0.01, 0.08)
            teams_copy[loser]["nrr"] -= random.uniform(0.01, 0.08)

            # update ELO
            update_elo(winner, loser, elo)

        # ---------- TRACK RANGE ----------
        for t in teams_copy:
            pts = teams_copy[t]["points"]
            points_range[t][0] = min(points_range[t][0], pts)
            points_range[t][1] = max(points_range[t][1], pts)

        # ---------- SORT ----------
        result = sorted(
            teams_copy.items(),
            key=lambda x: (x[1]["points"], x[1]["nrr"]),
            reverse=True
        )

        # ---------- COUNT ----------
        for i, (team, _) in enumerate(result):
            if i < 4:
                top4[team] += 1
            if i < 2:
                top2[team] += 1

    # ---------- PROBABILITIES ----------
    top4_prob = {t: top4[t] / SIMULATIONS for t in teams}
    top2_prob = {t: top2[t] / SIMULATIONS for t in teams}

    return teams, top4_prob, top2_prob, points_range