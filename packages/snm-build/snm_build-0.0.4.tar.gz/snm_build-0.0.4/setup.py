import setuptools

setuptools.setup(name='snm_build',
                 version='0.0.4',
                 description='Building and release project',
                 packages=setuptools.find_packages(),
                 install_requires=['pyinstaller>=4.5.1'],
                 author_email='serheos@gmail.com',
                 zip_safe=False)
