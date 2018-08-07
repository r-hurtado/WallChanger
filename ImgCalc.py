#! /usr/bin/python
import sys
from PIL import Image
import csv
import os

#default value
dirs = ['~/Pictures/']

#Why does these need to be arrays?
savLoc = ['~/Pictures/']
logNum = [10]

#array to hold all image paths
imgPaths = []

'''
Read as two column CSV, where col zero is the data type and col one is the data
Type options: 
  dir: directory
  sav: location to save temporary image to
  log: number of previous walls to save as a type of log.
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
      imgPaths.append('{}{}'.format(dirName, fileName))

def PickWalls():  
  #Recursive loop
  CheckSubDir('/home/miecatt/Pictures/Walls')

  #Checking for duplicates
  print('Images list: {}'.format(len(imgPaths)))
  imgPathSet = set(imgPaths)
  print('Images set:  {}'.format(len(imgPathSet)))
  for i in range(0, len(imgPaths), 1000):
    print(imgPaths[i])

  return 'Test1.jpg', 'Test2.jpg'

#takes the path of two images and concatenates them horizontally
def ConCatImg(img0, img1):
  images = map(Image.open, [img0, img1])
  widths, heights = zip(*(i.size for i in images))

  total_width = sum(widths)
  max_height = max(heights)

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
  img0, img1 = PickWalls()
  ConCatImg(img0, img1)
  
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
