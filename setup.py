from setuptools import setup
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('personal_mycroft_backend')

setup(
    name='personal-mycroft-backend',
    version='0.1.4',
    packages=['personal_mycroft_backend', 'personal_mycroft_backend.extra',
              'personal_mycroft_backend.backend',
              'personal_mycroft_backend.utils',
              'personal_mycroft_backend.database',
              'personal_mycroft_backend.frontend'],
    install_requires=['Flask>=0.12', 'WTForms>=2.1', 'SQLAlchemy>=1.1.9',
                      'bcrypt>=3.1.3', 'requests>=2.2.1', 'Flask-Mail',
                      'pygeoip', 'SpeechRecognition', 'pyOpenSSL',
                      "flask_sslify"],
    package_data={'': extra_files},
    include_package_data=True,
    url='',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description=''
)
