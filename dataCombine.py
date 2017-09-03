import sqlite3


conn = sqlite3.connect(" user_ID_Nick15.db")
conn.isolation_level = None					# Without transaction, set a auto Commit
cur = conn.cursor()
print("Success connect user_ID_Nick15.db DB file")

try:
	createTableQuery = "CREATE TABLE User(summonerId varchar(12) primary key, summonerName varchar(60));"
	cur.execute(createTableQuery)
	print("Success make Table")
except Exception as e:
	print(e)


def combineData(number):

	path = "opgg"+number+".db"

	conn2 = sqlite3.connect(path)
	conn2.isolation_level = None
	cur2 = conn2.cursor()
	print("Success connect " + path + " DB file")

	cur2.execute('SELECT * FROM User WHERE NOT summonerName LIKE "IS%" and NOT summonerName LIKE "%_DEL"')
	#cur2.execute("SELECT * FROM User")
	rows = cur2.fetchall()

	for row in rows:
		try:
			cur.execute("INSERT INTO User VALUES(?, ?)", row)
			print("input data : %s // %s")%(row[0], row[1])
		except Exception as err:
			print(err)
			continue

def main():
	for i in range(1, 23):
		number = str(i)
		combineData(number)

if __name__ == '__main__':
	main()