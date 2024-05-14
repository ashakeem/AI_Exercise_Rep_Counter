import cv2 

class Camera:

    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        if not self.camera.isOpened():
            raise Exception("Could not open camera")
            
        self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def getFrame(self):

        if self.camera.isOpened():
            ret, frame = self.camera.read()

            if not ret:
                return (ret,None)

            else:
                return (ret,cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  

        else:
            return None        
    
    
    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()          
          