from __future__ import print_function
from datetime import date, datetime, timedelta
import time
import bcrypt

import Database

query = ("SELECT id, password, administrator FROM Users WHERE username = %s")
adminQuery = ("SELECT administrator FROM Users WHERE id = %s")
privalegedQuery = ("SELECT privaleged FROM Users WHERE id = %s")
recentUsersQuery = ("SELECT id, username FROM Users ORDER BY creationDate DESC LIMIT 5")
updateToAdministrator = ("UPDATE Users SET administrator = 1 WHERE id = %s")
updateToPrivaleged = ("UPDATE Users SET privaleged = 1 WHERE id = %s")
jobLimitQuery = ("SELECT jobLimit FROM Users WHERE id = %s")
updateJobLimit = ("UPDATE Users SET jobLimit = %s WHERE id = %s")
userJobCountQuery = ("SELECT COUNT(*) FROM Jobs WHERE userId = %s")
userJobStatusCountQuery = ("SELECT COUNT(*) FROM Jobs WHERE userId = %s AND status = %s")
userIDQuery = ("SELECT id FROM Users WHERE username = %s")


def getRecentlyAddedUsers():
	connection = Database.pool.get_connection()

	result = []

	with connection.cursor() as cursor:
		cursor.execute(recentUsersQuery)
		result = cursor.fetchall()
	
	connection.close()

	usernames = []

	for user_id, username in result:
		usernames.append(username)

	return usernames

def checkIfAdmin(user_id):
	connection = Database.pool.get_connection()

	result = None
	with connection.cursor() as cursor:
		cursor.execute(adminQuery, (user_id,))
		result = cursor.fetchone()

	connection.close()

	if result is not None:
		return result[0]
	else:
		return False

def checkIfPrivaleged(user_id):
	connection = Database.pool.get_connection()

	result = None
	with connection.cursor() as cursor:
		cursor.execute(privalegedQuery, (user_id,))
		result = cursor.fetchone()

	connection.close()

	if result is not None:
		return result[0]
	else:
		return False

def promoteToAdmin(user_id):
	connection = Database.pool.get_connection()

	with connection.cursor() as cursor:
		cursor.execute(updateToAdministrator, (user_id,))

	connection.close()

def promoteToPrivaleged(user_id):
	connection = Database.pool.get_connection()

	with connection.cursor() as cursor:
		cursor.execute(updateToPrivaleged, (user_id,))

	connection.close()

def getJobLimit(user_id):
	connection = Database.pool.get_connection()
	result = None

	with connection.cursor() as cursor:
		cursor.execute(jobLimitQuery, (user_id,))
		result = cursor.fetchone()
	connection.close()

	if result is not None:
		return result[0]
	else:
		return 0

def setJobLimit(user_id, jobs):
	connection = Database.pool.get_connection()

	with connection.cursor() as cursor:
		cursor.execute(updateJobLimit, (jobs, user_id,))
	
	connection.close()

def getUserJobCount(user_id):
	connection = Database.pool.get_connection()

	result = None
	with connection.cursor() as cursor:
		cursor.execute(userJobCountQuery, (user_id,))
		result = cursor.fetchone()
	connection.close()

	if result is not None:
		return result[0]
	else:
		return 0

def getUserJobStatusCount(user_id, status):
	connection = Database.pool.get_connection()

	result = None
	with connection.cursor() as cursor:
		cursor.execute(userJobStatusCountQuery, (user_id, status,))
		result = cursor.fetchone()
	connection.close()

	if result is not None:
		return result[0]
	else:
		return 0

def getUserActiveJobCount(user_id):
	return getUserJobStatusCount(user_id, "Pending") + getUserJobStatusCount(user_id, "Running") + getUserJobStatusCount(user_id, "Suspended") + getUserJobStatusCount(user_id, "Completing")

def getID(username):
	connection = Database.pool.get_connection()

	result = None
	with connection.cursor() as cursor:
		cursor.execute(userIDQuery, (username.encode("utf-8"),))
		result = cursor.fetchone()
	connection.close()

	if result is not None:
		return result[0]
	else:
		return 0

#loginUser("david", "pass1234")