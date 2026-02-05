import os
from ultralytics import YOLO
import cv2

OUTPUT_FOLDER ='static/output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def prediction_image(image_path):
    try:
        # Load the YOLO model
        model = YOLO(r'Users\ship.pt')

        # Load and process the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        # Perform detection
        results = model.predict(image)

        # Visualize results
        annotated_image = results[0].plot()  # Annotated image with bounding boxes

        # Save the output
        output_filename = f"output_{os.path.basename(image_path)}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        cv2.imwrite(output_path, annotated_image)
        
        # Get detection results
        boxes = results[0].boxes
        num_ships = len(boxes)
        
        return {
            'success': True,
            'output_path': output_path,
            'num_ships': num_ships,
            'message': f'Successfully detected {num_ships} ships'
        }
    except Exception as e:
        return {
            'success': False,
            'output_path': None,
            'num_ships': 0,
            'message': f'Error processing image: {str(e)}'
        }
