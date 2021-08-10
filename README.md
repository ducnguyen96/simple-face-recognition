## 0. Requirements
  1. python==3.6.2
  2. tensorflow==1.3.0
  3. keras==2.1.2
   
details in the `packages.txt`

## 1. How to test
```sh
python main.py
```

## 2. How to train your all data set
1. Update data folder

2. Comment out the flask app

3. Uncomment 3 lines in the main function 

4. python main.py

## 3. How to install specified version of Python

1. First use need building tools
```sh
sudo apt-get install libssl-dev openssl make gcc
```

2. Download version you want to install
```sh
# Search for specified version here https://www.python.org/
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
tar xzvf Python-3.6.2.tgz
cd Python-3.6.2
```

3. Compile and build
```sh
./configure
make
make install
```
4. Create symlink
```sh
sudo ln -fs /opt/Python-3.6.2/Python /usr/bin/python3.6.2

```

## 4. Use specified version of Python on your project
```sh
virtualenv your-project --python=python3.6.2
source your-project/bin/activate
python --version
```

## 5. How to list installed packages
```sh
python3 -m pip freeze > packages.txt
```