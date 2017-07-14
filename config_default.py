
def generateConnectioString():
	conn = 'mysql+mysqldb://{}:{}@{}/{}'.format(mysql_user, mysql_password, 
								mysql_host, mysql_db_name)
	return conn

mysql_host = 'localhost'

mysql_db_name = 'langconnector'

mysql_user = 'lang'

mysql_password = 'lang'
