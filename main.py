from kaggle_environments import make

env = make("kore_fleets", debug=True)

env.run(["./pilot_tehsin.py", "./attacker.py"])
out = env.render(mode="ansi")
# print(type(out))
# print(out
