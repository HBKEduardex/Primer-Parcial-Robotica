from setuptools import find_packages, setup

package_name = 'ejer1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/ejer1/launch', ['launch/all_nodes.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='israel',
    maintainer_email='israel@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'sensor1_pub= ejer1.sensor1_pub:main',
        'sensor2_pub= ejer1.sensor2_pub:main',
        'sensor3_pub= ejer1.sensor3_pub:main',
        'nodo4_sub= ejer1.nodo4_sub:main',
        'nodo5_sub= ejer1.nodo5_sub:main',
        ],
    },
)
