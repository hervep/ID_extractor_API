# Import packages
import os
import sys

import cv2
import numpy as np
import tensorflow as tf

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from app.utils_extractor import label_map_util
from app.utils_extractor import visualization_utils as vis_util

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.dirname(os.path.realpath(__file__)) + '/model/frozen_inference_graph.pb'

# Path to label map file
PATH_TO_LABELS = os.path.dirname(os.path.realpath(__file__)) + '/data/labelmap.pbtxt'

# Number of classes the object detector can identify
NUM_CLASSES = 1

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.compat.v1.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')


# Load image using OpenCV and
# expand image dimensions to have shape: [1, None, None, 3]
# i.e. a single-column array, where each item in the column has the pixel RGB value

def convert_pdf_to_image (pdf):
    # conversion du pdf en image

    from pdf2image import convert_from_path, convert_from_bytes
    # from IPython.display import display #, Image

    images = convert_from_bytes(open(pdf, 'rb').read())
    # display(images[0])
    #i = 0
    #for page in images:
     #   indice = str(i)
     #   page.save('out' + indice + '.JPG', 'JPEG')
     #   i = i + 1
    return images

def get_card_from_image(image):
    """
    :param image: image = cv2.imread(image_path)
    :return: {
        "success": Boolean,
        "output_image": OpenCv Image object,
        "reason": Reason for failure in case success is False
    }
    """

    image_expanded = np.expand_dims(image, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
                                             feed_dict={image_tensor: image_expanded})

    # Draw the results of the detection (aka 'visulaize the results')
    image1, array_coord = vis_util.visualize_boxes_and_labels_on_image_array(image,
                                                                             np.squeeze(boxes),
                                                                             np.squeeze(classes).astype(np.int32),
                                                                             np.squeeze(scores),
                                                                             category_index,
                                                                             use_normalized_coordinates=True,
                                                                             line_thickness=10,
                                                                             min_score_thresh=0.60)

    ymin, xmin, ymax, xmax = array_coord
    shape = np.shape(image1)
    im_width, im_height = shape[1], shape[0]
    (left, right, top, bottom) = (xmin * 0.5 * im_width, xmax * im_width * 1, ymin * im_height * 0.5, ymax * im_height * 1)

    if ymin == xmax == xmin == ymax == 0:
        return image1
    else:
        cropped_image = image[int(top):int(bottom), int(left):int(right)]
        return cropped_image




if __name__ == '__main__':



    pdf = './carte20182019.pdf'
    result = convert_pdf_to_image (pdf);
    i = 0
    for page in result:
        indice = str(i)
        page.save('out' + indice + '.JPG', 'JPEG')
        i = i + 1

    
    #test_image_filepath ='C:/Users/djakd/Desktop/TFE/TITRE DE SEJOUR1.JPG'
    #test_image_filepath = 'C:/Users/djakd/Desktop/TFE/id_card_extractor-1.2.0.tar/dist/id_card_extractor-1.2.0/id_card_extractor/out0.JPG'
    #image = cv2.imread(test_image_filepath)
    image = cv2.imread('out0.jpg')

    cropped_image_response = get_card_from_image(image)

    #cv2.imshow("cropped_card", cropped_image_response)
    cv2.imwrite("cropped_card.jpg", cropped_image_response)


