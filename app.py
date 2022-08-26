from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import date

app = Flask(__name__)

app.config.from_pyfile('config.cfg')  # import the config file
db = SQLAlchemy(app)  # init the db session


#
#  How to create / define /modify a model table using the SQLAlchemy classes +  db.Model
#  Name of the class = name of the table
#  Always better to specify a length for a String column
#  Don't forget to run create_all.py after modifying any table model class.
#

class Test(db.Model):  # only for test
    id = db.Column(db.Integer, primary_key=True)


class Member(db.Model):  # Creating a table witht the name Member
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(50))
    join_date = db.Column(db.DateTime)

    orders = db.relationship('Order', backref='member',
                             lazy='dynamic')  # backref is like a virtual column in the other table, lazy = dynamic(standard)




	#  classmethod to query search a member with provided username
    @classmethod
    def search_by_username(cls, username):
        return db.session.query(Member).filter(Member.username == username).first()



    @classmethod
    def delete(cls, username):
        current_user = db.session.query(Member).filter(Member.username == username).delete()
        db.session.commit()



    # staticmethod to query search a member with provided username
    @staticmethod
    def get_all_members():
         return db.session.query(Member).all()






def __repr__(self):
        return '<Member %r>' % self.username





# Third Table for relationships exemple. One Member to many orders.
#

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    member_id = db.Column(db.Integer, db.ForeignKey(
        'member.id'))  # dynamic relationship (one to many) made using db.ForeignKey to point to member_id! easy


#
# Exemple of adding (INSERT New row) inside the a table.
#
def add_new_user(username, password, email):
    new_user = Member(username=username, password=password, email=email, join_date='2018-06-06')
    # new_user = Member(username= 'Jordan', password='secret', email='jordan@alchemistware.com', date='') # for testing
    db.session.add(new_user)  # add new user to the session
    db.session.commit()  # commit the session. Save to MySQL.


def delete_user(member_username):
    current_user = Member.query.filter(Member.username == member_username).first()
    db.session.delete(current_user)
    db.session.commit()


# add an order to the order table with a relationship to a member (one to many)
# When we will query information about a member, the order will be 'attached' to it.
def add_new_order(price, member_id):
    new_order = Order(price=price, member_id=member_id)
    db.session.add(new_order)
    db.session.commit()


def get_list_of_member():
    # Query all the members in the Member table
    results = Member.query.all()
    # list them (for demonstration)
    for user in results:
        print(f'{user.username}:{user.email} email: {user.email}')

    return results


def get_specific_member_informations(member_username):
    return Member.query.filter(Member.username == member_username).first()


def get_specific_member_informations_by_id(id):
    return Member.query.filter(Member.id == id).first()


def change_password(username, new_password):
    current_user = Member.query.filter(Member.username == username).first()  # Select the specific member's row
    current_user.password = new_password  # edit password

    #  You can change many columns at once an then commit.
    #  current_user.email = 'new_email@gmail.com'
    #  current_user.join_date = new_date

    db.session.commit()  # Commit change(s), simple!


def query_all_member_with_NULL_email():
    return Member.query.filter(Member.email is None).all()


def query_all_member_with_email():
    return Member.query.filter(Member.email != None).all()


def query_stacking_filter():
    # How to add a filte again and again a query!
    # It can be use to be for efficient and avoid multiple queries.
    # The more you filter, the less result(s) we will have at the end.

    q1 = Member.query
    q2 = q1.filter(Member.username == 'Jordan')
    q3 = q2.filter(Member.email == 'jordan@alchemistware.com')
    q4 = q3.filter(Member.password == 'this_is_not_a_password')
    print(q1)
    print(q2)
    print(q3)
    print(q4)


def query_AND_1():
    return Member.query.filter(
        filter(Member.username == 'Jordan').filter(
            Member.password == 'Password'
        )
    ).first()


def query_AND_2():
    return Member.query.filter(
        db.and_(
            Member.username == 'Jordan',
            Member.email != None,
            Member.join_date != None,
        )
    ).all()


def query_OR():  # using OR  in a query
    return Member.query.filter(
        db.or_(Member.username != None, Member.email != None)
    ).all()


def query_LIMIT():  # impose a limit of row returned
    return Member.query.limit(2).all()


def query_OFFSET():
    return Member.query.offset(100).all()


def query_COUNT_1():
    return Member.query.count()


def query_COUNT_2():  # Count number of row inside the table/ with or without filter(s)
    return Member.query.filter(Member.email != Null).count()


def query_inequality():  # filter the 1000 first members.
    return Member.query.filter(Member.id <= 1000)


def list_all_orders_of_a_member(current_member):
    return current_member.orders.all()




def demo():

    # # #  ---------  Interacting using the standard traditionnal functions     ---------
    # add_new_order(50, 14) #14 = id of Jordan (relationship), price = 50
    # add_new_order_with_member_object(200, current_user) current_user reprensent an SQLAlchemy user object
    # change_password('Jordan', 'this_is_my_new_passwordssss')


    current_member = get_specific_member_informations(
        'Jordan')  # get all the information about member Jordan including the orders.

    Jordans_orders = list_all_orders_of_a_member(current_member)

    # You can user current_member.orders or Jordans_orders as your list.


    # Relation exemple number 1.

    print('List of orders:')  # exemple of using a relationship, listing all the order attached to a specific user.
    for order in current_member.orders:
        print(f'ID:{str(order.id)} Price: {str(order.price)}')

    # Relation exemple number 2. (one query instead instead of many queries)

    all_the_member = get_list_of_member()  # one query

    for current_member in all_the_member:  # process one member at the time

        #  for each member, display the name + total number of orders.
        print('--------------------------------------------------------------')  # separator for every user
        print(
            f'Member username: {current_member.username} Total order(s): {str(current_member.orders.count())}'
        )

        if current_member.orders:  # if user have order(s), print the out.
            print('List of orders: ')
            for order in current_member.orders:
                #  for each order, print out the unique id and price)
                print(f'ID:{str(order.id)} Price: {str(order.price)}')






    # # #  ---------  Interacting using @classmetod(s) instead of traditionnal functions.    ---------
    print('')
    print('')
    print('##############    Interacting using @classmetod(s) instead of traditionnal functions. ##############')
    print('classmethod exemple:')
    print('')

    current_member = Member.search_by_username('Jordan')
    print(current_member.username + '\'s id is :' +  str(current_member.id))





    # # #  ---------  Interacting using @staticmethod(s) instead of traditionnal functions.    ---------
    print('')
    print('##############    Interacting using @staticmethod(s) instead of traditionnal functions. ##############')
    print('staticmethod exemple:')
    print('')

    all_members = Member.get_all_members()

    for member in all_members:
        print(member.username)

        print(
            f'Member username: {current_member.username} Total order(s): {str(member.orders.count())}'
        )


        if current_member.orders:  # if user have order(s), print the out.
            #  for each order, print out the unique id and price)

            for order in member.orders:
                print(order.id)
                print(f'ID:{str(order.id)} Price: {str(order.price)}')



    Member.delete('asdf')




demo()


if __name__ == '__main__':  # standard flask app.run

    app.run()
