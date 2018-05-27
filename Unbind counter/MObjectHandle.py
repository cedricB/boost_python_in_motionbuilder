"""
    MIT License

    L I C E N S E:
        Copyright (c) 2018 Cedric BAZILLOU All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
    and associated documentation files (the "Software"), to deal in the Software without restriction,
    including without limitation the rights to use, copy, modify, merge, publish, distribute,
    sublicense, and/or sell copies of the Software,and to permit persons to whom the Software 
    is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies 
    or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

    https://opensource.org/licenses/MIT
"""

import pyfbsdk

class ModelHandle(object):
    """
        utility class for pyfbsdk.FBBModel:
            -support storing of object in pyside tool in a transparent manner.
            -Undo and unbind error will get taken care of transparently

        example use:
            #Find your transfrom from its name
            cubeNode = pyfbsdk.FBFindModelByLabelName('Cube')

            #Create an handle instance
            handleUtils = ModelHandle(cubeNode)
            
            #Retrieve your node
            cubeNode = handleUtils.getNode()
            print cubeNode
    """
        
    UNDO_STATUS = pyfbsdk.FBObjectStatus.kFBStatusOwnedByUndo

    def __init__(self, model):
        """
            args:
                model(pyfbsdk.FBBModel).[or any element deriver from FBModel - ie FBModelNull]
        """
        self.__model__ = None
        
        self.isValid = False

        if not isinstance(model,
                          pyfbsdk):
            return

        self.initialize(model)

    def initialize(self,
                   model):
        """
            args:
                model(pyfbsdk.FBBModel).[or any element deriver from FBModel - ie FBModelNull]
        """
        self.__model__ = model
        
        self.isValid = True
        
        self.__model__.OnUnbind.Add(self.resetModel)

    def clear(self):
        self.__model__.OnUnbind.Remove(self.resetModel)
        self.isValid = False
        self.__model__ = None

    def getNode(self):
        """
            return:
               (pyfbsdk.FBBModel). when node is valid
               
               None in all other cases.
        """
        if self.__model__ is None:
            self.isValid = False

            return None

        if self.__model__.__class__.__name__.endswith('_Unbound'):
            self.clear()

            return None
            
        if not self.__model__.GetObjectStatus(self.UNDO_STATUS):
            self.isValid = True

            return self.__model__

        if not self.__model__.GetDstCount():
            return None

        return None
    
    def resetModel(self, control, event):
        """
            When a new scene is opened or the undo queue is cleared 
            the OnUnbind callback will be triggered and we will be able to clean up our
            node reference.
        """
        self.clear()
