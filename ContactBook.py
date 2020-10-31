"""
Program Contact Book.  Allows users to input contacts into sqlite database

Classes
-------
class ContactBook

Functions
--------
main()
"""

import sqlite3


class ContactBook:
    """
    This class allows users to input names, addresses, and phone numbers into a
    sqlite dataase

    Attributes
    ----------
    conn    Database connection object

    Methods
    --------
    databaseConnect Returns database connection object
    addInfo         Allows user to add information to database
    searchInfo      Allows user to search database
    getAllData      Returns entire database to user
    """

    def __init__(self):
        """
        init method

        Establishes database connection, gets a choice from the user
        for what action they would like to perform

        Parameters
        ---------
        self

        :return:
        --------
        No return statement
        """
        self.conn = self.databaseConnect()
        print("Would you like to add, search, or view the entire contact book?")
        userChoice = input("Please enter 1 for add, 2 for search, 3 for view, "
                           "q to quit: ")
        # Get user choice in __init__ because needs a choice to continue.
        # Didn't make sense to put it in another method to me
        if userChoice == '1':
            self.addInfo()
        elif userChoice == '2':
            self.searchInfo()
        elif userChoice == '3':
            self.getAllData()
        elif userChoice == 'q':
            print("See you later!")
            exit(0)
        else:
            print("That input does not match!")

    def databaseConnect(self):
        """
        This method establishes a connection to a sqlite database

        :parameter:
        self

        :return:
        Database connection object
        """
        conn = sqlite3.connect('contactbook.db')
        return conn

    def addInfo(self):
        """
        This method allows users to add information to the database

        Starts by establishing database cursor, handling exception if table
        has already been created.
        Enters while loop.  While loop will continue until user enters 'n',
        indicating that they don't have another entry
        In while loop, user asked for name, address, phone number.  These are
        inserted into the database

        :exception:
        sqlite3.OperationalError

        :parameter:
        self

        :return:
        No return statement
        """
        c = self.conn.cursor()
        try:  # Handles exception for when table already exists
            c.execute("""CREATE TABLE Contacts (
                                name TEXT,
                                address TEXT,
                                phone_number TEXT
                                )""")
        except sqlite3.OperationalError:
            pass

        while True:
            name = input("Enter name to add to contact book here: ")
            address = input('Enter address here: ')
            phoneNum = input("Add phone number here: ")

            c.execute("""INSERT INTO Contacts(name, address, phone_number) VALUES
            (?, ?, ?)""", (name.lower(), address.lower(), phoneNum.lower()))
            self.conn.commit()

            anotherEntry = input("Do you have another entry? ( y / n ) ")
            if anotherEntry.lower() == 'n':
                break

    def searchInfo(self):
        """
        This methods allows users to search for info from the database

        Establishes database cursor
        Enters while loop, runs until user indicates that they do not have any
        more searches
        Asks user what they would like to search for.  Searches for name, if no name
        found tells user that.  Returns all results found with same name
        Asks user if they would like to go again.

        :return:
        No return statement
        """
        c = self.conn.cursor()

        while True:
            searchType = input("Are you looking for a name (n), address (a), or "
                               "phone number (p)? ")
            if searchType == 'n':
                name = input("Please enter a name here: ")
                c.execute("SELECT * FROM Contacts WHERE name=?", (name.lower(),))
                returnList = c.fetchall()
                returnString = ''
                if returnList == []:  # If empty return list
                    print("Nobody found under that name!")
                for element in returnList:  # Makes list string for user to read
                    for word in element:
                        returnString += word + ", "
                print(returnString)
            elif searchType == 'a':
                address = input("Please enter an address here: ")
                c.execute("SELECT * FROM Contacts WHERE address=?",
                          (address.lower(),))
                returnList = c.fetchall()
                returnString = ''
                if returnList == []:
                    print("Nobody found under that address!")
                for element in returnList:
                    for word in element:
                        returnString += word + ", "
                print(returnString)
            elif searchType == 'p':
                phoneNum = input("Enter a phone number here: ")
                c.execute("SELECT * FROM Contacts WHERE phone_number=?",
                          (phoneNum.lower(),))
                returnList = c.fetchall()
                returnString = ''
                if returnList == []:
                    print("Nobody found under that phone number!")
                for element in returnList:
                    for word in element:
                        returnString += word + ", "
                print(returnString)
            else:
                print("Incorrect input!")

            goAgain = input("Do you have another search? ( y / n ) ")
            if goAgain.lower() == 'n':
                break

    def getAllData(self):
        """
        Allows user to get all data in database

        Establishes cursor, gets all information from database.  Iterates over
        database to get string instead of list.  Separates by each line of database
        Prints database to user
        :return:
        """
        c = self.conn.cursor()
        c.execute('SELECT * FROM Contacts')
        returnList = c.fetchall()
        returnString = ''
        for element in returnList:
            for word in element:
                returnString += word + ", "
            returnString += '\n'
        print(returnString)


def main():
    """
    Main contains a while loop to allow users to make another choice

    Creates instance of ContactBook class, asks user if they would like to go again
    If the user presses 'n', database closes connection, program exits

    :return:
    No return statement
    """
    while True:
        contact = ContactBook()
        goAgain = input("Would you like to make another choice? (y / n) ")
        if goAgain.lower() == 'n':
            print("See you later!")
            contact.conn.close()
            exit(0)


if __name__ == '__main__':
    main()

