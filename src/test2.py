import pymongo


def main():
	client = pymongo.MongoClient('mongodb',27017)

	fruitsDB = client["fruitsDB"]

	fruitsCollection = fruitsDB["fruits"]

	fruitsCollection.insert_many([{"name": "orange", "color": "orange"},
								  {"name": "apple", "color": "red"}]);

	print(fruitsCollection)

	col = fruitsCollection.find()

	for x in col:
		print(x)

if __name__ == '__main__':
	main()