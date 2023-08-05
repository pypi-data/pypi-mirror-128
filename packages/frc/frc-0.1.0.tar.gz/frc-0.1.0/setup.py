# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['frc']

package_data = \
{'': ['*']}

install_requires = \
['diplib>=3.1.0,<4.0.0',
 'numpy>=1.18,<2.0',
 'rustfrc>=1.1.2,<2.0.0',
 'scipy>=1.3,<2.0']

setup_kwargs = {
    'name': 'frc',
    'version': '0.1.0',
    'description': 'Library for computing Fourier Ring Correlation (FRC) curves and using them to determine image resolution.',
    'long_description': '# frc\n\n`frc` is a Python library for calculating Fourier Ring Correlation (FRC) curves and their associated resolution.\n\nThis is particularly useful for determining the resolution of images taken with super-resolution microscopy techniques.\n\nIts most computationally intensive functions are all implemented either in NumPy or Rust, making this library very fast.\n\n### Fourier Ring Correlation\n\nIntroduced in 1982, Fourier Ring Correlation compares two 2D images, which are assumed to be noise-independent. In Fourier space, mage structure dominates the lower spatial frequencies (in the Fourier domain), while noise dominates at the higher frequencies.\n\nIn Fourier space, there are rings of constant spatial frequency around the origin. By calculating the correlation between the rings in the two images, you get the FRC curve:\n\n![formula](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bgray%7D%5Ctext%7BFRC%7D%28q%29%20%3D%20%5Cfrac%7B%5Csum_%7B%5Cvec%7Bq%7D%20%5Cin%20%5Ctext%7Bcircle%7D%7D%20%5Cwidehat%7Bf_1%7D%28%5Cvec%7Bq%7D%29%20%5Cwidehat%7Bf_2%7D%28%5Cvec%7Bq%7D%29%5E%7B%5Ctextbf%7B%2A%7D%7D%7D%7B%5Csqrt%7B%5Csum_%7B%5Cvec%7Bq%7D%20%5Cin%20%5Ctext%7Bcircle%7D%7D%20%5Clvert%5Cwidehat%7Bf_1%7D%28%5Cvec%7Bq%7D%29%5Crvert%5E2%7D%20%5Csqrt%7B%5Csum_%7B%5Cvec%7Bq%7D%20%5Cin%20%5Ctext%7Bcircle%7D%7D%20%5Clvert%5Cwidehat%7Bf_2%7D%28%5Cvec%7Bq%7D%29%5Crvert%5E2%7D%7D%0A)\n\nSee the accompanying `FRC.pdf` for additional details.\n\nAt some spatial frequency, the signal cannot be separated from the noise. What spatial frequency exactly depends on what threshold function is used. The standard 0.143 and 1/2-bit thresholds are both available, as well as an algorithm to compute the intersection and resulting resolution.\n\n\n\n### Installation\n\nYou can download this library from PyPI:\n\n```shell\npip install frc\n```\n\nThis library depends on [tmtenbrink/rustfrc](https://www.github.com/tmtenbrink/rustfrc), [DIPlib](https://github.com/DIPlib/diplib), [scipy](https://scipy.org/) and of course, [numpy](https://numpy.org/).\n\n### Usage\n\nThe code snippet below (which for illustration purposes assumes you have a numpy array or DIP image representing your input, its associated scale and also matplotlib to plot the result) will calculate the FRC curve and the associated resolution using the standard 1/7 threshold.\n\n```python\nimport frc\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n... # get an image and scale\n\nimg = np.array(img)\n# Input can be a numpy array or DIP image\nimg = frc.util.square_image(img, add_padding=False)\nimg = frc.util.apply_tukey(img)\n# Apply 1FRC technique\nfrc_curve = frc.one_frc(img)\n\nimg_size = img.shape[0]\nxs_pix = np.arange(len(frc_curve)) / img_size\n# scale has units [pixels <length unit>^-1] corresponding to original image\nxs_nm_freq = xs_pix * scale\nfrc_res, res_y, thres = frc.frc_res(xs_nm_freq, frc_curve, img_size)\nplt.plot(xs_nm_freq, thres(xs_nm_freq))\nplt.plot(xs_nm_freq, frc_curve)\nplt.show()\n```',
    'author': 'Tip ten Brink',
    'author_email': 'T.M.tenBrink@student.tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
