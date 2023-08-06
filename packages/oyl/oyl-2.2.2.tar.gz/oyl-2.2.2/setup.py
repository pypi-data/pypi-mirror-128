from setuptools import setup,find_packages
setup(name='oyl',version='2.2.2',author='Lin Ouyang', 
    packages=["oyl","oyl.nn"], 
    include_package_data=True,
    install_requires=["numpy","matplotlib","cartopy",
                      "xarray","sklearn","pyshp"]
)
