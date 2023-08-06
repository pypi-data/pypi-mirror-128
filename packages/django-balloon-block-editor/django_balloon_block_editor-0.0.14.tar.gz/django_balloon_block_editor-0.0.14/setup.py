from setuptools import setup, find_packages


with open('VERSION.txt') as f:
    version = f.readline()


setup(
    name='django_balloon_block_editor',
    version=version,
    url='https://github.com/matix-io/django-balloon-block-editor',
    license='MIT',
    description='Implementation of CKEditor\'s Balloon Block Editor, for Django.',
    long_description='',
    author='Connor Bode',
    author_email='connor@matix.io',
    packages=find_packages(),
	include_package_data=True,
    install_requires=[
		'pillow',
	],
    zip_safe=False,
    classifiers=[],
)
