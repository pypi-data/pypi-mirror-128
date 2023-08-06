from pymongo import MongoClient as CLIENT, collation
import json,os
class Colors: fail = '\033[91m' ; good = '\033[92m' ; end = '\033[0m'
class MongodbPlus:
    def __init__(self,databaseName:str):
        self.thisDir = os.path.dirname(__file__)+'/'
        self.databaseName=databaseName
        self.__mongoClient = CLIENT("mongodb://localhost:27017/")
        self.__mongoDb = self.__mongoClient[databaseName]
        self.__wasCollectionSet__ = False
        defaultPath = f'{self.thisDir}__defaults__.json'
        # create default json file to store db information
        if not os.path.exists(defaultPath):
            open(defaultPath,'w').write('{}')
        self.defaultPath=defaultPath

    def setCollection(self,collectionName:str):
        self.collection = self.__mongoDb[collectionName]
        self.collectionName = collectionName
        self.__wasCollectionSet__ = True

    def showDatabases(self): return self.__mongoClient.list_database_names()

    def showCollections(self): return self.__mongoDb.list_collection_names()

    def count(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.count_documents(filter)
        return result

    def deleteOne(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.delete_one(filter)
        return result

    def deleteMany(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.delete_many(filter)
        return result

    def findOne(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.find_one(filter)
        return result

    def findMany(self,filter:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.find(filter)
        return result

    def updateOne(self,filter:dict={},newData:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.update_one(filter,{'$set':newData})
        return result

    def updateMany(self,filter:dict={},newData:dict={},collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        result = col.update_many(filter,{'$set':newData})
        return result

    def insertOne(self,document:dict={},collectionName:str='',checkDuplicate:bool=False,duplicateKey:str='',checkSchema=False):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        # get defaults info, if schema and lastId not found create a new one
        default = json.loads(open(self.defaultPath,'r').read())
        if collectionName not in default:
            collectionSchema={}
            for docName,docValue in document.items():
                schemaType = type(docValue).__name__
                collectionSchema[docName]=schemaType
            default[collectionName]={
                'lastId':0,
                'schema':collectionSchema
            }
        # if checking for collection schema
        if checkSchema:
            schema = default[collectionName]['schema']
            _document = document
            schemaLength = len(schema)
            docLength = len(document)
            if '_id' in document: docLength=docLength-1 ; del _document['_id']
            if schemaLength != docLength:
                print(f'{Colors.fail}Schema size supposed to be {schemaLength} and the document size is {docLength}{Colors.end}')
                print(f'{Colors.fail}Document size supposed to be {docLength} and the document size is {docLength}{Colors.end}')
                print(f'{Colors.fail}Schema: {schema}{Colors.end}')
                print(f'{Colors.fail}Document: {_document}{Colors.end}')
                return False
            # check for schema keys
            for Key,KeyValue in _document.items():
                if Key not in schema:
                    print(f'{Colors.fail}Key: "{Key}" not found in collection: "{collectionName}" schema{Colors.end}')
                    print(f'{Colors.fail}Schema: {schema}{Colors.end}')
                    print(f'{Colors.fail}Update schema file __defaults__.json or use schema keys and types: {schema}{Colors.end}')
                    print(f'{Colors.fail}Path: __defaults__.json = {self.thisDir}__defaults__.json{Colors.end}')
                    return False
                else:
                    schemaKeyValueType = schema[Key]
                    givenKeyValueType = type(KeyValue).__name__
                    if schemaKeyValueType != givenKeyValueType:
                        print(f'{Colors.fail}Key: "{Key}" expecting a "{schemaKeyValueType}" not "{givenKeyValueType}"{Colors.end}')
                        print(f'{Colors.fail}Schema: {schema}{Colors.end}')
                        print(f'{Colors.fail}Document: {_document}{Colors.end}')
                        return False
        # check if _id was given if yes check if it exists
        newId = default[collectionName]['lastId']+1
        # check if new id exists, if yes get a new one
        while True:
            if not col.find_one({'_id':newId}): break
            else: newId=newId+1
        # check if _id was given on document
        if '_id' in document:
            givenId=document['_id']
            if col.find_one({'_id':givenId}):
                print(f'{Colors.fail}Document with _id: {givenId} already exists when trying to insert {self.cuteME(document)}{Colors.end}') ; return False
        else:document['_id']=newId
        # if check duplicate is set to true
        if checkDuplicate:
            if not duplicateKey:
                print(f'{Colors.fail}DuplicateKey can not be empty if you setted checkDuplicate=True{Colors.end}')
                return False
            if duplicateKey not in document:
                print(f'{Colors.fail}DuplicateKey: {duplicateKey} not found in {self.cuteME(document)}{Colors.end}')
                return False
            if col.find_one({duplicateKey:document[duplicateKey]}):
                keyName,keyValue=duplicateKey,document[duplicateKey]
                print(f'{Colors.fail}Key: {keyName} with value: {keyValue} already exists{Colors.end}') ; return False
        # else insert
        result = col.insert_one(document)
        # update defaults
        default[collectionName]['lastId']=newId
        open(self.defaultPath,'w').write(json.dumps(default,indent=4))
        return result

    def insertMany(self,listOfDocuments:list=[],collectionName:str='',checkDuplicate:bool=False,duplicateKey:str='',checkSchema:bool=False):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        idsInserted=[]
        for document in listOfDocuments:
            # get defaults info, if schema and lastId not found create a new one
            default = json.loads(open(self.defaultPath,'r').read())
            if collectionName not in default:
                collectionSchema={}
                for docName,docValue in document.items():
                    schemaType = type(docValue).__name__
                    collectionSchema[docName]=schemaType
                default[collectionName]={
                    'lastId':0,
                    'schema':collectionSchema
                }
            # if checking for collection schema
            if checkSchema:
                schema = default[collectionName]['schema']
                _document = document
                schemaLength = len(schema)
                docLength = len(document)
                if '_id' in document: docLength=docLength-1 ; del _document['_id']
                if schemaLength != docLength:
                    print(f'{Colors.fail}Schema size supposed to be {schemaLength} and the document size is {docLength}{Colors.end}')
                    print(f'{Colors.fail}Document size supposed to be {docLength} and the document size is {docLength}{Colors.end}')
                    print(f'{Colors.fail}Schema: {schema}{Colors.end}')
                    print(f'{Colors.fail}Document: {_document}{Colors.end}')
                    return False
                # check for schema keys
                for Key,KeyValue in _document.items():
                    if Key not in schema:
                        print(f'{Colors.fail}Key: "{Key}" not found in collection: "{collectionName}" schema{Colors.end}')
                        print(f'{Colors.fail}Schema: {schema}{Colors.end}')
                        print(f'{Colors.fail}Update schema file __defaults__.json or use schema keys and types: {schema}{Colors.end}')
                        print(f'{Colors.fail}Path: __defaults__.json = {self.thisDir}__defaults__.json{Colors.end}')
                        return False
                    else:
                        schemaKeyValueType = schema[Key]
                        givenKeyValueType = type(KeyValue).__name__
                        if schemaKeyValueType != givenKeyValueType:
                            print(f'{Colors.fail}Key: "{Key}" expecting a "{schemaKeyValueType}" not "{givenKeyValueType}"{Colors.end}')
                            print(f'{Colors.fail}Schema: {schema}{Colors.end}')
                            print(f'{Colors.fail}Document: {_document}{Colors.end}')
                            return False
            # check if _id was given if yes check if it exists
            newId = default[collectionName]['lastId']+1
            # check if new id exists, if yes get a new one
            while True:
                if not col.find_one({'_id':newId}): break
                else: newId=newId+1
            # check if _id was given on document
            if '_id' in document:
                givenId=document['_id']
                if col.find_one({'_id':givenId}):
                    print(f'{Colors.fail}Document with _id: {givenId} already exists when trying to insert {self.cuteME(document)}{Colors.end}') ; return False
            else:document['_id']=newId
            # if check duplicate is set to true
            if checkDuplicate:
                if not duplicateKey:
                    print(f'{Colors.fail}DuplicateKey can not be empty if you setted checkDuplicate=True{Colors.end}')
                    return False
                if duplicateKey not in document:
                    print(f'{Colors.fail}DuplicateKey: {duplicateKey} not found in {self.cuteME(document)}{Colors.end}')
                    return False
                if col.find_one({duplicateKey:document[duplicateKey]}):
                    keyName,keyValue=duplicateKey,document[duplicateKey]
                    print(f'{Colors.fail}Key: {keyName} with value: {keyValue} already exists{Colors.end}') ; return False
            # insert document
            col.insert_one(document)
            idsInserted.append(newId)
            # update defaults
            default[collectionName]['lastId']=newId
            open(self.defaultPath,'w').write(json.dumps(default,indent=4))
        return {'idsInserted':idsInserted}
    
    def dropCollection(self,collections:list):
        for collectionName in collections:
            self.__mongoDb.drop_collection(collectionName)

    def export(self,exportToPath:str=''):
        collections = self.showCollections()
        collectionsList={}
        if collections:
            for collectionName in collections:
                # add colletion name to collection list to export
                collectionsList[collectionName]={}
                for item in self.findMany({},collectionName):
                    itemId = item['_id']
                    del item['_id']
                    collectionsList[collectionName][itemId]=item
        result = self.cuteME(collectionsList)
        if not exportToPath: open(f'{self.thisDir+self.databaseName}.json','w').write(result)
        else: open(f'{exportToPath+self.databaseName}.json','w').write(result)
        print(f'{Colors.good}collections in {self.databaseName} exported exportName:{self.databaseName}.json{Colors.end}')
        return True

    def Import(self,databasePath:str):
        # check if db path exits
        if not os.path.exists(databasePath):
            print(f'{Colors.fail}Path {databasePath} not found{Colors.end}')
            return False
        collections = json.loads(open(databasePath,'r').read())
        for collectionName,collectionItems in collections.items():
            # drop current collection if it exists
            if collectionName in self.showCollections(): self.dropCollection([collectionName])
            # insert item into current collection
            for itemId,itemData in collectionItems.items():
                itemData['_id']=int(itemId)
                self.C_O_L_L_E_C_T_I_O_N(collectionName).insert_one(itemData)
    
    def addKey(self,keyAndDefaultValue:dict,collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        # check if more than one key was given
        if len(keyAndDefaultValue) > 1:
            print(f'{Colors.fail}key and default value only take one key{Colors.end}')
            return False
        # get last id and last id data
        lastId = self.count({},collectionName)
        lastIdData = self.findOne({'_id':lastId})
        keyName,keyValue=list(keyAndDefaultValue)[0],keyAndDefaultValue[list(keyAndDefaultValue)[0]]
        # check if key name already exists in last id data
        if keyName in lastIdData:
            print(f'{Colors.fail}The key >> {keyName} << already exists{Colors.end}')
            return False
        # else run the code
        numUpdated=0
        allDocuments = self.findMany({},collectionName)
        for item in allDocuments:
            item[keyName]=keyValue
            # update current item
            self.updateOne({'_id':item['_id']},item)
            numUpdated=numUpdated+1
        print(f'{Colors.good}The key >> {keyName} << added to {numUpdated} documents{Colors.end}')
        return True

    def removeKey(self,keyName:str,collectionName:str=''):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        numUpdated=0
        allDocuments = self.findMany({},collectionName)
        for item in allDocuments:
            if keyName in item:
                # update current item
                col = self.C_O_L_L_E_C_T_I_O_N(collectionName)
                col.update_one({'_id':item['_id']},{'$unset': {keyName:{ '$exists':True}}})
                numUpdated=numUpdated+1
        print(f'{Colors.good}{numUpdated} documents where updated{Colors.end}')
        return True

    def aggregate(self,pipeLine:list,collectionName:str):
        # check if collection name was setted
        if collectionName: collectionName=collectionName
        elif self.__wasCollectionSet__: collectionName=self.collectionName
        else: self.__printCollectionNameError__() ; return False
        col = self.__mongoDb[collectionName]
        return col.aggregate(pipeLine)

    def C_O_L_L_E_C_T_I_O_N(self,collectionName:str): return self.__mongoDb[collectionName]
    def M_O_N_G_O_C_L_I_E_N_T(self): return self.__mongoClient
    def __printCollectionNameError__(self):
        print(f'{Colors.fail}Set collection .setCollection(name) before runnig this function or set the collectionName:str{Colors.end}')
    def cuteME(self,data): return json.dumps(data,indent=4)