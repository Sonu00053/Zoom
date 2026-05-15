from flask import render_template
import subprocess

class LudoController:

    @staticmethod
    def start_game():
        subprocess.Popen(["python3", "game/ludo_game.py"])  # Mac/Linux
        return render_template("ludo.html", title="Ludo Game")