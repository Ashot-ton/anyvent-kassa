from xmlrpc import client as xmlrpclib

##################################################
#  XMLRPC client used to connect to odoo client  #
##################################################

#  DB info

url = 'http://127.0.0.1:8071'
db = 'pos-db'
username = 'ehb@ehb'
password = '123'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

uid = common.login(db, username, password)


#  Search and read records

result = models.execute(db, uid, password, 'res.partner', 'search_read', [['id', '=', 1]])
number_of_customers = models.execute(db, uid, password, 'res.partner', 'search_count', [])

print('Number of customers: ' + str(number_of_customers))
print('result: ' + str(result[0].get('name')))


#  Create records

id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
	'name':"New Partner",
}])


#  Update records

models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {
    'name': "Newer partner"
}])

# get record name after having changed it

models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])


#  Delete records

models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])

# check if the deleted record is still in the database

models.execute_kw(db, uid, password,
    'res.partner', 'search', [[['id', '=', id]]])
