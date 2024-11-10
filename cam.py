import cv2
import numpy as np
from PIL import Image
import torch

from mltu.inferenceModel import OnnxInferenceModel
from configs import ModelConfigs
from inferenceModel import ImageToWordModel

class CameraTextRecognition:
    def __init__(self, model_path, vocab, img_height, img_width):
        self.model = ImageToWordModel(model_path=model_path)
        self.vocab = vocab
        self.img_height = img_height
        self.img_width = img_width

    def process_frame(self, frame):
        # Preprocess the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.img_width, self.img_height))
        frame = np.expand_dims(frame, axis=0)

        # Make prediction
        prediction = self.model.predict(frame[0])

        # Decode the prediction
        text = self.decode_prediction(prediction)

        return text

    def decode_prediction(self, prediction):
        index_to_char = {index: char for index, char in enumerate(self.vocab)}
        text = ''.join([index_to_char[index] for index in np.argmax(prediction, axis=1)])
        return text.replace('▁', ' ')

if __name__ == "__main__":
    # Load the trained model and configurations
    configs = ModelConfigs()
    model = CameraTextRecognition(
        model_path="Models/08_handwriting_recognition_torch/202411060704/model.onnx",
        vocab=configs.vocab,
        img_height=configs.height,
        img_width=configs.width
    )

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        text = model.process_frame(frame)
        print(f"Recognized text: {text}")

        # Display the frame with recognized text
        cv2.imshow("Camera Text Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()