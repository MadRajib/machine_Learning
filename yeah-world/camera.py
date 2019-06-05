#!/usr/bin/python
import cv2, queue, threading

# bufferless VideoCapture
class Camera:

  def __init__(self,training_mode=False ):
    self.cap = cv2.VideoCapture(0)
    self.q = queue.Queue()
    self.t = threading.Thread(target=self._reader)
    self.t.daemon = True
    self.t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      frame  = cv2.resize(frame,(128,128),3)
      M = cv2.getRotationMatrix2D((64,64), 90, 1.0)
      frame = cv2.warpAffine(frame, M, (128, 128))
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      
      self.q.put(frame)

  def next_frame(self):
    return self.q.get()

  def release(self):
    self.release()
    self.t.terminate()
