from setuptools import setup,find_packages
setup(name='oyl',version='2.2.1',author='Lin Ouyang', 
    packages=["src.oyl","src.oyl.nn"], 
    include_package_data=True,
    package_data={
        "oyl": ["shapefiles/*"],
    },
    install_requires=["cartopy","xarray","sklearn"]
)
