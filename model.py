import cv2
import numpy as np
import PIL
from sklearn.svm import LinearSVC

class Model:
    def __init__(self):
        self.model = LinearSVC()
        
        
        
    def trainModel(self, counters):
        imgList = np.array([])
        groupList = np.array([])
        
        for i in range(1, counters[0]):
            img = cv2.imread(f"1/frame{i}.jpg")[:,:,0]
            img = img.reshape(16950)
            imgList = np.append(imgList, [img])
            groupList = np.append(groupList, 1)
            
        for i in range(1, counters[1]):
            img = cv2.imread(f"2/frame{i}.jpg")[:,:,0]
            img = img.reshape(16950)
            imgList = np.append(imgList, [img])
            groupList = np.append(groupList, 2)
            
            
            
        imgList = imgList.reshape(counters[0]-1+counters[1]-1, 16950)
        
        
        self.model.fit(imgList, groupList)
        print("Model trained successfully!")
        
        
        
        
    def predict(self, frame):
        frame = frame[1]
        cv2.imwrite("frame.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        img = PIL.Image.open("frame.jpg")
        img.thumbnail((150,150), PIL.Image.ANTIALIAS)
        
        img.save("frame.jpg")
        img = cv2.imread("frame.jpg")[:,:,0]
        img = img.reshape(16950)
        
        prediction = self.model.predict([img])
        return prediction[0]
          