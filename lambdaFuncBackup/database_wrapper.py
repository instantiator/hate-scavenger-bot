import boto3
from typing import Dict, Any, List


class Db():
    """
    Very simple class that is a wrapper for dynamodb. 
    """
    
    def __init__(self, logger):
        self.db = boto3.resource('dynamodb')
        self.logger = logger
        
        self.logger.info("DynamoDB client ready")
    
        
    def add_to_database(self, item: Dict[str, Any], table_name:str):
        #self.logger.info(f"Attempting to add item into {table_name}.")
        
        table = self.db.Table(table_name)
        response = table.put_item(Item=item)
        return response
        
    def add_to_database_as_batch(self, items: List[Dict[str, Any]], table_name:str):
        #self.logger.info(f"Attempting to add item into {table_name} (as a 'batch write' process)")
        table = self.db.Table(table_name)
        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
        
    def read_from_database(self, key_id, key_value, table_name) -> Dict[Any, Any]:
        table = self.db.Table(table_name)
        response = table.get_item(Key={key_id: key_value})
        return response