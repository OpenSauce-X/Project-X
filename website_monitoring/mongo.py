import pymongo

def initialize_database():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["website_monitoring"]

        # Create a collection for website data
        websites_collection = db["websites"]

        # Create a collection for performance data
        performance_collection = db["performance_data"]

        print("Collections created successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:    
        client.close()

if __name__ == "__main__":
    initialize_database()
