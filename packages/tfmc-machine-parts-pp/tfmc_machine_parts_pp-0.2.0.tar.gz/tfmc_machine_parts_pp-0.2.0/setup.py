# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Copyright 2021 TechnipFMC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import setuptools
import tfmc.machine_parts_pp as pp

with open('README.md', 'r') as fh:
    long_description = fh.read()

__version__ = pp.__version__
    
setuptools.setup(
    name='tfmc_machine_parts_pp',
    version=__version__,
    author='Daniel Bakkelund, Marcel Castro',
    author_email='daniel.bakkelund@ifi.uio.no, marcel.cavalcantidecastro@technipfmc.com',
    description='Planted partitions over machine part data with part-of relations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tfmcdigital/tfmc-data-in-brief-article/tree/main/python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
    ],
    package_data={'tfmc':['*.csv','*.json']},
    python_requires='>=3.0',
    install_requires=[
        'numpy'
    ],
    zip_safe=False
)
