# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamic_beast']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['dynamic-beast = dynamic_beast.main:app']}

setup_kwargs = {
    'name': 'dynamic-beast',
    'version': '1.5.0',
    'description': '',
    'long_description': '# Dynamic BEAST\n\n[![PyPi](https://img.shields.io/pypi/v/dynamic-beast.svg)](https://pypi.org/project/dynamic-beast/)\n[![tests](https://github.com/Wytamma/dynamic-beast/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/dynamic-beast/actions/workflows/test.yml)\n[![cov](https://codecov.io/gh/Wytamma/dynamic-beast/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/dynamic-beast)\n\nThis command line tool can be used to create a dynamic version of [BEAST2](http://www.beast2.org/) XML files. This dynamic XML file can be used to set BEAST parameters at runtime, which can be useful for testing different configurations or quickly modifying parameters without having to edit the XML file. \n\n## Install\nInstall `dynamic-beast` with pip (requires python -V >= 3.6.2).\n\n```\npip install dynamic-beast\n```\n\n## Usage\n\nGive `dynamic-beast` the path to a BEAST2 XML file and specify where to save the dynamic XML file (if `--outfile` is not specified XML will be printed to stdout).\n\n```bash\ndynamic-beast --outfile dynamic_hcv_coal.xml hcv_coal.xml\n```\n\nThis will produce a `dynamic_hcv_coal.xml` file that can be used as standard in a BEAST analysis.\n\n```bash\nbeast dynamic_hcv_coal.xml\n```\n\nTo modify parameters at runtime use the `beast` definitions option `-D`.\n\n```bash\n# Change the chain length to 1000. \nbeast -D \'mcmc.chainLength=1000\' dynamic_hcv_coal.xml\n``` \n\nMultiple definitions can be passed at the same time.\n\n```bash\n# Change the treelog and tracelog sampling freq to 10000. \nbeast -D \'treelog.logEvery=10000,tracelog.logEvery=10000\' dynamic_hcv_coal.xml\n``` \n\nThe full `id` of a parameter you\'d like to set must be specified. \n\n```bash \nbeast -D \'clockRate.c:hcv=7.9E-4\' dynamic_hcv_coal.xml\n```\n\n### CoupledMCMC\n\nMC3 options for the BEAST package [CoupledMCMC](https://github.com/nicfel/CoupledMCMC) can be added by using the `--mc3` option. This will add the default CoupledMCMC options which can then be configured at runtime with `-D`. \n\n```bash\n# Create dynamic MC3 XML \ndynamic-beast --mc3 --outfile dynamic_mc3_hcv_coal.xml hcv_coal.xml\n# Configure MC3 with BEAST\nbeast -D \'mcmc.chains=4\' dynamic_mc3_hcv_coal.xml\n```\n\n### Path Sampling (Stepping Stone)\n\nPath sampling options for the package [model-selection](https://github.com/BEAST2-Dev/model-selection) can be add by using the `--ps` option. This will add the default model-selection options (e.g. stepping stone) which can then be configured at runtime with `-D`. \n\n```bash\n# Create dynamic Path Sampling XML \ndynamic-beast --ps --outfile dynamic_ps_hcv_coal.xml hcv_coal.xml\n# Configure Path Sampling with BEAST\nbeast -D "ps.doNotRun=true,ps.rootdir=$(pwd)" dynamic_ps_hcv_coal.xml\n```\n\n## Explanation\n\nThe `dynamic-beast` tool replaces all the parameter values in the XML file with the `$(id.key=value)` format. The value variable is the default value that was initially specified in the XML file. However, the value can be redefined when running a BEAST analysis by making use of the [BEAST2 definitions option](https://www.beast2.org/2021/03/31/command-line-options.html#-d) (`-D`) that allows for user specified values. \n\nTo ensure reproducibility you should recreate static XML files of runs using dynamic parameters, this can be achieved using the `-DFout` argument e.g., `beast -D \'clockRate.c:hcv=7.9E-4\' -DFout static_hcv_coal.xml dynamic_hcv_coal.xml`. \n',
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
