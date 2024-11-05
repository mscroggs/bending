from bending import animate_cylinder, make_gif

animate_cylinder("puffin.jpg", direction="horizontal", folder="puffin-h", output_width=500)
make_gif("puffin-h", "examples/puffin-h.gif")

animate_cylinder("puffin.jpg", direction="vertical", folder="puffin-v", output_width=500)
make_gif("puffin-v", "examples/puffin-v.gif")
