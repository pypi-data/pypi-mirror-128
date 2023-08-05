import os

from setuptools import find_packages, setup


def prerelease_local_scheme(version):
    """
    Return local scheme version unless building on master in CircleCI.

    This function returns the local scheme version number
    (e.g. 0.0.0.dev<N>+g<HASH>) unless building on CircleCI for a
    pre-release in which case it ignores the hash and produces a
    PEP440 compliant pre-release version number (e.g. 0.0.0.dev<N>).
    """
    from setuptools_scm.version import get_local_node_and_date

    if os.getenv('CIRCLE_BRANCH') in ('master', ):
        return ''
    else:
        return get_local_node_and_date(version)


setup(
    name='large-image-source-openjpeg',
    use_scm_version={'root': '../..', 'local_scheme': prerelease_local_scheme},
    setup_requires=['setuptools-scm'],
    description='An Openjpeg tilesource for large_image',
    long_description='See the large-image package for more details.',
    author='Kitware, Inc.',
    author_email='kitware@kitware.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'large-image>=1.0.0',
        'glymur>=0.8.18 ; python_version >= "3.7"',
        'glymur>=0.8.18,<0.9.4 ; python_version < "3.7"',
    ],
    extras_require={
        'girder': 'girder-large-image>=1.0.0',
    },
    license='Apache Software License 2.0',
    keywords='large_image, tile source',
    packages=find_packages(exclude=['test', 'test.*']),
    url='https://github.com/girder/large_image',
    python_requires='>=3.6',
    entry_points={
        'large_image.source': [
            'openjpeg = large_image_source_openjpeg:OpenjpegFileTileSource'
        ],
        'girder_large_image.source': [
            'openjpeg = large_image_source_openjpeg.girder_source:OpenjpegGirderTileSource'
        ]
    },
)
