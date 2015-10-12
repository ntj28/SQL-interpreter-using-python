# Checks if the tables and columns are valid
def checkSemantics(query,data,tb):
	cols_tb = []
	cols_query = []
	tableName = ""
	error = ""
	if(query[0].lower() == "update"):
		tableName = query[1]
		error = checkTable(tableName,tb)							# check if table exists
		if(error == False):
			cols_tb = getColumnsFromMetadata(tableName,tb)			# gets list of columns from metadata
			cols_query = getColumnsFromQuery(query,"update")		# gets list of columsn from query
			error = checkColumns(cols_query,cols_tb)				# check if columns exists
			if(error == False and ("where" in query or "WHERE" in query)):
				wIndex = getWhereIndex(query)
				cols_query = getColumnsFromWhereQuery(query[wIndex+1:])
				error = checkColumns(cols_query,cols_tb)			# check if columns in where clause exists
				if(error == False):
					error = checkColumnValues(tableName,tb,query[3:wIndex])		# check columns values of set clause
					if(error == False):
						return (checkColumnValues(tableName,tb,query[wIndex+1:]),"value")	# check columns values of where clause
					else:
						return error,"value"
			elif(error == False and not ("where" in query or "WHERE" in query)):
				return (checkColumnValues(tableName,tb,query[3:]),"value")		# check columns values of where clause
			else:
				return error,"column"										# error on column name
		else:
			return error,"table"											# error on table name
	elif(query[0].lower() == "delete"):	
		tableName = query[2]
		error = checkTable(tableName,tb)
		if(error == False and ("where" in query or "WHERE" in query)):
			wIndex = getWhereIndex(query)
			cols_tb = getColumnsFromMetadata(tableName,tb)					# gets list of columns from metadata
			cols_query = getColumnsFromWhereQuery(query[wIndex+1:])
			error = checkColumns(cols_query,cols_tb)						# check if columns in where clause exists
			if(error == False):
				return (checkColumnValues(tableName,tb,query[wIndex+1:]),"value")	# check columns values of where clause
			else:
				return error,"column"
		else:
			return error,"table"
	elif(query[0].lower() == "desc"):
		tableName = query[1]	
		return (checkTable(tableName,tb),"table")

# Gets the index of the WHERE keyword
def getWhereIndex(query):
	if("where" in query):
		return(query.index('where'))
	else:
		return(query.index('WHERE'))

# Checks whether the table exists
def checkTable(tableName,tb):
	if(tableName in tb.keys()):
			return False
	return tableName

# Gets the Columns of a table from metadata
def getColumnsFromMetadata(tableName,tb):
	cols_tb = []
	temp = tb[tableName]
	for i in temp.keys():
		cols_tb.append(temp[i][0])		#index zero since 1st element is columnName
	return cols_tb

# Gets the Columns of a table from query
def getColumnsFromQuery(query,statement):
	cols_query = []
	if(statement == "update"):
		i = 3
		if("where" in query or "WHERE" in query):
			wIndex = getWhereIndex(query)
			while(i < wIndex):
				cols_query.append(query[i])
				i+=4
		else:
			while(i < len(query)):
				cols_query.append(query[i])
				i+=4

	return cols_query

# Gets the Columns of a table from wherequery
def getColumnsFromWhereQuery(query):
	cols_query = []
	i=0
	while(i < len(query)):
		cols_query.append(query[i])
		i+=4
	return cols_query

# Checks whether the columns exist
def checkColumns(cols_query,cols_tb):
	i = 0
	while(i < len(cols_query)):
		if(cols_query[i] not in cols_tb):
			return cols_query[i]
		i += 1

	return False

# Checks whether the type of values are appropriate for the column
def checkColumnValues(tbl,tb,changeList):
	i = 0
	while(i < len(changeList)):
		if(getType(tb,tbl,changeList[i]) == "varchar" or getType(tb,tbl,changeList[i]) == "date"):
			if("'" in str(changeList[i+2]) or '"' in str(changeList[i+2])):
				return False
			else:
				return str(changeList[i+2])
		else:
			if("'" in str(changeList[i+2]) or '"' in str(changeList[i+2])):
				return str(changeList[i+2])
			else:
				return False
		i+=4

# Returns the data type of the column
def getType(tb,tbl,col):
	i = 0
	while(i<5):
		if(col == tb[tbl][i][0]):
			return tb[tbl][i][1]
		i+=1