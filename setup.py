from setuptools import setup

setup(name='snaplint',
      version='0.2',
      description='Clean up your snap',
      author='Scott Sweeny',
      author_email='scott.sweeny@canonical.com',
      packages=['snaplint',
                'snaplint.rules'],
      entry_points=dict(
          console_scripts=[
              'snaplint = snaplint.__main__:main'
          ]),
)
