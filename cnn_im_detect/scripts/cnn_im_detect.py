import argparse
import cv2
import numpy as np
import tensorflow as tf
import rclpy
from rclpy.executors import SingleThreadedExecutor

#importing the custom service created
from customsrv.srv import ImgStr

#creating a class for the service definition
class Service:
  def __init__(self):
    self.node = rclpy.create_node('image_client')
    self.srv = self.node.create_service(ImgStr, 'image_detect', self.detect_callback)

  def detect_callback(self, request, response):
    #loading the tensorflow graph
    model_file = \
    "Tensorflow/Temp_fc/output_graph.pb"
    label_file = "Tensorflow/Temp_fc/output_labels.txt"
    input_layer = "Placeholder"
    output_layer = "final_result"
    graph = load_graph(model_file)
    print("received data")
    global img
    for i in range(224):
      for j in range(224):
       for k in range(3):
          img[j,i,k]=request.im.data[k+j*3+i*224*3]
    
    #converting the image into a tensor form
    t = read_tensor_from_image_file(img)
   
    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)
    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t })
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    response.veg.data = labels[top_k[0]]
    for i in top_k:
        print(labels[i], results[i])
    return response

#defining the load graph function
def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()
  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)
  return graph

#defining the function which converts the image data into a tensor
def read_tensor_from_image_file(img):
  np_image_data = np.asarray(img)
  np_image_data= np.divide(np_image_data.astype(float),255)
  np_final = np.expand_dims(np_image_data,axis=0)
  return np_final

def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label

def main(args=None):
  rclpy.init(args=args)
  print("creating service")
  #create the service
  service = Service()
  
  #spinning the node with a blocking call 
  print("spinning")
  executor = SingleThreadedExecutor()
  executor.add_node(service.node)
  executor.spin_once(timeout_sec=-1)

if __name__ == '__main__':
    main()
