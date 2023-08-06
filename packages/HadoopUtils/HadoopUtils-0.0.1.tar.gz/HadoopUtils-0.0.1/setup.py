from setuptools import setup,find_packages 
setup(name='HadoopUtils',
      version='0.0.1',
      description='Use python to connect to the relevant configuration of the CDP cluster',
      author='Zhuhs',
      author_email='zhuhs087@163.com',
      requires= ['impyla','boto3','kafka'], 
      packages=find_packages(),  
      license="apache 3.0"
      )
