from bending import animate_cylinder, animate_torus, make_gif

"""
animate_cylinder("puffin.jpg", direction="horizontal", folder="puffin-h", output_width=500)
make_gif("puffin-h", "examples/cylinder-h.gif")

animate_cylinder("puffin.jpg", direction="vertical", folder="puffin-v", output_width=500)
make_gif("puffin-v", "examples/cylinder-v.gif")
"""

animate_torus("puffin.jpg", folder="puffin-torus", output_width=500)
make_gif("puffin-torus", "examples/torus.gif")

