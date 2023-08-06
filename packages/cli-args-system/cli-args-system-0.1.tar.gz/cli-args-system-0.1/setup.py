from distutils.core import setup
setup(
  name = 'cli-args-system',        
  packages = ['cli_args_system'],
  version = '0.1',    
  license='MIT',     
  description = 'A Cli flags libary  to control argv flags and content',   
  author = 'Mateus Moutinho Queiroz',               
  author_email = 'mateusmoutinho01@gmail.com',      
  url = 'https://github.com/mateusmoutinho/python-cli-args.git',  
  download_url = 'https://github.com/mateusmoutinho/python-cli-args/archive/refs/heads/main.zip',    # I explain this later on
  keywords = ['ARGV', 'ClI ARGUMENTS'], 

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ]
)