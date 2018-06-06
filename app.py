from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import date

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)

#
#  How to create / define a table, name of the class = name of the table
#

class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), unique=True)
	password = db.Column(db.String(30))
	email = db.Column(db.String(50))
	join_date = db.Column(db.DateTime)

	orders = db.relationship('Order', backref='member', lazy='dynamic')  # backref is like a virtual column in the other table, lazy = dynamic(standard)


	def __repr__(self):
		return '<Member %r>' % self.username



# Third Table for relationships exemple
#
class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Integer)
	member_id = db.Column(db.Integer, db.ForeignKey('member.id')) # dynamic relationship (one to many) made using db.ForeignKey to point to member_id! easy



@app.route('/add_user')
def index():
	add_new_user('aaaaaaaaaaaaa', 'pass', 'email')
	return 'Success'


#
# Exemple of adding (INSERT New row) inside the a table.
#
def add_new_user(username, password, email):

	new_user = Member(username=username, password=password, email=email, join_date='2018-06-06')

	# new_user = Member(username= 'William', password='secret', email='jordan@alchemistware.com', date=date)
	# new_user = Member(username= 'Jordan', password='secret', email='jordan@alchemistware.com', date=date)

	db.session.add(new_user)
	db.session.commit()


# add order with a relationship to a member (one to many)
def add_new_order(price, member_id):

	new_order = Order(price=price, member_id=member_id)


	db.session.add(new_order)
	db.session.commit()




def get_list_of_user():
	results = Member.query.all()  # Query all the members in the table

	#list them
	for user in results:
		print(user.username + ':' + user.email)



def get_specific_member_informations(member_username):
	current_user = Member.query.filter(Member.username == member_username).first()

	return current_user



def change_password(username, new_password):

	current_user = Member.query.filter(Member.username == username).first() # Select the specific user row
	current_user.password = new_password # edit password
	db.session.commit() # Commit change(s)


def query_all_member_with_NULL_email():
	q = Member.query.filter(Member.email == None).all()
	return q


def query_all_member_with_email():
	q = Member.query.filter(Member.email != None).all()  # normal filter
	return q



def query_stacking_filter():

	# filters on top of filters
	q1 = Member.query
	q2 = q1.filter(Member.username == 'Jordan')
	q3 = q2.filter(Member.email == 'jordan@alchemistware.com')
	q4 = q3.filter(Member.password == 'this_is_not_a_password')
	print(q1)
	print(q2)
	print(q3)
	print(q4)


def query_AND_1(): # using AND in a query
	q = Member.query.filter(db.and_(Member.username == 'Jordan').filter(Member.password == 'Password')).first()
	return q


def query_AND_2():
	q = Member.query.filter(db.and_(Member.username == 'Jordan', Member.email != None, Member.join_date != None)).all()
	return q



def query_OR(): # using OR  in a query
	q = Member.query.filter(db.or_(Member.username != None,  Member.email != None)).all()
	return q


def query_LIMIT(): # impose a limit of row returned
	#Member.query.all() #no limit

	q = Member.query.limit(2).all() #limit of 2
	return q


def query_OFFSET(): # skip the first X number

	q = Member.query.offset(100).all() #skip the first 100 member of the query
	return q





def query_COUNT_1(): # Count number of row inside the table/ with or without filter(s)

	q = Member.query.count()
	q = Member.query.count() #count all the members

	return q



def query_COUNT_2(): # Count number of row inside the table/ with or without filter(s)

	q = Member.query.count()
	q = Member.query.filter(Member).count() #count all the members who have email registered

	return q



def query_inequality(): # filter the 1000 first member.

	q = Member.query.filter(Member.id <= 1000)
	return q



def list_all_orders_of_a_member(current_member): # THE MAGIC IS HAPPENING HERE: The orders are "included" with the member(s).
	q = current_member.orders.all()
	return q



add_new_order(50, 14) #14 = uid of Jordan (relationship)

#add_new_order_with_member_object(200, current_user) current_user reprensent an SQLAlchemy user object


#change_password('Jordan', 'this_is_my_new_passwordssss')


current_member = get_specific_member_informations('Jordan')

Jordans_orders = list_all_orders_of_a_member(current_member)


print('List of orders:')
for order in Jordans_orders:
	print('ID:' + str(order.id) + ' Price: ' + str(order.price))



if __name__ == '__main__':
	app.run()

