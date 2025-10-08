import gradio as gr
from ultralytics import YOLO
import numpy as np
from PIL import Image

# Load your trained YOLO model
model = YOLO("your_model.pt")  # <-- replace with your model file name

# Function to run crack detection
def detect_crack(image):
    # Convert PIL image to numpy array if needed
    if isinstance(image, Image.Image):
        image = np.array(image)
        
    # Run prediction
    results = model.predict(image)
    
    # Get result image with detections
    result_image = results[0].plot()  # returns image with boxes drawn
    
    return result_image

# Gradio interface
iface = gr.Interface(
    fn=detect_crack,
    inputs=gr.Image(type="numpy"),
    outputs=gr.Image(),
    title="Building Crack Detection",
    description="Upload an image of a wall or structure to detect cracks automatically."
)

# Launch the app (Hugging Face does this automatically)
iface.launch()
