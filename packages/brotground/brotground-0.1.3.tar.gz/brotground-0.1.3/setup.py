# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brotground']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'numba>=0.54.0,<0.55.0']

setup_kwargs = {
    'name': 'brotground',
    'version': '0.1.3',
    'description': 'A playground for experimenting and getting mesmerized by the wonderful world of brots!',
    'long_description': '[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n[![Binder](https://binder.pangeo.io/badge_logo.svg)](https://binder.pangeo.io/v2/gh/Naereen/badges/master)\n\n\n\n<p align="center">\n<img src="https://i.ibb.co/L8pHqrv/logo.png" alt="logo" border="0">\n</p>\n\n# Brotground\n\nThis python package is for people who want to learn and explore the wonderful world of brots. Provides an api that allows rapid experimenting and visualization. \n\n```\npip install brotground\n```\n\n## Features\n1. _Light weight_, well documented, easy to understand code base\n2. _Extremely modular_, Replace any module with your own definition\n3. _Flexible_, Comes with good defaults but can be overridden\n4. _Zero Effort Setup_, Includes google colab notebooks to start experimenting without any setup\n5. _Minimal Dependency_, Numba for iteration and Matplotlib for rendering\n\n##  Overview\nBrots are generalization of Mandelbrot that takes a generic Mandelbrot equation. This library makes every part of the Mandelbrot equation as a parameter offering extreme flexibility to override or use the default implementation.\n\n>An equation means nothing to me unless it expresses a thought of God. — Srinivasa Ramanujan\n\nA Standard **Mandelbrot** equation,\n<p align="center">\n<img src="https://render.githubusercontent.com/render/math?math=Z_{n %2B 1} = Z_n^2 %2B \\mathbb{C}" width=200 height=100 color=\'grey\'>\n</p>\nwhen implemented and rendered will look like this,\n\n```python\nmandel = MandelBrot() # Initialize Mandelbrot\nmatplot_renderer = MatplotJupyterRenderer() # Initialize the renderer\n\nmandel.iterate_diverge(max_iterations=25) # Run the iterate diverge loop\nmatplot_renderer.plot(mandel, cmap="RdGy") # Plot the results\n```\n<p align="center">\n<img src="https://i.ibb.co/17H8MZV/mandelbrot-simple.png" alt="mandelbrot-simple" border="0" />\n</p>\n\nWe can further zoom in on the coordinates and iterate-diverge on those coordinates,\n\n```python\nmandel.set_boundaries((-0.02, 0.02), (0.780, 0.820)) # Zoom in on the coordinates\nmandel.iterate_diverge(max_iterations=100)\nmatplot_renderer.plot(mandel, cmap="plasma")\n```\n\nwill render like below,\n<p align="center">\n<img src="https://i.ibb.co/kDsRb81/mandelbrot-zoomed.png" alt="mandelbrot-zoomed" border="0">\n</p>\n\n\nBy changing each part of the equation you can get a range of generation.\nGeneralizing the above Mandelbrot equation to k, we get **Multibrot** where,\n\n<p align="center">\n<img src="https://render.githubusercontent.com/render/math?math=Z_{n %2B 1} = Z_n^k %2B \\mathbb{C}" width=200 height=100>\n</p>\n\nFor a K value of 3 we get a Multibrot rendered like this, \n\n```python\nmulti = MultiBrot()\n\nmulti.iterate_diverge(max_iterations=15)\nmatplot_renderer.plot(multi, cmap="binary")\n```\n\n<p align="center">\n<img src="https://i.ibb.co/w6PtBGY/multibrot.png" alt="multibrot" border="0">\n</p>\n\nA **Tricorn** brot is expressed as,  \n\n<p align="center">\n<img src="https://render.githubusercontent.com/render/math?math=Z_{n %2B 1} = \\overline{Z_n^2} %2B \\mathbb{C}" width=200 height=100>\n</p>\n\n```python\ntricorn = UserBrot(brot_equation=tricorn_brot_equation)\n\ntricorn.iterate_diverge(max_iterations=15)\nmatplot_renderer.plot(tricorn, cmap="RdYlBu")\n```\n\n<p align="center">\n<img src="https://i.ibb.co/F03qv0H/tricorn.png" alt="tricorn" border="0">\n</p>\n\n\nA **Burning ship** brot is expressed as,  \n<p align="center">\n<img src="https://render.githubusercontent.com/render/math?math=Z_{n %2B 1} = {|\\Re(Z)| %2B 1j %2B |\\Im(Z)|}^2 %2B \\mathbb{C}" width=500 height=200>\n</p>\n\n```python\nburning_ship = UserBrot(brot_equation=burning_ship_brot_equation)\n\nburning_ship.iterate_diverge(max_iterations=15)\nmatplot_renderer.plot(burning_ship, cmap="copper")\n```\n\n<p align="center">\n<img src="https://i.ibb.co/1sWn7yr/burning-ship.png" alt="burning-ship" border="0">\n</p>\n\n**JuliaBrot** is an extension to Mandelbrot, in which instead of initializing Z and C as 0 and `complex(i, j)` respectively we initialize Z as `complex(i, j)` and C as a function `f(i, j)` based on the julia set that we want to generate.\n\nFor example, to generate a `` julia set we initialize C as `complex(-0.7, 0.35)` and this generates the following,\n\n```python\njulia = JuliaBrot(julia_name="frost_fractal")\njulia.iterate_diverge(max_iterations=100)\n\nmatplot_renderer.plot(julia, cmap="inferno")\n```\n\n<p align="center">\n<img src="https://i.ibb.co/yk1b12z/frost-fractal.png" alt="frost-fractal" border="0">\n</p>\n\n```python\njulia = JuliaBrot(julia_name="galaxiex_fractal")\njulia.iterate_diverge(max_iterations=100)\n\nmatplot_renderer.plot(julia, cmap="inferno")\n```\n\n<p align="center">\n<img src="https://i.ibb.co/nzhy6CN/galaxiex-fractal.png" alt="galaxiex-fractal" border="0">\n</p>\n\n\n',
    'author': 'Adiamaan Keerthi Matheswaran',
    'author_email': 'mak.adi55@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adiamaan92/brotground',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
