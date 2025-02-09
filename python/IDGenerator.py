class IDGenerator:

    current = 1
    
    ids = {}    
    maxID = 100
    for index in range (maxID):
        ids[index+1] = False    

    @staticmethod
    def _next():
        
        if(IDGenerator.current == -1):
            for index in range(1, IDGenerator.maxID+1):
                if(not IDGenerator.ids[index]):
                    
                    IDGenerator.current = index
                    return True
        else:
            for index in range(IDGenerator.current, IDGenerator.maxID):
                
                if(not IDGenerator.ids[index+1]):                
                    
                    IDGenerator.current = index+1
                    return True
            for index in range(1, IDGenerator.current):
                
                if(not IDGenerator.ids[index]):
                    IDGenerator.current = index
                    return True
            IDGenerator.current = -1
            return False
    
    @staticmethod
    def GetNext():
         
        if(IDGenerator.current!=-1):
            newId = IDGenerator.current
            IDGenerator.ids[newId] = True;
            
            IDGenerator._next()
            
            return newId
        else:
            IDGenerator._next()
            if(IDGenerator.current == -1):
                return -1
            newId = IDGenerator.current
            IDGenerator.ids[newId] = True;
            IDGenerator._next()
            return newId
            #IDGenerator.MoveToNextFreeID()

        
    @staticmethod
    def HasID():
        for index in range(1, IDGenerator.maxID+1):
            if(not IDGenerator.ids[index]):
                return True
        
        return False
    
    @staticmethod
    def DeleteByID(GenID):
        if(IDGenerator.ids[GenID] == True):
            IDGenerator.ids[GenID] = False
            return True
        else:
            #print "the id is free"
            return False

    @staticmethod
    def IncreaseLimitBy(additionIdNumbers):
        for index in range(IDGenerator.maxID, IDGenerator.maxID + additionIdNumbers):
            IDGenerator.ids[index+1] = False

        IDGenerator.maxID = IDGenerator.maxID + additionIdNumbers
        
    @staticmethod        
    def TestGenerator1():
        print "current : ",IDGenerator.current
        print "-----------------------"
        print "TakeId():",IDGenerator.GetNext()
        print "-----------------------"
        print "IDs", IDGenerator.ids
        print "-----------------------"
        print "current : ",IDGenerator.current
        print "-----------------------"
        print "TakeId():",IDGenerator.GetNext()
        print "-----------------------"
        print "IDs", IDGenerator.ids
        print "-----------------------"
        print "current : ",IDGenerator.current
        print "-----------------------"
        print "TakeId():",IDGenerator.GetNext()
        print "-----------------------"
        print "IDs", IDGenerator.ids
        print "-----------------------"
        print "current : ",IDGenerator.current
        print "-----------------------"
        print "ReleaseID(3)", IDGenerator.DeleteByID(3)
        print "-----------------------"
        print "IDs", IDGenerator.ids
        print "-----------------------"
        print "MoveToNextFreeID()", IDGenerator.GetNext()
        print "-----------------------"
        print "IDs", IDGenerator.ids
        print "-----------------------"    
        print "current : ",IDGenerator.current
        print "-----------------------"
        print "ReleaseID(2)", IDGenerator.DeleteByID(2)
        print "-----------------------"
        print "IDs", IDGenerator.ids
        print "-----------------------"
        print "current : ",IDGenerator.current
        print "-----------------------"
        print "TakeId():",IDGenerator.GetNext()
        print "-----------------------"
        print "IDs", IDGenerator.ids
        print "-----------------------"
        print "current : ",IDGenerator.current
        print "-----------------------"
        print "HasFreeID()",IDGenerator.HasID()
        IDGenerator.IncreaseLimitBy(5)


#IDGenerator.TestGenerator1()
        
        
        
