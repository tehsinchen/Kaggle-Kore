from kaggle_environments import make

env = make("kore_fleets", debug=True)

env.run(["./pilot_tehsin.py", "./attacker.py"])
env.render(mode="ansi")
