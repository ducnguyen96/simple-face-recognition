## Demo

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/y5h_FX7mhdE/0.jpg)](https://www.youtube.com/watch?v=y5h_FX7mhdE)

## 0. Requirements

1. python==3.6.2
2. tensorflow==1.3.0
3. keras==2.1.2

details in the `packages.txt`

## 1. How to test

Because I updated the model for classifying on more than 1000 classes so the model now is pretty big (>159 MB) so I can't upload to github.
You can train your model follow the steps below

```sh
python main.py
```

## 2. How to train your all data set

0. You can use this tool https://github.com/Joeclinton1/google-images-download to download image

- go to `google-images-download` folder --> update config file --> python google_images_download.py

1. Put your data as

```
project
│
└───src
│
└───static
│
└───downloads
│   └───Emma Watson
│   │   │pic1.jpg
│   │   │pic2.jpg
│   │
│   └───Albert Baldwin
│       │pic1.jpg
│       │pic2.jpg
│
│debug.py
│Dockerfile
│README.md
```

2. python split_data.py

3. python train.py

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
