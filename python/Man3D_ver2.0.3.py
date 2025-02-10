'''
Created on 23.12.2010

@author: Nikolay and Mica
'''
from visual import *
from IDGenerator import IDGenerator 
import thread
from math import pi,cos
from compiler.misc import Stack
#from ver_0_1.HelpDoc import HelpUtil
from Tkinter import *
from tkSimpleDialog import *
import tkFileDialog
from xml.dom import minidom
from xml.dom.minidom import Node
from xml.dom.minidom import Document
import os
from tkFileDialog import askdirectory

#from msilib.schema import CheckBox


class LoadSaveHelper():
    
    @staticmethod
    def prepareMethod():
        prepareMethod = {}
        
        idsToSave = [key for key in Object3DDictionary.keys() if Object3DDictionary[key].visible==True]
        
        NewOrderOfIds = []
        
        counter = 0
        while 1 and counter<10000:
            counter+=1
            for elemToSave in idsToSave:
                if(elemToSave in NewOrderOfIds):
                    pass
                else:
                    willAdd= True
                  
                    for parId in Object3DDictionary[elemToSave].initParents:
                        if(parId not in NewOrderOfIds):                    
                            willAdd = False
                            break
                    if(willAdd):
                        NewOrderOfIds.append(elemToSave)            
            if(len(idsToSave)==len(NewOrderOfIds)):
                print "prepare successful!!!"
                return NewOrderOfIds
                                
        if counter ==10000:
            print 'Now you can not save this file,ask support for more information www.man3d.bg'
            return []

    @staticmethod
    def SaveObjects(fileName):
        
        
        try:
            doc = Document()
            
    
            root = doc.createElement('root')
            doc.appendChild(root)
            LoadSaveHelper.prepareMethod()
            IdsToSave = LoadSaveHelper.prepareMethod()
            
            for id in IdsToSave:
                object =doc.createElement('object')
                root.appendChild(object)
                object.setAttribute("class", Object3DDictionary[id].__class__.__name__)
                object.setAttribute("id",repr(id))
                object.setAttribute("parentsIds",repr(Object3DDictionary[id].initParents))
                object.setAttribute("initArguments",repr(Object3DDictionary[id].Save()))
    
    #        
    
            f = open(fileName+'.man', 'w')
            doc.writexml(f)
            f.close()
            return True
        except:
            print 'there is problem with saving ,contact the support:www.man3d.bg'
            return False
        
        
    @staticmethod
    def Open(fileName):
        try:
            dom = minidom.parse(fileName)
            objects = dom.getElementsByTagName('object')
            objectOld3Dictionary = {}
            for node in objects:
                id = eval(node.getAttribute('id'))
                arguments = eval(node.getAttribute('initArguments'))
                
                parents = eval(node.getAttribute('parentsIds'))
                for parentId in parents:
                    arguments.append(objectOld3Dictionary[parentId])
                
                className = node.getAttribute('class')
                
                objectOld3Dictionary[id] = eval(className)(*tuple(arguments))
            return True
        except: 
            print 'choose file with extension .man'
            return False
#            


def is_number(s):
    try:
        if(s==None):
            return False
        float(s)
        return True
    except ValueError:
        return False


class CoordinatePlanesXYZ:
    coordinatePlane = None
    isVisible = False
    isXYvisible = True
    isYZvisible = True
    isXZvisible = True
    
    
    
    @staticmethod
    def ChangeCoordinateSystemVisibility(changeVisibility= True):
        if(changeVisibility):
            if(not CoordinatePlanesXYZ.isVisible):                
                CoordinatePlanesXYZ.coordinatePlane.ShowAllPlanes(changeVisibility)
            else:
                CoordinatePlanesXYZ.coordinatePlane.HideAllPlanes(changeVisibility) 
            
            CoordinatePlanesXYZ.isVisible = not CoordinatePlanesXYZ.isVisible
            CoordinatePlanesXYZ.coordinatePlane.SetLabels() 
        else:
            if(CoordinatePlanesXYZ.isVisible):                
                CoordinatePlanesXYZ.coordinatePlane.ShowAllPlanes(changeVisibility)
            else:
                CoordinatePlanesXYZ.coordinatePlane.HideAllPlanes(changeVisibility)
        
        
            
        
        
    
     
    def init3DPlanes(self,x,y,z,linesPerUnit):
        
        self.arrowX = arrow(pos=(0,0,0), axis=(x,0,0),fixedwidth = 1, shaftwidth=0.04 , color = (0.5,0,0.3), visible = False, radius = 0.01)
        self.labelX = label(pos = (x,0,0),text = "X Coordinate", visible = False, height = 8)
        self.arrowY = arrow(pos=(0,0,0), axis=(0,y,0),fixedwidth = 1, shaftwidth=0.04, color = (0,0.5,0.3), visible = False,radius = 0.01)
        self.labelY = label(pos = (0,y,0),text = "Y Coordinate", visible = False , height = 8)
        self.arrowZ = arrow(pos=(0,0,0), axis=(0,0,z),fixedwidth = 1, shaftwidth=0.04, color = (0,0.3,0.5), visible = False,radius = 0.01)
        self.labelZ = label(pos = (0,0,z),text = "Z Coordinate", visible = False, height = 8)
        self.lineColor =(0.3,0.3,0.3) #color.white
        self.xyColor = (0.3,0.3,0)
        self.yzColor = (0,0.3,0.3)
        self.xzColor = (0.3,0,0.3)
        self.sizeX = x
        self.sizeY = y
        self.sizeZ = z
        #int XY   
        self.planeXY = []        
        self.planeXZ = []
        self.planeYZ = []    
        for y_coord in range(self.sizeY):
            xyCurve1 = curve(pos=[(-self.sizeX,y_coord,0),(self.sizeX,y_coord,0)],color = self.lineColor,visible = False)
            self.planeXY.append(xyCurve1)
            for index in range(linesPerUnit-1):
                xyCurve1 = curve(pos=[(-self.sizeX,((index+1)/float(linesPerUnit))+y_coord,0),(self.sizeX,(index+1)/float(linesPerUnit)+y_coord,0)],color = self.xyColor,visible = False)
                self.planeXY.append(xyCurve1)
        xyCurve1 = curve(pos=[(-self.sizeX,self.sizeY,0),(self.sizeX,self.sizeY,0)],color = self.lineColor,visible = False)
        self.planeXY.append(xyCurve1)
        #XY -
        for y_coord in range(self.sizeY):
            xyCurve1 = curve(pos=[(-self.sizeX,-y_coord,0),(self.sizeX,-y_coord,0)],color = self.lineColor,visible = False)
            self.planeXY.append(xyCurve1)
            for index in range(linesPerUnit-1):
                xyCurve1 = curve(pos=[(-self.sizeX,-((index+1)/float(linesPerUnit))-y_coord,0),(self.sizeX,-(index+1)/float(linesPerUnit)-y_coord,0)],color = self.xyColor,visible = False)
                self.planeXY.append(xyCurve1)
        xyCurve1 = curve(pos=[(-self.sizeX,-self.sizeY,0),(self.sizeX,-self.sizeY,0)],color = self.lineColor,visible = False)
        self.planeXY.append(xyCurve1)
            
        for x_coord in range(self.sizeX):
            xyCurve2 = curve(pos=[(x_coord,-self.sizeY,0),(x_coord,self.sizeY,0)],color = self.lineColor,visible = False)
            self.planeXY.append(xyCurve2)
            for index in range(linesPerUnit-1):
                xyCurve2 = curve(pos=[(((index+1)/float(linesPerUnit))+x_coord,-self.sizeY,0),(((index+1)/float(linesPerUnit))+x_coord,self.sizeY,0)],color = self.xyColor,visible = False)
                self.planeXY.append(xyCurve2)
        xyCurve2 = curve(pos=[(self.sizeX,-self.sizeY,0),(self.sizeX,self.sizeY,0)],color = self.lineColor,visible = False)
        self.planeXY.append(xyCurve2)
        
        for x_coord in range(self.sizeX):
            xyCurve2 = curve(pos=[(-x_coord,-self.sizeY,0),(-x_coord,self.sizeY,0)],color = self.lineColor,visible = False)
            self.planeXY.append(xyCurve2)
            for index in range(linesPerUnit-1):
                xyCurve2 = curve(pos=[(-((index+1)/float(linesPerUnit))-x_coord,-self.sizeY,0),(-((index+1)/float(linesPerUnit))-x_coord,self.sizeY,0)],color = self.xyColor,visible = False)
                self.planeXY.append(xyCurve2)
        xyCurve2 = curve(pos=[(-self.sizeX,-self.sizeY,0),(-self.sizeX,self.sizeY,0)],color = self.lineColor,visible = False)
        self.planeXY.append(xyCurve2)
        #init XZ
        for x_coord in range(self.sizeX):
            xyCurve1 = curve(pos=[(x_coord,0,-self.sizeZ),(x_coord,0,self.sizeZ)],color = self.lineColor,visible = False)
            self.planeXZ.append(xyCurve1)
            for index in range(linesPerUnit-1):
                xyCurve1 = curve(pos=[(((index+1)/float(linesPerUnit))+x_coord,0,-self.sizeZ),(((index+1)/float(linesPerUnit))+x_coord,0,self.sizeZ)],color = self.xzColor,visible = False)
                self.planeXZ.append(xyCurve1)
        xyCurve2 = curve(pos=[(self.sizeX,0,-self.sizeZ),(self.sizeX,0,self.sizeZ)],color = self.lineColor,visible = False)
        self.planeXZ.append(xyCurve2)
        
        for x_coord in range(self.sizeX):
            xyCurve1 = curve(pos=[(-x_coord,0,-self.sizeZ),(-x_coord,0,self.sizeZ)],color = self.lineColor,visible = False)
            self.planeXZ.append(xyCurve1)
            for index in range(linesPerUnit-1):
                xyCurve1 = curve(pos=[(-((index+1)/float(linesPerUnit))-x_coord,0,-self.sizeZ),(-((index+1)/float(linesPerUnit))-x_coord,0,self.sizeZ)],color = self.xzColor,visible = False)
                self.planeXZ.append(xyCurve1)
        xyCurve2 = curve(pos=[(-self.sizeX,0,-self.sizeZ),(-self.sizeX,0,self.sizeZ)],color = self.lineColor,visible = False)
        self.planeXZ.append(xyCurve2)
            
        for z_coord in range(self.sizeZ):
            xyCurve2 = curve(pos=[(-self.sizeX,0,z_coord),(self.sizeX,0,z_coord)],color = self.lineColor,visible = False)
            self.planeXZ.append(xyCurve2)
            for index in range(linesPerUnit-1):
                xyCurve2 = curve(pos=[(-self.sizeX,0,((index+1)/float(linesPerUnit))+z_coord),(self.sizeX,0,((index+1)/float(linesPerUnit))+z_coord)],color = self.xzColor,visible = False)
                self.planeXZ.append(xyCurve2)
        xyCurve2 = curve(pos=[(-self.sizeX,0,self.sizeZ),(self.sizeX,0,self.sizeZ)],color = self.lineColor,visible = False)
        self.planeXZ.append(xyCurve2)
        
        for z_coord in range(self.sizeZ):
            xyCurve2 = curve(pos=[(-self.sizeX,0,-z_coord),(self.sizeX,0,-z_coord)],color = self.lineColor,visible = False)
            self.planeXZ.append(xyCurve2)
            for index in range(linesPerUnit-1):
                xyCurve2 = curve(pos=[(-self.sizeX,0,-((index+1)/float(linesPerUnit))-z_coord),(self.sizeX,0,-((index+1)/float(linesPerUnit))-z_coord)],color = self.xzColor,visible = False)
                self.planeXZ.append(xyCurve2)
        xyCurve2 = curve(pos=[(-self.sizeX,0,-self.sizeZ),(self.sizeX,0,-self.sizeZ)],color = self.lineColor,visible = False)
        self.planeXZ.append(xyCurve2)
        
        #init YZ
        for y_coord in range(self.sizeY):
            xyCurve1 = curve(pos=[(0,y_coord,-self.sizeZ),(0,y_coord,self.sizeZ)],color = self.lineColor,visible = False)
            self.planeYZ.append(xyCurve1)
            for index in range(linesPerUnit-1):
                xyCurve1 = curve(pos=[(0,((index+1)/float(linesPerUnit))+y_coord,-self.sizeZ),(0,((index+1)/float(linesPerUnit))+y_coord,self.sizeZ)],color = self.yzColor,visible = False)
                self.planeYZ.append(xyCurve1)
        xyCurve2 = curve(pos=[(0,self.sizeY,-self.sizeZ),(0,self.sizeY,self.sizeZ)],color = self.lineColor,visible = False)
        self.planeYZ.append(xyCurve2)
        
        for y_coord in range(self.sizeY):
            xyCurve1 = curve(pos=[(0,-y_coord,-self.sizeZ),(0,-y_coord,self.sizeZ)],color = self.lineColor,visible = False)
            self.planeYZ.append(xyCurve1)
            for index in range(linesPerUnit-1):
                xyCurve1 = curve(pos=[(0,-((index+1)/float(linesPerUnit))-y_coord,-self.sizeZ),(0,-((index+1)/float(linesPerUnit))-y_coord,self.sizeZ)],color = self.yzColor,visible = False)
                self.planeYZ.append(xyCurve1)
        xyCurve2 = curve(pos=[(0,-self.sizeY,-self.sizeZ),(0,-self.sizeY,self.sizeZ)],color = self.lineColor,visible = False)
        self.planeYZ.append(xyCurve2)
        
        for z_coord in range(self.sizeZ):
            xyCurve2 = curve(pos=[(0,-self.sizeY,z_coord),(0,self.sizeY,z_coord)],color = self.lineColor,visible = False)
            self.planeYZ.append(xyCurve2)
            for index in range(linesPerUnit-1):
                xyCurve2 = curve(pos=[(0,-self.sizeY,((index+1)/float(linesPerUnit))+z_coord),(0,self.sizeY,((index+1)/float(linesPerUnit))+z_coord)],color = self.yzColor,visible = False)
                self.planeYZ.append(xyCurve2)
        xyCurve2 = curve(pos=[(0,-self.sizeY,self.sizeZ),(0,self.sizeY,self.sizeZ)],color = self.lineColor,visible = False)
        self.planeYZ.append(xyCurve2)
        
        for z_coord in range(self.sizeZ):
            xyCurve2 = curve(pos=[(0,-self.sizeY,-z_coord),(0,self.sizeY,-z_coord)],color = self.lineColor,visible = False)
            self.planeYZ.append(xyCurve2)
            for index in range(linesPerUnit-1):
                xyCurve2 = curve(pos=[(0,-self.sizeY,-((index+1)/float(linesPerUnit))-z_coord),(0,self.sizeY,-((index+1)/float(linesPerUnit))-z_coord)],color = self.yzColor,visible = False)
                self.planeYZ.append(xyCurve2)
        xyCurve2 = curve(pos=[(0,-self.sizeY,-self.sizeZ),(0,self.sizeY,-self.sizeZ)],color = self.lineColor,visible = False)
        self.planeYZ.append(xyCurve2)
            
            
                
    def __init__(self,knumbers, linesPerUnit = 2):
        self.init3DPlanes(knumbers, knumbers, knumbers, linesPerUnit)
       
    def removePlane(self, plane):
        for curve1 in plane:
            plane.remove(curve1)
            curve1.visible = False
            del curve1
        
        
    
    def change(self,knumbers):
        self.removePlane(self.planeXY)
        self.removePlane(self.planeYZ)
        self.removePlane(self.planeXZ)
        self.init3DPlanes(knumbers, knumbers, knumbers)
    
    def showPlane(self,plane):
      #  print "ShowPLane"
        for curve1 in plane:
            curve1.visible=True

        
    def hidePlane(self,plane):
        for curve1 in plane:
            curve1.visible=False
        
    def HideLabels(self):
        self.arrowX.visible = False
        self.arrowY.visible = False
        self.arrowZ.visible = False
        self.labelX.visible = False 
        self.labelY.visible = False
        self.labelZ.visible = False
    def SetLabels(self):
        if(self.isVisible == False):
            self.arrowX.visible = False
            self.arrowY.visible = False
            self.arrowZ.visible = False
            self.labelX.visible = False 
            self.labelY.visible = False
            self.labelZ.visible = False
        elif self.isXYvisible == True and self.isYZvisible == True and self.isXZvisible == True:
            self.arrowX.visible = True
            self.arrowY.visible = True
            self.arrowZ.visible = True
            self.labelX.visible = True 
            self.labelY.visible = True
            self.labelZ.visible = True
        elif self.isXYvisible:
            self.arrowX.visible = True
            self.arrowY.visible = True
            self.arrowZ.visible = False
            self.labelX.visible = True 
            self.labelY.visible = True
            self.labelZ.visible = False
        elif self.isYZvisible:
            self.arrowX.visible = False
            self.arrowY.visible = True
            self.arrowZ.visible = True
            self.labelX.visible = False 
            self.labelY.visible = True
            self.labelZ.visible = True
        elif self.isXZvisible:
            self.arrowX.visible = True
            self.arrowY.visible = False
            self.arrowZ.visible = True
            self.labelX.visible = True 
            self.labelY.visible = False
            self.labelZ.visible = True
            
            
            
    
    def HideAllPlanes(self, changeVisibility):
        if(not changeVisibility): 
            if(self.isVisible):           
                if(self.isXYvisible):
                    self.hidePlane(self.planeXY)                
                else:
                    self.showPlane(self.planeXY)                
                if(self.isXZvisible):        
                    self.hidePlane(self.planeXZ)
                else:
                    self.showPlane(self.planeXZ)
                if(self.isYZvisible):
                    self.hidePlane(self.planeYZ)
                else:
                    self.hidePlane(self.planeYZ)
                
            
        else:
            self.hidePlane(self.planeXY)
            self.hidePlane(self.planeXZ)
            self.hidePlane(self.planeYZ)
       
        
    def ShowAllPlanes(self, changeVisibility):
        if(self.isXYvisible):
            self.showPlane(self.planeXY)
        else:
            self.hidePlane(self.planeXY)
        if(self.isXZvisible):
            self.showPlane(self.planeXZ)
        else:
            self.hidePlane(self.planeXZ)
        if(self.isYZvisible):
            self.showPlane(self.planeYZ)
        else:
            self.hidePlane(self.planeYZ)
        
        
  
    

def setSelectedColor(object3d):
    object3d.color = color.yellow # tuk 6te izplzva settingite
    
def setUnselectedColor(object3d):
    object3d.color = colorSettings

class SelectedObjects(list):
    def isPlaneInIndex(self,index):
        if len(self)<= index:
            return False
        else:
            return issubclass(type(self[index]) , Plane)
    def isSegmentInIndex(self,index):
        if len(self)<= index:
            return False
        else:
            return issubclass(type(self[index]) , Segment)
    def isPointInIndex(self,index):
        if len(self)<= index:
            return False
        else:
            return issubclass(type(self[index]) , Point)
    def freeSelectedObjects(self):
        for element in self:
            setUnselectedColor(element)
        del self[:]

selected3DObject= SelectedObjects()
    


Object3DDictionary = {}
idSetting = 1
colorSettings = color.green
pointColor = color.green
segmentColor = color.green
radiusPointSettings = 0.1






class abstractUndoRedoObject:
    
    def Undo(self):
        pass
    def Redo(self):
        pass

class UndoRedoManager:
    undoStack = Stack()
    redoStack = Stack()
    
    numberOfObjects = 150
    
    @staticmethod
    def SetNumberOfUndoObjects(newNumber):
        UndoRedoManager.numberOfUndoObjects = newNumber
    
    @staticmethod
    def checkUndoStack():
        if len(UndoRedoManager.undoStack)<UndoRedoManager.numberOfObjects:
            return True
        else:
            print 'save the changes,because your memory which save them increased is out of limit ----',UndoRedoManager.numberOfObjects
            return False     
    
    @staticmethod
    def checkRedoStack():
        if len(UndoRedoManager.redoStack)<UndoRedoManager.numberOfObjects:
            return True
        else:
            print 'save the changes,because your memory which save them increased is out of limit ----',UndoRedoManager.numberOfObjects
            return False
    
    @staticmethod
    def PushToUndoStack(abstractUndoRedoObject,isToClearRedoStack = True):
        if(isToClearRedoStack):
            while UndoRedoManager.redoStack.__len__()> 0:
                x = UndoRedoManager.redoStack.pop()
                del x
            
            UndoRedoManager.redoStack = Stack()
        UndoRedoManager.undoStack.push(abstractUndoRedoObject)
        
        
    
    @staticmethod
    def PushToRedoStack(abstractUndoRedoObject):
        
        UndoRedoManager.redoStack.push(abstractUndoRedoObject)
    
    @staticmethod    
    def Undo():
        if len(UndoRedoManager.undoStack)>0:
            UndoRedoManager.undoStack.pop().Undo()
    
    @staticmethod    
    def Redo():
        if len(UndoRedoManager.redoStack)>0:
            UndoRedoManager.redoStack.pop().Redo()
            
    @staticmethod
    def Clear():
          
        
        for element in Object3DDictionary.values():
            if element.visible == False:
                element.Delete()
        while UndoRedoManager.undoStack.__len__()> 0:
            x = UndoRedoManager.undoStack.pop()
            del x
        UndoRedoManager.undoStack = Stack()
        
        while UndoRedoManager.redoStack.__len__()> 0:
            x = UndoRedoManager.redoStack.pop()
            del x
        UndoRedoManager.redoStack = Stack()
        SpecialElementsForTransformation.ValidatorListAfterDelete(Object3DDictionary.values())
          
##class ModifiedObserverHelpsForLables:
  ###  isModified = False
       
class MoveUndoRedo(abstractUndoRedoObject):
    def __init__(self,dictionaryIdAndPosition):
        self.dictionary = dictionaryIdAndPosition
    #    print 'modifier setted',ModifiedObserverHelpsForLables.isModified
        LabelHelper.ShowLabels()
###        if ModifiedObserverHelpsForLables.isModified == False:
###            ModifiedObserverHelpsForLables.isModified = True
    def Undo(self):
        dictionaryForRedo={}
        for id in self.dictionary.keys():#topElement[0].keys():
            vectorNewPos = Object3DDictionary[id].pos
            dictionaryForRedo[id]=vector(vectorNewPos.x,vectorNewPos.y,vectorNewPos.z)
            Object3DDictionary[id].pos = self.dictionary[id]
            Object3DDictionary[id].RedrawChildDynamics(True)
        
        UndoRedoManager.PushToRedoStack(MoveUndoRedo(dictionaryForRedo))                        
        
    def Redo(self):
        dictionaryForUndo={}
        for id in self.dictionary.keys():#topElement[0].keys():
            vectorNewPos = Object3DDictionary[id].pos
            dictionaryForUndo[id]=vector(vectorNewPos.x,vectorNewPos.y,vectorNewPos.z)
            Object3DDictionary[id].pos = self.dictionary[id]
            Object3DDictionary[id].RedrawChildDynamics(True)
        
        UndoRedoManager.PushToUndoStack(MoveUndoRedo(dictionaryForUndo),False)    

class CreateUndoRedo(abstractUndoRedoObject):
    def __init__(self,listOfIds):
        self.listIds = listOfIds
        LabelHelper.ShowLabels()
##        if ModifiedObserverHelpsForLables.isModified == False:
##            ModifiedObserverHelpsForLables.isModified = True
        
    def Undo(self):
    #    print self.listIds
        for id in self.listIds:
            Object3DDictionary[id].ChangeVisible()#Undo(topElement[1])
        UndoRedoManager.PushToRedoStack(CreateUndoRedo(self.listIds))
        
    def Redo(self):
        for id in self.listIds:
            Object3DDictionary[id].ChangeVisible()#Undo(topElement[1])
        UndoRedoManager.PushToUndoStack(CreateUndoRedo(self.listIds),False)


class DeleteUndoRedo(abstractUndoRedoObject):
    def __init__(self,listOfIds):
        self.listIds = listOfIds
##        if ModifiedObserverHelpsForLables.isModified == False:
##            ModifiedObserverHelpsForLables.isModified = True
        LabelHelper.ShowLabels()
        
    def Undo(self):
        for id in self.listIds:
            Object3DDictionary[id].ChangeVisible(True)#Undo(topElement[1])
        UndoRedoManager.PushToRedoStack(DeleteUndoRedo(self.listIds))
        
    def Redo(self):
        for id in self.listIds:
            Object3DDictionary[id].ChangeVisible(True)#Undo(topElement[1])
        UndoRedoManager.PushToUndoStack(DeleteUndoRedo(self.listIds),False)




class FreeUndoRedo(abstractUndoRedoObject):
    def __init__(self,listOfDataForFreeObjects):
        self.listOfDataForFreeObjects = listOfDataForFreeObjects
    
    def Undo(self):
        for dataForFreeObject in self.listOfDataForFreeObjects:
            Object3DDictionary[dataForFreeObject.freedId].Bind(dataForFreeObject)#Undo(topElement[1])
        UndoRedoManager.PushToRedoStack(FreeUndoRedo(self.listOfDataForFreeObjects))
        
    def Redo(self):
        for dataForFreeObject in self.listOfDataForFreeObjects:
            Object3DDictionary[dataForFreeObject.freedId].Free()#Undo(topElement[1])
        UndoRedoManager.PushToUndoStack(FreeUndoRedo(self.listOfDataForFreeObjects),False)

class Settings :

    @staticmethod
    def makeDynamicsSettingsOf3DObject(object3DtoSet):        
        nextId= IDGenerator.GetNext()

        if nextId == -1:
            
            IDGenerator.IncreaseLimitBy(50)
            nextId = IDGenerator.GetNext()
            
     
        object3DtoSet.id = nextId
        object3DtoSet.children = []
        object3DtoSet.parents = []
        object3DtoSet.initParents = []
        Object3DDictionary[object3DtoSet.id ]= object3DtoSet
                
        
    @staticmethod        
    def makeUndoRedoSettingsOf3DObject(object3DtoSet):
        object3DtoSet.deletedByID = 0
        
    @staticmethod
    def SetDynamicRelationsOnPointCreation(object3DtoSet,*args):

        segmentIds =[]
        for arg in args:
            object3DtoSet.initParents.append(arg.id)
            if(type(arg)==Segment):
                segmentIds.append(arg.id)
                object3DtoSet.parents.append(Object3DDictionary[arg.id].parents[0])
                Object3DDictionary[Object3DDictionary[arg.id].parents[0]].children.append(object3DtoSet.id)
                object3DtoSet.parents.append(Object3DDictionary[arg.id].parents[1])
                Object3DDictionary[Object3DDictionary[arg.id].parents[1]].children.append(object3DtoSet.id)
            elif(type(arg)==Plane):
                object3DtoSet.parents.append(arg.id)
                Object3DDictionary[arg.id].children.append(object3DtoSet.id)
            else:
                object3DtoSet.parents.append(arg.id)
                Object3DDictionary[arg.id].children.append(object3DtoSet.id)
        for id in segmentIds:
            object3DtoSet.parents.append(id)
            Object3DDictionary[id].children.append(object3DtoSet.id)
    
        
        
    


    
class interfaceRecursiveDelete:
    def Delete(self):
        pass
         
class recursiveDeleteOf3dObjects(interfaceRecursiveDelete):
    def Delete(self):
        for idObject in self.children:
            if idObject in Object3DDictionary.keys():
                Object3DDictionary[idObject].Delete()
        for parentId in self.parents:
            if parentId in Object3DDictionary.keys():
                if self.id in Object3DDictionary[parentId].children:
                    Object3DDictionary[parentId].children.remove(self.id)
        if self.id in Object3DDictionary.keys():
            Object3DDictionary.__delitem__(self.id)
        IDGenerator.DeleteByID(self.id)
        
        del self

class interfaceRecursiveVisibility:
    def ChangeVisible(self,isVisible):
        pass
         
class recursiveVisibilityOf3DObjects(interfaceRecursiveVisibility):
    

    def ChangeVisible(self,recursive = False,isFirstCall=True):
        
        self.visible = not self.visible#new value

        if recursive:
            for idObject in self.children:
                if(self.visible == False):
                    if(Object3DDictionary[idObject].deletedByID==0):
                        Object3DDictionary[idObject].deletedByID=self.id
                        Object3DDictionary[idObject].ChangeVisible(recursive,False)
                    else:
                        pass
                else:
                    if(Object3DDictionary[idObject].deletedByID!= self.id ):
                        pass
                    else:
                        Object3DDictionary[idObject].ChangeVisible(recursive,False)
                        Object3DDictionary[idObject].deletedByID = 0
        if isFirstCall:
            if self.visible == True:
                self.deletedByID = 0
            else:
                self.deletedByID = self.id
                    

class DataForFreeObject:
    def __init__(self,Id,ParentsIds,ClassReference,IsDraggable,initParentsIds):
        self.freedId = Id
        self.freedParentsIds = ParentsIds[:]
        self.freedClassReference = ClassReference
        self.freedIsDraggable = IsDraggable
        self.freedInitParentsIds = initParentsIds[:]
           
class interfaceFreeObjects():
    def Free(self):
        pass
    def Bind(self,dataForFreeObject):
        pass    

class FreeAndBindObjects():
    def Free(self):
        for id in self.parents:
            Object3DDictionary[id].children.remove(self.id)
        self.parents = []
        
        self.__class__ = Point
        self.IsDraggable = True
        self.initParents = []
    def Bind(self,dataForFreeObject):
        self.__class__=dataForFreeObject.freedClassReference
        self.IsDraggable = dataForFreeObject.freedIsDraggable
        Settings.SetDynamicRelationsOnPointCreation(self,*tuple([Object3DDictionary[id] for id in dataForFreeObject.freedInitParentsIds]))
        
        pass    
            
        
    
class dynamicRedraw3dObjects:
    def RedrawChildDynamics(self,isFirstCall,additionalParam=None):#shpere or cylinder
        if isFirstCall:
            self.move()
        else:
            self.move()
    
        if self.children == []:
            return
        else:
            for idObject in self.children:
                Object3DDictionary[idObject].RedrawChildDynamics(False)
        
    def move(self):
        pass

class interfaceLabel:
    
    def ShowLabel(self):
        pass
    def HideLabel(self):
        pass

class interfaceSave:
    def Save(self):
        return []

class man3DObject(dynamicRedraw3dObjects,recursiveVisibilityOf3DObjects,recursiveDeleteOf3dObjects,interfaceLabel,interfaceSave):
    
    def __init__(self,name = None,*args):
        Settings.makeDynamicsSettingsOf3DObject(self)
        Settings.makeUndoRedoSettingsOf3DObject(self)
        self.name = ''
        self.label = label( xoffset=5, yoffset=3,visible = False, height = 10, border=0, box = 0)
    def GetParent(self,index):
        if index < len(self.parents):
            return Object3DDictionary[self.parents[index]]
        else: 
            return None

    def GetSize(self):
        return 0
    
    def area(self):
        return 0
            
    def isFree(self):
        return len(self.parents)==0
            
    def isDeleted(self):
        return self.deletedByID!=0
    
    def setName(self,name):
        pass
    def canDrag(self):
        return self.IsDraggable
    

class Plane(convex,man3DObject):#,FreeAndBindObjects):
    def __init__(self,*parentsElement):
        convex.__init__(self)
        man3DObject.__init__(self)
        
        self.loadPreferenceSettings()
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.A = self.GetParent(0).pos
        self.b =self.GetParent(1).pos-self.GetParent(0).pos
        self.c =self.GetParent(2).pos-self.GetParent(0).pos
        self.bxc = self.b.cross(self.c)
        self.move()
        self.IsDraggable = self.GetParent(0).isFree() and self.GetParent(1).isFree() and self.GetParent(2).isFree()
        self.setName()
        pass

    def setName(self,name=None):
        if name == None :
            self.name = '('+Object3DDictionary[self.parents[0]].name+','+Object3DDictionary[self.parents[1]].name+','+Object3DDictionary[self.parents[2]].name+')'
        elif name in [obj.name for obj in Object3DDictionary.values()]: 
            print "Object with this name exists"          
            self.name = '('+Object3DDictionary[self.parents[0]].name+','+Object3DDictionary[self.parents[1]].name+','+Object3DDictionary[self.parents[2]].name+')' 
        else:
            self.name = name
            
    def loadPreferenceSettings(self):
        self.color = color.orange
        
    def ShowLabel(self):
      
        if(self.visible):
            self.label.pos = (Object3DDictionary[self.parents[0]].pos+Object3DDictionary[self.parents[1]].pos+Object3DDictionary[self.parents[2]].pos)/3.
       
            self.label.text = self.name
        self.label.visible = self.visible    
    def HideLabel(self):
        self.label.visible = False  
     
    def move(self):
        self.pos = [Object3DDictionary[self.parents[0]].pos, Object3DDictionary[self.parents[1]].pos, Object3DDictionary[self.parents[2]].pos]  
        self.A = self.GetParent(0).pos
        self.b =self.GetParent(1).pos-self.GetParent(0).pos
        self.c =self.GetParent(2).pos-self.GetParent(0).pos
        self.bxc = self.b.cross(self.c)
    def isFree(self):
        return self.GetParent(0).isFree() and self.GetParent(1).isFree() and self.GetParent(2).isFree()
    def canDrag(self):
        return self.isFree()
    
    def area(self):
        return mag(self.bxc)/2.
                
class Point(sphere,man3DObject,FreeAndBindObjects):#,dynamicRedraw3dObjects,undoRedoOf3DObjects):
    def __init__(self,position = None):
        
        sphere.__init__(self)
        man3DObject.__init__(self)
        self.loadPreferenceSettings()
        if(position != None ):
            self.pos = position
        self.IsDraggable = True 
        self.setName(None)
    def setName(self,name):
        if name == None :
            self.name = 'A'+str(self.id)
        elif name in [obj.name for obj in Object3DDictionary.values()]: 
            print "Object with this name exists"          
            self.name = 'A'+str(self.id)
        else:
            self.name = name
    def ShowLabel(self):
        if(self.visible):
            self.label.pos = self.pos
            self.label.text = self.name +'(%.1f,%.1f,%.1f)'%(self.pos.x,self.pos.y,self.pos.z)
        self.label.visible = self.visible    
    def HideLabel(self):
        self.label.visible = False       
           
    def SetPosition(self,newPosition):
        self.pos = newPosition
    def SetColor(self,newColor):
        self.color = newColor
    def SetRadius(self,newRadius):
        self.radius = newRadius
    
    def loadPreferenceSettings(self):
        global colorSettings
        global radiusPointSettings
        self.SetColor(colorSettings)  
        self.SetRadius(radiusPointSettings)
    
    def Save(self):
        return [self.pos]    
        
class PointByPlane(Point):
    def __init__(self,position,*parentsElement):
        Point.__init__(self)
        
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.IsDraggable = True
        self.pos = position
        self.calculateKoeficients()
        #self.move()
    
    def move(self):
        self.pos =self.GetParent(0).A + self.k1*self.GetParent(0).b+self.k2*self.GetParent(0).c
    
    def calculateKoeficients(self):
        self.k2 = -(self.GetParent(0).b.cross(self.GetParent(0).bxc)).dot(self.GetParent(0).A - self.pos)/(self.GetParent(0).c.dot(self.GetParent(0).b.cross(self.GetParent(0).bxc)))
        self.k1 = -(self.GetParent(0).c.cross(self.GetParent(0).bxc)).dot(self.GetParent(0).A - self.pos)/(self.GetParent(0).b.dot(self.GetParent(0).c.cross(self.GetParent(0).bxc)))
                        
    def RedrawChildDynamics(self,isFirstCall):
        if(isFirstCall):
            self.calculateKoeficients()
            self.move()
        else:
            self.move()
        if self.children == []:
            return
        else:
            for idObject in self.children:
                Object3DDictionary[idObject].RedrawChildDynamics(False) 

    
        

class RotatedPointByAngle(Point):
    def __init__(self,angle,*parentsElement):#*segmentOrTwoPoints,rotatedPoint):
        Point.__init__(self)
        self.SetAngle(angle)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
        self.IsDraggable = False

    def SetAngle(self,newAngle):
        self.rotationAngle= newAngle 
    
    
    
    def setPositionOfRotatedPoint(self):
        
        normalizedAxis=norm(Object3DDictionary[self.parents[1]].pos-Object3DDictionary[self.parents[0]].pos)
        vectorBetweenCenterAndPoint=Object3DDictionary[self.parents[2]].pos-Object3DDictionary[self.parents[0]].pos
        rotatedVector=vectorBetweenCenterAndPoint*cos(self.rotationAngle)+cross(normalizedAxis,vectorBetweenCenterAndPoint)*sin(self.rotationAngle)+(normalizedAxis.dot(vectorBetweenCenterAndPoint))*normalizedAxis*(1-cos(self.rotationAngle)) 
        self.pos = rotatedVector+Object3DDictionary[self.parents[0]].pos
        
    def move(self):
            self.setPositionOfRotatedPoint()
    
    def Save(self):
        return [self.rotationAngle] 

class ScrewMotion(RotatedPointByAngle):
    def __init__(self,sizeOfVector,angle,*parentsElement):   
        self.SetSizeOfVector(sizeOfVector)
        RotatedPointByAngle.__init__(self,angle, *parentsElement)
        
    def SetSizeOfVector(self,nSizeOfVector):
        self.sizeOfVector = nSizeOfVector
    def move(self):
        RotatedPointByAngle.move(self)
        self.pos = self.pos + norm(self.GetParent(1).pos-self.GetParent(0).pos)*self.sizeOfVector
    
    def Save(self):
        return [self.sizeOfVector,self.rotationAngle] 
        
class CrossPoint(Point):
    def __init__(self,*parentsElement):#pointA,pointB,pointC,pointD
        Point.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.IsDeleted = False
        self.move()
        self.IsDraggable = False
        
        
       
    def getCrossPointPosition(self,pointApos,pointBpos,pointCpos,pointDpos):
        a= pointApos - pointCpos
        b= pointBpos - pointApos
        c = pointDpos - pointCpos
        bxc = b.cross(c)
        if -0.00001<mag(bxc)<0.00001:
            
            return None
        axc = a.cross(c)
        if not(-0.01<mag(bxc.cross(axc))<0.01):
            
            return None
        
        sign = 1
        if axc.dot(bxc)<0:
            sign = -1
        return pointApos - mag(axc)/mag(bxc)*b *sign
     
    def move(self):
        crossPointpos = self.getCrossPointPosition(Object3DDictionary[self.parents[0]].pos,Object3DDictionary[self.parents[1]].pos,Object3DDictionary[self.parents[2]].pos,Object3DDictionary[self.parents[3]].pos) 
        
        if crossPointpos == None:
            
            
            #print 'is visible',self.visible
            if self.visible  :#and self.deletedByID != self.id: #and self.deletedByID != self.id:
                if not self.IsDeleted:
                    self.ChangeVisible(True, True)
                    
                
        else:
            
            
            self.pos = crossPointpos
            if not self.visible :
                if not self.IsDeleted:
                    if self.deletedByID ==0:
                        self.visible = True
                    elif self.deletedByID == self.id:
                        self.ChangeVisible(True, True)
    
                
                    
            
    def ChangeVisible(self,recursive = False,isFirstCall=True):
        
        if not recursive :
            self.IsDeleted = not self.IsDeleted
            
        if not self.IsDeleted:
            self.visible = not self.visible
            
            #new value
            if recursive:
               
                for idObject in self.children:
                    if(self.visible == False):
                        if(Object3DDictionary[idObject].deletedByID==0):
                            Object3DDictionary[idObject].deletedByID=self.id
                            Object3DDictionary[idObject].ChangeVisible(recursive,False)
                        else:
                            pass
                    else:
                        if(Object3DDictionary[idObject].deletedByID!= self.id ):
                            pass
                        else:
                            Object3DDictionary[idObject].ChangeVisible(recursive,False)
                            Object3DDictionary[idObject].deletedByID = 0
            if isFirstCall:
                if self.visible == True:
                    self.deletedByID = 0
                else:
                    self.deletedByID = self.id 
        else :
            self.visible = False 
    def Save(self):
        return [] 

class MiddlePoint(Point):
    def __init__(self,*parentsElement):#pointA,pointB):
        Point.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
        self.IsDraggable = False
        
    def move(self):
        self.pos = (Object3DDictionary[self.parents[0]].pos + Object3DDictionary[self.parents[1]].pos)/2.#resultpos.pos = (ball1.pos + ball2.pos)/2.
        
    def Save(self):
        return [] 

class BisectorPoint(Point):
    def __init__(self,*parentsElement):#three points:
        Point.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
        self.IsDraggable = False
        
    def move(self):
        if(not abs(Object3DDictionary[self.parents[0]].pos - Object3DDictionary[self.parents[2]].pos)<0.001):
            
            self.pos =(mag(Object3DDictionary[self.parents[0]].pos - Object3DDictionary[self.parents[1]].pos) /(mag(Object3DDictionary[self.parents[0]].pos - Object3DDictionary[self.parents[1]].pos)+mag(Object3DDictionary[self.parents[2]].pos - Object3DDictionary[self.parents[1]].pos)))*(Object3DDictionary[self.parents[2]].pos - Object3DDictionary[self.parents[0]].pos) +Object3DDictionary[self.parents[0]].pos 
        else:
            self.pos = Object3DDictionary[self.parents[0]].pos
        
        
    def Save(self):
        return []
    
   

class DelitatePoint(Point):
    def __init__(self,homotheticCoeficentX,homotheticCoeficentY,homotheticCoeficentZ,*parentsObject):# first symetric point and then point to make symetric
        self.setCoeficentX(homotheticCoeficentX)
        self.setCoeficentY(homotheticCoeficentY)
        self.setCoeficentZ(homotheticCoeficentY)
        Point.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsObject)
        #self.SetCoeficent(homotheticCoeficent)
        self.move()
        self.IsDraggable = False
    
    def setCoeficentX(self,ceoficentX):
        self.HomotheticCoeficentX = ceoficentX
    
    def setCoeficentY(self,ceoficentY):
        self.HomotheticCoeficentY = ceoficentY
        
    def setCoeficentZ(self,ceoficentZ):
        self.HomotheticCoeficentZ = ceoficentZ
    
    def move(self):
        self.pos.x = (1+self.HomotheticCoeficentX)*Object3DDictionary[self.parents[0]].pos.x - self.HomotheticCoeficentX*Object3DDictionary[self.parents[1]].pos.x 
        self.pos.y = (1+self.HomotheticCoeficentY)*Object3DDictionary[self.parents[0]].pos.y - self.HomotheticCoeficentY*Object3DDictionary[self.parents[1]].pos.y
        self.pos.z = (1+self.HomotheticCoeficentZ)*Object3DDictionary[self.parents[0]].pos.z - self.HomotheticCoeficentZ*Object3DDictionary[self.parents[1]].pos.z        
    
    def Save(self):
        return [self.HomotheticCoeficentX,self.HomotheticCoeficentY,self.HomotheticCoeficentZ]   
class HomotheticPoint(DelitatePoint):
    def __init__(self,homotheticCoeficent,*parentsObject):# first symetric point and then point to make symetric
        DelitatePoint.__init__(self,homotheticCoeficent, homotheticCoeficent, homotheticCoeficent,*parentsObject)
#        Settings.SetDynamicRelationsOnPointCreation(self,*parentsObject)
        self.move()
    def Save(self):
        return [self.HomotheticCoeficentX]

class SymetricPoint(HomotheticPoint):
    def __init__(self,*parentsObject):# first symetric point and then point to make symetric
        HomotheticPoint.__init__(self,1,*parentsObject)
#        Settings.SetDynamicRelationsOnPointCreation(self,*parentsObject)
        self.move()
    def Save(self):
        return []     
class ProjectionPlanePoint(Point): 
    def __init__(self):
        Point.__init__(self)
        self.IsDraggable = False
        
    def move(self):
        
        if not -0.00001< self.vector.dot(Object3DDictionary[self.parents[0]].bxc)<0.00001:
            
            self.pos =(((Object3DDictionary[self.parents[0]].A - Object3DDictionary[self.parents[1]].pos).dot(Object3DDictionary[self.parents[0]].bxc))/self.vector.dot(Object3DDictionary[self.parents[0]].bxc))*self.vector +Object3DDictionary[self.parents[1]].pos 
        else:
            
            self.pos = self.pos+100*norm(self.vector)
        
    def RedrawChildDynamics(self,isFirstCall):
        self.move()
        if self.children == []:
            return
        else:
            for idObject in self.children:
                Object3DDictionary[idObject].RedrawChildDynamics(False)
    

class ProjectionPlanePointBySegment(ProjectionPlanePoint):#1 wi argumen e plane ftori segmenta(dveteTochki) 
    def __init__(self,*parentsElement):#1 wi argumen e plane ftori pravata
        ProjectionPlanePoint.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
        
    def move(self): 
        self.vector =Object3DDictionary[self.parents[2]].pos - Object3DDictionary[self.parents[1]].pos
        ProjectionPlanePoint.move(self)
    def Save(self):
        return []

class ProjectionPlanePointByVector(ProjectionPlanePoint):
    def __init__(self,projectVector,*parentsElement):
        ProjectionPlanePoint.__init__(self)
        self.vector = vector(projectVector.x,projectVector.y,projectVector.z)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
    def Save(self):
        return [self.vector]
    

class PerpendicularProjectionPlane(ProjectionPlanePoint):
    def __init__(self,*parentsElement):#first is plane second is object to transform
        ProjectionPlanePoint.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
        
    def move(self):
        self.vector = self.GetParent(0).bxc
        self.pos =(((Object3DDictionary[self.parents[0]].A - Object3DDictionary[self.parents[1]].pos).dot(Object3DDictionary[self.parents[0]].bxc))/self.vector.dot(Object3DDictionary[self.parents[0]].bxc))*self.vector +Object3DDictionary[self.parents[1]].pos
        #ProjectionPlanePoint.move(self)
    def Save(self):
        return []

class SymetriaByPlane(PerpendicularProjectionPlane):
    def __init__(self,*parentsElement):#first is plane second is object to transform
        PerpendicularProjectionPlane.__init__(self,*parentsElement)
        
    def move(self):
        PerpendicularProjectionPlane.move(self)
        self.pos = 2*self.pos - self.GetParent(1).pos 
    
   
class SymetriaByPlaneAndVector(SymetriaByPlane):
    def __init__(self,tranlateVector,*parentsElement):#first is plane second is object to transform
        self.translateVector = tranlateVector
        SymetriaByPlane.__init__(self,*parentsElement)
        
    def move(self):
        SymetriaByPlane.move(self)
        self.pos = self.pos + self.translateVector
   
    def Save(self):
        return [self.translateVector]       
   

   



class TranslatedPointVector(Point):
    def __init__(self):
        Point.__init__(self)
    def move(self):
        
        self.pos = Object3DDictionary[self.parents[0]].pos + self.k*self.vector
        
    def RedrawChildDynamics(self,isFirstCall):
        
        if isFirstCall:
            self.calculateNewK()
            self.move()
        else:
            self.move()
        if self.children == []:
            return
        else:
            for idObject in self.children:
                Object3DDictionary[idObject].RedrawChildDynamics(False)
    def calculateNewK(self):
        pass

class TranslatedPointByVector(TranslatedPointVector):
    def __init__(self,translateVector,*parentsElement):
        TranslatedPointVector.__init__(self)
        self.vector = vector(translateVector.x,translateVector.y,translateVector.z)
        self.k = 1
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
        self.IsDraggable = False
   
    def Save(self):
        return [self.vector]
#    def calculateNewK(self):
#        sign = 1
#        if( self.vector.dot( self.pos - Object3DDictionary[self.parents[0]].pos) <=0):
#            sign = -1
#        self.k = mag( self.pos - Object3DDictionary[self.parents[0]].pos)/mag(self.vector)*sign
#    
    
                

class TranslatedPointBySegmentForGeneration(TranslatedPointVector):
    def __init__(self,koeficient,*parentsElement):
        TranslatedPointVector.__init__(self)
        #self.vector = Object3DDictionary[parentsElement[1].parents[1]].pos - Object3DDictionary[parentsElement[1].parents[0]].pos
        self.k = koeficient
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
        
    def calculateNewK(self):
        #self.vector =Object3DDictionary[self.parents[2]].pos - Object3DDictionary[self.parents[1]].pos
        if mag(self.vector)<0.0001:
            self.k = 0
        else:
            sign = 1
            if( self.vector.dot( self.pos - Object3DDictionary[self.parents[0]].pos) <=0):
                sign = -1
            self.k = mag( self.pos - Object3DDictionary[self.parents[0]].pos)/mag(self.vector)*sign
    def move(self):
        self.vector =Object3DDictionary[self.parents[2]].pos - Object3DDictionary[self.parents[1]].pos
        self.pos = Object3DDictionary[self.parents[0]].pos + self.k*self.vector
    def Save(self):
        return [self.k]
               
        
  
class ProportionalPoint(Point):
    
    def __init__(self):
        Point.__init__(self)
#        self.moveOnlyInSegmentAB = True

    

    def calculateNewProp(self):
        projectVector = Object3DDictionary[self.parents[1]].pos - Object3DDictionary[self.parents[0]].pos
        vectorToProject = self.pos - Object3DDictionary[self.parents[1]].pos
        resultVector = vectorToProject.proj(projectVector)
            
        self.prop =resultVector.mag/projectVector.mag
#        if(self.moveOnlyInSegmentAB): 
        if 1.00-self.prop < 0.001:
            self.prop = 0.999
#        else:
#            pass
    def Save(self):
        return []

class ProportionalPointCreatedByProportion(ProportionalPoint):

    def __init__(self,numerator,denumerator,*parentsElement):
        ProportionalPoint.__init__(self)
        self.prop = numerator/float(denumerator)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElement)
        self.move()
    
    def move(self):
        self.pos = self.prop *Object3DDictionary[self.parents[0]].pos + (1-self.prop)*Object3DDictionary[self.parents[1]].pos#resultpos.pos = (ball1.pos + ball2.pos)/2.

    def RedrawChildDynamics(self,isFirstCall,newProp=None):
        if isFirstCall :
            self.calculateNewProp()
            self.move()
        else:
            if(newProp!=None):
                self.prop = newProp
            self.move()
        if self.children == []:
            return
        else:
            for idObject in self.children:
                Object3DDictionary[idObject].RedrawChildDynamics(False)
    
    def Save(self):
        return [self.prop,1]
                
class ProportionalPointCreatedByProportionalPoint(ProportionalPoint):
    def __init__(self,*parentsElements):#last element is proportion Point
        ProportionalPoint.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElements)
        self.move()
    
    def move(self):
        self.prop = Object3DDictionary[self.parents[2]].prop
        self.pos = Object3DDictionary[self.parents[2]].prop *Object3DDictionary[self.parents[0]].pos + (1-Object3DDictionary[self.parents[2]].prop)*Object3DDictionary[self.parents[1]].pos#resultpos.pos = (ball1.pos + ball2.pos)/2. 
        
    def RedrawChildDynamics(self,isFirstCall,newProp=None):
        if isFirstCall :
            self.calculateNewProp()
            Object3DDictionary[self.parents[2]].RedrawChildDynamics(False, self.prop)
             
        else:
            if newProp != None :
                Object3DDictionary[self.parents[2]].RedrawChildDynamics(False, newProp)
            else:
                self.move()

        if self.children == []:
            return
        else:
            for idObject in self.children:
                Object3DDictionary[idObject].RedrawChildDynamics(False)
                
class PerpendicularPoint(Point):
    def __init__(self,*parentsElements):#first argument -Point To Project
        Point.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,*parentsElements)
        self.setPositionOfPerpendicularPoint()
        self.IsDraggable = False
        self.color = color.white
        
    def setPositionOfPerpendicularPoint(self):
        ProjectionVector = Object3DDictionary[self.parents[2]].pos - Object3DDictionary[self.parents[1]].pos
        vectorToProject = Object3DDictionary[self.parents[0]].pos - Object3DDictionary[self.parents[1]].pos
        resultVector = vectorToProject.proj(ProjectionVector)
        self.pos = Object3DDictionary[self.parents[1]].pos + resultVector
      
    def move(self):
        self.setPositionOfPerpendicularPoint()
    
    def Save(self):
        return []

class Segment(cylinder,man3DObject):
    def __init__(self,pointA,pointB):
        cylinder.__init__(self)
        self.loadPreferenceSettings()
        man3DObject.__init__(self)
        Settings.SetDynamicRelationsOnPointCreation(self,pointA,pointB)
        self.move()
        #self.createLine(pointA.id,pointB.id)
        self.IsDraggable = self.GetParent(0).isFree() and self.GetParent(1).isFree()
        
        self.setName(None)
    
    def setName(self,name):
        
        if name == None: #or name in [obj.name  for obj in Object3DDictionary.values()]:
            self.name = self.GetParent(0).name+self.GetParent(1).name
        elif name in [obj.name for obj in Object3DDictionary.values()]: 
            print "Object with this name exists"          
            self.name = self.GetParent(0).name+self.GetParent(1).name        
        else:
            self.name = name
        
    def isFree(self):
        return self.GetParent(0).isFree() and self.GetParent(1).isFree()
    def canDrag(self):
        return self.isFree()
    
        
    def SetPosition(self,newPosition):
        self.pos = newPosition
    def SetColor(self,newColor):
        self.color = newColor
    def SetRadius(self,newRadius):
        self.radius = newRadius
    
    def ShowLabel(self):
        if(self.visible):
            self.label.pos = self.pos+self.axis/2
            self.label.text = self.name #+'(%.2f,%.2f,%.2f)'%(self.pos.x,self.pos.y,self.pos.z)
        self.label.visible = self.visible    
    def HideLabel(self):
        self.label.visible = False
    
    def loadPreferenceSettings(self):
        global colorSettings
        global radiusPointSettings
        self.SetColor(colorSettings)  
        self.SetRadius(radiusPointSettings/2.)
    
    def GetSize(self):
        return mag(self.axis)
    
    
    
    #===========================================================================
    # def createLine(self,pointAid,pointBid):
    #    
    #    self.pos = Object3DDictionary[pointAid].pos
    #    self.axis=Object3DDictionary[pointBid].pos-Object3DDictionary[pointAid].pos
    #    
    #    self.parents.append(pointAid)
    #    self.parents.append(pointBid)
    #    
    #    Object3DDictionary[pointAid].children.append(self.id)
    #    Object3DDictionary[pointBid].children.append(self.id)
    #    
    #    self.visible = True
    # 
    #===========================================================================
    def move(self):
            self.pos = Object3DDictionary[self.parents[0]].pos
            self.axis=Object3DDictionary[self.parents[1]].pos-Object3DDictionary[self.parents[0]].pos
    

class TwinkerHelper:

    _colorList = [color.orange,color.green , color.blue, color.red, color.yellow, color.magenta ,color.cyan ]

   
    @staticmethod
    def takeOldColors(elementsOf3DObjects):        
        return [x.color for x in elementsOf3DObjects]

    @staticmethod
    def TwinkleVector(listOfArgsToTwinkle,newColor,lableSegment):
        if(len(listOfArgsToTwinkle)>0):
            newaxis=vector(1,3,1)
            newpos = vector(0,0,0)
            radiusForLabel = 0.3#take from setting static class but now
            
            if(issubclass(type(listOfArgsToTwinkle[0]),Segment)):                                
                newaxis=listOfArgsToTwinkle[0].axis/4.                
                newpos=listOfArgsToTwinkle[0].pos 
                
            elif(issubclass(type(listOfArgsToTwinkle[0]), Point)):                            
                newaxis=(listOfArgsToTwinkle[1].pos-listOfArgsToTwinkle[0].pos)/4.
                newpos=listOfArgsToTwinkle[0].pos                                 
            elif(issubclass(type(listOfArgsToTwinkle[0]), vector)):            
                newaxis=listOfArgsToTwinkle[0]/4.
                newpos=vector(0,0,0)                 
            
            LabelHelper.ShowLabel(newpos, lableSegment)                    
            pointer1 = arrow(pos=newpos, axis=newaxis, shaftwidth=2*radiusForLabel,color=newColor)
            for ll in range(4):
                newpos1=newpos+ll*newaxis
                pointer1.pos = newpos1
                time.sleep(.3)
            
            pointer1.visible=0
            del pointer1  
            
            LabelHelper.HideLabel()
        else:
            pass
     
    @staticmethod
    def Twinkle(PointToTwinkle,labelText):
        if(issubclass(type(PointToTwinkle),man3DObject)):
            oldColor = PointToTwinkle.color
            #radius = PointToTwinkle.radius
            if issubclass(type(PointToTwinkle),Point):#"Five digits after decimal in float %.5f" % floatValue
                LabelHelper.ShowLabel(PointToTwinkle.pos, labelText+' :'+PointToTwinkle.name+'(%.2f,%.2f,%.2f)'%(PointToTwinkle.pos.x,PointToTwinkle.pos.y,PointToTwinkle.pos.z))              
            elif issubclass(type(PointToTwinkle),Segment):
                LabelHelper.ShowLabel(PointToTwinkle.pos+PointToTwinkle.axis/2., labelText+' :'+PointToTwinkle.name+' ((%.1f,%.1f,%.1f),(%.1f,%.1f,%.1f))'%(PointToTwinkle.pos.x,PointToTwinkle.pos.y,PointToTwinkle.pos.z,PointToTwinkle.axis.x,PointToTwinkle.axis.y,PointToTwinkle.axis.z))
            elif issubclass(type(PointToTwinkle),Plane):
                LabelHelper.ShowLabel((PointToTwinkle.pos[0]+PointToTwinkle.pos[1]+PointToTwinkle.pos[2])/3., labelText+' :'+PointToTwinkle.name) 
            for colorChange in TwinkerHelper._colorList:
                PointToTwinkle.color = colorChange
                time.sleep(0.2)
            
            PointToTwinkle.color = oldColor 
            #PointToTwinkle.radius = radius 
            
            LabelHelper.HideLabel()
            
        else:
            LabelHelper.ShowLabel(vector(0,0,0), labelText)
            
            time.sleep(1)
            LabelHelper.HideLabel()
            
                 

    
    
    @staticmethod
    def TwinkeElements(label3Delements, isFree = None, isDragable = None):
        ElementsToTwink = Object3DDictionary.values()
        if(isFree):
            ElementsToTwink = [elem for elem in ElementsToTwink if elem.isFree()]
        if(isDragable):
            ElementsToTwink = [elem for elem in ElementsToTwink if elem.canDrag()]
        oldColorsList = TwinkerHelper.takeOldColors(ElementsToTwink)
        
        label3Delements = label(pos=ElementsToTwink[0].pos, text=label3Delements, xoffset=20, yoffset=12, space=ElementsToTwink[0].radius + 0.3, height=10, border=6)
        for colorChange in TwinkerHelper._colorList:
            for elem3D in ElementsToTwink:                
                elem3D.color = colorChange
                if type(elem3D) != Plane: 
                    label3Delements.pos = elem3D.pos
                #elif type(elem3D) != Plane: 
                 #   label3Delements.pos = elem3D.pos
            time.sleep(0.2)
        i = 0
        for elem3D in ElementsToTwink:
            elem3D.color = oldColorsList[i]
            i=i+1        
        label3Delements.visible = False
        del label3Delements 
        del oldColorsList

class MeasurementHelper:#'(%.1f,%.1f,%.1f)'%(self.pos.x,self.pos.y,self.pos.z)
    @staticmethod
    def LengthOfSegments(selectedObjects):
        segments = [obj for obj in selectedObjects if issubclass(type(obj),Segment)]
        Length = 0
        name = 'All Segments:'
        if segments.__len__()==0:
            print 'choose segments to see all legth'
        else:
            for segment in segments:
                Length += segment.GetSize()
                name += ' '+segment.name+'( size = %.3f )'%(segment.GetSize())
            name += '\n\n Complete length = '+str(Length)
            print name
    
    @staticmethod
    def AreaOfPlanes(selectedObjects):
        planes = [obj for obj in selectedObjects if issubclass(type(obj),Plane)]
        Area = 0
        name = 'All planes:'
        if planes.__len__()==0:
            print 'choose planes to see all area'
        else:
            for plane in planes:
                Area += plane.area()
                name += ' '+plane.name+'( area = %.3f )'%(plane.area())
            name += '\n\n Complete area = '+str(Area)
            print name
            
class Object3DHelper:
    @staticmethod
    def PrintSpecialInformation():
        print "count Selected Objects"+str(len(selected3DObject))
        print "count visible 3D Object" +str(len([x for x in Object3DDictionary.values() if x.visible == True])) 
        print "count all 3D Object" +str(len(Object3DDictionary.values()))
    
    @staticmethod
    def SelectAll(alreadySelected3DObject):
        alreadySelected3DObject.freeSelectedObjects()
        selecetedElements = [x for x in Object3DDictionary.values() if x.visible==True]
        map(setSelectedColor,selecetedElements)
        alreadySelected3DObject.extend(selecetedElements)
    @staticmethod
    def isPointExist(vectorPos):
        for pointsPos in [elem.pos for elem in Object3DDictionary.values() if(elem.visible and issubclass(type(elem),Point))]:
                if(mag(vectorPos - pointsPos)<0.01):
                    return False
        return True
    
    @staticmethod
    def DeleteAll():
        for obj in Object3DDictionary.values():
            obj.visible = False
        UndoRedoManager.Clear()
class LabelHelper:
    showLabels = False
    draggableLabel = label( xoffset=20, yoffset=12, height=10, border=6,visible = False)
    @staticmethod
    def ShowLabel(positionOfMan3DObject,nameOfMan3DObject):
        
        if LabelHelper.draggableLabel.visible == False:
            LabelHelper.draggableLabel.visible =True 
        LabelHelper.draggableLabel.pos = positionOfMan3DObject#PointToShowLabel.pos
        LabelHelper.draggableLabel.text =nameOfMan3DObject#+str(positionOfMan3DObject)
        
            
    @staticmethod
    def HideLabel():
        if(LabelHelper.draggableLabel != None):
            LabelHelper.draggableLabel.visible = False
            
    @staticmethod
    def HideLabels(FromDragging = False):#listOfObject,FromDragging = False):
        if FromDragging == True:
            for obj in Object3DDictionary.values():#listOfObject:
                obj.HideLabel() 
        else:
            if not LabelHelper.showLabels:
                for obj in Object3DDictionary.values():#listOfObject:
                    obj.HideLabel()
    @staticmethod
    def ShowLabels():#listOfObject):
        if LabelHelper.showLabels:
            for obj in Object3DDictionary.values():#listOfObject:
                obj.ShowLabel()
                
    
            
            
######------------------------------------------------------------------------
######----------------SpecialElementsForTransformation---------------------

   
class SpecialElementsForTransformation:
    
    
    
    rotatedAngle = None
    rotatedSegmentOs = None
    symetricSegmentOs = None
    translateVector = None
    projectionSegment = None
    showProjectionDirection =  False
    
    homoteticCenter = None
    homoteticCoefficient = None
    delitationCoeficentX = None
    delitationCoeficentY = None
    delitationCoeficentZ = None
    
    
    parallelSegment = None
 #   isPlusDirection = None
    proportion = None
    proportionPoint = None
    screwMotionSize = None
    
    planeToProject = None
    vectorToProjectOnPlane = None
    
    
    @staticmethod
    def ValidatorListAfterDelete(listOfCurrentObject):
        for attributeName in dir(SpecialElementsForTransformation):
         #   print attributeName
            if issubclass(type(getattr(SpecialElementsForTransformation, attributeName)),man3DObject):
                attributeElement = getattr(SpecialElementsForTransformation, attributeName)
                if not attributeElement in listOfCurrentObject:
              #      print 'setting None ', attributeName
                    setattr(SpecialElementsForTransformation, attributeName, None) 
        
    
    @staticmethod
    def getterHelper(element):
        if element == None :
#            print 'Set object first'
            return None
        elif element.visible==True:
#            print  'getting',element
            return element
        else:
            print 'Ctrl+z or Ctrl+y to return object and then try again.You delete this object in current operations'
            print 'Or free the object'
            return None
        
    
    
    
    
    
    
    
    
    
                    #######################
                    #######Setters#########
                    #######################
    @staticmethod
    def SetRotatedAngle(newAngle):
        SpecialElementsForTransformation.rotatedAngle = newAngle
        
    @staticmethod
    def SetRotatedSegmentOs(newRotatedSegmentOs):
        SpecialElementsForTransformation.rotatedSegmentOs = newRotatedSegmentOs
        
        
        
    
    @staticmethod
    def SetSymetricSegmentOs(newSymetricSegmentOs):
        SpecialElementsForTransformation.symetricSegmentOs = newSymetricSegmentOs
        
   
    @staticmethod
    def SetTranslateVector(newTranslateVector):
        SpecialElementsForTransformation.translateVector = vector((newTranslateVector.x,newTranslateVector.y,newTranslateVector.z))
             
    @staticmethod
    def SetProjectionSegment(newProjectionSegment):
        SpecialElementsForTransformation.projectionSegment = newProjectionSegment
    
    @staticmethod
    def SetHomoteticCenter(newHomoteticCenter):
        SpecialElementsForTransformation.homoteticCenter = newHomoteticCenter
        
        
    
    @staticmethod    
    def SetHomoteticCoefficient(newHomoteticCoefficient):
        SpecialElementsForTransformation.homoteticCoefficient = newHomoteticCoefficient
            
    @staticmethod
    def SetDelitationCoeficentX(DelitationCoeficenX):
        SpecialElementsForTransformation.delitationCoeficentX = DelitationCoeficenX
    
    @staticmethod  
    def SetDelitationCoeficentY(DelitationCoeficenY):
        SpecialElementsForTransformation.delitationCoeficentY = DelitationCoeficenY
        
    @staticmethod    
    def SetDelitationCoeficentZ(DelitationCoeficenZ):
        SpecialElementsForTransformation.delitationCoeficentZ = DelitationCoeficenZ
        
    @staticmethod
    def SetParallelSegment(newParallelSegment):
        SpecialElementsForTransformation.parallelSegment = newParallelSegment
    
    @staticmethod
    def SetProportion(newProportion):
        SpecialElementsForTransformation.proportion = newProportion
        
    @staticmethod
    def SetProportionPoint(newProportionPoint):
        SpecialElementsForTransformation.proportionPoint = newProportionPoint
        
    @staticmethod
    def SetScrewMotionSize(newSize):
        SpecialElementsForTransformation.screwMotionSize = newSize
    
    @staticmethod
    def SetShowProjectionDirection(isToShow):
        SpecialElementsForTransformation.showProjectionDirection = isToShow
        
    @staticmethod
    def SetPlaneToProject(PlaneToProject):
        SpecialElementsForTransformation.planeToProject = PlaneToProject
    
    @staticmethod
    def SetVectorToProjectOnPlane(VectorToProjectOnPlane):
        SpecialElementsForTransformation.vectorToProjectOnPlane = VectorToProjectOnPlane
    
     
                
      
                    #######################
                    #######Getters#########
                    #######################
    
    @staticmethod
    def GetRotateAngle():
        return SpecialElementsForTransformation.rotatedAngle
    
    @staticmethod
    def GetRotatedSegmentOs():
        return SpecialElementsForTransformation.getterHelper(SpecialElementsForTransformation.rotatedSegmentOs)
        
            
    
    @staticmethod
    def GetSymetricSegmentOs():
        return SpecialElementsForTransformation.getterHelper(SpecialElementsForTransformation.symetricSegmentOs)
    
    @staticmethod
    def GetTranslateVector():
        return SpecialElementsForTransformation.translateVector
    
    @staticmethod
    def GetProjectionSegment():
        return SpecialElementsForTransformation.getterHelper(SpecialElementsForTransformation.projectionSegment)
    @staticmethod
    def GetHomoteticCenter():
        return SpecialElementsForTransformation.getterHelper(SpecialElementsForTransformation.homoteticCenter)
         
    @staticmethod
    def GetHomoteticCoefficient():
        return SpecialElementsForTransformation.homoteticCoefficient
    
    @staticmethod
    def GetDelitationCoeficentX():
        return SpecialElementsForTransformation.delitationCoeficentX
    
    @staticmethod  
    def GetDelitationCoeficentY():
        return SpecialElementsForTransformation.delitationCoeficentY
        
    @staticmethod    
    def GetDelitationCoeficentZ():
        return SpecialElementsForTransformation.delitationCoeficentZ 

    
    @staticmethod
    def GetParallelSegment():
        return SpecialElementsForTransformation.getterHelper(SpecialElementsForTransformation.parallelSegment)
    
#    @staticmethod
#    def GetIsPlusDirection():
#        return SpecialElementsForTransformation.isPlusDirection
#    
    @staticmethod
    def GetProportion():
        return SpecialElementsForTransformation.proportion
        
    @staticmethod
    def GetProportionPoint():
        return SpecialElementsForTransformation.getterHelper(SpecialElementsForTransformation.proportionPoint)
    
    @staticmethod
    def GetScrewMotionSize():
        return SpecialElementsForTransformation.screwMotionSize
    
    @staticmethod
    def GetShowProjectionDirection():
        return SpecialElementsForTransformation.showProjectionDirection
    
    @staticmethod
    def GetPlaneToProject():
        return SpecialElementsForTransformation.getterHelper(SpecialElementsForTransformation.planeToProject)
    
#    @staticmethod
#    def GetVectorToProjectOnPlane():
#        return SpecialElementsForTransformation.vectorToProjectOnPlane
#    
    
    
                    #######################
                    #####Free Method#######
                    #######################
    @staticmethod
    def FreeRotateAngle():
        SpecialElementsForTransformation.rotatedAngle= None
        
    @staticmethod
    def FreeRotatedSegmentOs():
        SpecialElementsForTransformation.rotatedSegmentOs=None

    @staticmethod
    def FreeSymetricSegmentOs():
        SpecialElementsForTransformation.symetricSegmentOs=None
            
    @staticmethod
    def FreeTranslateVector():
        SpecialElementsForTransformation.translateVector=None
            
    @staticmethod
    def FreeProjectionSegment():
        SpecialElementsForTransformation.projectionSegment=None
            
    @staticmethod
    def FreeHomoteticCenter():
        SpecialElementsForTransformation.homoteticCenter=None
        
    @staticmethod
    def FreeHomoteticCoefficient():
        SpecialElementsForTransformation.homoteticCoefficient=None
    
    @staticmethod
    def FreeDelitationCoeficents():
        SpecialElementsForTransformation.delitationCoeficentX = None
        SpecialElementsForTransformation.delitationCoeficentY = None
        SpecialElementsForTransformation.delitationCoeficentZ = None
            
    @staticmethod
    def FreeParallelSegment():
        SpecialElementsForTransformation.parallelSegment = None
    
            
    @staticmethod
    def FreeProportion():
        SpecialElementsForTransformation.proportion = None
        
    
    @staticmethod
    def FreeProportionPoint():
        SpecialElementsForTransformation.proportionPoint = None
        
    @staticmethod
    def FreeScrewMotionSize():    
        SpecialElementsForTransformation.screwMotionSize =None
        
    @staticmethod
    def FreeShowProjectionDirection():    
        SpecialElementsForTransformation.showProjectionDirection =False
        
    @staticmethod
    def FreePlaneToProject():
        SpecialElementsForTransformation.planeToProject = None
        
    @staticmethod
    def FreeVectorToProjectOnPlane():
        SpecialElementsForTransformation.vectorToProjectOnPlane = None
            
    ###########################################################
    ######----------------SpecialElementsForTransformation---------------------      
######------------------------------------------------------------------------
        

 

######?????if twinckle shoutld be on other place
class interfaceTwinklerOfSpecialArgs():
    def twinckle(self):
        pass    
#######################################################
#-----------------------Initializer Classes---------------
#######################################################
class OperationInitializer(interfaceTwinklerOfSpecialArgs):
    def initializeSpecialArguments(self):
        pass

class DefaultInitializer(OperationInitializer):
    pass

class RotateInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.AofOsAB = SpecialElementsForTransformation.GetRotatedSegmentOs().GetParent(1)
        self.BofOsAB = SpecialElementsForTransformation.GetRotatedSegmentOs().GetParent(0)
        self.rotationAngle = SpecialElementsForTransformation.GetRotateAngle()
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetRotatedSegmentOs(), "Rotation OS"+", with angle : "+str(SpecialElementsForTransformation.GetRotateAngle()))
        
class ScrewMotionInitializer(RotateInitializer):
    def initializeSpecialArguments(self):
        RotateInitializer.initializeSpecialArguments(self)
        self.sizeOfVector = SpecialElementsForTransformation.GetScrewMotionSize()
    
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetRotatedSegmentOs(), "Screw Motion OS"+", with angle : "+str(SpecialElementsForTransformation.GetRotateAngle())+ "Screw Motion Size : "+str(self.sizeOfVector))
        TwinkerHelper.TwinkleVector([-norm(SpecialElementsForTransformation.GetRotatedSegmentOs().axis)*self.sizeOfVector], color.red, "translated vector ")
        
class TranslateInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.translateVector = SpecialElementsForTransformation.GetTranslateVector()
        
    def twinckle(self):
        TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue, "translated vector "+str(self.translateVector))

class SymetriaBySegmentInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.AofOsAB = SpecialElementsForTransformation.GetSymetricSegmentOs().GetParent(1)
        self.BofOsAB = SpecialElementsForTransformation.GetSymetricSegmentOs().GetParent(0)
        self.rotationAngle = pi 
        self.symetricOs = SpecialElementsForTransformation.GetSymetricSegmentOs()       
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetSymetricSegmentOs(),"Symetric Os")
    
        




 
#----------------------------------------------------------------------------------
##############abstract class########
class OperationByCenterInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.homoteticCenter = SpecialElementsForTransformation.GetHomoteticCenter()
##############abstract class######## 
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------               

class DilitateInitializer(OperationByCenterInitializer):
    def initializeSpecialArguments(self):
        OperationByCenterInitializer.initializeSpecialArguments(self)
        self.HomotheticCoeficentX = SpecialElementsForTransformation.GetDelitationCoeficentX()
        self.HomotheticCoeficentY = SpecialElementsForTransformation.GetDelitationCoeficentY()
        self.HomotheticCoeficentZ = SpecialElementsForTransformation.GetDelitationCoeficentZ()
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Deletation Center, coefficent: "+"("+str(SpecialElementsForTransformation.GetDelitationCoeficentX())+str(SpecialElementsForTransformation.GetDelitationCoeficentY())+str(SpecialElementsForTransformation.GetDelitationCoeficentZ())+")")

class HomotetiaInitializer(OperationByCenterInitializer):
    def initializeSpecialArguments(self):
        OperationByCenterInitializer.initializeSpecialArguments(self)
        self.homoteticCoefficient = SpecialElementsForTransformation.GetHomoteticCoefficient()
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Homothetic Center, coefficent: "+str(SpecialElementsForTransformation.GetHomoteticCoefficient()))
        
class SymetriaByCenterInitializer(OperationByCenterInitializer):
    def initializeSpecialArguments(self):
        OperationByCenterInitializer.initializeSpecialArguments(self)
        self.homoteticCoefficient = 1
    
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Symetric Center")

       
#-----------------------------------------------------------------------------------

class ShowProjectionDirectionInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.isToShowProjectionDirection = SpecialElementsForTransformation.GetShowProjectionDirection()

class ProjectOnSegmentInitializer(ShowProjectionDirectionInitializer):
    def initializeSpecialArguments(self):
        self.projectionSegment = SpecialElementsForTransformation.GetProjectionSegment()
        ShowProjectionDirectionInitializer.initializeSpecialArguments(self)
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetProjectionSegment(),"Projection Os")
    
        #self.isToShowProjectionDirection = SpecialElementsForTransformation.GetShowProjectionDirection()


class ParallelsBySegmentInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.parallelSegment = SpecialElementsForTransformation.GetParallelSegment()
        #self.isPlusDirection = SpecialElementsForTransformation.GetIsPlusDirection()
    
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetParallelSegment(),"Parallel Os")



#class MakeTranslatedPoint(OperationInitializer):
#    def initializeSpecialArguments(self):
#        self.vector = SpecialElementsForTransformation.GetTranslateVector()
class ProportionInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.proportion = SpecialElementsForTransformation.GetProportion()

class ProportionPointInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.propPoint = SpecialElementsForTransformation.GetProportionPoint()
        
class PlaneInitializer(OperationInitializer):
    def initializeSpecialArguments(self):
        self.planeToProject = SpecialElementsForTransformation.GetPlaneToProject()
    def twinckle(self):
        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane")
    
class PlaneWithTranslateVectorInitializer(PlaneInitializer,TranslateInitializer):
    def initializeSpecialArguments(self):
        PlaneInitializer.initializeSpecialArguments(self)
        TranslateInitializer.initializeSpecialArguments(self)
        #self.translateVector = SpecialElementsForTransformation.GetTranslateVector()
    def twinckle(self):
        PlaneInitializer.twinckle(self)
        TranslateInitializer.twinckle(self)
        

class PlaneWithVectorInitializer(PlaneInitializer,TranslateInitializer):
    def initializeSpecialArguments(self):
        PlaneInitializer.initializeSpecialArguments(self)
        TranslateInitializer.initializeSpecialArguments(self)
        #self.translateVector = SpecialElementsForTransformation.GetTranslateVector()
    def twinckle(self):
        PlaneInitializer.twinckle(self)
        TranslateInitializer.twinckle(self)#(PlaneInitializer):
#    def initializeSpecialArguments(self):
#        PlaneInitializer.initializeSpecialArguments(self)
#        self.projectVector = SpecialElementsForTransformation.GetVectorToProjectOnPlane()


class PerpendicularOnPlaneInitializer(ShowProjectionDirectionInitializer,PlaneInitializer):
    def initializeSpecialArguments(self):
        ShowProjectionDirectionInitializer.initializeSpecialArguments(self)
        PlaneInitializer.initializeSpecialArguments(self)
        
        
#-----------------------------------------------------------------------------------

###################################################
#-----------------Movement------------------
################################################
class MoveOperation:
    def Move(self,pointToRotate):
        pass
    def prepare(self,argsList):
        return argsList

class MovementBySegmentAndAngle(MoveOperation):
    def Move(self,pointToRotate):
        normalizedAxis=norm(self.AofOsAB.pos-self.BofOsAB.pos)#Object3DDictionary[self.parents[2]].pos-Object3DDictionary[self.parents[1]].pos)
        vectorBetweenCenterAndPoint=pointToRotate.pos-self.BofOsAB.pos
        rotatedVector=vectorBetweenCenterAndPoint*cos(self.rotationAngle)+cross(normalizedAxis,vectorBetweenCenterAndPoint)*sin(self.rotationAngle)+(normalizedAxis.dot(vectorBetweenCenterAndPoint))*normalizedAxis*(1 - cos(self.rotationAngle)) 
        pointToRotate.pos = rotatedVector+self.BofOsAB.pos
 

class RotateMovement(RotateInitializer,MovementBySegmentAndAngle):
    pass

class SymetricMovementBySegment(SymetriaBySegmentInitializer,MovementBySegmentAndAngle):
    pass

class ScrewMovement(ScrewMotionInitializer,MovementBySegmentAndAngle):
    def Move(self,pointToRotate):
        MovementBySegmentAndAngle.Move(self, pointToRotate)
        pointToRotate.pos += norm(self.BofOsAB.pos - self.AofOsAB.pos)*self.sizeOfVector
    def prepare(self,argsList):
        resultList = []
        for arg in argsList:
            if arg.id!=self.AofOsAB.id and arg.id!=self.BofOsAB.id:
                resultList.append(arg)
        return resultList 

class TranslateMovementByVector(TranslateInitializer,MoveOperation):
    def Move(self,pointToTranslate):
        pointToTranslate.pos = pointToTranslate.pos+self.translateVector

class DelitaticMovementByCenter(DilitateInitializer,MoveOperation):        
    def Move(self,elementsToProject):    
        #elementsToProject.pos = self.homoteticCenter.pos + self.homoteticCoefficient*(elementsToProject.pos-self.homoteticCenter.pos )
        elementsToProject.pos.x = (1+self.HomotheticCoeficentX)*self.homoteticCenter.pos.x - self.HomotheticCoeficentX*elementsToProject.pos.x 
        elementsToProject.pos.y = (1+self.HomotheticCoeficentY)*self.homoteticCenter.pos.y - self.HomotheticCoeficentY*elementsToProject.pos.y
        elementsToProject.pos.z = (1+self.HomotheticCoeficentZ)*self.homoteticCenter.pos.z - self.HomotheticCoeficentZ*elementsToProject.pos.z

class HomoteticMovementByCenter(HomotetiaInitializer,MoveOperation):        
    def Move(self,elementsToProject):    
        elementsToProject.pos = self.homoteticCenter.pos - self.homoteticCoefficient*(elementsToProject.pos-self.homoteticCenter.pos )

class SymetricMovementByCenter(SymetriaByCenterInitializer,HomoteticMovementByCenter):        
    pass

class ProjectionToLine(ProjectOnSegmentInitializer, MoveOperation):
    def Move(self,elementsToProject):    
        ProjectionVector = self.projectionSegment.GetParent(1).pos - self.projectionSegment.GetParent(0).pos
        #elementsToProject.pos - self.projectionSegment.GetParent(0).pos
        vectorToProject = elementsToProject.pos - self.projectionSegment.GetParent(0).pos
        resultVector = vectorToProject.proj(ProjectionVector)
        elementsToProject.pos = self.projectionSegment.GetParent(0).pos + resultVector

class ProjectToPlaneMovement(PlaneWithVectorInitializer,MoveOperation):
    def Move(self,elementsToProject):
        elementsToProject.pos =(((self.planeToProject.A - elementsToProject.pos).dot(self.planeToProject.bxc))/self.translateVector.dot(self.planeToProject.bxc))*self.translateVector +elementsToProject.pos 
       
class PerpendicularProjectionToPlane(PlaneInitializer,MoveOperation):
    def Move(self,elementsToProject):
        elementsToProject.pos =(((self.planeToProject.A - elementsToProject.pos).dot(self.planeToProject.bxc))/self.planeToProject.bxc.dot(self.planeToProject.bxc))*self.planeToProject.bxc +elementsToProject.pos 
    
class SymetricMovementByPlane(PlaneInitializer,MoveOperation):
    def Move(self,elementsToProject):
        elementsToProject.pos =2*((((self.planeToProject.A - elementsToProject.pos).dot(self.planeToProject.bxc))/self.planeToProject.bxc.dot(self.planeToProject.bxc))*self.planeToProject.bxc +elementsToProject.pos) - elementsToProject.pos 
    
class SymetricMovementByPlaneAndVector(PlaneWithTranslateVectorInitializer,MoveOperation):
    def Move(self,elementsToProject):
        elementsToProject.pos =2*((((self.planeToProject.A - elementsToProject.pos).dot(self.planeToProject.bxc))/self.planeToProject.bxc.dot(self.planeToProject.bxc))*self.planeToProject.bxc +elementsToProject.pos) - elementsToProject.pos + self.translateVector 
    
    def prepare(self,argsList):
        resultList = []
        for arg in argsList:
            if arg.id!=self.planeToProject.GetParent(0).id and arg.id!=self.planeToProject.GetParent(1).id and arg.id != self.planeToProject.GetParent(2).id:
                resultList.append(arg)
        return resultList 


###################################################
#-----------------Creation------------------
################################################



class interfacePrepareArgumentsForMethodCreate:
    def prepare(self,argsList):
        pass
    def Create(self, FromPointToCreateDynamicPoint):
        pass


    
class CreateMethodNoConstraints(interfacePrepareArgumentsForMethodCreate):
    def prepare(self,argsList):
        #Remove points that exists from segments parent
        listToReturn = argsList[:]
      #  print "before", len(listToReturn)
        #listOfPointsToRemove = []
        for elem3D in argsList:
            if issubclass(type(elem3D), Segment):
                if(elem3D.GetParent(0) in listToReturn):
                    #listOfPointsToRemove.append(elem3D.GetParent(0))
                    listToReturn.remove(elem3D.GetParent(0))
                if(elem3D.GetParent(1) in listToReturn):
                    #listOfPointsToRemove.append(elem3D.GetParent(1))
                    listToReturn.remove(elem3D.GetParent(1))
            if issubclass(type(elem3D), Plane):
                if(elem3D.GetParent(0) in listToReturn):
                    #listOfPointsToRemove.append(elem3D.GetParent(0))
                    listToReturn.remove(elem3D.GetParent(0))
                if(elem3D.GetParent(1) in listToReturn):
                    #listOfPointsToRemove.append(elem3D.GetParent(1))
                    listToReturn.remove(elem3D.GetParent(1))
                if(elem3D.GetParent(2) in listToReturn):
                    #listOfPointsToRemove.append(elem3D.GetParent(1))
                    listToReturn.remove(elem3D.GetParent(2))
            else:
                pass
       #print "after", len(listToReturn)
        return listToReturn

class CreateMethodOnlyPoints(interfacePrepareArgumentsForMethodCreate):
    def prepare(self,argsList):
        resultList = []
        for i in range(len(argsList)):
            if argsList.isPointInIndex(i):
                resultList.append(argsList[i])
        return resultList
        #return argsList

class CreateMethodOnlySegments(interfacePrepareArgumentsForMethodCreate):
    def prepare(self,argsList):
        resultList = []
        for i in range(len(argsList)):
            if argsList.isSegmentInIndex(i):
                resultList.append(argsList[i])
        return resultList

class CreateMethodTwoPoints(interfacePrepareArgumentsForMethodCreate):
    def prepare(self,argsList):
        firstList = []
        for i in range(len(argsList)):
            if argsList.isPointInIndex(i):
                firstList.append(argsList[i])
        resultList = []
        length = len(firstList)
        if length<2:
            return resultList
        elif length==2:
            resultList = [[firstList[0],firstList[1]]]
            return resultList
        else:    
            for i in range(len(firstList)):
                resultList.append([firstList[i],firstList[(i+1)%length]])
        return resultList

class CreateMethodTwoSegments(interfacePrepareArgumentsForMethodCreate):
    def prepare(self,argsList):
        firstList = []
        for i in range(len(argsList)):
            if argsList.isSegmentInIndex(i):
                firstList.append(argsList[i])
        resultList = []
        length = len(firstList)
        if length<2:
            return resultList
        elif length==2:
            resultList = [[firstList[0],firstList[1]]]
            return resultList
        else:    
            for i in range(len(firstList)):
                resultList.append([firstList[i],firstList[(i+1)%length]])
        return resultList

class CreateMethodOnlyThreePoints(interfacePrepareArgumentsForMethodCreate):
    def prepare(self,argsList):
      #  print argsList
        resultList = []
        for i in range(len(argsList)):
            if argsList.isPointInIndex(i):
                resultList.append(argsList[i])
        if len(resultList)>=3:
            if mag((resultList[0].pos-resultList[1].pos).cross(resultList[1].pos-resultList[2].pos))<0.0001:
                return []
            else:
                return [resultList[:3]]
        else:
            return []
        
class CreateMethodNoPlane(interfacePrepareArgumentsForMethodCreate):
    def prepare(self,argsList):
        #Remove points that exists from segments parent
        listToReturn = argsList[:]
     #   print "before", len(listToReturn)
        #listOfPointsToRemove = []
        for elem3D in argsList:
            if issubclass(type(elem3D), Segment):
                if(elem3D.GetParent(0) in listToReturn):
                    #listOfPointsToRemove.append(elem3D.GetParent(0))
                    listToReturn.remove(elem3D.GetParent(0))
                if(elem3D.GetParent(1) in listToReturn):
                    #listOfPointsToRemove.append(elem3D.GetParent(1))
                    listToReturn.remove(elem3D.GetParent(1))
            if issubclass(type(elem3D), Plane):                                  
                listToReturn.remove(elem3D)
                
            else:
                pass
      #  print "after", len(listToReturn)
        return listToReturn
        

    
class CreateRotatedObject(RotateInitializer,CreateMethodNoConstraints):
        
    def Create(self,rotationalObjectToCreateFrom):
        undoRedoIds = []
        rotatedOs = SpecialElementsForTransformation.GetRotatedSegmentOs()
        if issubclass(type(rotationalObjectToCreateFrom) , Segment):
            A1 = RotatedPointByAngle(self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(0))
            B1 = RotatedPointByAngle(self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
        elif(issubclass(type(rotationalObjectToCreateFrom) , Plane)):
            A1 = RotatedPointByAngle(self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(0))
            B1 = RotatedPointByAngle(self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(1))
            C1 = RotatedPointByAngle(self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
        
        else:
            undoRedoIds.append(RotatedPointByAngle(self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom).id)
        return undoRedoIds

class CreateScrewMotionObject(ScrewMotionInitializer,CreateMethodNoConstraints):
        
    def Create(self,rotationalObjectToCreateFrom):
        undoRedoIds = []
        rotatedOs = SpecialElementsForTransformation.GetRotatedSegmentOs()
        #sezeOfVector = SpecialElementsForTransformation.GetScrewMotionSize()
        if issubclass(type(rotationalObjectToCreateFrom) , Segment):
            A1 = ScrewMotion(self.sizeOfVector,self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(0))
            B1 = ScrewMotion(self.sizeOfVector,self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
        elif(issubclass(type(rotationalObjectToCreateFrom) , Plane)):
            A1 = ScrewMotion(self.sizeOfVector,self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(0))
            B1 = ScrewMotion(self.sizeOfVector,self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(1))
            C1 = ScrewMotion(self.sizeOfVector,self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
        
        else:
            undoRedoIds.append(ScrewMotion(self.sizeOfVector,self.rotationAngle,rotatedOs,rotationalObjectToCreateFrom).id)
        return undoRedoIds
    


class CreateSymetricObject(SymetriaByCenterInitializer,CreateMethodNoConstraints):
    def Create(self, symetricObjectsToCreateFrom):
        undoRedoIds = []         
        if issubclass(type(symetricObjectsToCreateFrom) , Segment):
            A1 = SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(0))
            B1 = SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
            
        if issubclass(type(symetricObjectsToCreateFrom) , Plane):
            A1 = SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(0))
            B1 = SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(1))
            C1 = SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
    
        else:
            undoRedoIds.append(SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom).id)
        return undoRedoIds
    
class CreateHomotheticObject(HomotetiaInitializer,CreateMethodNoConstraints):    
    def Create(self, symetricObjectsToCreateFrom):
        undoRedoIds = []         
        if issubclass(type(symetricObjectsToCreateFrom) , Segment):
            A1 = HomotheticPoint(self.homoteticCoefficient,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(0))
            B1 = HomotheticPoint(self.homoteticCoefficient,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
            
        if issubclass(type(symetricObjectsToCreateFrom) , Plane):
            A1 = HomotheticPoint(self.homoteticCoefficient,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(0))
            B1 = HomotheticPoint(self.homoteticCoefficient,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(1))
            C1 = HomotheticPoint(self.homoteticCoefficient,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
    
        else:
            undoRedoIds.append(HomotheticPoint(self.homoteticCoefficient,self.homoteticCenter,symetricObjectsToCreateFrom).id)
        return undoRedoIds
    
class CreateDelitaticObject(DilitateInitializer,CreateMethodNoConstraints):    
    def Create(self, symetricObjectsToCreateFrom):
        undoRedoIds = []         
        if issubclass(type(symetricObjectsToCreateFrom) , Segment):
            A1 = DelitatePoint(self.HomotheticCoeficentX,self.HomotheticCoeficentY,self.HomotheticCoeficentZ,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(0))
            B1 = DelitatePoint(self.HomotheticCoeficentX,self.HomotheticCoeficentY,self.HomotheticCoeficentZ,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
            
        if issubclass(type(symetricObjectsToCreateFrom) , Plane):
            A1 = DelitatePoint(self.HomotheticCoeficentX,self.HomotheticCoeficentY,self.HomotheticCoeficentZ,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(0))
            B1 = DelitatePoint(self.HomotheticCoeficentX,self.HomotheticCoeficentY,self.HomotheticCoeficentZ,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(1))
            C1 = DelitatePoint(self.HomotheticCoeficentX,self.HomotheticCoeficentY,self.HomotheticCoeficentZ,self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
    
        else:
            undoRedoIds.append(DelitatePoint(self.HomotheticCoeficentX,self.HomotheticCoeficentY,self.HomotheticCoeficentZ,self.homoteticCenter,symetricObjectsToCreateFrom).id)
        return undoRedoIds
#class CreateSymetricObject(MakeSymetricObjectByCenter,CreateMethodNoConstraints):
#    def Create(self, symetricObjectsToCreateFrom):
#        undoRedoIds = []         
#        if issubclass(type(symetricObjectsToCreateFrom) , Segment):
#            A1 = SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(0))
#            B1 = SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom.GetParent(1))
#            A1B1 = Segment(A1,B1)
#            undoRedoIds.append(A1.id)
#            undoRedoIds.append(B1.id)
#            undoRedoIds.append(A1B1.id)
#        else:
#            undoRedoIds.append(SymetricPoint(self.homoteticCenter,symetricObjectsToCreateFrom).id)
#        return undoRedoIds

class CreateProjectionOfObjects(ProjectOnSegmentInitializer, CreateMethodNoPlane):
#
    def Create(self, symetricObjectsToCreateFrom):
        undoRedoIds = []         
        if issubclass(type(symetricObjectsToCreateFrom) , Segment):
            A1 = PerpendicularPoint(symetricObjectsToCreateFrom.GetParent(0),self.projectionSegment)
            B1 = PerpendicularPoint(symetricObjectsToCreateFrom.GetParent(1),self.projectionSegment)
            A1B1 = Segment(A1,B1)
            if self.isToShowProjectionDirection:
                A1C1= Segment(A1,symetricObjectsToCreateFrom.GetParent(0))
                B1D1= Segment(B1,symetricObjectsToCreateFrom.GetParent(1))
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
            if self.isToShowProjectionDirection:
                undoRedoIds.append(A1C1.id)
                undoRedoIds.append(B1D1.id) 
        else:
            #undoRedoIds.append(PerpendicularPoint(symetricObjectsToCreateFrom,self.projectionSegment).id)
            A1 = PerpendicularPoint(symetricObjectsToCreateFrom,self.projectionSegment)
            if self.isToShowProjectionDirection:
                A1C1= Segment(A1,symetricObjectsToCreateFrom)
            undoRedoIds.append(A1.id)
            if self.isToShowProjectionDirection:
                undoRedoIds.append(A1C1.id)
        return undoRedoIds



class CreateParallelSegment(ParallelsBySegmentInitializer,CreateMethodOnlyPoints):#CreateOperation):#only for Points
    def Create(self,pointToCreateParallelSegmentFrom):
        undoRedoIds = []
        B =  TranslatedPointBySegmentForGeneration(1,pointToCreateParallelSegmentFrom,self.parallelSegment)#TranslatedPoint(self.isPlusDirection,pointToCreateParallelSegmentFrom, self.parallelSegment )
        AB=Segment(pointToCreateParallelSegmentFrom,B)
        undoRedoIds.append(B.id)
        undoRedoIds.append(AB.id)
        return undoRedoIds
    
class CreateTranslatedPoint(TranslateInitializer,CreateMethodNoConstraints):#CreateOperationByPoints):
    def Create(self, ObjectsToCreateFrom):
        undoRedoIds = []
        if issubclass(type(ObjectsToCreateFrom) , Segment):
            A1 = TranslatedPointByVector(self.translateVector,ObjectsToCreateFrom.GetParent(0))
            B1 = TranslatedPointByVector(self.translateVector,ObjectsToCreateFrom.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
            
        if issubclass(type(ObjectsToCreateFrom) , Plane):
            A1 = TranslatedPointByVector(self.translateVector,ObjectsToCreateFrom.GetParent(0))
            B1 = TranslatedPointByVector(self.translateVector,ObjectsToCreateFrom.GetParent(1))
            C1 = TranslatedPointByVector(self.translateVector,ObjectsToCreateFrom.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
    
        else:
            undoRedoIds.append(TranslatedPointByVector(self.translateVector,ObjectsToCreateFrom).id)         
            
        return undoRedoIds

class CreateSymetricPointBySegment(SymetriaBySegmentInitializer,CreateMethodNoConstraints):
    def Create(self, ObjectsToCreateFrom):
        undoRedoIds = []
        symetricOs = self.symetricOs
        if issubclass(type(ObjectsToCreateFrom) , Segment):
            A1 = RotatedPointByAngle(self.rotationAngle,symetricOs,ObjectsToCreateFrom.GetParent(0))
            B1 = RotatedPointByAngle(self.rotationAngle,symetricOs,ObjectsToCreateFrom.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
        elif(issubclass(type(ObjectsToCreateFrom) , Plane)):
            A1 = RotatedPointByAngle(self.rotationAngle,symetricOs,ObjectsToCreateFrom.GetParent(0))
            B1 = RotatedPointByAngle(self.rotationAngle,symetricOs,ObjectsToCreateFrom.GetParent(1))
            C1 = RotatedPointByAngle(self.rotationAngle,symetricOs,ObjectsToCreateFrom.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
        
        else:
            undoRedoIds.append(RotatedPointByAngle(self.rotationAngle,symetricOs,ObjectsToCreateFrom).id)
        return undoRedoIds 

    
class CreateMiddlePointBySegments(DefaultInitializer,CreateMethodOnlySegments):
    
    def Create(self,SegmentToCreateMiddlePointTo):
        undoRedoIds = []
        undoRedoIds.append(MiddlePoint(SegmentToCreateMiddlePointTo).id)
        return undoRedoIds

class CreateMiddlePointByPoints(DefaultInitializer,CreateMethodTwoPoints):
    
    def Create(self,twoElementsToCreateMiddlePointTo):
        undoRedoIds = []
        undoRedoIds.append(MiddlePoint(twoElementsToCreateMiddlePointTo[0],twoElementsToCreateMiddlePointTo[1]).id)
        return undoRedoIds


class CreateProportionPointBySegmentsAndProportion(ProportionInitializer,CreateMethodOnlySegments):
    def Create(self,SegmentToCreateMiddlePointTo):
        undoRedoIds = []
        undoRedoIds.append(ProportionalPointCreatedByProportion(1-self.proportion,1,SegmentToCreateMiddlePointTo).id)
        return undoRedoIds

class CreateProportionPointByPointsAndProportion(ProportionInitializer,CreateMethodTwoPoints):
    def Create(self,twoElementsToCreatePropPoint):
        undoRedoIds = []
        undoRedoIds.append(ProportionalPointCreatedByProportion(1-self.proportion,1,twoElementsToCreatePropPoint[0],twoElementsToCreatePropPoint[1]).id)
        return undoRedoIds
    
class CreateProportionPointBySegmentsAndProportionalPoint(ProportionPointInitializer,CreateMethodOnlySegments):
    def Create(self,SegmentToCreateMiddlePointTo):
        undoRedoIds = []
        undoRedoIds.append(ProportionalPointCreatedByProportionalPoint(SegmentToCreateMiddlePointTo,self.propPoint).id)
        return undoRedoIds

class CreateProportionPointByPointsAndProportionalPoint(ProportionPointInitializer,CreateMethodTwoPoints):
    def Create(self,TwoElementsToCreatePropPoint):
        undoRedoIds = []
        undoRedoIds.append(ProportionalPointCreatedByProportionalPoint(TwoElementsToCreatePropPoint[0],TwoElementsToCreatePropPoint[1],self.propPoint).id)
        return undoRedoIds


class CreateSegment(DefaultInitializer,CreateMethodTwoPoints):
    def Create(self,twoElementsToCreateSegment):
        undoRedoIds = []
        
        undoRedoIds.append(Segment(twoElementsToCreateSegment[0],twoElementsToCreateSegment[1]).id)
        return undoRedoIds
    
class CreateCrossPoint(DefaultInitializer,CreateMethodTwoSegments):
    def Create(self,twoElementsToCreatePoint):
        undoRedoIds = []
        undoRedoIds.append(CrossPoint(twoElementsToCreatePoint[0],twoElementsToCreatePoint[1]).id)
        return undoRedoIds

class CreateIntersactionOfPlaneAndSegment(PlaneInitializer,CreateMethodOnlySegments):
    def Create(self,SegmentToCreateIntersactionWithPlane):
        undoRedoIds = []
        undoRedoIds.append(ProjectionPlanePointBySegment(self.planeToProject,SegmentToCreateIntersactionWithPlane).id)
        return undoRedoIds
    
class CreateProjectionOnPlane(PlaneWithVectorInitializer,CreateMethodNoConstraints):
    def Create(self,Object3dToProjectOn):
        undoRedoIds = []
        
        if issubclass(type(Object3dToProjectOn) , Segment):
            A1 = ProjectionPlanePointByVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(0))
            B1 = ProjectionPlanePointByVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
        elif(issubclass(type(Object3dToProjectOn) , Plane)):
            A1 = ProjectionPlanePointByVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(0))
            B1 = ProjectionPlanePointByVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(1))
            C1 = ProjectionPlanePointByVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
        
        else:
            undoRedoIds.append(ProjectionPlanePointByVector(self.translateVector,self.planeToProject,Object3dToProjectOn).id)
        return undoRedoIds
    
class CreateSymetricByPlane(PlaneInitializer,CreateMethodNoConstraints):
    def Create(self,Object3dToProjectOn):
        undoRedoIds = []
        
        if issubclass(type(Object3dToProjectOn) , Segment):
            A1 = SymetriaByPlane(self.planeToProject,Object3dToProjectOn.GetParent(0))
            B1 = SymetriaByPlane(self.planeToProject,Object3dToProjectOn.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
        elif(issubclass(type(Object3dToProjectOn) , Plane)):
            A1 = SymetriaByPlane(self.planeToProject,Object3dToProjectOn.GetParent(0))
            B1 = SymetriaByPlane(self.planeToProject,Object3dToProjectOn.GetParent(1))
            C1 = SymetriaByPlane(self.planeToProject,Object3dToProjectOn.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
        
        else:
            undoRedoIds.append(SymetriaByPlane(self.planeToProject,Object3dToProjectOn).id)
        return undoRedoIds

class CreateSymetricByPlaneAndVector(PlaneWithTranslateVectorInitializer,CreateMethodNoConstraints):
    def Create(self,Object3dToProjectOn):
        undoRedoIds = []
        
        if issubclass(type(Object3dToProjectOn) , Segment):
            A1 = SymetriaByPlaneAndVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(0))
            B1 = SymetriaByPlaneAndVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(1))
            A1B1 = Segment(A1,B1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
        elif(issubclass(type(Object3dToProjectOn) , Plane)):
            A1 = SymetriaByPlaneAndVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(0))
            B1 = SymetriaByPlaneAndVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(1))
            C1 = SymetriaByPlaneAndVector(self.translateVector,self.planeToProject,Object3dToProjectOn.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
        
        else:
            undoRedoIds.append(SymetriaByPlaneAndVector(self.translateVector,self.planeToProject,Object3dToProjectOn).id)
        return undoRedoIds
    

class CreatePerpendicularPlane(PerpendicularOnPlaneInitializer,CreateMethodNoConstraints):
    def Create(self,Object3dToPerpendicularOn):
        undoRedoIds = []         
        if issubclass(type(Object3dToPerpendicularOn) , Segment):
            A1 = PerpendicularProjectionPlane(self.planeToProject,Object3dToPerpendicularOn.GetParent(0))
            B1 = PerpendicularProjectionPlane(self.planeToProject,Object3dToPerpendicularOn.GetParent(1))
            A1B1 = Segment(A1,B1)
            if self.isToShowProjectionDirection:
                A1C1= Segment(A1,Object3dToPerpendicularOn.GetParent(0))
                B1D1= Segment(B1,Object3dToPerpendicularOn.GetParent(1))
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(A1B1.id)
            if self.isToShowProjectionDirection:
                undoRedoIds.append(A1C1.id)
                undoRedoIds.append(B1D1.id)
        elif(issubclass(type(Object3dToPerpendicularOn) , Plane)):
            A1 = PerpendicularProjectionPlane(self.planeToProject,Object3dToPerpendicularOn.GetParent(0))
            B1 = PerpendicularProjectionPlane(self.planeToProject,Object3dToPerpendicularOn.GetParent(1))
            C1 = PerpendicularProjectionPlane(self.planeToProject,Object3dToPerpendicularOn.GetParent(2))
            if self.isToShowProjectionDirection:
                A1A2= Segment(A1,Object3dToPerpendicularOn.GetParent(0))
                B1B2= Segment(B1,Object3dToPerpendicularOn.GetParent(1))
                C1C2= Segment(C1,Object3dToPerpendicularOn.GetParent(2))
            A1B1C1 = Plane(A1,B1,C1)
            undoRedoIds.append(A1.id)
            undoRedoIds.append(B1.id)
            undoRedoIds.append(C1.id)
            undoRedoIds.append(A1B1C1.id)
            if self.isToShowProjectionDirection:
                undoRedoIds.append(A1A2.id)
                undoRedoIds.append(B1B2.id)
                undoRedoIds.append(C1C2.id)
        
        else:
            
            A1 = PerpendicularProjectionPlane(self.planeToProject,Object3dToPerpendicularOn)
            if self.isToShowProjectionDirection:
                A1C1= Segment(A1,Object3dToPerpendicularOn)
            undoRedoIds.append(A1.id)
            if self.isToShowProjectionDirection:
                undoRedoIds.append(A1C1.id)
        return undoRedoIds

class CreatePlane(DefaultInitializer,CreateMethodOnlyThreePoints):
    def Create(self,threeElementsToCreatePoint):
       # print threeElementsToCreatePoint
        undoRedoIds = []
        undoRedoIds.append(Plane(threeElementsToCreatePoint[0],threeElementsToCreatePoint[1],threeElementsToCreatePoint[2]).id)
        return undoRedoIds
    
class CreateBisectorPoint(DefaultInitializer,CreateMethodOnlyThreePoints):
    def Create(self,threeElementsToCreatePoint):
       # print threeElementsToCreatePoint
        undoRedoIds = []
        undoRedoIds.append(BisectorPoint(threeElementsToCreatePoint[0],threeElementsToCreatePoint[1],threeElementsToCreatePoint[2]).id)
        return undoRedoIds 

###################################################
#-----------------Create API------------------
################################################
class Creator:
    
    rotate = CreateRotatedObject()
    screwMotion = CreateScrewMotionObject()#OK with transform
    translate = CreateTranslatedPoint()
    
    symetric = CreateSymetricObject()#OK with transform
    homothetic = CreateHomotheticObject()
    delitatic = CreateDelitaticObject()
    symetricBySegment =CreateSymetricPointBySegment()
    symetricByPlane = CreateSymetricByPlane()
    symetricByPlaneAndVector = CreateSymetricByPlaneAndVector()

    projection = CreateProjectionOfObjects()
    perpendicularProjectionOnPlane = CreatePerpendicularPlane()#OK ,but in creation there is no creation for Plane
    projectOnPlane = CreateProjectionOnPlane()
#    projectionToLine = CreateProjectionLineOfObjects()#No sense  to move or to use Plane
    parallelSegment = CreateParallelSegment()
    
    midPointsBySegments = CreateMiddlePointBySegments()
    midPointsByPoints = CreateMiddlePointByPoints()
    proportionPointBySegmentsAndProportion = CreateProportionPointBySegmentsAndProportion()
    proportionPointByPointsAndProportion = CreateProportionPointByPointsAndProportion()
    proportionPointBySegmentsAndProportionalPoint = CreateProportionPointBySegmentsAndProportionalPoint()
    proportionPointByPointsAndProportionalPoint = CreateProportionPointByPointsAndProportionalPoint()
    segment = CreateSegment()
    crossPoint = CreateCrossPoint()
    intersactionSegmentAndPlane=CreateIntersactionOfPlaneAndSegment()
    
    
    plane = CreatePlane()
    bisector = CreateBisectorPoint()
 
              
    @staticmethod  
    def _Create(creationName,elementsToCreateFrom):
        undoRedoListIds=[]
        preparedElementsToCreateFrom = creationName.prepare(elementsToCreateFrom)
        creationName.initializeSpecialArguments()
        creationName.twinckle()
         
        
        for element in preparedElementsToCreateFrom:
            undoRedoIds = creationName.Create(element)
            for id in undoRedoIds:
                undoRedoListIds.append(id)
        if len(undoRedoListIds)>0:
            UndoRedoManager.PushToUndoStack(CreateUndoRedo(undoRedoListIds))
            #UndoRedoManager.PushToRedoStack(CreateUndoRedo(undoRedoListIds))
            #undoStack.push((undoRedoListIds,1))
        
        
    @staticmethod
    def Rotate(elementsToTransform):
        Creator._Create(Creator.rotate,elementsToTransform)
        
    @staticmethod
    def ScrewMotion(elementsToTransform):
        Creator._Create(Creator.screwMotion,elementsToTransform)
        
    @staticmethod
    def MakeSymetric(elementsToTransform):
        Creator._Create(Creator.symetric, elementsToTransform)
        
    @staticmethod
    def MakeHomothetic(elementsToTransform):
        Creator._Create(Creator.homothetic, elementsToTransform)
    
    @staticmethod
    def MakeDelitatic(elementsToTransform):
        Creator._Create(Creator.delitatic, elementsToTransform)
    
    @staticmethod
    def MakeSymetricBySegment(elementsToTransform):
        Creator._Create(Creator.symetricBySegment, elementsToTransform)
    
    @staticmethod
    def MakeSymetricByPlane(elementsToTransform):
        Creator._Create(Creator.symetricByPlane, elementsToTransform)
        
    @staticmethod
    def MakeSymetricByPlaneAndTranslateVector(elementsToTransform):
        Creator._Create(Creator.symetricByPlaneAndVector, elementsToTransform)
        
    @staticmethod
    def ProjectToLine(elementsToTransform):
        Creator._Create(Creator.projection, elementsToTransform)
    
#    @staticmethod   
#    def MakeProjectionLines(elementsToTransform):
#        Creator._Create(Creator.projectionToLine, elementsToTransform)
#        
    @staticmethod   
    def MakeParallelSegments(elementsToTransform):
        Creator._Create(Creator.parallelSegment, elementsToTransform)
    
    @staticmethod 
    def MakeMiddlePointsBySegments(elementsToTransform):
        Creator._Create(Creator.midPointsBySegments, elementsToTransform)
    
    @staticmethod 
    def MakeMiddlePointsByPoints(elementsToTransform):
        Creator._Create(Creator.midPointsByPoints, elementsToTransform)
    
        
    @staticmethod
    def MakeProportionPointBySegmentsAndProportion(elementsToTransform):
        Creator._Create(Creator.proportionPointBySegmentsAndProportion, elementsToTransform)
    
    @staticmethod
    def MakeProportionPointByPointsAndProportion(elementsToTransform):
        Creator._Create(Creator.proportionPointByPointsAndProportion, elementsToTransform)
    
    
    @staticmethod
    def MakeProportionPointBySegmentsAndProportionalPoint(elementsToTransform):
        Creator._Create(Creator.proportionPointBySegmentsAndProportionalPoint, elementsToTransform)    
    
    @staticmethod
    def MakeProportionPointByPointsAndProportionalPoint(elementsToTransform):
        Creator._Create(Creator.proportionPointByPointsAndProportionalPoint, elementsToTransform)    
    
    @staticmethod
    def MakeSegment(elementsToTransform):
        Creator._Create(Creator.segment, elementsToTransform)    
    
    @staticmethod
    def MakeCrossPoint(elementsToTransform):
        Creator._Create(Creator.crossPoint, elementsToTransform)
    
    @staticmethod
    def MakeIntersactionOfPlaneAndSegmentt(elementsToTransform):
        Creator._Create(Creator.intersactionSegmentAndPlane, elementsToTransform)
    
        
    @staticmethod
    def MakeTranslation(elementsToTransform):
        Creator._Create(Creator.translate, elementsToTransform)
    
    @staticmethod
    def MakePlane(elementsToTransform):
     #   print 'MakePlane'
        Creator._Create(Creator.plane, elementsToTransform)
        
    @staticmethod
    def MakeBisectorPoint(elementsToTransform):
     #   print 'MakePlane'
        Creator._Create(Creator.bisector, elementsToTransform)
    
    @staticmethod
    def MakeProjectionOnPlane(elementsToTransform):
        Creator._Create(Creator.projectOnPlane, elementsToTransform)
    
    @staticmethod
    def MakePerpendicularProjectionOnPlane(elementsToTransform):
        Creator._Create(Creator.perpendicularProjectionOnPlane, elementsToTransform)    
    
        
###################################################
#-----------------Delete API------------------
################################################
class DeletorAndFreeHelper:
    
    @staticmethod
    def Delete3DObjectForUndoRedoManager(vMan3DObjects):
        undoStackIds = []
        for man3DObject in vMan3DObjects:
            if not man3DObject.isDeleted():
                undoStackIds.append(man3DObject.id)
                man3DObject.ChangeVisible(True)
        if len(undoStackIds)>0:
            UndoRedoManager.PushToUndoStack(DeleteUndoRedo(undoStackIds))
            #UndoRedoManager.PushToRedoStack(DeleteUndoRedo(undoStackIds))
    
    @staticmethod
    def Free3DObjectForUndoRedoManager(vMan3DObjects):
        undoStackDataList = []
        for man3DObject in vMan3DObjects:
             
            if issubclass(type(man3DObject),Point) and not man3DObject.isFree() and not issubclass(type(man3DObject),ProportionalPoint):
                dataForFreePoint = DataForFreeObject(man3DObject.id,man3DObject.parents, man3DObject.__class__,man3DObject.IsDraggable,man3DObject.initParents)
                undoStackDataList.append(dataForFreePoint)
                man3DObject.Free()
        if len(undoStackDataList)>0:
            UndoRedoManager.PushToUndoStack(FreeUndoRedo(undoStackDataList))
            #UndoRedoManager.PushToRedoStack(FreeUndoRedo(undoStackDataList))   
        

###################################################
#-----------------Transform API------------------
################################################        
class Transformer:
    rotate = RotateMovement()
    screwMotion = ScrewMovement()
    translate = TranslateMovementByVector()
    symetricByPoint = SymetricMovementByCenter()
    symetricByPlane = SymetricMovementByPlane()
    symetricByPlanePlusVector = SymetricMovementByPlaneAndVector()
    
    projectOnSegment = ProjectionToLine()
    projectOnPlane = ProjectToPlaneMovement()
    perpProjOnPlane = PerpendicularProjectionToPlane()
    
    makeHomotetia = HomoteticMovementByCenter()
    makeDelitatia = DelitaticMovementByCenter()
    symetricBySegment = SymetricMovementBySegment()
    
    @staticmethod
    def prepareTransformationArgs(elementsToTransform):  
           
        listOfElementsToTransform = []
        for element in elementsToTransform:
            if type(element)==Point and element.isFree() and element not in listOfElementsToTransform:
                listOfElementsToTransform.append(element);
           
            elif type(element)== Segment :
                if element.GetParent(0).isFree()and element.GetParent(0) not in listOfElementsToTransform:
                    listOfElementsToTransform.append(element.GetParent(0))
                if element.GetParent(1).isFree()and element.GetParent(1) not in listOfElementsToTransform:
                    listOfElementsToTransform.append(element.GetParent(1))
            elif type(element)== Plane :
                if element.GetParent(0).isFree()and element.GetParent(0) not in listOfElementsToTransform:
                    listOfElementsToTransform.append(element.GetParent(0))
                if element.GetParent(1).isFree()and element.GetParent(1) not in listOfElementsToTransform:
                    listOfElementsToTransform.append(element.GetParent(1))
                if element.GetParent(2).isFree()and element.GetParent(2) not in listOfElementsToTransform:
                    listOfElementsToTransform.append(element.GetParent(2))
               
        return listOfElementsToTransform
      
    @staticmethod  
    def _Transform(transformationName,elementsToTransform):
        dictionaryOdIdsAndPositions = {}
        transformationName.initializeSpecialArguments()
        transformationName.twinckle()
        elementsToTransform = transformationName.prepare(Transformer.prepareTransformationArgs(elementsToTransform))
         
        for element in elementsToTransform:
            vectorOldPosition = vector((element.pos.x,element.pos.y,element.pos.z))
            transformationName.Move(element)
            element.RedrawChildDynamics(True)           
            dictionaryOdIdsAndPositions[element.id]=vectorOldPosition
        
        if len(dictionaryOdIdsAndPositions)>0:
            UndoRedoManager.PushToUndoStack(MoveUndoRedo(dictionaryOdIdsAndPositions))
            #UndoRedoManager.PushToRedoStack(MoveUndoRedo(dictionaryOdIdsAndPositions))
        #undoStack.push((dictionaryOdIdsAndPositions,3))    
    
    @staticmethod
    def Rotate(elementsToTransform):
        Transformer._Transform(Transformer.rotate, elementsToTransform)
    
    @staticmethod
    def ScrewMotion(elementsToTransform):
        Transformer._Transform(Transformer.screwMotion, elementsToTransform)
            
    @staticmethod
    def Translate(elementsToTransform):
        Transformer._Transform(Transformer.translate, elementsToTransform)
    
    @staticmethod    
    def ProjectToSegment(elementsToTransform):
        Transformer._Transform(Transformer.projectOnSegment, elementsToTransform)
        
    @staticmethod    
    def ProjectToPlane(elementsToTransform):
        
        Transformer._Transform(Transformer.projectOnPlane, elementsToTransform)
        
    @staticmethod    
    def PrpendicularProjectToPlane(elementsToTransform):
        Transformer._Transform(Transformer.perpProjOnPlane, elementsToTransform)
        
    @staticmethod    
    def HomotetiaByPoint(elementsToTransform):
        Transformer._Transform(Transformer.makeHomotetia, elementsToTransform)

    @staticmethod    
    def DelitationByPoins(elementsToTransform):
        Transformer._Transform(Transformer.makeDelitatia, elementsToTransform)
    
    @staticmethod    
    def SymetricByCenter(elementsToTransform):
        Transformer._Transform(Transformer.symetricByPoint, elementsToTransform)
        
    @staticmethod    
    def SymetricByPlane(elementsToTransform):
        Transformer._Transform(Transformer.symetricByPlane, elementsToTransform)
    
    @staticmethod    
    def SymetricByPlanePlusTranslateVector(elementsToTransform):
        Transformer._Transform(Transformer.symetricByPlanePlusVector, elementsToTransform)
    
    @staticmethod    
    def SymetricByLine(elementsToTransform):#implemented by rotation
        Transformer._Transform(Transformer.symetricBySegment, elementsToTransform)

class GenerateElements:
    def Generate(self,*elementsArgs):
        pass
    def prepare(self,list):
        return list
        
class GenerateDefault:
    def __init__(self):
        self.TranslaterVector = vector((0.1,0.1,0.1))
    def updateNewPosition(self):
        self.TranslaterVector += vector((0.1,0.1,0.1))

class GenerateConstructions(GenerateDefault,GenerateElements):
    def __init__(self):
        GenerateDefault.__init__(self) 

class GeneratePoint(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    def Generate(self,position = None,proportion = None,bySegment = None):
        if position != None:
            return [Point(position).id]
        else:
            position = vector((0,0,0)) + self.TranslaterVector
            self.updateNewPosition()
            return [Point(position).id]
        
class GeneratePointBySegment(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    def Generate(self,koeficient,bySegment):
        return [TranslatedPointBySegmentForGeneration(koeficient,bySegment.GetParent(0),bySegment).id]
        
class GeneratePointByPlane(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    def Generate(self,position,byPlane):
        return [PointByPlane(position,byPlane).id]
 



class GenerateSegment(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    def Generate(self,positionA = None,positionB = None):
        listOfIds = []
        
        if positionA == None :
            positionA = vector((0.2,0,0)) + self.TranslaterVector 
        if positionB == None :
            positionB = vector((0,0.2,0)) + self.TranslaterVector
        
        A = Point(positionA)
        B = Point(positionB)
        AB = Segment(A,B)
        listOfIds.append(A.id)
        listOfIds.append(B.id)
        listOfIds.append(AB.id)
        self.updateNewPosition()
        return listOfIds
            
class GenerateTriangle(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    def Generate(self,positionA = None,positionB = None,positionC = None):
        listOfIds = []
        
        if positionA == None :
            positionA = vector((0.6,0.5,0)) + self.TranslaterVector 
        if positionB == None :
            positionB = vector((0,0.5,0.6)) + self.TranslaterVector
        if positionC == None :
            positionC = vector((0.6,0,0)) + self.TranslaterVector
        
        A = Point(positionA)
        B = Point(positionB)
        C = Point(positionC)
        AB = Segment(A,B)
        BC = Segment(B,C)
        CA = Segment(C,A)
        ABC = Plane(A,B,C)
        
        listOfIds.append(A.id)
        listOfIds.append(B.id)
        listOfIds.append(C.id)
        listOfIds.append(AB.id)
        listOfIds.append(BC.id)
        listOfIds.append(CA.id)
        listOfIds.append(ABC.id)
        self.updateNewPosition()
        return listOfIds
    
class GeneratePyramid(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    
    def updateNewPosition(self):
        self.TranslaterVector += vector((0.3,0.3,0.3))
    
    def Generate(self,positionA = None,positionB = None,positionC = None,positionD = None):
        listOfIds = []
        
        if positionA == None :
            positionA = vector((0.7,0,0.7)) + self.TranslaterVector 
        if positionB == None :
            positionB = vector((0.7,0.7,0)) + self.TranslaterVector
        if positionC == None :
            positionC = vector((0,0.7,0.7)) + self.TranslaterVector
        if positionD == None :
            positionD = vector((0.2,0.2,0.2)) + self.TranslaterVector
        
        
        A = Point(positionA)
        B = Point(positionB)
        C = Point(positionC)
        D = Point(positionD)
        AB = Segment(A,B)
        BC = Segment(B,C)
        CA = Segment(C,A)
        AD = Segment(A,D)
        BD = Segment(B,D)
        CD = Segment(C,D)
        
        listOfIds.append(A.id)
        listOfIds.append(B.id)
        listOfIds.append(C.id)
        listOfIds.append(D.id)
        listOfIds.append(AB.id)
        listOfIds.append(BC.id)
        listOfIds.append(CA.id)
        listOfIds.append(AD.id)
        listOfIds.append(BD.id)
        listOfIds.append(CD.id)
        self.updateNewPosition()
        return listOfIds


class GenerateNthPyramid(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    
    def updateNewPosition(self):
        self.TranslaterVector += vector((0.3,0.3,0.3))
    
    def Generate(self,Nth=4):
        listOfIds = []
        
        
        PointsList = []
        if(Nth-1>0.001):
            A = Point(vector(0,0,2)+ self.TranslaterVector)
            B = Point(vector(1,0,0)+ self.TranslaterVector)
            O = Point(vector(0,0,0)+ self.TranslaterVector)
            listOfIds.append(A.id)
            listOfIds.append(B.id)
            #listOfIds.append(O.id)
            PointsList.append(B)
            angle = 2*pi/Nth
            for i in range(Nth-1):
                angle1 = (i+1)*angle
                C = RotatedPointByAngle(angle1,A,O,B)
                C.Free()
                
                PointsList.append(C)
                listOfIds.append(C.id)
            self.updateNewPosition()
            
            for i in range(0,Nth):
                listOfIds.append(Segment(PointsList[i],PointsList[(i+1)%Nth]).id)
                listOfIds.append(Segment(PointsList[i],A).id)
            
            O.ChangeVisible(False)
            O.Delete()
                
        return listOfIds
            
class GeneratePrizma(GenerateConstructions):
    def __init__(self):
        GenerateConstructions.__init__(self)
    
    def updateNewPosition(self):
        self.TranslaterVector += vector((0.4,0.4,0.4))
    
    def Generate(self,positionA = None,positionB = None,positionC = None,positionC1 = None):
        listOfIds = []
        
        if positionA == None :
            positionA = vector((0.5,0,-0.5)) + self.TranslaterVector 
        if positionB == None :
            positionB = vector((-0.4,0.5,0)) + self.TranslaterVector
        if positionC == None :
            positionC = vector((0,-0.4,0.5)) + self.TranslaterVector
        if positionC1 == None :
            positionC1 = vector((0.2,0.6,-0.2)) + self.TranslaterVector
        
        
        A = Point(positionA)
        B = Point(positionB)
        C = Point(positionC)
        A1 = Point(positionC1)
        AA1 = Segment(A,A1)
        
        B1 = TranslatedPointBySegmentForGeneration(1,B, AA1 )
        C1 = TranslatedPointBySegmentForGeneration(1,C, AA1 )
        AB = Segment(A,B)
        BC = Segment(B,C)
        CA = Segment(C,A)
        A1B1 = Segment(A1,B1)
        B1C1 = Segment(B1,C1)
        C1A1 = Segment(C1,A1)
        BB1= Segment(B,B1)
        CC1= Segment(C,C1)
        
        listOfIds.append(A.id)
        listOfIds.append(B.id)
        listOfIds.append(C.id)
        listOfIds.append(A1.id)
        listOfIds.append(AA1.id)
        listOfIds.append(B1.id)
        listOfIds.append(C1.id)
        listOfIds.append(AB.id)
        listOfIds.append(BC.id)
        listOfIds.append(CA.id)
        listOfIds.append(A1B1.id)
        listOfIds.append(B1C1.id)
        listOfIds.append(C1A1.id)
        listOfIds.append(BB1.id)
        listOfIds.append(CC1.id)
        self.updateNewPosition()
        return listOfIds
            
            
            
    
#generate Nsten->Free method za tochkite        
###################################################
#-----------------Generation API------------------
################################################ 
class Generator:
    
    pointByPos = GeneratePoint()
    pointBySegment = GeneratePointBySegment()
    pointByPlane = GeneratePointByPlane()
    segmentsByPos = GenerateSegment()
    triangleByPos = GenerateTriangle()
    pyramidByPos = GeneratePyramid()
    prizmaByPos = GeneratePrizma()
    pyramidNth = GenerateNthPyramid()
    @staticmethod  
    def _Generate(generationName,*elementsToGenerateFrom):
        undoRedoListIds=[]
        undoRedoIds = generationName.Generate(*elementsToGenerateFrom)
        for id in undoRedoIds:
            undoRedoListIds.append(id)
        if len(undoRedoListIds)>0:               
            UndoRedoManager.PushToUndoStack(CreateUndoRedo(undoRedoListIds))
            #undoStack.push((undoRedoListIds,1))
    
    @staticmethod    
    def CreatePointByPosition(*elementsToGenerateFrom):
        Generator._Generate(Generator.pointByPos, *elementsToGenerateFrom)    
    
    @staticmethod    
    def CreatePointBySegment(*elementsToGenerateFrom):
        Generator._Generate(Generator.pointBySegment, *elementsToGenerateFrom)
    
    @staticmethod    
    def CreatePointByPlane(*elementsToGenerateFrom):
        Generator._Generate(Generator.pointByPlane, *elementsToGenerateFrom)
    
    @staticmethod    
    def CreateSegmentByPositions(*elementsToGenerateFrom):
        Generator._Generate(Generator.segmentsByPos, *elementsToGenerateFrom)    
    
    @staticmethod    
    def CreateTriangleByPositions(*elementsToGenerateFrom):
        Generator._Generate(Generator.triangleByPos, *elementsToGenerateFrom)
        
    @staticmethod    
    def CreatePyramidByPositions(*elementsToGenerateFrom):
        Generator._Generate(Generator.pyramidByPos, *elementsToGenerateFrom)    
    
    @staticmethod    
    def CreatePryzmaByPositions(*elementsToGenerateFrom):
        Generator._Generate(Generator.prizmaByPos, *elementsToGenerateFrom)    
    
    @staticmethod    
    def CreateNthPyramid(*elementsToGenerateFrom):
        Generator._Generate(Generator.pyramidNth, *elementsToGenerateFrom)

class SceneHelper:
    
    defaultProjectionVector = scene.forward
    
    workingProjectVector = scene.forward 
    #projectVectorByPlane = scene.forward
    
    projectionVector = scene.forward
    projectionPoint = vector(0,0,0)
    #isSetProjectionPlane = False
    
    speedOfMovement = 0.1
    defautCenter = vector(0,0,0)
    
    @staticmethod
    def MoveCenter(vectorToMoveWith,isPlus):
        if(isPlus):
            scene.center = scene.center+SceneHelper.speedOfMovement*vectorToMoveWith
        else:
            scene.center = scene.center-SceneHelper.speedOfMovement*vectorToMoveWith
    
    @staticmethod
    def RestoreCenter():
        scene.center = SceneHelper.defautCenter
    
    
    
    
          
    
    @staticmethod
    def setProjectionVector(vector):
        SceneHelper.projectionVector = vector
        
       
        #isSetProjectionPlane = True
        
    @staticmethod
    def setProjectionVectorByPerpVector(vectorToProject):
#        print 'Before, SceneHelper.projectionVector ',SceneHelper.projectionVector
#        oy = vector(0,1,0)
#        SceneHelper.projectionVector = vector(0,0,1)
#        if(mag(vectorToProject.cross(oy))>0.001):
#            SceneHelper.projectionVector = cross(vectorToProject,oy)
#        print 'After, SceneHelper.projectionVector ',SceneHelper.projectionVector
        candidateForProjectVect=scene.forward.proj(vectorToProject)-scene.forward
        if mag(candidateForProjectVect.cross(scene.up))<0.001:
            SceneHelper.projectionVector =vector.rotate(candidateForProjectVect,0.1,vectorToProject.cross(scene.forward)) 
        SceneHelper.projectionVector = candidateForProjectVect
    
    @staticmethod
    def setNewForwardVectorA(vectorAB,isForLine = True,angleLimit = pi/3.0):
        if(mag(vectorAB.cross(scene.forward))<0.001):
         #   print 'see the vectorAB parallel with scene.forward'
            scene.forward = vector(scene.forward.x+0.1,scene.forward.y,scene.forward.z)
            
        dotProduct = vectorAB.dot(scene.forward)
        notRightAgnle = (abs(dotProduct) >cos(angleLimit)*mag(vectorAB)*mag(scene.forward))
        if isForLine == False:
            notRightAgnle = (abs(dotProduct) <cos(angleLimit)*mag(vectorAB)*mag(scene.forward))
        if notRightAgnle:
            angleStartWith = acos(dotProduct/(mag(vectorAB)*mag(scene.forward)))
            if(dotProduct<0):
                vectorAB = - vectorAB
                angleStartWith = pi - angleStartWith
            
            osRotation = vectorAB.cross(scene.forward)
            increasedBy = 0.1
            if isForLine == False:
                increasedBy = -0.1
                while (angleStartWith > angleLimit):
                    vectorChecker = vector.rotate(scene.forward,increasedBy,osRotation)
                    if(vectorChecker== scene.up):
                        vectorChecker = vector.rotate(scene.forward,increasedBy,osRotation)
                    scene.forward = vectorChecker
                    angleStartWith+=increasedBy
                    time.sleep(0.1) 
                #angleStartWith *=-1
                #angleLimit *=-1
            else:
                while (angleStartWith < angleLimit):
                    scene.forward = vector.rotate(scene.forward,increasedBy,osRotation)
                    angleStartWith+=increasedBy
                    time.sleep(0.1) 
            
    
           
class ChangePointNameDialog(Dialog):
    def body(self, master):
        self.labelName = Label(master,text="Name : ",width = 6)
        self.entry = Entry(master, text="", textvariable=Man3dCommand.newNameVar)
        #self.ShowLabelButton8 = Button(master,text='ChangeName',command=Man3dCommand.ChangeNames3DObject,width = 11)
        self.labelName.grid(row = 0,column=0,columnspan = 2, sticky = E+W)
        self.entry.grid(row = 0,column=2,columnspan = 2, sticky = E+W)
        #self.ShowLabelButton8.grid(row = 0,column=4,columnspan = 2, sticky = E+W)
        return self.entry # initial focus

    def apply(self):
        print "Operation Changing name - finish :)"
    
    def changeNameReturn(self,event = None):
        Man3dCommand.ChangeNames3DObject()
        
    
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="Change Name", width=13, command=Man3dCommand.ChangeNames3DObject, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        #self.bind("<Return>", self.ok)
        self.bind("<Return>", self.changeNameReturn)
        self.bind("<Escape>", self.cancel)

        box.pack()
        
    
        
class CreatePointDialog(Dialog):
    def body(self, master):
         
        labelX = Label(master,text="x=",width = 4)#,width = 4 )
        entry1 = Entry(master, textvariable=Man3dCommand.X1,width = 4)
        labelY = Label(master,text="y=",width = 4)#,width = 4 )
        entry2 = Entry(master, textvariable=Man3dCommand.Y1,width = 4)
        labelZ = Label(master,text="z=",width = 4)#,width = 4 )
        entry3 = Entry(master, textvariable=Man3dCommand.Z1,width = 4)
        
        labelX.grid(row = 0,column=0, sticky = E+W)
        entry1.grid(row = 0,column=1, sticky = E+W)
        labelY.grid(row = 0,column=2, sticky = E+W)
        entry2.grid(row = 0,column=3, sticky = E+W)
        labelZ.grid(row = 0,column=4, sticky = E+W)
        entry3.grid(row = 0,column=5, sticky = E+W)
        #frameInputPos.grid(row = rowA,column=0,columnspan = 2, sticky = E+W)
        #CreatePoint = Button(master,text='Create New Point',command=Man3dCommand.CreateNewPoint,width = 15)
        #CreatePoint.grid(row = 0,column=6,columnspan = 2, sticky = E+W)
        return entry1 # initial focus
    
    def CreateNewPointReturn(self,event=None):
        Man3dCommand.CreateNewPoint()
    
    def apply(self):
        print "Operation Creation points - finish :)"
        
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text='Create New Point', width=15, command=Man3dCommand.CreateNewPoint, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        #self.bind("<Return>", self.ok)
        self.bind("<Return>", self.CreateNewPointReturn)
        self.bind("<Escape>", self.cancel)
        box.pack()

class CreateNPyramideDialog(Dialog):
    def body(self, master):
         
        NumberX = Label(master,text="Number Of Vertex=",width = 16)#,width = 4 )
        entry1 = Entry(master, textvariable=Man3dCommand.VertexNumber,width = 4)
       
        NumberX.grid(row = 0,column=0, sticky = E+W)
        entry1.grid(row = 0,column=1, sticky = E+W)
        
        #frameInputPos.grid(row = rowA,column=0,columnspan = 2, sticky = E+W)
        #CreatePoint = Button(master,text='Create New Pyramide',command=Man3dCommand.CreateNPyramideOperation,width = 19)
        #CreatePoint.grid(row = 0,column=6,columnspan = 2, sticky = E+W)
        return entry1 # initial focus

    def apply(self):
        print "Operation Creation Pyramide - finish :)"
    
    def CreateNPyramideOperationReturn(self,event=None):
        Man3dCommand.CreateNPyramideOperation()
        
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w1 = Button(box, text='Create New Pyramide', width=19, command=Man3dCommand.CreateNPyramideOperation, default=ACTIVE)
        w1.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.CreateNPyramideOperationReturn)
        self.bind("<Escape>", self.cancel)
        box.pack()

class Man3dCommand():
    
    @staticmethod
    def CalculateLengthOfSemgnetsCommand():
        MeasurementHelper.LengthOfSegments(selected3DObject)

    @staticmethod
    def CalculateAreaOfPlanesCommand():
        MeasurementHelper.AreaOfPlanes(selected3DObject)
    
    @staticmethod
    def ChangeNameCommand():
        dialog1 = ChangePointNameDialog(Man3dCommand.rootWindow)
    
    @staticmethod
    def CreatePointCommand():
        dialog1 = CreatePointDialog(Man3dCommand.rootWindow)
    
    @staticmethod
    def CreateNPyramideCommand():
        cr = CreateNPyramideDialog(Man3dCommand.rootWindow)
    
    @staticmethod
    def ChangeNames3DObject():
        #print 'you are in t'
        if len(selected3DObject)==1:
            newName = Man3dCommand.newNameVar.get()
            if(newName != None and newName != "" and newName != selected3DObject[0].name):                               
                selected3DObject[0].setName(newName)
                print "new Name : ", newName
                LabelHelper.ShowLabels()               
            else:
                print "No change, Set appropriate name, please :)"                
        else:
            print  "Select One Element"
            
        selected3DObject.freeSelectedObjects()
     
    @staticmethod
    def CreateNewPoint():
        print "Creating New Elements"
        #print "pos:(+",str(Man3dCommand.X1.get()),str(Man3dCommand.Y1.get()),str(Man3dCommand.Z1.get()),")"
        canMakePoint = True
        try:
            x1= Man3dCommand.X1.get()
            y1= Man3dCommand.Y1.get()
            z1= Man3dCommand.Z1.get()
            
        except ValueError:
            print "please, write all coordinate in format X.XXX"            
            Man3dCommand.X1.set(0.0)           
            Man3dCommand.Y1.set(0.0)
            Man3dCommand.Z1.set(0.0)
            canMakePoint = False
            return  
        
        if(canMakePoint):
            vectorPos = vector(x1,y1,z1)            
#            for pointsPos in [elem.pos for elem in Object3DDictionary.values() if(elem.visible and issubclass(type(elem),Point))]:
#                if(mag(vectorPos - pointsPos)<0.01):
#                    canMakePoint = False
                       
            
        if(canMakePoint and Object3DHelper.isPointExist(vectorPos)):
            Generator.CreatePointByPosition(vectorPos)
        else:
            print "Sorry, This point exist"
    @staticmethod
    def CreateNPyramideOperation():     
        try:                
            countNumberOfVertex = int(Man3dCommand.VertexNumber.get())
            
        except ValueError:
            print "Please, write number like 1,2,4,5,"
            return
        if(countNumberOfVertex>2 and countNumberOfVertex<25):
            Generator.CreateNthPyramid(int(countNumberOfVertex))
            
        else:
            print "Please, write number bigger than 2 and less than 25"
            Man3dCommand.VertexNumber.set(3)
    
    @staticmethod
    def CreatePointByDefaultCommand():
        Generator.CreatePointByPosition()
    
    @staticmethod
    def CreateSegmentByDefaultCommand():
        Generator.CreateSegmentByPositions()
    
    @staticmethod
    def CreatePlaneByDefaultCommand():
        Generator.CreateTriangleByPositions()
        
    @staticmethod
    def CreatePyramidByDefaultCommand():
        Generator.CreateNthPyramid()
    
    @staticmethod
    def CreatePryzmByDefaultCommand():
        Generator.CreatePryzmaByPositions()
        
    
    
    
    @staticmethod
    def SetForwardVectorFromRadioButtonCommand():
        CoordinatePlanesXYZ.coordinatePlane.HideLabels()
        
        if Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==1:            
            CoordinatePlanesXYZ.isXYvisible = True
            CoordinatePlanesXYZ.isXZvisible =True
            CoordinatePlanesXYZ.isYZvisible = True
            CoordinatePlanesXYZ.ChangeCoordinateSystemVisibility(False)
            scene.userspin = 1
            SceneHelper.workingProjectVector = SceneHelper.defaultProjectionVector
            CoordinatePlanesXYZ.coordinatePlane.SetLabels() 
            
        else:
            scene.userspin = 0
            if Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==2:
                CoordinatePlanesXYZ.isXYvisible = False
                CoordinatePlanesXYZ.isXZvisible =False
                CoordinatePlanesXYZ.isYZvisible = True
                CoordinatePlanesXYZ.ChangeCoordinateSystemVisibility(False)
                SceneHelper.setNewForwardVectorA(vector(1,0,0),False,0.01)                 
                SceneHelper.workingProjectVector = vector(1,0,0)
                CoordinatePlanesXYZ.coordinatePlane.SetLabels()
                
            elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==3:
                CoordinatePlanesXYZ.isXYvisible = False
                CoordinatePlanesXYZ.isXZvisible =True
                CoordinatePlanesXYZ.isYZvisible = False
                CoordinatePlanesXYZ.ChangeCoordinateSystemVisibility(False)
                SceneHelper.setNewForwardVectorA(vector(0,1,0),False,0.01)            
                SceneHelper.workingProjectVector = vector(0,1,0)
                CoordinatePlanesXYZ.coordinatePlane.SetLabels()
                
            elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==4:
                CoordinatePlanesXYZ.isXYvisible = True
                CoordinatePlanesXYZ.isXZvisible =False
                CoordinatePlanesXYZ.isYZvisible = False
                CoordinatePlanesXYZ.ChangeCoordinateSystemVisibility(False)
                SceneHelper.setNewForwardVectorA(vector(0,0,1),False,0.01)                
                SceneHelper.workingProjectVector = vector(0,0,1)
                CoordinatePlanesXYZ.coordinatePlane.SetLabels()
            
                
            
                
            
    
    @staticmethod
    def ShowAllSpecialElementsCommand():
        print "All special elements For Transformation:)"
        if(SpecialElementsForTransformation.GetRotatedSegmentOs()!=None):                                           
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetRotatedSegmentOs(), "Rotation OS" + str(SpecialElementsForTransformation.GetRotateAngle())) 
                   
        if(SpecialElementsForTransformation.GetTranslateVector()!=None):                       
            TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.red, "translated vector "+str(SpecialElementsForTransformation.GetTranslateVector()))
        
        if(SpecialElementsForTransformation.GetProjectionSegment()!=None):
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetProjectionSegment(), "Projection Line" )
        
        if(SpecialElementsForTransformation.GetHomoteticCenter()!=None):
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"homothetic Center, coefficent: "+str(SpecialElementsForTransformation.GetHomoteticCoefficient()))
        
        if(SpecialElementsForTransformation.GetHomoteticCenter()!=None):                        
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Symetric Center")
        
        if(SpecialElementsForTransformation.GetSymetricSegmentOs()!=None): 
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetSymetricSegmentOs(),"Symetric Os")
        
        if(SpecialElementsForTransformation.GetParallelSegment()!=None):                 
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetParallelSegment(),"Parallel Segment")#+str(SpecialElementsForTransformation.GetIsPlusDirection()))
        
        if(SpecialElementsForTransformation.GetProportionPoint()!=None):                        
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetProportionPoint(),"Proportion : "+str(SpecialElementsForTransformation.GetProportionPoint().prop))
            
        if(SpecialElementsForTransformation.GetPlaneToProject()!=None):                        
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane ")
            
    @staticmethod
    def ShowOrHideLabelsCommand():
        if not LabelHelper.showLabels:
            LabelHelper.showLabels =True
            LabelHelper.ShowLabels()#Object3DDictionary.values())
            
            #[obj.ShowLabel() for obj in selected3DObject ]
        else:
            LabelHelper.showLabels =False
            LabelHelper.HideLabels()#Object3DDictionary.values())
     
    @staticmethod
    def CountInfoObjectCommand():
        Object3DHelper.PrintSpecialInformation()   
#        print "count Selected Objects"+str(len(selected3DObject))
#        print "count visible 3D Object" +str(len([x for x in Object3DDictionary.values() if x.visible == True])) 
#        print "count all 3D Object" +str(len(Object3DDictionary.values()))
    
    @staticmethod
    def ShowAllElementsCommand():   
        TwinkerHelper.TwinkeElements( "All 3D Objects")
     
    @staticmethod
    def ShowDragableElementsCommand():    
        TwinkerHelper.TwinkeElements( "Dragable Points", isDragable = True)
    
    @staticmethod
    def ShowFreeElementsCommand(): 
        TwinkerHelper.TwinkeElements( "Free 3D Objects",isFree = True)
    
    @staticmethod
    def SelectAllElementsCommand():
        Object3DHelper.SelectAll(selected3DObject)

    
    @staticmethod
    def ShowCoordinateSystemCommand(changevisibility = True):
        if(CoordinatePlanesXYZ.coordinatePlane==None):
            CoordinatePlanesXYZ.coordinatePlane = CoordinatePlanesXYZ(4)                    
        CoordinatePlanesXYZ.ChangeCoordinateSystemVisibility(changevisibility)
    
    @staticmethod
    def UndoCommand():
        if UndoRedoManager.checkRedoStack():
            UndoRedoManager.Undo()
            if LabelHelper.showLabels:
                LabelHelper.ShowLabels()#Object3DDictionary.values())

    
    @staticmethod
    def RedoCommand():                   
#                elif ss == 'ctrl+y':  # make midpoint
        if UndoRedoManager.checkUndoStack(): 
            UndoRedoManager.Redo()
            if LabelHelper.showLabels:
                LabelHelper.ShowLabels()#Object3DDictionary.values())
    @staticmethod
    def ClearUndoRedoStackCommand():            

        UndoRedoManager.Clear()
    
    
    #--------FILE MENU
    
    
    
    myFormats = [
            ('MAN 3d','*.man')
            ]
    @staticmethod
    def NewObjectCommand():
        directory = askdirectory()
        print directory
        newName = askstring("Enter file name(not starting with .)", "File name:")
        print os.getcwd()
###        print [stri[:-4] for stri in os.listdir(os.getcwdu()) if stri[-4:]=='.man']
###        if len(newName)>0 and newName[0]!='.':
###            if newName in [stri[:-4] for stri in os.listdir(os.getcwdu()) if stri[-4:]=='.man']:
###                print 'there is such a name ,choose another'
###            else:
###                Man3dCommand.nameOfFile = newName
###                print 'your working file name is:',Man3dCommand.nameOfFile
        if len(newName)>0 and newName[0]!='.':
            if newName in [stri[:-4] for stri in os.listdir(directory) if stri[-4:]=='.man']:
                print 'there is such a name ,choose another'
            else:
                Man3dCommand.nameOfFile = directory+'/'+newName
                print 'your working file name is:',Man3dCommand.nameOfFile
        else:
            print 'file name should not starting with . or .. and should not be empty)'
    
    
    @staticmethod
    def SaveObjectsCommand():
        
        if Man3dCommand.nameOfFile != None:
            
            if(LoadSaveHelper.SaveObjects(Man3dCommand.nameOfFile)):
                UndoRedoManager.Clear()
                print 'successful save the file in ',Man3dCommand.nameOfFile
        else:
            print 'select New,Open or Save As  ,then you can save the objects in choosed file name'
    
    
        
    @staticmethod
    def CloseProjectCommand():
        Man3dCommand.nameOfFile = None
        LabelHelper.showLabels =False
        LabelHelper.HideLabels()
        Object3DHelper.DeleteAll()
        
    
    @staticmethod    
    def SaveAndCloseProjectCommand():
        if Man3dCommand.nameOfFile != None:
            if(LoadSaveHelper.SaveObjects(Man3dCommand.nameOfFile)):
                print 'successful save the file in ',Man3dCommand.nameOfFile
                Man3dCommand.CloseProjectCommand()
                
        else:
            print 'select New,Open or Save As  ,then you can save the objects in choosed file name'
                    
            
             
    
    @staticmethod
    def OpenObjectsCommand():
        if Man3dCommand.nameOfFile == None:
            file = tkFileDialog.askopenfile(parent=root,mode='rb',filetypes=Man3dCommand.myFormats,title='Choose a file')
            if file != None :
                if LoadSaveHelper.Open(file.name):
                    Man3dCommand.nameOfFile = file.name[:-4]#without man
                    print 'successful setting working file name',file.name
        else:
            print 'close the working task first'  
                
    
    @staticmethod
    def ExitMan3dCommand():
        root.destroy()
        scene.visible = False
        
    @staticmethod
    def LoadMan3dCommand():

        file = tkFileDialog.askopenfile(parent=root,filetypes=Man3dCommand.myFormats,mode='rb',title='Choose a file')
       
        if file != None :
            
            LoadSaveHelper.Open(file.name)

    @staticmethod
    def SaveAsMan3dCommand():

        fileName = tkFileDialog.asksaveasfilename(parent=root,filetypes=Man3dCommand.myFormats ,title="Save the file as...")
        if len(fileName ) > 0:
            if len(fileName)>3 and fileName[-4:]=='.man':
                fileName =fileName[:-4]
            Man3dCommand.nameOfFile=fileName
            if(LoadSaveHelper.SaveObjects(Man3dCommand.nameOfFile)):
                UndoRedoManager.Clear()
                print 'successful save the file in ',Man3dCommand.nameOfFile
            
            print fileName

        
          
    #------End File Menu
    
    @staticmethod
    def OyPlusCommand():
        SceneHelper.MoveCenter(vector(0,1,0), True)
    
    @staticmethod
    def OyMinusCommand():
        SceneHelper.MoveCenter(vector(0,1,0), False)
    
    @staticmethod
    def OxPlusCommand():
        SceneHelper.MoveCenter(vector(1,0,0), True)
    
    @staticmethod
    def OxMinusCommand():
        SceneHelper.MoveCenter(vector(1,0,0), False)
    
    @staticmethod
    def OzPlusCommand():
        SceneHelper.MoveCenter(vector(0,0,1), True)
    
    @staticmethod
    def OzMinusCommand():
        SceneHelper.MoveCenter(vector(0,0,1), False)
        
    @staticmethod
    def O_0_0Command():
        SceneHelper.RestoreCenter()
    
        
        
#    if ss == 'up':
#                    SceneHelper.MoveCenter(vector(0,1,0), True)
                    
#                if ss == 'down':
#                    SceneHelper.MoveCenter(vector(0,1,0), False)
#                    
#                if ss == 'left':
#                    SceneHelper.MoveCenter(vector(1,0,0), False)
#
#                if ss == 'right':
#                    SceneHelper.MoveCenter(vector(1,0,0), True)
#                
#                if ss == '+':                    
#                    SceneHelper.MoveCenter(vector(0,0,1), True)                    
#                
#                if ss == '-':
#                    SceneHelper.MoveCenter(vector(0,0,1), False)
#                
#                if ss == '*':
#                    SceneHelper.RestoreCenter()
    
    @staticmethod
    def BisectorPointOperation():
        Creator.MakeBisectorPoint(selected3DObject)
        selected3DObject.freeSelectedObjects()
    
    @staticmethod
    def PlaneOperation():
        Creator.MakePlane(selected3DObject)
        selected3DObject.freeSelectedObjects()
    
    @staticmethod
    def SegmentOperation():
        Creator.MakeSegment(selected3DObject)
        selected3DObject.freeSelectedObjects()
        
    @staticmethod
    def CrossTwoSegmentsOperation():
        Creator.MakeCrossPoint(selected3DObject)
        selected3DObject.freeSelectedObjects()
    
    @staticmethod
    def SetProportionPoint():
        if(SpecialElementsForTransformation.GetProportionPoint()==None):
            if selected3DObject.isPointInIndex(0) and issubclass(type(selected3DObject[0]),ProportionalPoint):#len(selected3DLines)==1 :
                
                SpecialElementsForTransformation.SetProportionPoint(selected3DObject[0])
                TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetProportionPoint(),"Proportion : "+str(SpecialElementsForTransformation.GetProportionPoint().prop))
                print 'successful setting of proportion Point'
            else:    
                print 'select proportion point'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetProportionPoint(),"Proportion : "+str(SpecialElementsForTransformation.GetProportionPoint().prop))
    @staticmethod
    def UnSetProportionPoint():
        SpecialElementsForTransformation.FreeProportionPoint()
    
    @staticmethod
    def ProportionPointOperation():
        if(SpecialElementsForTransformation.GetProportionPoint()!=None):
            TwinkerHelper.Twinkle(None, "Proportion: " +str(SpecialElementsForTransformation.GetProportionPoint()))
            if Man3dCommand.Point1Segment2.get()==1:
                Creator.MakeProportionPointByPointsAndProportionalPoint(selected3DObject)
            else :
                Creator.MakeProportionPointBySegmentsAndProportionalPoint(selected3DObject)
            selected3DObject.freeSelectedObjects()
        else:
            print 'set proporion point'
    
    
    @staticmethod
    def SetProportion():
        if(SpecialElementsForTransformation.GetProportion()==None):
            x_str = askstring("Please Insert Number (0,1)", "like X.XXXX format")
            if(is_number(x_str)):
                if 0<float(x_str)<1:
                    SpecialElementsForTransformation.SetProportion(float(x_str))
                    TwinkerHelper.Twinkle(None, "Proportion: " +str(SpecialElementsForTransformation.GetProportion()))
                    print 'successful set proportion'
                else :
                    print 'try again entering number between 0 and 1'
            else:
                print 'enter a number'
        else:
            TwinkerHelper.Twinkle(None, "Proportion: " +str(SpecialElementsForTransformation.GetProportion()))
    @staticmethod
    def UnSetProportion():
        SpecialElementsForTransformation.FreeProportion()
    
    @staticmethod
    def ProportionOperation():
        if(SpecialElementsForTransformation.GetProportion()!=None):
            TwinkerHelper.Twinkle(None, "Proportion: " +str(SpecialElementsForTransformation.GetProportion()))
            if Man3dCommand.Point1Segment2.get()==1:
                Creator.MakeProportionPointByPointsAndProportion(selected3DObject)
            else :
                Creator.MakeProportionPointBySegmentsAndProportion(selected3DObject)
            selected3DObject.freeSelectedObjects()
        else:
            print 'set proporion'
        
    @staticmethod
    def SetNothing():
        pass
    @staticmethod
    def UnsetNothing():
        pass
    
    @staticmethod
    def MiddlePointOperation():
        if Man3dCommand.Point1Segment2.get()==1:
            Creator.MakeMiddlePointsByPoints(selected3DObject)
        else :
            Creator.MakeMiddlePointsBySegments(selected3DObject)
        selected3DObject.freeSelectedObjects()
    @staticmethod
    def SetTranslatedVector():
        if(SpecialElementsForTransformation.GetTranslateVector()==None):
            if selected3DObject.isSegmentInIndex(0):#len(selected3DLines)==1 :
                vectorToTranslate = selected3DObject[0].axis
                SpecialElementsForTransformation.SetTranslateVector(vectorToTranslate)
                print 'successful setting of translate vector',selected3DObject[0].axis
                TwinkerHelper.TwinkleVector([selected3DObject[0]], color.red, "translated vector "+str(vectorToTranslate))
            elif selected3DObject.isPointInIndex(0) and selected3DObject.isPointInIndex(1):#len(selected3DPoints)==2:
                vectorToTranslate = selected3DObject[1].pos - selected3DObject[0].pos 
                SpecialElementsForTransformation.SetTranslateVector(vectorToTranslate)
                TwinkerHelper.TwinkleVector([selected3DObject[0],selected3DObject[1]], color.red, "translated vector "+str(vectorToTranslate))
                print 'successful setting of translate vector'
            else:
                x_str = askstring("Please Insert X", "like X.XXXX format")
                if(is_number(x_str)):
                    x = float(x_str)
                else:
                    x=None
                    
                y_str = askstring("Please Insert Y", "like Y.YYYY format")
                if(is_number(y_str)):
                    y = float(y_str)
                else:
                    y=None    
                
                z_str = askstring("Please Insert Z", "like Z.ZZZ format")
                if(is_number(z_str)):
                    z = float(z_str)
                else:
                    z=None
                #x = raw_input('x = ')
                if(x != None and y != None and z!= None):
                    vectorToTranslate = vector(x,y,z)
                    SpecialElementsForTransformation.SetTranslateVector(vectorToTranslate)
                    TwinkerHelper.TwinkleVector([vectorToTranslate], color.red, "translated vector "+str(vectorToTranslate))
                else:
                    print "Please set only numbers"                        
            selected3DObject.freeSelectedObjects()  
        else:
            TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.red, "translated vector "+str(SpecialElementsForTransformation.GetTranslateVector()))
            pass
    
    @staticmethod
    def UnSetTranslatedVector():
        SpecialElementsForTransformation.FreeTranslateVector()   
    
    @staticmethod   
    def TranslateOperation():
        if(SpecialElementsForTransformation.GetTranslateVector()!=None):
            if Man3dCommand.Move1Create2.get()==1:
                Transformer.Translate(selected3DObject)
                #Man3dCommand.TranslateTransform()
            else:
                Creator.MakeTranslation(selected3DObject)
        else:
            print 'set elements first'
                #Man3dCommand.TranslateCreation()
    
    
    @staticmethod    
    def SetHomotetia():
        if(SpecialElementsForTransformation.GetHomoteticCenter()==None):
            if selected3DObject.isPointInIndex(0):
                SpecialElementsForTransformation.SetHomoteticCenter(selected3DObject[0])
                if SpecialElementsForTransformation.GetHomoteticCoefficient()== None:       
                    coefficient = askstring("Please Insert Number", "HomoteticCoefficient")#raw_input('DelitationCoefficientX = ')
                    if is_number(coefficient):
                        SpecialElementsForTransformation.SetHomoteticCoefficient(float(coefficient))
                        print 'successful setting of homotetic coefficient:',SpecialElementsForTransformation.GetHomoteticCoefficient()
                    else:
                        print 'write number for Homotetic coefficient .You have to set it agian'
                if SpecialElementsForTransformation.GetHomoteticCoefficient()!= None:
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Homotetic Center, coefficent: "+str(SpecialElementsForTransformation.GetHomoteticCoefficient()))
                    print 'successful setting of Center and Homotetic Coefficient'
                
            else:
                print 'select point to make it center'
            selected3DObject.freeSelectedObjects()
        else:
            if SpecialElementsForTransformation.GetHomoteticCoefficient()== None:       
                    coefficient = askstring("Please Insert Number", "HomoteticCoefficient")#raw_input('DelitationCoefficientX = ')
                    if is_number(coefficient):
                        SpecialElementsForTransformation.SetHomoteticCoefficient(float(coefficient))
                        print 'successful setting of homotetic coefficient:',SpecialElementsForTransformation.GetHomoteticCoefficient()
                    else:
                        print 'write number for Homotetic coefficient .You have to set it agian'
            if SpecialElementsForTransformation.GetHomoteticCoefficient()!= None:
                TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Homotetic Center, coefficent: "+str(SpecialElementsForTransformation.GetHomoteticCoefficient()))
                print 'successful setting of Center and Homotetic Coefficient'
                    
    @staticmethod
    def UnSetHomotetia():
        SpecialElementsForTransformation.FreeHomoteticCenter()
        SpecialElementsForTransformation.FreeHomoteticCoefficient()
        
    @staticmethod   
    def HomotetiaOperation():
        if SpecialElementsForTransformation.GetHomoteticCenter()!=None and SpecialElementsForTransformation.GetHomoteticCoefficient()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetHomoteticCenter().isFree():
                    Transformer.HomotetiaByPoint(selected3DObject)
                    #Man3dCommand.DilitateTransform()
                else:
                    print 'choose free element,if you want to Move(homotetia) objects'
            else:
                Creator.MakeHomothetic(selected3DObject)
                #Man3dCommand.DilitateCreation()
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
       
    
    @staticmethod    
    def SetSymetria():
        if(SpecialElementsForTransformation.GetHomoteticCenter()==None):
            if selected3DObject.isPointInIndex(0):
                SpecialElementsForTransformation.SetHomoteticCenter(selected3DObject[0])
                TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Symetry Center")
                print 'successful setting of Center'
                
            else:
                print 'select point to make it Center'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Symetry Center")
            print 'successful setting of Center'
                    
    @staticmethod
    def UnSetSymetria():
        SpecialElementsForTransformation.FreeHomoteticCenter()
        
        
    @staticmethod   
    def SymetriaOperation():
        if SpecialElementsForTransformation.GetHomoteticCenter()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetHomoteticCenter().isFree():
                    Transformer.SymetricByCenter(selected3DObject)
                
                else:
                    print 'choose free element,if you want to Move(symetry) objects'
            else:
                Creator.MakeSymetric(selected3DObject)
                
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
            
    
#    elif ss == 'ctrl+w':
#                    if(SpecialElementsForTransformation.GetSymetricSegmentOs()==None):
#                        
#                        if selected3DObject.isSegmentInIndex(0):#len(selected3DLines)==1 :
#                            SpecialElementsForTransformation.SetSymetricSegmentOs(selected3DObject[0])
#                            TwinkerHelper.Twinkle(selected3DObject[0],"Symetric Os")
#                            print 'successful setting of symetric Segment'                            
#                            selected3DObject.freeSelectedObjects()
#                    else:
#                        TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetSymetricSegmentOs(),"Symetric Os")
#               
    
    @staticmethod    
    def SetSymetriaBySegment():
        if(SpecialElementsForTransformation.GetSymetricSegmentOs()==None):
            if selected3DObject.isSegmentInIndex(0):
                SpecialElementsForTransformation.SetSymetricSegmentOs(selected3DObject[0])
                TwinkerHelper.Twinkle(selected3DObject[0],"Symetric Os")
                print 'successful setting of symetric Segment' 
                
            else:
                print 'select segment to make it segment Os'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetSymetricSegmentOs(),"Symetric Os")
            print 'successful setting of symetric Segment' 
                    
    @staticmethod
    def UnSetSymetriaBySegment():
        SpecialElementsForTransformation.FreeSymetricSegmentOs()
    
    
    @staticmethod   
    def SymetriaOperationBySegment():
        if SpecialElementsForTransformation.GetSymetricSegmentOs()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetSymetricSegmentOs().isFree():
                    Transformer.SymetricByLine(selected3DObject)
                
                else:
                    print 'choose free element,if you want to Move(symetry) objects'
            else:
                Creator.MakeSymetricBySegment(selected3DObject)
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
        
    @staticmethod   
    def SymetriaOperationByPlane():
        if SpecialElementsForTransformation.GetPlaneToProject()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetPlaneToProject().isFree():
                    Transformer.SymetricByPlane(selected3DObject)
                
                else:
                    print 'choose free element,if you want to Move(symetry) objects'
            else:
                Creator.MakeSymetricByPlane(selected3DObject)
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
    
    
    
    @staticmethod    
    def SetSymetriaByPlane():
        if(SpecialElementsForTransformation.GetPlaneToProject()==None):
            if selected3DObject.isPlaneInIndex(0):
                SpecialElementsForTransformation.SetPlaneToProject(selected3DObject[0])
                TwinkerHelper.Twinkle(selected3DObject[0],"Symetric Plane")
                print 'successful setting of symetric Plane' 
                
            else:
                print 'select plane'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Symetric Plane")
            print 'successful setting of symetric Plane'
                    
    @staticmethod
    def UnSetSymetriaByPlane():
        SpecialElementsForTransformation.FreePlaneToProject()
        
    
    
    
    @staticmethod
    def CrossSegmentAndPlaneOperation():
        if SpecialElementsForTransformation.GetPlaneToProject()!=None:
            Creator.MakeIntersactionOfPlaneAndSegmentt(selected3DObject)
            selected3DObject.freeSelectedObjects()
        else:
            print 'set special element-plane first'
    
    @staticmethod    
    def SetCrossSegmentAndPlane():
        if(SpecialElementsForTransformation.GetPlaneToProject()==None):
            if selected3DObject.isPlaneInIndex(0):
                SpecialElementsForTransformation.SetPlaneToProject(selected3DObject[0])
                TwinkerHelper.Twinkle(selected3DObject[0],"Plane to cross with")
                print 'successful setting of Plane' 
                
            else:
                print 'select plane'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane to cross with")
            print 'successful setting of Plane'  
                    
    @staticmethod
    def UnSetCrossSegmentAndPlane():
        SpecialElementsForTransformation.FreePlaneToProject()
    
    @staticmethod   
    def OrthogonalProjectionOperationOnPlane():
        if SpecialElementsForTransformation.GetPlaneToProject()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetPlaneToProject().isFree():
                    Transformer.PrpendicularProjectToPlane(selected3DObject)
                
                else:
                    print 'choose free element,if you want to Move(orthogonal projection) objects'
            else:
                SpecialElementsForTransformation.SetShowProjectionDirection(Man3dCommand.Show1Hide0.get())
                Creator.MakePerpendicularProjectionOnPlane(selected3DObject)
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
    
    
    
    @staticmethod    
    def SetOrthogonalProjectionOnPlane():
        if(SpecialElementsForTransformation.GetPlaneToProject()==None):
            if selected3DObject.isPlaneInIndex(0):
                SpecialElementsForTransformation.SetPlaneToProject(selected3DObject[0])
                TwinkerHelper.Twinkle(selected3DObject[0],"Plane To Project")
                print 'successful setting of Plane' 
                
            else:
                print 'select plane'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane To Project")
            print 'successful set of Plane' 
                    
    @staticmethod
    def UnSetOrthogonalProjectionOnPlane():
        SpecialElementsForTransformation.FreePlaneToProject()
     
    
    
    
    @staticmethod   
    def SlidingImpactOperationByPlane():
        if SpecialElementsForTransformation.GetPlaneToProject()!=None and SpecialElementsForTransformation.GetTranslateVector()!= None :
            if abs(SpecialElementsForTransformation.GetTranslateVector().dot(SpecialElementsForTransformation.GetPlaneToProject().b))>0.001:
                if Man3dCommand.Move1Create2.get()==1:
                    if SpecialElementsForTransformation.GetPlaneToProject().isFree():
    #                    Transformer.SymetricByPlane(selected3DObject)
                        Transformer.SymetricByPlanePlusTranslateVector(selected3DObject)
                    else:
                        print 'choose free element,if you want to Move(sliding impact) objects'
                else:
                    Creator.MakeSymetricByPlaneAndTranslateVector(selected3DObject)
                    #Creator.MakeSymetricByPlane(selected3DObject)
                    selected3DObject.freeSelectedObjects()
            else:
                print 'Set Translated Vector not perpendicular on plane'
        else:
            print 'set elements first'
    
    
    
    @staticmethod    
    def SetSlidingImpactByPlane():
        if(SpecialElementsForTransformation.GetPlaneToProject()==None):
            if selected3DObject.isPlaneInIndex(0):
                SpecialElementsForTransformation.SetPlaneToProject(selected3DObject[0])
                if SpecialElementsForTransformation.GetTranslateVector()==None:
                    print 'Set Translated Vector First!'
                elif abs(SpecialElementsForTransformation.GetTranslateVector().dot(SpecialElementsForTransformation.GetPlaneToProject().b))<0.001:
                    TwinkerHelper.Twinkle(selected3DObject[0],"Symetric Plane")
                    TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'translate vector')
                    print 'Set Translated Vector not perpendicular on plane'
                else:
                    TwinkerHelper.Twinkle(selected3DObject[0],"Symetric Plane")
                    TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'translate vector')
                    print 'successful setting of symetric Plane and translated vector' 
                
            else:
                print 'select plane'
            selected3DObject.freeSelectedObjects()
        else:
            if SpecialElementsForTransformation.GetTranslateVector()==None:
                print 'Set Translated Vector First!'
            elif abs(SpecialElementsForTransformation.GetTranslateVector().dot(SpecialElementsForTransformation.GetPlaneToProject().b))<0.001:
                TwinkerHelper.Twinkle(selected3DObject[0],"Symetric Plane")
                TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'translate vector')
                print 'Set Translated Vector not perpendicular on plane'
            else:
                TwinkerHelper.Twinkle(selected3DObject[0],"Symetric Plane")
                TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'translate vector')
                print 'successful setted of symetric Plane and translated vector'  
                    
    @staticmethod
    def UnSetSlidingImpactByPlane():
        SpecialElementsForTransformation.FreePlaneToProject()
        SpecialElementsForTransformation.FreeTranslateVector()
    
    
    
    @staticmethod   
    def ProjectOnPlaneOperation():
        if SpecialElementsForTransformation.GetPlaneToProject()!=None and SpecialElementsForTransformation.GetTranslateVector()!= None :
            if abs(SpecialElementsForTransformation.GetTranslateVector().dot(SpecialElementsForTransformation.GetPlaneToProject().bxc))>0.001:
                if Man3dCommand.Move1Create2.get()==1:
                    if SpecialElementsForTransformation.GetPlaneToProject().isFree():
    #                    Transformer.SymetricByPlane(selected3DObject)
                        Transformer.ProjectToPlane(selected3DObject)
                    else:
                        print 'choose free element,if you want to Move(sliding impact) objects'
                else:
                    Creator.MakeProjectionOnPlane(selected3DObject)
                    #Creator.MakeSymetricByPlane(selected3DObject)
                    selected3DObject.freeSelectedObjects()
            else:
                print 'Set Vector not parallel to plane'
        else:
            print 'set elements first'
    
    
    
    @staticmethod    
    def SetProjectOnPlane():
        if(SpecialElementsForTransformation.GetPlaneToProject()==None):
            if selected3DObject.isPlaneInIndex(0):
                SpecialElementsForTransformation.SetPlaneToProject(selected3DObject[0])
                if SpecialElementsForTransformation.GetTranslateVector()==None:
                    print 'Set Vector!'
                elif abs(SpecialElementsForTransformation.GetTranslateVector().dot(SpecialElementsForTransformation.GetPlaneToProject().bxc))<0.001:
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane To Project")
                    TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'project vector')
                    print 'Set projection Vector not parallel on plane'
                else:
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane To Project")
                    TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'project vector')
                    print 'successful setting of Plane and projection vector' 
                
            else:
                print 'select plane'
            selected3DObject.freeSelectedObjects()
        else:
            if SpecialElementsForTransformation.GetTranslateVector()==None:
                    print 'Set Vector!'
            elif abs(SpecialElementsForTransformation.GetTranslateVector().dot(SpecialElementsForTransformation.GetPlaneToProject().bxc))<0.001:
                TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane To Project")
                TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'project vector')
                print 'Set Projection Vector not parallel on plane'
            else:
                TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetPlaneToProject(),"Plane To Project")
                TwinkerHelper.TwinkleVector([SpecialElementsForTransformation.GetTranslateVector()], color.blue,'project vector')
                print 'successful set of Plane and projection vector'   
                    
    @staticmethod
    def UnSetProjectOnPlane():
        SpecialElementsForTransformation.FreePlaneToProject()
        SpecialElementsForTransformation.FreeTranslateVector()    
  
    
    @staticmethod    
    def SetProjectionOnSegment():
        if(SpecialElementsForTransformation.GetProjectionSegment()==None):
            if selected3DObject.isSegmentInIndex(0):
                SpecialElementsForTransformation.SetProjectionSegment(selected3DObject[0])
                TwinkerHelper.Twinkle(selected3DObject[0],"Projection Segment")
                print 'successful setting of Projection Segment' 
                
            else:
                print 'select segment to make it segment Os'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetProjectionSegment(),"Symetric Os")
            print 'successful setting of Projection Segment' 
                    
    @staticmethod
    def UnSetProjectionOnSegment():
        SpecialElementsForTransformation.FreeProjectionSegment()
    
    
    @staticmethod   
    def ProjectionOnSegmentOperation():
        if SpecialElementsForTransformation.GetProjectionSegment()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetProjectionSegment().isFree():
                    Transformer.ProjectToSegment(selected3DObject)
                
                else:
                    print 'choose free element,if you want to Move(symetry) objects'
            else:
                SpecialElementsForTransformation.SetShowProjectionDirection(Man3dCommand.Show1Hide0.get())
                Creator.ProjectToLine(selected3DObject)
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
    
    
    
    @staticmethod
    def UnSetDilition():
        SpecialElementsForTransformation.FreeSymetricSegmentOs()
   
    @staticmethod    
    def SetDilatation():
        if(SpecialElementsForTransformation.GetHomoteticCenter()==None):
            if selected3DObject.isPointInIndex(0):
                SpecialElementsForTransformation.SetHomoteticCenter(selected3DObject[0])
                if SpecialElementsForTransformation.GetDelitationCoeficentX()== None:       
                    deletationX = askstring("Please Insert Number", "DelitationCoefficientX")#raw_input('DelitationCoefficientX = ')
                    if is_number(deletationX):
                        SpecialElementsForTransformation.SetDelitationCoeficentX(float(deletationX))
                        print 'successful setting of DelitationCoefficientX with coefficient:',SpecialElementsForTransformation.GetDelitationCoeficentX()
                    else:
                        print 'write number for DelitationCoefficientX .You have to set it agian'
                if SpecialElementsForTransformation.GetDelitationCoeficentY()== None:       
                    deletationY = askstring("Please Insert Number", "DelitationCoefficientY")#raw_input('DelitationCoefficientX = ')
                    if is_number(deletationY):
                        SpecialElementsForTransformation.SetDelitationCoeficentY(float(deletationY))
                        print 'successful setting of DelitationCoefficientY with coefficient:',SpecialElementsForTransformation.GetDelitationCoeficentY()
                    else:
                        print 'write number for DelitationCoefficientY .You have to set it agian'
                if SpecialElementsForTransformation.GetDelitationCoeficentZ()== None:       
                    deletationZ = askstring("Please Insert Number", "DelitationCoefficientZ")#raw_input('DelitationCoefficientX = ')
                    if is_number(deletationZ):
                        SpecialElementsForTransformation.SetDelitationCoeficentZ(float(deletationZ))
                        print 'successful setting of DelitationCoefficientZ with coefficient:',SpecialElementsForTransformation.GetDelitationCoeficentZ()
                    else:
                        print 'write number for DelitationCoefficientZ .You have to set it agian'
                if SpecialElementsForTransformation.GetHomoteticCenter()!=None and SpecialElementsForTransformation.GetDelitationCoeficentX()!= None and SpecialElementsForTransformation.GetDelitationCoeficentY()!= None and SpecialElementsForTransformation.GetDelitationCoeficentZ()!= None:
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Deletation Center, coefficent: "+"("+str(SpecialElementsForTransformation.GetDelitationCoeficentX())+str(SpecialElementsForTransformation.GetDelitationCoeficentY())+str(SpecialElementsForTransformation.GetDelitationCoeficentZ())+")")
                    print 'successful setting of Center and Dilitation Coefficients'
                
            else:
                print 'select point to make it center'
            selected3DObject.freeSelectedObjects()
        else:
            if SpecialElementsForTransformation.GetDelitationCoeficentX()== None:       
                    deletationX = askstring("Please Insert Number", "DelitationCoefficientX")#raw_input('DelitationCoefficientX = ')
                    if is_number(deletationX):
                        SpecialElementsForTransformation.SetDelitationCoeficentX(float(deletationX))
                        print 'successful setting of DelitationCoefficientX with coefficient:',SpecialElementsForTransformation.GetDelitationCoeficentX()
                    else:
                        print 'write number for DelitationCoefficientX .You have to set it agian'
            if SpecialElementsForTransformation.GetDelitationCoeficentY()== None:       
                deletationY = askstring("Please Insert Number", "DelitationCoefficientY")#raw_input('DelitationCoefficientX = ')
                if is_number(deletationY):
                    SpecialElementsForTransformation.SetDelitationCoeficentY(float(deletationY))
                    print 'successful setting of DelitationCoefficientY with coefficient:',SpecialElementsForTransformation.GetDelitationCoeficentY()
                else:
                    print 'write number for DelitationCoefficientY .You have to set it agian'
            if SpecialElementsForTransformation.GetDelitationCoeficentZ()== None:       
                deletationZ = askstring("Please Insert Number", "DelitationCoefficientZ")#raw_input('DelitationCoefficientX = ')
                if is_number(deletationZ):
                    SpecialElementsForTransformation.SetDelitationCoeficentZ(float(deletationZ))
                    print 'successful setting of DelitationCoefficientZ with coefficient:',SpecialElementsForTransformation.GetDelitationCoeficentZ()
                else:
                    print 'write number for DelitationCoefficientZ .You have to set it agian'
            if SpecialElementsForTransformation.GetHomoteticCenter()!=None and SpecialElementsForTransformation.GetDelitationCoeficentX()!= None and SpecialElementsForTransformation.GetDelitationCoeficentY()!= None and SpecialElementsForTransformation.GetDelitationCoeficentZ()!= None:
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetHomoteticCenter(),"Deletation Center, coefficent: "+"("+str(SpecialElementsForTransformation.GetDelitationCoeficentX())+str(SpecialElementsForTransformation.GetDelitationCoeficentY())+str(SpecialElementsForTransformation.GetDelitationCoeficentZ())+")")
    
                    print 'successful setting of Center and Dilitation Coefficients'       
    
    
    


    @staticmethod   
    def DilitateOperation():
        if SpecialElementsForTransformation.GetHomoteticCenter()!=None and SpecialElementsForTransformation.GetDelitationCoeficentX()!=None and SpecialElementsForTransformation.GetDelitationCoeficentY()!=None and SpecialElementsForTransformation.GetDelitationCoeficentZ()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetHomoteticCenter().isFree():
                    Transformer.DelitationByPoins(selected3DObject)
                    #Man3dCommand.DilitateTransform()
                else:
                    print 'choose free element,if you want to Move(dilitate) objects'
            else:
                Creator.MakeDelitatic(selected3DObject)
                #Man3dCommand.DilitateCreation()
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
    
    
    @staticmethod
    def SetScrewMotion():
        
        if(SpecialElementsForTransformation.GetRotatedSegmentOs()==None): 
            if  selected3DObject.isSegmentInIndex(0):                  
                print 'successful setting of rotational os'
                SpecialElementsForTransformation.SetRotatedSegmentOs(selected3DObject[0])
                
                if SpecialElementsForTransformation.GetRotateAngle()== None:
                    angleStr = askstring("Please Insert Angle", "inDegrees")
                    if(is_number(angleStr)):
                        angle = float(angleStr)*pi/180
                        SpecialElementsForTransformation.SetRotatedAngle(angle)
                    else:
                        print 'write number for degrees .You have to set it agian'
                        angleStr = ""
                if SpecialElementsForTransformation.GetScrewMotionSize()== None:
                    motionSizeStr = askstring("Please Insert Screw motion size", "size(if any)")
                    if(is_number(motionSizeStr)):
                        motionSize = float(motionSizeStr)
                        SpecialElementsForTransformation.SetScrewMotionSize(float(motionSize))
                        print 'successful setting of sizeOfVectorToTranslate about screw motion:',SpecialElementsForTransformation.GetScrewMotionSize()
                    else :
                        print 'write number for screwSize .You have to set it agian'
                
                if(SpecialElementsForTransformation.GetRotatedSegmentOs()!=None and SpecialElementsForTransformation.GetRotateAngle()!= None and SpecialElementsForTransformation.GetScrewMotionSize()!= None):  
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetRotatedSegmentOs(), "Rotation OS" +str(SpecialElementsForTransformation.GetRotateAngle()))#+'traslate with size'+str(sizeOfVectorToTranslate))
                selected3DObject.freeSelectedObjects()
        else:
            if SpecialElementsForTransformation.GetRotateAngle()== None:
                    angleStr = askstring("Please Insert Angle", "inDegrees")
                    if(is_number(angleStr)):
                        angle = float(angleStr)*pi/180
                        SpecialElementsForTransformation.SetRotatedAngle(angle)
                    else:
                        print 'write number for degrees .You have to set it agian'
                        angleStr = ""
            if SpecialElementsForTransformation.GetScrewMotionSize()== None:
                    motionSizeStr = askstring("Please Insert Screw motion size", "size(if any)")
                    if(is_number(motionSizeStr)):
                        motionSize = float(motionSizeStr)
                        SpecialElementsForTransformation.SetScrewMotionSize(float(motionSize))
                        print 'successful setting of sizeOfVectorToTranslate about screw motion:',SpecialElementsForTransformation.GetScrewMotionSize()
                    else :
                        print 'write number for screwSize .You have to set it agian'
            if(SpecialElementsForTransformation.GetRotatedSegmentOs()!=None and SpecialElementsForTransformation.GetRotateAngle()!= None and SpecialElementsForTransformation.GetScrewMotionSize()!= None):  
                TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetRotatedSegmentOs(), "Rotation OS" +str(SpecialElementsForTransformation.GetRotateAngle()))#+'traslate with size'+str(sizeOfVectorToTranslate))
                 
    
    @staticmethod
    def UnSelectScrew():
        SpecialElementsForTransformation.FreeRotatedSegmentOs()
        SpecialElementsForTransformation.FreeRotateAngle()
        SpecialElementsForTransformation.FreeScrewMotionSize()
    
    
    @staticmethod
    def ScrewMotionOperation():
        if SpecialElementsForTransformation.GetRotatedSegmentOs()!= None and SpecialElementsForTransformation.GetRotateAngle()!=None and SpecialElementsForTransformation.GetScrewMotionSize()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                #Man3dCommand.ScrewTransform()
                if SpecialElementsForTransformation.GetRotatedSegmentOs().isFree():
                    Transformer.ScrewMotion(selected3DObject)
                else:
                    print 'choose free element,if you want to Move(screwMotion) objects'
            else:
                Creator.ScrewMotion(selected3DObject)
                selected3DObject.freeSelectedObjects()
        else:
            print 'set rotation os and angle and size of direction first'
#                Man3dCommand.ScrewCreation()
        
         
    @staticmethod
    def SetRotate():
        
        if(SpecialElementsForTransformation.GetRotatedSegmentOs()==None): 
            if  selected3DObject.isSegmentInIndex(0):                  
                print 'successful setting of rotational os'
                SpecialElementsForTransformation.SetRotatedSegmentOs(selected3DObject[0])
                if SpecialElementsForTransformation.GetRotateAngle()== None:
                    angleStr = askstring("Please Insert Angle", "inDegrees")
                    if(is_number(angleStr)):
                        angle = float(angleStr)*pi/180
                        SpecialElementsForTransformation.SetRotatedAngle(angle)
                    else:
                        print 'write number for degrees .You have to set it agian'
                        angleStr = ""
                

                if SpecialElementsForTransformation.GetRotatedSegmentOs()!=None and SpecialElementsForTransformation.GetRotateAngle()!= None:
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetRotatedSegmentOs(), "Rotation OS" + str(SpecialElementsForTransformation.GetRotateAngle()))#+'traslate with size'+str(sizeOfVectorToTranslate))
                selected3DObject.freeSelectedObjects()
        else:
            if SpecialElementsForTransformation.GetRotateAngle()== None:
                    angleStr = askstring("Please Insert Angle", "inDegrees")
                    if(is_number(angleStr)):
                        angle = float(angleStr)*pi/180
                        SpecialElementsForTransformation.SetRotatedAngle(angle)
                    else:
                        print 'write number for degrees .You have to set it agian'
                        angleStr = ""
            if SpecialElementsForTransformation.GetRotateAngle()!= None:
                    TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetRotatedSegmentOs(), "Rotation OS" + str(SpecialElementsForTransformation.GetRotateAngle()))#+'traslate with size'+str(sizeOfVectorToTranslate)) 
    
    @staticmethod
    def UnSetRotate():
        SpecialElementsForTransformation.FreeRotatedSegmentOs()
        SpecialElementsForTransformation.FreeRotateAngle()
        
            
   
    
    @staticmethod
    def RotateOperation():
        if SpecialElementsForTransformation.GetRotatedSegmentOs()!= None and SpecialElementsForTransformation.GetRotateAngle()!=None:
            if Man3dCommand.Move1Create2.get()==1:
                if SpecialElementsForTransformation.GetRotatedSegmentOs().isFree():
                    Transformer.Rotate(selected3DObject)
                else:
                    print 'choose free element,if you want to Move(rotate) objects'
                #Man3dCommand.RotateTransform()
            else:
                Creator.Rotate(selected3DObject)
                selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
                #Man3dCommand.RotateCreation()
                
                
                
    @staticmethod    
    def SetParallelBySegment():
        if(SpecialElementsForTransformation.GetParallelSegment()==None):
            if selected3DObject.isSegmentInIndex(0):
                SpecialElementsForTransformation.SetParallelSegment(selected3DObject[0])
                TwinkerHelper.Twinkle(selected3DObject[0],"Parallel Os")
                print 'successful setting of parallel Segment' 
                
            else:
                print 'select segment to make it parallel Os'
            selected3DObject.freeSelectedObjects()
        else:
            TwinkerHelper.Twinkle(SpecialElementsForTransformation.GetParallelSegment(),"Parallel Os")
            print 'successful setting of parallel Segment' 
                    
    @staticmethod
    def UnSetParallelBySegment():
        SpecialElementsForTransformation.FreeParallelSegment()
    
    
    @staticmethod   
    def ParallelOperationBySegment():
        if SpecialElementsForTransformation.GetParallelSegment()!=None:
            Creator.MakeParallelSegments(selected3DObject)
            selected3DObject.freeSelectedObjects()
        else:
            print 'set elements first'
    
    @staticmethod
    def DeleteOperation():
        if len(selected3DObject)!=0:
            DeletorAndFreeHelper.Delete3DObjectForUndoRedoManager(selected3DObject)
            selected3DObject.freeSelectedObjects()
        else:
            print 'select elements to delete'
      
    @staticmethod
    def FreeOperation():
        if len(selected3DObject)!=0:
            DeletorAndFreeHelper.Free3DObjectForUndoRedoManager(selected3DObject)
            selected3DObject.freeSelectedObjects()
        else:
            print 'select elements to free'      
        

class TxtboxOut(object):

    def __init__(self, tkintertxt):
        self.T = tkintertxt
        
    def write(self, txt):
        self.T.insert(END, "%s" % str(txt))
        self.T.yview(MOVETO, 1.0)
            




class GuiMan3D:
    def addEntryTOGrid(self,columnElementsLabelText,columntSetButtonCommand,columntUnSetButtonCommand,columntOperationButtonText,columntOperationButtonCommand,columnOperationArgumentsText):
        column,row = self.parentWindow.grid_size()
        if columnElementsLabelText != None:
            self.columntSetButton = Button(self.parentWindow,text='Set',command=columntSetButtonCommand,width = 8,height = 1)
            self.columntUnSetButton = Button(self.parentWindow,text='UnSet',command=columntUnSetButtonCommand,width = 8,height = 1)
            self.columnElementsLabel = Label(self.parentWindow,text=columnElementsLabelText,width = 22,height = 1)
            self.columntSetButton.grid(row=row,column = 0, sticky =E+W)        
            self.columntUnSetButton.grid(row=row,column = 1, sticky =E+W)
            self.columnElementsLabel.grid(row=row,column = 2, sticky =E+W)
        self.columntOperationButton = Button(self.parentWindow,text=columntOperationButtonText,command=columntOperationButtonCommand,width = 22,height = 1)
        self.columnElementsLabel2 = Label(self.parentWindow,text=columnOperationArgumentsText,width = 18,height = 1)
        
                
                
        self.columntOperationButton.grid(row=row,column = 3, sticky =E+W)
        self.columnElementsLabel2.grid(row=row,column = 4, sticky =E+W)
        
    def addEntryLabelCommandsToGrid(self,textLable,*labelsAndCommands):
        self.subFrame = Frame(self.parentWindow )
        column,row = self.parentWindow.grid_size()
        self.RowLabel=Label(self.subFrame,text=textLable)
        self.RowLabel.grid(row=0,column = 0,sticky =E+W)
        i = 0
        k = 1
        
        while i < len(labelsAndCommands):
            self.ButtonOnOneRow = Button(self.subFrame,text = labelsAndCommands[i],command = labelsAndCommands[i+1])
            self.ButtonOnOneRow.grid(row=0,sticky =E+W,column = k)
            i+=2
            k+=1
         
        self.subFrame.grid(row = row,columnspan = 5,sticky =W)   
#        for labelText,comandOperation in labelsAndCommands:
#            self.ButtonOnOneRow = Button(self.parentWindow,text = labelText,command = comandOperation)
#            self.ButtonOnOneRow.grid(row=row,sticky =E+W)
    def addEntryMovementRestrictionToGrid(self):
        self.subFrame = Frame(self.parentWindow )
        column,row = self.parentWindow.grid_size() 
        Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4 = IntVar()
        self.MovementRegulationLabel = Label(self.subFrame,text='Movement restriction:')
        self.Default3DRadioButton = Radiobutton(self.subFrame, text="Default 3D(no restriction)", variable=Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4, value=1,command = Man3dCommand.SetForwardVectorFromRadioButtonCommand)
        self.Default3DRadioButton.select()
        self.OYZ2DRadioButton =Radiobutton(self.subFrame, text="||Oyz(see 2D)", variable=Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4, value=2,command = Man3dCommand.SetForwardVectorFromRadioButtonCommand)
        self.OXZ2DRadioButton =Radiobutton(self.subFrame, text="||Oxz(see 2D)", variable=Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4, value=3,command = Man3dCommand.SetForwardVectorFromRadioButtonCommand)
        self.OXY2DRadioButton =Radiobutton(self.subFrame, text="||Oxy(see 2D)", variable=Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4, value=4,command = Man3dCommand.SetForwardVectorFromRadioButtonCommand)
        
        
        self.MovementRegulationLabel.grid(row=0,column =0, sticky = W)
#        self.columnThreeLabel.grid(row=2,column =2, sticky = E+W)
        self.Default3DRadioButton.grid(row=0,column =1, sticky = E+W)
        self.OYZ2DRadioButton.grid(row=0,column =2, sticky = E+W)
        self.OXZ2DRadioButton.grid(row=0,column =3, sticky = E+W)
        self.OXY2DRadioButton.grid(row=0,column =4, sticky = E+W)
        
        self.subFrame.grid(row = row,columnspan = 5,sticky =W)
        
   
        
    def __init__(self,parentWindow):
        
        
        
        
        Man3dCommand.nameOfFile = None
        Man3dCommand.newNameVar = StringVar()
        
        Man3dCommand.X1 = DoubleVar()
        Man3dCommand.X1.set(0.0)
        Man3dCommand.Y1 = DoubleVar()
        Man3dCommand.Y1.set(0.0)
        Man3dCommand.Z1 = DoubleVar()
        Man3dCommand.Z1.set(0.0)
        Man3dCommand.Move1Create2 = IntVar()
        Man3dCommand.Show1Hide0 = IntVar()
        Man3dCommand.Point1Segment2 = IntVar()
        Man3dCommand.VertexNumber = IntVar()
        Man3dCommand.VertexNumber.set(0)
        
       # self.CreationOr
        
        self.parentWindow = parentWindow
        Man3dCommand.rootWindow= parentWindow
        
        
        #new added
        self.menubar = Menu(self.parentWindow)

# create a pulldown menu, and add it to the menu bar
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New(set file name)", command=Man3dCommand.NewObjectCommand)
        self.filemenu.add_command(label="Open", command=Man3dCommand.OpenObjectsCommand)
        self.filemenu.add_command(label="Load", command=Man3dCommand.LoadMan3dCommand)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close(ctrl+q)", command=Man3dCommand.CloseProjectCommand)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save(ctrl+s)", command=Man3dCommand.SaveObjectsCommand)
        self.filemenu.add_command(label="Save And Close(ctrl+shift+s)", command=Man3dCommand.SaveAndCloseProjectCommand)
        self.filemenu.add_command(label="Save As", command=Man3dCommand.SaveAsMan3dCommand)
        
        self.filemenu.add_separator()
        
        
        
        
        self.filemenu.add_command(label="Exit(Esc)", command=Man3dCommand.ExitMan3dCommand)#lambda:self.parentWindow.destroy())#Man3dCommand.ExitMan3dCommand)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        
       
        
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Undo(ctrl+z)", command=Man3dCommand.UndoCommand)
        self.editmenu.add_command(label="Redo(ctrl+y)", command=Man3dCommand.RedoCommand)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Free UndoRedo(q)", command=Man3dCommand.ClearUndoRedoStackCommand)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Select All(ctrl+a)", command=Man3dCommand.SelectAllElementsCommand)
        self.editmenu.add_command(label="Delete(delete)", command=Man3dCommand.DeleteOperation)
        self.editmenu.add_command(label="Free Points(ctrl+f)", command=Man3dCommand.FreeOperation)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Set Name(one 3D object)", command=Man3dCommand.ChangeNameCommand)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        
        self.figure = Menu(self.menubar, tearoff=0)
        self.figure.add_command(label="Point(1)", command=Man3dCommand.CreatePointByDefaultCommand)
        self.figure.add_command(label="Segment(2)", command=Man3dCommand.CreateSegmentByDefaultCommand)
        self.figure.add_command(label="Plane(3)", command=Man3dCommand.CreatePlaneByDefaultCommand)
        self.figure.add_command(label="Pyramid(4)", command=Man3dCommand.CreatePyramidByDefaultCommand)
        self.figure.add_command(label="Pryzm(5)", command=Man3dCommand.CreatePryzmByDefaultCommand)
        self.figure.add_separator()
        self.figure.add_command(label="Pyramid By Vertex Number", command=Man3dCommand.CreateNPyramideCommand)
        self.figure.add_command(label="Point By Position", command=Man3dCommand.CreatePointCommand)
        
        self.menubar.add_cascade(label="Figure", menu=self.figure)
        
        self.showHide = Menu(self.menubar, tearoff=0)
        self.showHide.add_command(label="3D Object Names(a)", command=Man3dCommand.ShowOrHideLabelsCommand)
        self.showHide.add_command(label="Coordinate System(A)", command=Man3dCommand.ShowCoordinateSystemCommand)
        self.menubar.add_cascade(label="Show/Hide", menu=self.showHide)
        
        
        
        self.showTwincle = Menu(self.menubar, tearoff=0)
        self.showTwincle.add_command(label="All 3D Objects(,)", command=Man3dCommand.ShowAllElementsCommand)
        self.showTwincle.add_command(label="Special Elements(;)", command=Man3dCommand.ShowAllSpecialElementsCommand)
        self.showTwincle.add_command(label="Dragable Objects(/)", command=Man3dCommand.ShowDragableElementsCommand)
        self.showTwincle.add_command(label="Free 3D Objects(.)", command=Man3dCommand.ShowFreeElementsCommand)
        self.showTwincle.add_separator()
        self.showTwincle.add_command(label="Count 3D Objects([)", command=Man3dCommand.CountInfoObjectCommand)
        self.menubar.add_cascade(label="Show(Twincle)", menu=self.showTwincle)
        
        self.measurement = Menu(self.menubar, tearoff=0)
        self.measurement.add_command(label="Segments Length(i)", command=Man3dCommand.CalculateLengthOfSemgnetsCommand)
        self.measurement.add_command(label="Planes Area(y)", command=Man3dCommand.CalculateAreaOfPlanesCommand)
        self.menubar.add_cascade(label="Measurement", menu=self.measurement)
        
        
        
#        helpmenu = Menu(menubar, tearoff=0)
#        helpmenu.add_command(label="About", command=hello)
#        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.parentWindow.config(menu=self.menubar)
        
        
#        self.mainFrame = Frame(parentWindow)
        
        
        self.columnOneAndTwoAndThree = Label(self.parentWindow,text='Set/Unset special element(s) for transformation',width = 38)
#        self.columnThreeLabel = Label(self.parentWindow,text='(special For transformation)',width = 22)
        
        self.columnFour = Label(self.parentWindow,text='with name',width = 22)
        self.columnFive = Label(self.parentWindow,text='over selected:',width = 18)

        

        self.scrollBar = Scrollbar(self.parentWindow,width = 3)
        self.TextControl = Text(self.parentWindow,height = 4,width = 75)
        
         
        newout = TxtboxOut(self.TextControl)
        console = sys.stdout
        sys.stdout = newout
        self.TextControl.focus_set()
        
        
        
        self.columnRadioButtonLabel = Label(self.parentWindow,text='Choose Type of Transformations: Move/Create')
        self.TransformOperationRB = Radiobutton(self.parentWindow, text="Move", variable=Man3dCommand.Move1Create2, value=1,width = 8)
        self.TransformOperationRB.select()
        self.CreateOperationRB =Radiobutton(self.parentWindow, text="Create", variable=Man3dCommand.Move1Create2, value=2,width = 8)
        
        
        self.checkBoxPerpendiculars = Checkbutton(self.parentWindow,text="Show perpendiculars",variable=Man3dCommand.Show1Hide0,onvalue = 1,offvalue = 0 )
        self.TransformOperationRB.select()
        
        self.OnlyCreateLabel = Label(self.parentWindow,text='Type of Transformations: Create')
        
        
        self.PointSegmentButtonLabel = Label(self.parentWindow,text='Work with:')
        self.PointRB = Radiobutton(self.parentWindow, text="Points", variable=Man3dCommand.Point1Segment2, value=1,width = 8)
        self.PointRB.select()
        self.SegmentRB =Radiobutton(self.parentWindow, text="Segments", variable=Man3dCommand.Point1Segment2, value=2,width = 8)
        
      
        
###        self.addEntryLabelCommandsToGrid('Undo,Redo,SelectAll,Clear: ','Undo(ctrl+z)',Man3dCommand.UndoCommand,'Redo(ctrl+y)',Man3dCommand.RedoCommand,'Select All(ctrl+a)',Man3dCommand.SelectAllElementsCommand,'Clear UndoRedoStack(q)',Man3dCommand.ClearUndoRedoStackCommand)
###        self.addEntryLabelCommandsToGrid('Show/Hide: ','Names(a)',Man3dCommand.ShowOrHideLabelsCommand,'CoordinateSystem(A)',Man3dCommand.ShowCoordinateSystemCommand)
###        self.addEntryLabelCommandsToGrid('Show(Twincle): ','All 3D Objects(,)',Man3dCommand.ShowAllElementsCommand,'Special Elements(;)',Man3dCommand.ShowAllSpecialElementsCommand,'Dragable Objects(/)',Man3dCommand.ShowDragableElementsCommand,'Free 3D Objects(.)',Man3dCommand.ShowFreeElementsCommand,'Count 3D Objects([)',Man3dCommand.CountInfoObjectCommand)
###        #self.addEntryLabelCommandsToGrid('----------------------------------------------------Scene Movement(Keyboard)------------------------------------------------------------------')
        self.addEntryLabelCommandsToGrid('Scene Movement(Keyboard):','Oy+(up)',Man3dCommand.OyPlusCommand,'Oy-(down)',Man3dCommand.OyMinusCommand,'Ox+(right)',Man3dCommand.OxPlusCommand,'Ox-(left)',Man3dCommand.OxMinusCommand,'Oz+(+)',Man3dCommand.OzPlusCommand,'Oz-(-)',Man3dCommand.OzMinusCommand,'O(0,0,0)(*)',Man3dCommand.O_0_0Command)
        #self.addEntryLabelCommandsToGrid('----------------------------------------------------Scene Movement(Mouse)------------------------------------------------------------------')
        self.addEntryLabelCommandsToGrid('Scene Movement(Mouse): Rotate(hold Right button),Move near and far(hold right and left buttons)')
        self.addEntryMovementRestrictionToGrid()
        
        
     
        
        column,rowA = self.parentWindow.grid_size()
        self.scrollBar.grid(row = rowA,column=0,columnspan = 5, sticky = E)
        self.TextControl.grid(row = rowA,column = 0,columnspan = 5, sticky = W)
        self.scrollBar.config(command=self.TextControl.yview)
        self.TextControl.config(yscrollcommand=self.scrollBar.set)
        self.addEntryLabelCommandsToGrid("Create point on plane,segment or 3d space(Alt+ Left click)")
        column,rowA = self.parentWindow.grid_size()
        self.columnRadioButtonLabel.grid(row=rowA,column =0,columnspan = 3, sticky = W)
        self.TransformOperationRB.grid(row=rowA,column =3, sticky = W)
        self.CreateOperationRB.grid(row=rowA,column =3, sticky = E)
        
        column,rowA = self.parentWindow.grid_size()
        self.columnOneAndTwoAndThree.grid(row=rowA,column =0,columnspan =3, sticky = E)
#        self.columnThreeLabel.grid(row=2,column =2, sticky = E+W)
        self.columnFour.grid(row=rowA,column =3, sticky = E+W)
        self.columnFive.grid(row=rowA,column =4, sticky = E+W)
        
       
        
       
        self.addEntryTOGrid("Rotation os and angle", Man3dCommand.SetRotate, Man3dCommand.UnSetRotate,"Rotate(r)", Man3dCommand.RotateOperation, "All 3D Objects")
        self.addEntryTOGrid("Rotation os,angle,direction",  Man3dCommand.SetScrewMotion,  Man3dCommand.UnSelectScrew,"ScrewMotion(R)", Man3dCommand.ScrewMotionOperation, "All 3D Objects")
        self.addEntryTOGrid("vector",  Man3dCommand.SetTranslatedVector,  Man3dCommand.UnSetTranslatedVector,"Translate(t)", Man3dCommand.TranslateOperation, "All 3D Objects")
        self.addEntryTOGrid("Center,coefficientX,Y,Z",  Man3dCommand.SetDilatation, Man3dCommand.UnSetDilition,"Dilitate(d)", Man3dCommand.DilitateOperation, "All 3D Objects")
        self.addEntryTOGrid("Center,homotetic coefficient",  Man3dCommand.SetHomotetia, Man3dCommand.UnSetHomotetia,"Homotete(h)", Man3dCommand.HomotetiaOperation, "All 3D Objects")
        self.addEntryTOGrid("Center",  Man3dCommand.SetSymetria, Man3dCommand.UnSetSymetria,"SymetryByCenter(s)", Man3dCommand.SymetriaOperation, "All 3D Objects")
        self.addEntryTOGrid("Symetry os",  Man3dCommand.SetSymetriaBySegment, Man3dCommand.UnSetSymetriaBySegment,"SymetryBySegment(S)", Man3dCommand.SymetriaOperationBySegment, "All 3D Objects")
        self.addEntryTOGrid("Plane",  Man3dCommand.SetSymetriaByPlane, Man3dCommand.UnSetSymetriaByPlane,"SymetryByPlane(z)", Man3dCommand.SymetriaOperationByPlane, "All 3D Objects")
        self.addEntryTOGrid("Plane,vector(translation)",  Man3dCommand.SetSlidingImpactByPlane, Man3dCommand.UnSetSlidingImpactByPlane,"SlidingImpact(T)", Man3dCommand.SlidingImpactOperationByPlane, "All 3D Objects")
        self.addEntryTOGrid("Plane,vector(direction)",  Man3dCommand.SetProjectOnPlane, Man3dCommand.UnSetProjectOnPlane,"ProjectOnPlane(p)", Man3dCommand.ProjectOnPlaneOperation, "All 3D Objects")
        column,rowA = self.parentWindow.grid_size()
        self.checkBoxPerpendiculars.grid(row = rowA,column=0,columnspan = 5, sticky = E)
        self.addEntryTOGrid("Plane",  Man3dCommand.SetOrthogonalProjectionOnPlane, Man3dCommand.UnSetOrthogonalProjectionOnPlane,"OrthogonalProjectOnPlane(P)", Man3dCommand.OrthogonalProjectionOperationOnPlane, "All 3D Objects")
        self.addEntryTOGrid("Projection os",  Man3dCommand.SetProjectionOnSegment, Man3dCommand.UnSetProjectionOnSegment,"ProjectionOnSegment(ctrl+p)", Man3dCommand.ProjectionOnSegmentOperation, "Point,Segment")
        column,rowA = self.parentWindow.grid_size()
        self.OnlyCreateLabel.grid(row= rowA,column=0,columnspan = 5, sticky = W)
        
        
        
        self.addEntryTOGrid(None,  Man3dCommand.SetNothing, Man3dCommand.UnsetNothing,"Segment(l)", Man3dCommand.SegmentOperation, "Two Points")
        self.addEntryTOGrid(None,  Man3dCommand.SetNothing, Man3dCommand.UnsetNothing,"Plane(k)", Man3dCommand.PlaneOperation, "Three Points")
        self.addEntryTOGrid(None,  Man3dCommand.SetNothing, Man3dCommand.UnsetNothing,"Bisector Point(b)", Man3dCommand.BisectorPointOperation, "Three Points")
        self.addEntryTOGrid("Parallel os",  Man3dCommand.SetParallelBySegment, Man3dCommand.UnSetParallelBySegment,"ParallelBySegment(u)", Man3dCommand.ParallelOperationBySegment, "Points")
        self.addEntryTOGrid(None,  Man3dCommand.SetNothing, Man3dCommand.UnsetNothing,"CrossTwoSegments(c)", Man3dCommand.CrossTwoSegmentsOperation, "Two Segments")
        self.addEntryTOGrid("Plane",  Man3dCommand.SetCrossSegmentAndPlane, Man3dCommand.UnSetCrossSegmentAndPlane,"CrossPlaneAdnSegments(C)", Man3dCommand.CrossSegmentAndPlaneOperation, "Segments")
        
        
        
        column,rowA = self.parentWindow.grid_size()
        self.PointSegmentButtonLabel.grid(row=rowA,column =0,columnspan =3, sticky = E)
#        self.columnThreeLabel.grid(row=2,column =2, sticky = E+W)
        self.PointRB.grid(row=rowA,column =3, sticky = E)
        self.SegmentRB.grid(row=rowA,column =4, sticky = W)
        
        
        self.addEntryTOGrid(None,  Man3dCommand.SetNothing, Man3dCommand.UnsetNothing,"MiddlePoint(m)", Man3dCommand.MiddlePointOperation, "Points/Segments")
        self.addEntryTOGrid("Number between(0,1)",  Man3dCommand.SetProportion, Man3dCommand.UnSetProportion,"ProportionPoint(n)", Man3dCommand.ProportionOperation, "Points/Segments")
        self.addEntryTOGrid("Proportion point",  Man3dCommand.SetProportionPoint, Man3dCommand.UnSetProportionPoint,"ProportionPointByPoint(N)", Man3dCommand.ProportionPointOperation, "Points/Segments")
        
####        self.addEntryLabelCommandsToGrid("Type of Transformations:  ","Delete(delete)",Man3dCommand.DeleteOperation,"FreePoints(f)",Man3dCommand.FreeOperation,"Set new name(Of one 3D selected object)",Man3dCommand.ChangeNameCommand)
####        self.addEntryLabelCommandsToGrid("Create(By Default)","Point(1)",Man3dCommand.CreatePointByDefaultCommand,"PointByPosition",Man3dCommand.CreatePointCommand,"Segment(2)",Man3dCommand.CreateSegmentByDefaultCommand,"Plane(3)",Man3dCommand.CreatePlaneByDefaultCommand,"Pyramid(4)",Man3dCommand.CreatePyramidByDefaultCommand, "Pryzm(5)",Man3dCommand.CreatePryzmByDefaultCommand,"Pyramid By Number",Man3dCommand.CreateNPyramideCommand)
      
        
       
          
        
        self.sizeOfWindow= self.scrollBar.winfo_reqwidth()+self.TextControl.winfo_reqwidth()+90
        

        
def pickKeyboard():
        while 1:
            
            if scene.kb.keys:
                 
                ss = scene.kb.getkey() # obtain keyboard information
                #print "you click ",ss
                
                
                   
                

                if ss == 'up':
                    Man3dCommand.OyPlusCommand()
                elif ss == 'down':
                    Man3dCommand.OyMinusCommand()
                elif ss == 'left':
                    Man3dCommand.OxPlusCommand()
                elif ss == 'right':
                    Man3dCommand.OxMinusCommand()
                elif ss == '+':
                    Man3dCommand.OzPlusCommand()                    
                elif ss == '-':
                    Man3dCommand.OzMinusCommand()
                elif ss == '*':
                    Man3dCommand.O_0_0Command()
                
                elif ss == 'ctrl+z':
                    Man3dCommand.UndoCommand()
                        
                elif ss == 'i':  
                    Man3dCommand.CalculateLengthOfSemgnetsCommand()
                elif ss == 'y':  
                    Man3dCommand.CalculateAreaOfPlanesCommand()
                        
                elif ss == 'ctrl+y':  # make midpoint
                    Man3dCommand.RedoCommand()
                
                elif ss == 'ctrl+q':
                    Man3dCommand.CloseProjectCommand()

                elif ss == 'q':
                    Man3dCommand.ClearUndoRedoStackCommand()
                elif ss == 'ctrl+s':
                    Man3dCommand.SaveObjectsCommand()
                elif ss == 'ctrl+shift+s':
                    Man3dCommand.SaveAndCloseProjectCommand()                    
                    #UndoRedoManager.Clear()
                    
                #----------------------------------------------------------
                
                #---------------------Generation------------------------------
                elif ss == '1':
                    Man3dCommand.CreatePointByDefaultCommand()

                elif ss == '2':
                    Man3dCommand.CreateSegmentByDefaultCommand()
                   
                elif ss == '3':
                    Man3dCommand.CreatePlaneByDefaultCommand()
                elif ss == '4':
                    Man3dCommand.CreatePyramidByDefaultCommand()
                elif ss == '5':
                    Man3dCommand.CreatePryzmByDefaultCommand()
               

                    
                
                #-----------------------------------------------------------------------        
                #-----------Segment and Cross Point intersaction of Plane And Segment----           
                elif ss == 'l':
                    Man3dCommand.SegmentOperation()

                
                if ss == 'k':
                    Man3dCommand.PlaneOperation()

                if ss == 'b':
                    Man3dCommand.BisectorPointOperation()
                
                elif ss == 'c':
                    Man3dCommand.CrossTwoSegmentsOperation()
                
                elif ss == 'C':
                    Man3dCommand.CrossSegmentAndPlaneOperation()
                
                
                #-----------------------------------------------------------------------
                #-----------Rotation and Screw Motion----------------------------           
                       

                    
                elif ss == 'r':
                    Man3dCommand.RotateOperation()
                         
                elif ss == 'R':
                    Man3dCommand.ScrewMotionOperation()
                        
                #-----------------------------------------------------------------------        
                #-----------Translation-------------------------------------------------           
      

                elif ss == 't':
                    Man3dCommand.TranslateOperation()
                
                elif ss == 'ctrl+p':
                    Man3dCommand.ProjectionOnSegmentOperation()
                        
                
                elif ss == 'P':
                    Man3dCommand.OrthogonalProjectionOperationOnPlane()
                #---------------------------------------------------------------------------        
                
                #---------------Homotetia Gui----------------------

                elif ss == 'h':
                    Man3dCommand.HomotetiaOperation()

                #---------------------------------------------------------------------------        
                
                #---------------Delitation,Symetry Gui----------------------

                elif ss == 'd':
                    Man3dCommand.DilitateOperation()
#                
                
                elif ss == 's':
                    Man3dCommand.SymetriaOperation()

                #---------------------------------------------------------------------------
                #---------------SymetriaByPlane----------------------

#                
                elif ss == 'T':
                    Man3dCommand.SlidingImpactOperationByPlane()
                elif ss == 'z':
                    Man3dCommand.SymetriaOperationByPlane()
                #---------------------------------------------------------------------------
                #---------------SymetriaBySegment Gui----------------------

                    
                elif ss == 'S':
                    Man3dCommand.SymetriaOperationBySegment()
       
                #---------------------------------------------------------------------------
                #---------------Parallel segment----------------------

                elif ss == 'u':
                    Man3dCommand.ParallelOperationBySegment()

                #---------------------------------------------------------------------------        
                #---------------Middle points And Proportions point----------------------
                
                elif ss == 'm':
                    Man3dCommand.MiddlePointOperation()
               
                elif ss == 'n':
                    Man3dCommand.ProportionOperation()
                elif ss == 'N':
                    Man3dCommand.ProportionPointOperation()
    
                
                
                #---------------------------------------------------------------------------
                #---------------Delete and free objects and labels show----------------------
                elif ss == 'delete':
                    Man3dCommand.DeleteOperation()
                elif ss == 'ctrl+f':
                    Man3dCommand.FreeOperation()

                elif ss == 'a':
                    Man3dCommand.ShowOrHideLabelsCommand()


                
                #---------------------------------------------------------------------------
                #---------------Special Operation twinclers---------------------- 
                               
                elif ss == ";":
                    Man3dCommand.ShowAllSpecialElementsCommand()
                elif ss == "[":
                    Man3dCommand.CountInfoObjectCommand()
                

                elif ss =="," :
                    Man3dCommand.ShowAllElementsCommand()
                
                elif ss =="." :
                    Man3dCommand.ShowFreeElementsCommand()
                    
                elif ss =="/" :
                    Man3dCommand.ShowDragableElementsCommand()
                    
                
####                if ModifiedObserverHelpsForLables.isModified :
####                    LabelHelper.ShowLabels()#Object3DDictionary.values())
####                    ModifiedObserverHelpsForLables.isModified = False 
                
                elif ss == "ctrl+a":
                    Man3dCommand.SelectAllElementsCommand()
                
                elif ss == 'A':                     
                    Man3dCommand.ShowCoordinateSystemCommand()  
                    
                        
                       
                        
                    
                    
                    
                
                
#                elif ss == 'f1':
#                    HelpUtil.callF(1)
#                elif ss == 'f2':
#                    HelpUtil.callF(2)
#                elif ss == 'f3':
#                    HelpUtil.callF(3)
#                elif ss == 'f4':
#                    HelpUtil.callF(4)
#                elif ss == 'f5':
#                    HelpUtil.callF(5)
#                elif ss == 'f6':
#                    HelpUtil.callF(6)
#                elif ss == 'f7':
#                    HelpUtil.callF(7)
#                elif ss == 'f8':
#                    HelpUtil.callF(8)                
#                elif ss == 'f9':
#                    HelpUtil.callF(9)
#                

                
            

def SelectFunction():
    pick = None
    specialElement = False
    
    
    while 1:
        
        
        if(scene.mouse.events):
            
            m1 = scene.mouse.getevent()
             

            if m1.drag:
                
                if(m1.pick in Object3DDictionary.values()):#m1.pick in object3D):
                    drag_pos = m1.pickpos
                    listOfPointToMove = []
                    
                    if(m1.pick.canDrag()):#IsDraggable == True):
                        
                        if(UndoRedoManager.checkUndoStack()):
                            
                            
                            if issubclass(type(m1.pick) , ProportionalPoint):
                                specialElement = True
                                
                                vectorAB = m1.pick.GetParent(1).pos - m1.pick.GetParent(0).pos
                                
                                SceneHelper.setNewForwardVectorA(vectorAB,True,pi/3)
                                SceneHelper.setProjectionVectorByPerpVector(vectorAB)
                                SceneHelper.workingProjectVector = SceneHelper.projectionVector
                                
                            elif issubclass(type(m1.pick) , TranslatedPointVector):
                                specialElement = True
                                
                                vectorAB = m1.pick.vector
                                SceneHelper.setNewForwardVectorA(vectorAB,True,pi/3)
                                SceneHelper.setProjectionVectorByPerpVector(vectorAB)
                                SceneHelper.workingProjectVector = SceneHelper.projectionVector
                                    
                            elif issubclass(type(m1.pick) , PointByPlane):
                                specialElement = True
                               # print 'you are in PointByPlane'
                                vectorAB = m1.pick.GetParent(0).bxc
                                SceneHelper.setProjectionVector(vectorAB)
                                SceneHelper.setNewForwardVectorA(vectorAB,False,pi/6)
                                SceneHelper.workingProjectVector = SceneHelper.projectionVector
                            else:
                                SceneHelper.setProjectionVector(SceneHelper.defaultProjectionVector)
                                if Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==1:
                                    scene.userspin = 1
                                    SceneHelper.workingProjectVector = SceneHelper.projectionVector
                                else:
                                    
                                    scene.userspin = 0
                                    if Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==2:
                                        SceneHelper.workingProjectVector =vector(1,0,0)
                                    elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==3:
                                        SceneHelper.workingProjectVector =vector(0,1,0)
                                    elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==4:
                                        SceneHelper.workingProjectVector =vector(0,0,1)
                                    
                                
                            SceneHelper.projectionPoint = drag_pos
                            
                            
                            
                            
                                        
#                                if SceneHelper.lockedRotation:
#                                    SceneHelper.workingProjectVector = SceneHelper.projectPlane.bxc#SceneHelper.projectVectorByPlane
#                                else:
#                                    SceneHelper.workingProjectVector = SceneHelper.projectionVector
                            
                            #if specialElement:
####                            SceneHelper.workingProjectVector = SceneHelper.projectionVector
#                            else:
#                                SceneHelper.workingProjectVector = 
#                            else:
#                                if Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==1:
#                                    scene.userspin = 1
#                                    SceneHelper.workingProjectVector = SceneHelper.projectionVector
#                                else:
#                                    scene.userspin = 0
#                                    if Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==2:
#                                        SceneHelper.workingProjectVector =vector(1,0,0)
#                                    elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==3:
#                                        SceneHelper.workingProjectVector =vector(0,1,0)
#                                    elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==4:
#                                        SceneHelper.workingProjectVector =vector(0,0,1)
                                        
#                                if SceneHelper.lockedRotation:
#                                    SceneHelper.workingProjectVector = SceneHelper.projectPlane.bxc#SceneHelper.projectVectorByPlane
#                                else:
#                                    SceneHelper.workingProjectVector = SceneHelper.projectionVector
                            #print 'SceneHelper.workingProjectVector',SceneHelper.workingProjectVector
                            scene.cursor.visible = 0
                            
                            
                            
                            if issubclass(type(m1.pick),Point):
                                listOfPointToMove.append(m1.pick)             
                                pick = vector(m1.pick.pos.x,m1.pick.pos.y,m1.pick.pos.z)
                                vectorOldPos = vector((m1.pick.pos.x,m1.pick.pos.y,m1.pick.pos.z))
                                UndoRedoManager.PushToUndoStack(MoveUndoRedo({m1.pick.id:vectorOldPos}))
                                
                            elif issubclass(type(m1.pick),Segment):
                                listOfPointToMove.append(m1.pick.GetParent(0))
                                listOfPointToMove.append(m1.pick.GetParent(1))             
                                pick = vector(m1.pick.pos.x,m1.pick.pos.y,m1.pick.pos.z)
                                vectorPoint0 = vector((m1.pick.GetParent(0).pos.x,m1.pick.GetParent(0).pos.y,m1.pick.GetParent(0).pos.z))
                                vectorPoint1 = vector((m1.pick.GetParent(1).pos.x,m1.pick.GetParent(1).pos.y,m1.pick.GetParent(1).pos.z))
                                UndoRedoManager.PushToUndoStack(MoveUndoRedo({m1.pick.GetParent(1).id:vectorPoint1,m1.pick.GetParent(0).id:vectorPoint0}))
                            elif issubclass(type(m1.pick),Plane):
                                listOfPointToMove.append(m1.pick.GetParent(0))
                                listOfPointToMove.append(m1.pick.GetParent(1))
                                listOfPointToMove.append(m1.pick.GetParent(2))             
                                pick = vector(m1.pick.GetParent(0).pos.x,m1.pick.GetParent(0).pos.y,m1.pick.GetParent(0).pos.z)
                                vectorPoint0 = vector((m1.pick.GetParent(0).pos.x,m1.pick.GetParent(0).pos.y,m1.pick.GetParent(0).pos.z))
                                vectorPoint1 = vector((m1.pick.GetParent(1).pos.x,m1.pick.GetParent(1).pos.y,m1.pick.GetParent(1).pos.z))
                                vectorPoint2 = vector((m1.pick.GetParent(2).pos.x,m1.pick.GetParent(2).pos.y,m1.pick.GetParent(2).pos.z))
                                UndoRedoManager.PushToUndoStack(MoveUndoRedo({m1.pick.GetParent(0).id:vectorPoint0,m1.pick.GetParent(1).id:vectorPoint1,m1.pick.GetParent(2).id:vectorPoint2}))
                            if LabelHelper.showLabels == True:
                                LabelHelper.HideLabels(True)
                            LabelHelper.ShowLabel(pick,m1.pick.name+str(pick))
                                
                            #Object3DDictionary.values(),True)
                            
                             
    
            elif m1.drop:
#                if SceneHelper.lockedRotation:
#                    SceneHelper.setNewForwardVectorA(SceneHelper.projectPlane.bxc,False,pi/16)
                if Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==2:
                    SceneHelper.setNewForwardVectorA(vector(1,0,0),False,0.1)
                    SceneHelper.workingProjectVector =vector(1,0,0)
                elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==3:
                    SceneHelper.setNewForwardVectorA(vector(0,1,0),False,0.1)
                    SceneHelper.workingProjectVector =vector(0,1,0)
                elif Man3dCommand.ForwardVector1_OYZ2_OXZ3_OXY4.get()==4:
                    SceneHelper.setNewForwardVectorA(vector(0,0,1),False,0.1)
                    SceneHelper.workingProjectVector =vector(0,0,1)
                specialElement = False 
                pick = None 
                scene.cursor.visible = 1
                LabelHelper.HideLabel()
                LabelHelper.ShowLabels()
###                if ModifiedObserverHelpsForLables.isModified :
###                    LabelHelper.ShowLabels()#Object3DDictionary.values())
###                    ModifiedObserverHelpsForLables.isModified = False 

            if m1.press=="left":                
                if m1.alt == True:
                                   
                    if m1.pick in Object3DDictionary.values() and issubclass(type(m1.pick) , Segment):
                       # print 'in 1stif'
                        TwinkerHelper.Twinkle(m1.pick,m1.pick.name)
                        lengthOfSegment = mag(m1.pick.axis)
                        lengthOfProp = mag(m1.pickpos - m1.pick.pos)
                        Generator.CreatePointBySegment(lengthOfProp/lengthOfSegment,m1.pick)
                    elif m1.pick in Object3DDictionary.values() and issubclass(type(m1.pick) , Plane):
                        
                        
                       # print 'before',m1.pick.bxc
                        new_posOnPlane = scene.mouse.project(m1.pick.bxc,point = m1.pick.A)
                       # print 'after',m1.pick.bxc
                        
                        Generator.CreatePointByPlane(m1.pickpos,m1.pick)
                        
                        
                    elif(m1.pick not in Object3DDictionary.values()):
                        
                        new_position = scene.mouse.project(SceneHelper.workingProjectVector,point = vector(0,0,0))
                        Generator.CreatePointByPosition(new_position)
#                    elif not m1.pick in Object3DDictionary.values():
#                        print 'in 2ndif',m1.pickpos,scene.forward,mag(scene.forward)
#                        if SceneHelper.isSetProjectionPlane == False:
#                            new_position = scene.mouse.project(scene.forward,point = -scene.forward)
#                        else:
#                            new_position = scene.mouse.project(SceneHelper.projectionVector,point = SceneHelper.projectionPoint)
#                        Generator.CreatePointByPosition(new_position)
                else:    
                   # print 'you are in else of press'
                    if m1.shift==0 and m1.pick :#shift==1 CHANGED TO shift==0 2007 JULY 18
                        if m1.pick in Object3DDictionary.values():# in object3D:                 
                            if  (not (m1.pick in selected3DObject)): 
                                setSelectedColor(m1.pick)
                                selected3DObject.append(m1.pick)
    
                            elif(m1.pick in selected3DObject):
                                setUnselectedColor(m1.pick)                                 
                                selected3DObject.remove(m1.pick)
                            
                                        
                if m1.pick and m1.ctrl==1:
                    pass
                if (not (m1.pick in Object3DDictionary.values())) and (m1.shift==0 and m1.ctrl==0):
                    for point in selected3DObject:
                        setUnselectedColor(point)
                    selected3DObject.freeSelectedObjects()# = []
                    
                if m1.click and m1.pick:
                    pass
        if pick:
                
            new_pos = scene.mouse.project(SceneHelper.workingProjectVector,point = SceneHelper.projectionPoint)

            if new_pos != drag_pos:
                for objectInList in listOfPointToMove:
                    objectInList.pos += new_pos - drag_pos
                    objectInList.RedrawChildDynamics(True) 
                pick += new_pos - drag_pos 
                #pick.RedrawChildDynamics(True)    
                drag_pos = new_pos
                LabelHelper.ShowLabel(pick,m1.pick.name+str(pick))



    
def startVpythonScene(scene_x,scene_y,scene_width,scene_height, textTitle):
    scene.x = scene_x
    scene.y=scene_y
    scene.width = scene_width
    scene.height = scene_height
    scene.forward = (-1,-0.25,-1)
    scene.title = textTitle
    scene.autoscale = 0
    Man3dCommand.ShowCoordinateSystemCommand()
    scene.visible = True
    
def startProgram(root):     
        
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    GuiMan=GuiMan3D(root)
    

    root_x = 0
    root_y = 0
    root_width = int(GuiMan.sizeOfWindow)
    root_height = screen_height-63
    
    rootGeometryString = str(root_width) + 'x'+str(root_height)+'+'+str(root_x)+'+'+str(root_y)
    
    scene_x = root_width+4
    scene_y = 0
    scene_width = screen_width - root_width
    scene_height = screen_height
    
    startVpythonScene(scene_x, scene_y, scene_width, scene_height, "MAN 3D, by the creators: M = Mihail Atanasov,A = Andrey Antonov,N = Nikolay Atanasov")
    
    root.title("Man3D ver2.0.3")
    root.geometry(rootGeometryString)
    

    
if __name__ == '__main__':
    scene.title = 'MAN3D'
    scene.autoscale = 0
    root = Tk()
    startProgram(root)
    
    thread.start_new_thread(SelectFunction,())
   # time.sleep(1)#this sleep helps for working exit from GUI
    thread.start_new_thread(pickKeyboard,())
    
    root.mainloop()
    
