from kaggle_environments import make

env = make("kore_fleets", debug=True)

env.run(["./do_nothing.py"])
out = env.render(mode="ansi")
print(type(out))
print(out)

# from kaggle_environments import make

# Inflate the response replay to visualize.
# env = make("kore_fleets", debug=True)
# env.run(["./do_nothing.py"])
# env.render(mode="ipython")
