from posixpath import split
from flask import Flask, render_template, request
from mineral_classification_engine import MineralClassificationEngine

app = Flask(__name__)

def split_and_strip(list_string):
    x = list_string.split(",")
    x = [e.strip() for e in x]
    return x

@app.route("/handle_data", methods=["POST"])
def handle_data():
    if request.method == 'POST': 
        # fetch data from request form
        if "rock_group" in request.form:
            rock_group = request.form["rock_group"]
        else:
            rock_group = None
        colors = request.form["colors"]
        streaks = request.form["streaks"]
        hardness = request.form["hardness"]
        specific_gravity = request.form["specific_gravity"]
        if "luster" in request.form:
            luster = request.form["luster"]
        else:
            luster = None
        if "fracture" in request.form:
            fracture = request.form["fracture"]
        else:
            fracture = None
        if "tenacity" in request.form:
            tenacity = request.form["tenacity"]
        else:
            tenacity = None
        if "crystal_system" in request.form:
            crystal_system = request.form["crystal_system"]
        else:
            crystal_system = None
        if "cleavage" in request.form:
            cleavage = request.form["cleavage"]
        else:
            cleavage = None
        if "diaphaneity" in request.form:
            diaphaneity = request.form["diaphaneity"]
        else:
            diaphaneity = []
        if "weathered" in request.form:
            weathered = "true"
        else:
            weathered = "false"
        if "magnetic" in request.form:
            magnetic = "true"
        else:
            magnetic = "false"

        # build initial facts
        mce = MineralClassificationEngine()
        if (rock_group is not None):
            rock_group_facts = [["rock-group", rock_group]]
        else:
            rock_group_facts = []
        color_facts = mce.make_facts_from_list("color", split_and_strip(colors))
        streak_facts = mce.make_facts_from_list("streak", split_and_strip(streaks))
        if hardness == "":
            hardness_facts = []
        else:
            hardness_facts = mce.get_hardness_facts(hardness)
        if specific_gravity == "":
            specific_gravity_facts = []
        else:
            specific_gravity_facts = mce.get_specific_gravity_facts(specific_gravity)
        if (luster is not None):
            luster_facts = [["luster", luster]]
        else:
            luster_facts = []
        if (fracture is not None):
            fracture_facts = [["fracture", fracture]]
        else:
            fracture_facts = []
        if (tenacity is not None):
            tenacity_facts = [["tenacity", tenacity]]
        else:
            tenacity_facts = []
        if crystal_system is not None:
            crystal_system_facts = [["crystal-system", crystal_system]]
        else:
            crystal_system_facts = []
        if (cleavage is not None):
            cleavage_facts = [["cleavage", cleavage]]
        else:
            cleavage_facts = []
        if diaphaneity is not None:
            diaphaneity_facts = [["diaphaneity", diaphaneity]]
        else:
            diaphaneity_facts = []
        weathered_facts = [["weathered", weathered]]
        magnetic_facts = [["magnetic", magnetic]]

        initial_facts = rock_group_facts + color_facts + streak_facts + hardness_facts + specific_gravity_facts + luster_facts + fracture_facts + crystal_system_facts + cleavage_facts + diaphaneity_facts + tenacity_facts + weathered_facts + magnetic_facts

        # infer minerals and chemical composition
        learned_facts = mce.infer(initial_facts)
        print(initial_facts)
        print(learned_facts)

        # build mineral list and chemical composition list
        minerals = [pair[1] for pair in learned_facts if pair[0] == "mineral"]
        chemical_composition = [pair[1] for pair in learned_facts if pair[0] == "chemical-composition"]

        return render_template("index.html", minerals=", ".join(minerals), chemical_composition=", ".join(chemical_composition))
    else:
        return render_template("index.html", minerals="", chemical_composition="")

@app.route("/")
def index():
    return render_template("index.html", minerals="", chemical_composition="")