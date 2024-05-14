import tkinter as tk
import os
import PIL.Image, PIL.ImageTk
import cv2
import camera
import model



class App:
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AI Workout Rep Counter")
        
        
        self.counters = [1,1]
        self.repCounter = 0
        
        # portions of the movements
        self.extended = False
        self.contracted = False
        
        # previous position of the arm
        self.lastPosition = 0
        
        self.model = model.Model() # model to be trained
        
        self.countingEnabled = False
        self.camera = camera.Camera()
        
        self.init_gui()
        
        
        self.delay = 15
        self.update()
        
        self.window.attributes("-topmost", True)
        self.window.mainloop()
        
        
        
    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()
        
        self.btn_toggleCount = tk.Button(self.window, text="Toggle Counting", width=50, command=self.countingToggle)
        self.btn_toggleCount.pack(anchor=tk.CENTER, expand=True)
        
        # count reps for group one(extending the arm)
        self.btn_groupOne = tk.Button(self.window, text="Extended", width=50, command= lambda: self.saveForGroup(1))
        self.btn_groupOne.pack(anchor=tk.CENTER, expand=True)
        
        # count reps for group two(contracting the arm)
        self.btn_groupTwo = tk.Button(self.window, text="Contracted", width=50, command=lambda: self.saveForGroup(2))
        self.btn_groupTwo.pack(anchor=tk.CENTER, expand=True)
        
        
        
        self.btn_train = tk.Button(self.window, text="Train", width=50, command=lambda: self.model.trainModel(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)
        
        
        
        self.counterLabel = tk.Label(self.window, text=f"{self.repCounter} Reps")
        self.counterLabel.config(font=("Courier", 44))
        self.counterLabel.pack(anchor=tk.CENTER, expand=True)
       
        
        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)
        
      
      
    def update(self):
        if self.countingEnabled:
            self.predict()
            
        if self.extended and self.contracted:
            self.extended = False
            self.contracted = False
            self.repCounter += 1
                
                
        self.counterLabel.config(text=f"{self.repCounter} Reps")
            
        ret, frame = self.camera.getFrame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image=self.photo, anchor=tk.NW)
                
                
        self.window.after(self.delay, self.update)
   
   
    def predict(self):
        frame =self.camera.getFrame()
        prediction = self.model.predict(frame)
        
        if prediction != self.lastPosition:
            if prediction == 1:
                self.extended = True
                self.lastPosition = 1
                
            elif prediction == 2:
                self.contracted = True
                self.lastPosition = 2
        

    
    def countingToggle(self):
        self.countingEnabled = not self.countingEnabled
    
    
    def saveForGroup(self, group):
        ret, frame = self.camera.getFrame()
        if not os.path.exists("1"):
            os.makedirs("1")
        if not os.path.exists("2"):
            os.makedirs("2")
            
            
        # save the frame to the appropriate group folder and resize it to 150x150 pixels 
        cv2.imwrite(f"{group}/frame{self.counters[group-1]}.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)) # save the frame
        img = PIL.Image.open(f"{group}/frame{self.counters[group-1]}.jpg")
        img.thumbnail((150,150), PIL.Image.ANTIALIAS)
        img.save(f"{group}/frame{self.counters[group-1]}.jpg")
        
        
        self.counters[group-1] += 1
   

    
    def reset(self):
        self.repCounter = 0
        
        