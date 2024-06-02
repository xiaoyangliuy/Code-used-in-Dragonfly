"""
Created on Sun Jun  2 00:13:31 2024
@author: lxiaoyang
"""

#Note: learn the .py package import
#Import each image in a folder to dragonfly, predict segmentation with pre-trained model, export segmented images to folder
from ORSServiceClass.segmentation.model.aiinterfacemethods import AIInterfaceMethods
from OrsPlugins.orsimageloader import OrsImageLoader
from OrsHelpers.managedhelper import ManagedHelper
from OrsPythonPlugins.OrsGenericMenuItems.menuItems import extractROIs_026bbe94998911e881c30cc47aab53c3
from OrsPythonPlugins.OrsGenericMenuItems.menuItems import extractROIs_026bbe94998911e881c30cc47aab53c3
from OrsPythonPlugins.OrsGenericMenuItems.menuItems import exportROIAsBinary_cfdc4c58867011e888c684a6c8f5618e
import os
import glob
import time
#input
path = r'/data/2022-12/eBERLight_rec/SM20220926_4_C3_030_rec/'
os.chdir(path)
files = glob.glob('*.tiff')
xSize = 1696
ySize = 1696
zSize = 1
tSize = 1
minX = 0
maxX = 1695
minY = 0
maxY = 1695
minZ = 0
maxZ = 0
xSampling = 1
ySampling = 1
zSampling = 1
tSampling = 1
xSpacing = 1.0
ySpacing = 1.0
zSpacing = 1.0
slope = 1.0
offset = 0.0
dataUnit = 'Density'
invertX = False
invertY = False
invertZ = False
axesTransformation = 0
convertFrom32To16bits = False
dataRangeMin = 0.0
dataRangeMax = 0.0
frameCount = 1
additionalInfo = 'input_image'

modelManagerInstance = AIInterfaceMethods.getAIModelsManager()
modelId = '1c79bdc6209811ef97b680615f0cd2ed'# <-- 2seg_wiz_unet_...model     '1c79bdc6209811ef97b680615f0cd2ed'
modelInstance = AIInterfaceMethods.getAIModel(aiModelManager=modelManagerInstance,modelId=modelId)
mask = None
useMarkedSlices = False
sf_path = r'/data/xiaoyang/seg_030/'
for f in files:
    fileNamesListElement = f
    fileNames = [fileNamesListElement]
    datasetName = f.rpartition('.tiff')[0]
    output = OrsImageLoader.createDatasetFromFiles(fileNames=fileNames,xSize=xSize,ySize=ySize,zSize=zSize,tSize=tSize,minX=minX,
                                               maxX=maxX,minY=minY,maxY=maxY,minZ=minZ,maxZ=maxZ,xSampling=xSampling,
                                               ySampling=ySampling,zSampling=zSampling,tSampling=tSampling,xSpacing=xSpacing,
                                               ySpacing=ySpacing,zSpacing=zSpacing,slope=slope,offset=offset,dataUnit=dataUnit,
                                               invertX=invertX,invertY=invertY,invertZ=invertZ,axesTransformation=axesTransformation,
                                               datasetName=datasetName,convertFrom32To16bits=convertFrom32To16bits,
                                               dataRangeMin=dataRangeMin,dataRangeMax=dataRangeMax,frameCount=frameCount,
                                               additionalInfo=additionalInfo)
    outputListElement = output[0]
    ManagedHelper.publish(anObject=outputListElement)
    inputs = [outputListElement]
    inputSettingsListListElement = {'CHANNEL_COUNT': 5, 'REF_IDX': 2, 'INC_SLICE_IDX': 1}
    inputSettingsList = [inputSettingsListListElement]
    normalizationTransformationsJSONDataListElement = {'_slope': 1.0, '_offset': 0.0, '_min_possible_value': -0.00029401780921034515, '_max_possible_value': 0.0002205165073974058, '_norm_min': 0.0, '_norm_max': 1.0, '_calib_min': 0.0, '_calib_max': 0.0, '_calib_min_key': '', '_calib_max_key': '', '_calibration_enabled': False, '_normalization_spread': 2.0, 'dim_unit_repr': "orsDimensionUnit(registrationKey='CANONICAL_DIMENSION_DENSITY', unitName='Density', unitAbbreviation='', unitType=COMWrapper.ORS_def.CxvUniverse_Dimension_Type.CXV_DIMENSION_CONTINUOUS_VARIABLE, conversionFactor=1, isImperial=False, calibrationValues={}, description='')"}
    normalizationTransformationsJSONData = [normalizationTransformationsJSONDataListElement]
    ret_value = AIInterfaceMethods.applySegmentationModel(model=modelInstance,
                                                          modelManager=modelManagerInstance,
                                                          inputs=inputs,
                                                          mask=mask,
                                                          useMarkedSlices=useMarkedSlices,
                                                          inputSettingsList=inputSettingsList,
                                                          normalizationTransformationsJSONData=normalizationTransformationsJSONData,
                                                          progress=None)
    listOfROIs = extractROIs_026bbe94998911e881c30cc47aab53c3.extractROIs_026bbe94998911e881c30cc47aab53c3.extractROIsFromMultiROI(source_multiROI=ret_value)
    for i in [0,1,2]:   #0: bkg, 1: filled_pore, 2: pore
        refROI=listOfROIs[i]  #bkg
        refROI.imsave(fileName=f'{sf_path}{datasetName}_seg.tif',extension='tif',value=i)
        ManagedHelper.delete(anObject=refROI)
        time.sleep(0.2)
    ManagedHelper.delete(anObject=outputListElement)
    time.sleep(0.5)
    ManagedHelper.delete(anObject=ret_value)
    time.sleep(0.5)
    
