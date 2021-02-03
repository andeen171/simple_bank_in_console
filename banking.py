import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
#  cur.execute(""'CREATE TABLE card (        '
#            'id INTEGER,                  '
#            'number TEXT NOT NULL,        '
#            'pin TEXT NOT NULL,           '
#            'balance INTEGER DEFAULT 0);'"")
#  conn.commit()
#  cur.fetchall()


def createui():  # show the first screen
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def createsecondui():  # show the second screen
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


def login(cardnum, pin):
    global user
    cur.execute("select * from card where number = {0} and pin = {1}".format(cardnum, pin))
    rud = cur.fetchall()
    user = Users(cardnum, pin)

    if rud:
        print('You have successfully logged in!')
        return True
    else:
        print("Wrong card number or PIN!")
        return False


def cc_checker(number):
    counter = 0
    check = 0
    for i in number:
        if counter == 15:
            break
        if (counter % 2) == 0:
            actual = 2 * int(i)
            if actual > 9:
                check += actual - 9
            else:
                check += actual
        else:
            check += int(i)
        print(check)
        counter += 1
    print(number[-1])
    print(check % 10)
    print(10 - (check % 10))
    if number[-1] == '0' and (check % 10) == 0:
        return True
    elif number[-1] == str(10 - (check % 10)):
        return True
    else:
        return False


def existing(number):
    cur.execute('SELECT * FROM card WHERE number = {0}'.format(number))
    rud = cur.fetchall()
    if rud:
        return True
    else:
        return False


class Users:  # class containing the users for now

    def __init__(self, cardnum, pin):
        self.cardnum = cardnum
        self.pin = pin
        self.balance = 0

    def register(self):
        cur.execute('INSERT INTO card(number, pin) VALUES ({0}, {1});'.format(self.cardnum, self.pin))
        conn.commit()

    def show_balance(self):
        cur.execute("select balance from card where number = {0} and pin = {1}".format(self.cardnum, self.pin))
        rud = cur.fetchone()
        textin = ''.join(map(str, rud))
        return textin

    def transfer(self, receiver, amount):
        cur.execute('UPDATE card SET balance = balance + {0} WHERE number = {1};'.format(amount, receiver))
        cur.execute('UPDATE card SET balance = balance - {0} WHERE number = {1};'.format(amount, self.cardnum))
        conn.commit()

    def add_income(self, money):
        cur.execute('UPDATE card SET balance = balance + {0} WHERE number = {1};'.format(int(money), self.cardnum))
        conn.commit()

    def delete_account(self):
        cur.execute('DELETE FROM card WHERE number = {0}'.format(self.cardnum))
        conn.commit()


user = Users("4000004938320895", "4444")
finished = False
randomcard = ""

while not finished:
    createui()
    option = input()

    if option == "1":
        print("Your card has been created")
        print("Your card number:")

        randomcard = "400000"
        check = 0
        actual = 0
        counter = 0

        while counter < 9:
            randomcard += str(random.randint(1, 9))
            counter += 1
        counter = 0
        for i in randomcard:
            if (counter % 2) == 0:
                actual = 2 * int(i)
                if actual > 9:
                    check += actual - 9
                else:
                    check += actual
            else:
                check += int(i)
            counter += 1

        if check % 10 == 0:
            randomcard += "0"
        else:
            randomcard += str(10 - (check % 10))

        counter = 0
        randompin = ""
        while counter < 4:
            randompin += str(random.randint(1, 9))
            counter += 1

        user = Users(randomcard, randompin)
        user.register()

        print(randomcard)
        print("Your card PIN:")
        print(randompin)
    elif option == "2":
        if login(input("Enter your card number:"), input("Enter your PIN:")):
            ui2finished = False
            while not ui2finished:
                createsecondui()
                option = input()

                if option == "1":
                    print(user.show_balance())
                elif option == "2":
                    user.add_income(input("How much money you want to deposit?"))
                elif option == "3":
                    receiverr = input("Card num of the receiver")
                    if receiverr == user.cardnum:
                        print("You can't transfer money to the same account!")
                    elif not cc_checker(receiverr):
                        print("Probably you made a mistake in the card number. Please try again")
                    elif not existing(receiverr):
                        print("Such a card does not exist.")
                    else:
                        amounte = int(input("How much do you want do transfer?"))
                        if amounte > int(user.show_balance()):
                            print("Not enough money!")
                        else:
                            user.transfer(receiverr, amounte)
                elif option == "4":
                    user.delete_account()
                    print("Account deleted sucessfully")
                elif option == "5":
                    print("You have successfully logged out!")
                    ui2finished = True
                else:
                    ui2finished = True
                    finished = True
    else:
        finished = True
