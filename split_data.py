import os
import math
import pickle
from pathlib import Path

print('Making data folders ...........')
Path("./data/train").mkdir(parents=True, exist_ok=True)
Path("./data/val").mkdir(parents=True, exist_ok=True)

print('Splitting .....................')

for person in os.listdir('./downloads'):
    os.mkdir('./data/train/' + person)
    os.mkdir('./data/val/' + person)
    num_path = len(os.listdir('./downloads/' + person))

    val_num_path = math.floor(num_path * 0.2)
    train_num_path = num_path - val_num_path

    index = 0
    for pic in os.listdir('./downloads/' + person):
        if index < val_num_path:
            os.replace('./downloads/' + person + '/' + pic,
                       "./data/val/" + person + '/' + pic)
            index = index + 1
        else:
            os.replace('./downloads/' + person + '/' + pic,
                       "./data/train/" + person + '/' + pic)

print('Saving People Names ..............')
with open('./src/model/data/trainy', 'wb') as fp:
    pickle.dump(os.listdir('./data/train'), fp)


print('Done !')
