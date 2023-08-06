from distutils.core import setup
setup(
  name = 'cmdMenuFramework',         
  packages = ['cmdMenuFramework'],  
  version = '1.0.3',
  license='MIT',
  description = 'This is a library/framework specialised in creating a command line menus, through the use of yaml files.',   # Give a short description about your library
  author = 'ARAGON Esteban',             
  author_email = 'aragonstban@gmail.com', 
  url = 'https://github.com/Este2013/command_line_menu_python',   
  download_url = 'https://github.com/Este2013/command_line_menu_python/archive/refs/tags/v1.0.3.tar.gz', 
  keywords = ['command', 'cmd', 'line', 'menu', 'framework'], 
  install_requires=[  
          'colorama',
          'pyyaml',
          'importlib'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',   # Choices are ["3 - Alpha", "4 - Beta", "5 - Production/Stable"]
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)