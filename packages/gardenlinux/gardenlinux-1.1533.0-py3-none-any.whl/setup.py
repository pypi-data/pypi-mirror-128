import os
import setuptools
import setuptools.command.build_py


own_dir = os.path.abspath(os.path.dirname(__file__))


# Removing specific modules from packages turns out to be tricky. Create a custom package-
# builder, override the method used to find package-modules and just skip over the
# module in question (ccc.deliverydb, hardcoded for now).
class custom_build_py(setuptools.command.build_py.build_py):
    def find_package_modules(self, package, package_dir):
        return [
            (package, module, filename)
            for package, module, filename in super().find_package_modules(package, package_dir)
            if not (package == 'ccc' and module == 'deliverydb')
        ]


def requirements():
    yield 'gardener-cicd-base>=' + version()
    yield 'gardener-oci>=' + version()

    with open(os.path.join(own_dir, 'requirements.txt')) as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if 'elasticsearch' in line:
                continue

            yield line


def modules():
    module_names = [
        os.path.basename(os.path.splitext(module)[0]) for module in
        os.scandir(path=own_dir)
        if module.is_file() and module.name.endswith('.py')
    ]

    # remove modules already contained in gardener-cicd-base
    module_names.remove('util')
    module_names.remove('ctx')
    module_names.remove('setup.base')
    module_names.remove('setup.gardenlinux')
    module_names.remove('setup.oci')
    module_names.remove('setup.whd')
    # remove modules already contained in gardener-cicd-dso
    module_names.remove('setup.dso')
    return module_names


def packages():
    package_names = setuptools.find_packages()

    # remove packages already contained in gardener-cicd-base
    package_names.remove('ci')
    package_names.remove('model')
    package_names.remove('oci')
    # remove whd (released in separate module)
    package_names.remove('whd')
    # remove dso (released in separate module)
    package_names.remove('checkmarx')
    package_names.remove('clamav')
    package_names.remove('deliverydb')
    package_names.remove('protecode')
    package_names.remove('whitesource')

    return package_names


def version():
    with open(os.path.join(own_dir, 'VERSION')) as f:
        return f.read().strip()


setuptools.setup(
    name='gardener-cicd-libs',
    version=version(),
    description='Gardener CI/CD Libraries',
    python_requires='>=3.9.*',
    py_modules=modules(),
    packages=packages(),
    package_data={
        '':['*.mako', 'VERSION'],
        'concourse':[
            'resources/LAST_RELEASED_TAG',
            'resources/*.mako',
            '*.mako',
        ],
    },
    install_requires=list(requirements()),
    entry_points={
    },
    cmdclass={'build_py': custom_build_py},
)
