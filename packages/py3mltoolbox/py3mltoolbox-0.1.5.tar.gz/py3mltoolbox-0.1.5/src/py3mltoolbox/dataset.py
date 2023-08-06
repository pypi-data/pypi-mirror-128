import os, sys
import py3toolbox as tb
import tensorflow_datasets as tfds



def load_tf_dataset(dataset_name="mnist"):
  """
    Load Tensorflow Datasets
    Save the result datasets into Train and Test
  
  """
  ds_train, ds_test = tfds.load(name=dataset_name,
                       split = ['train', 'test'], 
                       batch_size = -1,
                       as_supervised=True)


  # to shuffle
  #ds_train = ds_train.shuffle(buffer_size=10)  
  #ds_test  = ds_test.shuffle(buffer_size=10)  


  (train_data, train_labels)        =   tfds.as_numpy(ds_train)
  (test_data, test_labels)          =   tfds.as_numpy(ds_test)


  print ("Train Data    Shape  (numpy) : " + str(train_data.shape))
  print ("Train Labels  Shape  (numpy) : " + str(train_labels.shape))
  print ("Test  Data    Shape  (numpy) : " + str(test_data.shape))
  print ("Test  Labels  Shape  (numpy) : " + str(test_labels.shape))

  
  return ((train_data, train_labels), (test_data, test_labels))
  
  
