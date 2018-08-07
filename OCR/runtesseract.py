### Run Tesseract OCR

import os
import subprocess
import PIL
from PIL import Image

### Function takes in:
### 1) a list of strings of image file names
### 2) desired file name of merged file

def runTesseract(image_folder,output_folder,file_names,merged_file_name):

    tesseractFolder = 'Tesseract-OCR\\'

    for i in range(0,len(file_names)):
        imageName = file_names[i]
        outputName = 'output'+str(i+1)+'.txt'

        print(image_folder+imageName)

        #THRESHOLD IMAGE
        image_file = Image.open(image_folder+imageName)
        threshold = 177
        img = image_file.convert('L')
        img = img.point(lambda p: p > threshold and 255)

        #CROP IMAGE
        croppedName = 'cropped.png'
        width, height = img.size
        croppedIm = img.crop((0,height/6,width/2,height))
        croppedIm.save(croppedName, dpi=(300,300))

        command = [tesseractFolder+'tesseract','--psm','11',croppedName,'-','>',output_folder+outputName]

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = process.communicate()[0]
        exitCode = process.returncode
        print(output)

    mergeFiles = subprocess.Popen(['copy','/b',output_folder+'*.txt',output_folder+merged_file_name], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outputMerge = mergeFiles.communicate()[0]
    exitCodeMerge = mergeFiles.returncode
    print(outputMerge)
    
    return


if __name__ == '__main__':
    main()
