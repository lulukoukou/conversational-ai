
# coding: utf-8

# In[1]:


# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html
# As explained in the tutorial:
#     get the Access key ID,Secret access key from the IAM console
#     install awscli with conda or pip
#     run aws configure command
#     install the boto3 package
#Before running the ipython:
#     cd ~/usr/DynamoDB/dynamodb_local_latest/
#     java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb


# In[26]:

import sys

sys.path.append("verification/verification1/")

import boto3
from   botocore.exceptions import ClientError
from   boto3.dynamodb.conditions import Key, Attr
import json
import decimal
import random

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
    
class db:
    dynamodb = None
    debug = True
    last_index = 0
    
    def __init__(self):
        #self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000") 
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 
        #self.last_index = self.get_table('Indexes').item_count
        self.last_index = 9

    def create_table(self, TableName, KeySchema, AttributeDefinitions, ProvisionedThroughput):
        table = self.dynamodb.create_table(TableName=TableName,
                                      KeySchema=KeySchema,
                                      AttributeDefinitions=AttributeDefinitions,
                                      ProvisionedThroughput=ProvisionedThroughput)
        return table
    
    def get_table(self, TableName):
        return self.dynamodb.Table(TableName)
        
    def put_item(self, TableName, Item):
        table = self.get_table(TableName)
        return table.put_item(Item=Item)
    
    def get_item(self, TableName, Key):
        table = self.get_table(TableName)
        return table.get_item(Key=Key)
    
    def update_item(self, TableName, Key, UpdateExpression, ExpressionAttributeValues, ReturnValues):
        table = self.get_table(TableName)
        return table.update_item(Key= Key,
                                 UpdateExpression= UpdateExpression,
                                 ExpressionAttributeValues= ExpressionAttributeValues,
                                 ReturnValues= ReturnValues)
    
    def update_item_cond(self, TableName, Key, UpdateExpression, ExpressionAttributeValues, ReturnValues, ConditionExpression):
        table = self.get_table(TableName)
        return table.update_item(Key= Key,
                                 UpdateExpression= UpdateExpression,
                                 ConditionExpression= ConditionExpression,
                                 ExpressionAttributeValues= ExpressionAttributeValues,
                                 ReturnValues= ReturnValues)
    
    def delete_item(self, TableName, Key, ConditionExpression, ExpressionAttributeValues):
        table = self.get_table(TableName)
        return table.update_item(Key= Key,
                                 ConditionExpression= ConditionExpression,
                                 ExpressionAttributeValues= ExpressionAttributeValues)
    
    def query(self, TableName, KeyConditionExpression):
        table = self.get_table(TableName)
        return table.query(KeyConditionExpression= KeyConditionExpression)
    
    def query_cond(self, TableName, ProjectionExpression, ExpressionAttributeNames, KeyConditionExpression):
        table = self.get_table(TableName)
        return table.query(ProjectionExpression= ProjectionExpression,
                           ExpressionAttributeNames= ExpressionAttributeNames,
                           KeyConditionExpression= KeyConditionExpression)
    
    def delete(self, TableName):
        table = self.get_table(TableName)
        return table.delete()
    
    def create_words_table(self):
        #create a table
        #TableName – Name of the table.
        #KeySchema – Attributes that are used for the primary key.
        #AttributeDefinitions – Data types for the key schema attributes.
        #ProvisionedThroughput – Number of reads and writes per second that you need for this table.
        #create an 'Indexes' table to store a unique index for each word
        #this table will be used in selecting a random word.
        IndexTableName = 'Indexes'
        WordTableName = 'Words'
        
        KeySchema=[{'AttributeName': 'index','KeyType': 'HASH'}] #Partition key
        AttributeDefinitions=[{'AttributeName': 'index','AttributeType': 'N'}]
        ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
        try:
            table = self.create_table(IndexTableName, KeySchema, AttributeDefinitions, ProvisionedThroughput)
        except ClientError as e:
            if(self.debug):
                print(e.response['Error']['Message'])
                return False
        else:
            if(self.debug):
                print("Index Table status:", table.table_status)
                
               
        KeySchema=[{'AttributeName': 'word','KeyType': 'HASH'}] #Partition key
        AttributeDefinitions=[{'AttributeName': 'word','AttributeType': 'S'}]
        ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
        try:
            table = self.create_table(WordTableName, KeySchema, AttributeDefinitions, ProvisionedThroughput)
        except ClientError as e:
            if(self.debug):
                print(e.response['Error']['Message'])
            return False
        else:
            if(self.debug):
                print("Word Table status:", table.table_status)
            return True
        
        
    def add_word(self, word):
        #add an item to word table
        #check if the word is already in database
        KeyConditionExpression=Key('word').eq(word)
        #response = database.query('Words', KeyConditionExpression)
        response = self.query('Words', KeyConditionExpression)
        if (len(response['Items']) != 0):
            if(self.debug):
                print(word, "exist in database")
        else:
            response = self.put_item("Words", {'word': word, 'info':{'def':[], 'syn':[], 'exa':[]}})
            response = self.put_item("Indexes", {'index': self.last_index, 'word':word})
            self.last_index += 1
            if(self.debug):
                print(word, "added successfully.")

    def get_random_word(self, userId):
        words = self.getUserData(userId)
        if (len(words) >= self.last_index):
            #words = [words[-1]]
            words = []
            self.delUserData(userId)
            
        
        # tried_indexes = []
        # while (len(tried_indexes) < self.last_index):
        #     rand_index = random.randrange(self.last_index)
        #     if rand_index not in tried_indexes:
        #         tried_indexes.append(rand_index)
        #         response = self.get_item("Indexes", {'index': rand_index})
        #         word = response['Item']['word']
        #         if (word not in words):
        #             self.addUserData(userId, word)
        #             return word 
        
        rand_index = len(words)    
        response = self.get_item("Indexes", {'index': rand_index})
        word = response['Item']['word']
        self.addUserData(userId, word)
        return word
    
    def update_word(self, word, info):
        TableName = "Words"
        key={'word': word}
        UpdateExpression="set info.def = :d, info.syn=:s, info.exa=:e"
        ExpressionAttributeValues={
                ':d': info['def'],
                ':s': info['syn'],
                ':e': info['exa']
            }
        ReturnValues="UPDATED_NEW"
        try:
            #response = database.update_item(TableName, key, UpdateExpression, ExpressionAttributeValues, ReturnValues)
            response = self.update_item(TableName, key, UpdateExpression, ExpressionAttributeValues, ReturnValues)
        except:
            if(self.debug):
                print("Update failed.")
        else:
            if(self.debug):
                print("Update succeeded.")
                #print(json.dumps(response, indent=4, cls=DecimalEncoder))
                
    def get_word_info(self, word):
        key={'word': word}
        #response = database.get_item("Words", key)
        response = self.get_item("Words", key)
        try:
            item = response['Item']
        except:
            if(self.debug):
                print("GetItem failed.")
            return None
        else:
            if(self.debug):
                print("GetItem succeeded:")
                #print(json.dumps(response['Item'], indent=4, cls=DecimalEncoder)) 
            return response['Item']['info']
        
    def add_syn(self, word, syn):
        info = self.get_word_info(word)
        if (info != None):
            if (syn not in info['syn']):
                info['syn'].append(syn)
                return self.update_word(word, info)
            else:
                if(self.debug):
                    print('synonym is already in database.')
        else:
            return None
        
    def add_def(self, word, definition):
        info = self.get_word_info(word)
        if (info != None):
            if (definition not in info['def']):
                info['def'].append(definition)
                return self.update_word(word, info)
            else:
                if(self.debug):
                    print('synonym is already in database.')
        else:
            return None   
        
    def add_example(self, word, example):
        info = self.get_word_info(word)
        if (info != None):
            if (example not in info['exa']):
                info['exa'].append(example)
                return self.update_word(word, info)
            else:
                if(self.debug):
                    print('synonym is already in database.')
        else:
            return None         
         
    def create_users_table(self):
        UserTableName = 'Users'
        
        KeySchema=[{'AttributeName': 'userId','KeyType': 'HASH'}] #Partition key
        AttributeDefinitions=[{'AttributeName': 'userId','AttributeType': 'S'}]
        ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
        try:
            table = self.create_table(UserTableName, KeySchema, AttributeDefinitions, ProvisionedThroughput)
        except ClientError as e:
            if(self.debug):
                print(e.response['Error']['Message'])
                return False
        else:
            if(self.debug):
                print("Table status:", table.table_status)

    def getUserData(self, userId):
        key={'userId': userId}
        response = self.get_item("Users", key)
        try:
            item = response['Item']
        except:
            self.addUser(userId)
            if(self.debug):
                print("new user")
            return []
        else:
            if(self.debug):
                print("returning user")
                #print(json.dumps(response['Item'], indent=4, cls=DecimalEncoder)) 
            return response['Item']['words']
        
    def addUser(self, userId):
        response = self.put_item("Users", {'userId': userId, 'words':[]})
        
    def addUserData(self, userId, word):
        words = self.getUserData(userId)
        if (word not in words):
            words.append(word)
        response = self.put_item("Users", {'userId': userId, 'words':words})

    def delUserData(self, userId):
        words = self.getUserData(userId)
        #words = [words[-1]]
        words = []
        response = self.put_item("Users", {'userId': userId, 'words':words})
