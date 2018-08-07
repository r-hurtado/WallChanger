#! /usr/bin/python
import sys
from PIL import Image
import csv
import os
import random
import pyglet

#Seed RNG to insure chaos
random.seed()

#default value
dirs = ['~/Pictures/']

#Why does these need to be arrays?
savLoc = ['~/Pictures/']
logNum = [10]

#arrays to hold all image paths
imgHorizPaths = []
imgVertiPaths = []

#A list of 5-tuples in the form of (x, y, width, height, path)
#Represents monitor layout
screens = []

'''
Read as two column CSV, where col zero is the data type and col one is the data
Type options: 
  dir: directory
  sav: location to save temporary image to
  log: number of previous walls to save as a type of log.
  --something to help determine monitor layout
  more to come
'''
def ReadPrefs():  
  with open('Preferences.conf', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      
      #if there are directories listed in .conf, replace with default
      if row["type"] == 'dir':
        if dirs[0] == '~/Pictures/':
          dirs.pop()
        dirs.append(row["data"])

      #if there is a save location given, replace old one (only stores last)
      elif row["type"] == 'sav':
        savLoc[0] = row["data"]

      #if there is a save location given, replace old one (only stores last)
      elif row["type"] == 'log':
        logNum[0] = int(row["data"])

def CheckSubDir(subDir):
  for dirName, dirNames, fileNames in os.walk(subDir):
    for subDirName in dirNames:
      CheckSubDir(subDirName)
    for fileName in fileNames:
      #Only support .jpg for now, needs further testing in ConCatImg()
      #Need to add some logic here that seperates vertical form ladscape
      if '.jpg' in fileName:
        img = Image.open('{}/{}'.format(dirName, fileName))
        width, height = img.size
        if width < height:
          imgVertiPaths.append('{}/{}'.format(dirName, fileName))
        else:
          imgHorizPaths.append('{}/{}'.format(dirName, fileName))

def PickWalls():  
  #Recursive loop
  for directory in dirs:
    CheckSubDir(directory)

  platform = pyglet.window.get_platform()
  display = platform.get_default_display()
  for screen in display.get_screens():
    scrInfo = str(screen).split(', ')
    x = int(scrInfo[1].split('x=')[1])
    y = int(scrInfo[2].split('y=')[1])
    w = int(scrInfo[3].split('width=')[1])
    h = int(scrInfo[4].split('height=')[1])
    if w < h:
      p = random.sample(imgVertiPaths, 1)[0]
    else:
      p = random.sample(imgHorizPaths, 1)[0]
    screens.append((x, y, w, h, p))

def ConCatImg():
  imgs = []
  for i in screens:
    imgs.append(i[4])
    print i

  images = map(Image.open, imgs)
  widths, heights = zip(*(i.size for i in images))

  #Only support dual 1920x1080 monitors currently
  total_width = 1920*2 #sum(widths)
  max_height = 1080 #max(heights)

  #Create blank image at new size
  new_im = Image.new('RGB', (total_width, max_height))

  #Insert images into new blank image
  x_offset = 0
  for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

  #"Backup" wallpapers to "log"
  for x in range(logNum[0]):
    #create variable because of scoping issues
    oldImg = 0

    #Try to open prior image
    try:
      oldImg = Image.open('{}{}{}{}'.format(savLoc[0], 'Wall', logNum[0] - x - 1, '.jpg'))
    except: #IOError as e: <- Use to print
      #If IO fails for any reason just create a 1x1 black image
      oldImg = Image.new('RGB', (1, 1))

    oldImg.save('{}{}{}{}'.format(savLoc[0], 'Wall', logNum[0] - x, '.jpg'))

  #save image to path of concatonated wallpaper
  new_im.save('{}{}'.format(savLoc[0], 'Wall0.jpg'))

def main():
  pass
  ReadPrefs()
  PickWalls()
  ConCatImg()
  
  '''
  for x in dirs:
    print 'dir: {}'.format(x)

  print 'sav: {}'.format(savLoc[0])
  print 'log: {}'.format(logNum[0])
  '''
  
  fLoc = open("saveLocation.txt", "w")
  fLoc.write('{}{}{}'.format('file://', savLoc[0], 'Wall0.jpg'))

#Need to call main to run the script
main()
