"""
Database initialization and utility module.
"""

import ssl

from motor import motor_asyncio

from vitaltrack import config


class DatabaseManager:
    client: motor_asyncio.AsyncIOMotorClient = None
    db: motor_asyncio.AsyncIOMotorDatabase = None

    def connect_to_cluster(self, url: str, db_name: str | None = None):
        self.client = motor_asyncio.AsyncIOMotorClient(
            url,
            minPoolSize=config.MIN_CONNECTIONS_COUNT,
            maxPoolSize=config.MAX_CONNECTIONS_COUNT,
            uuidRepresentation="standard",
            # !Remove
            tlsAllowInvalidCertificates=True,
        )
        if db_name:
            self.db = self.client[db_name]

    def close_cluster_connection(self):
        self.client.close()

    def connect_to_database(self, db_name: str):
        self.db = self.client[db_name]

    async def get_collection(
        self, collection: str
    ) -> motor_asyncio.AsyncIOMotorCollection:
        return self.db[collection]


async def get_database_manager() -> DatabaseManager:
    return global_db_manager


global_db_manager = DatabaseManager()
