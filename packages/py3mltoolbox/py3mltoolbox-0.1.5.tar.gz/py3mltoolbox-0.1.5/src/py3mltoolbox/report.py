import os
import sys
import random
import py3toolbox as tb
import matplotlib.pyplot as plt



def preview_images(data, labels, count=10, save_folder=None):
  """
    Data is numpy array, transform to image and save 
  
  """  
  preview_files = []
  for i in range(1,count+1):
    preview_index = random.choice(range(1,len(data)+1))
    plt.clf()
    plt.title(str(labels[preview_index]))
    plt.imshow(data[preview_index], interpolation='nearest')
    plt.tight_layout()
    preview_file = save_folder + "/preview_" + str(preview_index) + "." + str(labels[preview_index]) + ".png"
    plt.savefig(preview_file)
    preview_files.append(preview_file)
    plt.clf()  
    
    
def show_result(history, file=None):

  # collect training history data
  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']
  loss = history.history['loss']
  val_loss = history.history['val_loss']
  epochs = range(len(acc))

  # draw result
  plt.clf()
  fig = plt.figure()
  
  ax1 = fig.add_subplot(121)
  ax1.plot(epochs, acc, 'r', label='Train accuracy')
  ax1.plot(epochs, val_acc, 'b', label='Val accuracy')
  ax1.title.set_text('Train/Val Accuracy')
  ax1.set_xlabel('epoches')
  ax1.set_ylabel('Accuracy')
  ax1.legend()
  
  ax2 = fig.add_subplot(122)

  ax2.plot(epochs, loss, 'r', label='Train Loss')
  ax2.plot(epochs, val_loss, 'b', label='Val Loss')
  ax2.title.set_text('Train/Val Loss')
  ax2.set_xlabel('epoches')
  ax2.set_ylabel('Loss')
  ax2.legend()
  plt.tight_layout()
  if file is not None:
    fig.savefig(file)

  plt.show()


def gen_report(save_folder):
  html = ""
  html += "<HTML>"
  html += "<BODY>"
  html += "<TABLE WIDTH=1800>"

  
  
  html += "</BODY>"
  html += "</HTML>"
  
  
  
  
  
  pass