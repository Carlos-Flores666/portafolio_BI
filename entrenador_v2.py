# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:07:00 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:25:35 2023

@author: carlo
"""

import cv2
import os
#import imutils
import numpy as np

personName = input('nombre: ')
dataPath = 'C:/Users/carlo/Documents/reconocimiento_facial/fotos' #Cambia a la ruta donde hayas almacenado Data
personPath = dataPath + '/' + personName+ '/' + personName

if not os.path.exists(personPath):
	print('Carpeta creada: ',personPath)
	os.makedirs(personPath)

#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture('C:/Users/carlo/Documents/reconocimiento_facial/videos/'+personName+'.mp4')

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
count = 0

while True:

	ret, frame = cap.read()
	if ret == False: break
	#frame =  cv2.resize(frame, (150,150))
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	auxFrame = frame.copy()

	faces = faceClassif.detectMultiScale(gray,1.3,5)

	for (x,y,w,h) in faces:
		cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
		rostro = auxFrame[y:y+h,x:x+w]
		rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
		cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
		count = count + 1
	cv2.imshow('frame',frame)

	k =  cv2.waitKey(1)
	if k == 27 or count >= 800:
		break

cap.release()
cv2.destroyAllWindows()



nombre = personName
dataPath = 'C:/Users/carlo/Documents/reconocimiento_facial/fotos/'+nombre#Cambia a la ruta donde hayas almacenado Data
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
	personPath = dataPath + '/' + nameDir
	print('Leyendo las imágenes')

	for fileName in os.listdir(personPath):
		#print('Rostros: ', nameDir + '/' + fileName)
		labels.append(label)
		facesData.append(cv2.imread(personPath+'/'+fileName,0))
		image = cv2.imread(personPath+'/'+fileName,0)
		cv2.imshow('image',image)
		cv2.waitKey(10)
	label = label + 1

#print('labels= ',labels)
#print('Número de etiquetas 0: ',np.count_nonzero(np.array(labels)==0))
#print('Número de etiquetas 1: ',np.count_nonzero(np.array(labels)==1))

# Métodos para entrenar el reconocedor
#face_recognizer = cv2.face.EigenFaceRecognizer_create()
#face_recognizer = cv2.face.FisherFaceRecognizer_create()
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Entrenando el reconocedor de rostros
print("Entrenando...")
face_recognizer.train(facesData, np.array(labels))

# Almacenando el modelo obtenido

face_recognizer.write('C:/Users/carlo/Documents/reconocimiento_facial/modelos/'+nombre+'.xml')

print("Modelo almacenado...")