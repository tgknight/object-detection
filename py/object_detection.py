import cv2
import numpy as np
import json
import sys
import re
import os
from darkflow.net.build import TFNet

def get_full_path(*args):
    return os.path.join(os.getcwd(), *args)

def model_init(cfg_path='yolo/yolo.cfg', weights_path='yolo/yolo.weights'):
    return TFNet({
        'model': cfg_path,
        'load': weights_path,
        'threshold': 0.1
    })

def extract_prediction_result(results, threshold=0.2):
    return list(filter(lambda result: result['confidence'] >= threshold, results))

def label_object_in_image(image, filtered_result):
    topleft = filtered_result['topleft']
    bottomright = filtered_result['bottomright']

    cv2.rectangle(image,
                  (topleft['x'], topleft['y']),
                  (bottomright['x'], bottomright['y']),
                  (220, 220, 0),
                  3)
    cv2.putText(image,
                filtered_result['label'],
                (topleft['x'] + 20, topleft['y'] + 20),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (255, 0, 127),
                thickness=2,
                lineType=cv2.LINE_AA)

def save_labeled_image(image, path, filtered_results):
    save_path = ['prediction', path.split('/')[-1]]

    for filtered_result in filtered_results:
        label_object_in_image(image, filtered_result)
    cv2.imwrite(get_full_path(*save_path), image)

def format_result(results):
    return list(map(lambda result: {result['label']: str(result['confidence'])}, results))

def predict(model, path, save=False):
    image = cv2.imread(path)
    # model = model_init() # assumed that model is already initialized
    results = model.return_predict(image)
    objects = extract_prediction_result(results, 0.4)

    if save:
        save_labeled_image(image, path, objects)

    return format_result(objects)

if __name__ == '__main__':
    print(predict(sys.argv[1], sys.argv[2]))
