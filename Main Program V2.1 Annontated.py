# Bryn Dyer
from guizero import App, warn, Text, Window, Combo, TextBox, CheckBox, PushButton, Combo, error, info, warn, yesno # Importing all nescasary GUI zero modules
import sqlite3 # Importing the sqlite3 library

# Variables
Main_App = App(title="Main Menu") # Declaring the App as main window as only one App can exist in a program, if the app is closed all other GUI elements also close so main window can never be closed.
Main_App.hide()
Logins = [] # Logins are stored in a local list imported from a external database file
Logged_In = False
Conn = sqlite3.connect('StudentInfo.db') # Student info is held in an external database and all changes edit the database directly through the SQLite3 library, this lines connects the program to the Student Info database
Cursor = Conn.cursor() # Using SQLite3 to create a cursor in the Student Info database
LoginGuess = 0
PasswordGuess = 0
LoginInput = 0
PasswordInput = 0


# Importing Data
def LoadLogins(Logins):
    with open("Logins.csv", "r") as DataFile: # Loading the comma seperated value file into a 2D list
        for EachLine in DataFile:
            EachLine = EachLine.strip()
            EachColumnItem = EachLine.split(",")
            Logins.append(EachColumnItem)

# This function creates the table Student info in the Student Info database if it doesn't exist if it does it does nothing
def StudentInfo_Connect():
    Cursor.execute('CREATE TABLE IF NOT EXISTS Student_Info_table(Student_ID INTEGER, First_Name TEXT, Surname TEXT, Gender TEXT, Subjects TEXT, Teachers TEXT, Year INTEGER, Band TEXT, Attendance INTEGER) ')

# This function creates the table Student grades in the Student Info database if it doesn't exist if it does it does nothing
def StudentGrades_Connect():
    Cursor.execute('CREATE TABLE IF NOT EXISTS Student_Grades_table(Student_ID INTERGER, Subject_ID INTERGER, Grades TEXT)')

# Log In Function
def LogIn(Logins, Logged_In, LoginGuess, PasswordGuess, LoginInput, PasswordInput):
    LoginInput = 0
    PasswordInput = 0
    global LogIn_Window # Created as a globalvariable so it can be closed or opened from any part of the program
    LogIn_Window = Window(Main_App, title="Log In", layout = "grid") #Creates the LogIn GUI window 
    if len(Logins) == 0:
        LoadLogins(Logins) # Uses anbother function to load the logins if they are not currently loaded
    Username_Text = Text(LogIn_Window, text = "Enter a username:", grid=[0,0],) # All the follwing code is GUI elements that are in the LogIN window
    LoginInput = TextBox(LogIn_Window, width = 30, grid = [1,0])
    Filler = Text(LogIn_Window, text = "", grid = [0,1,2,1])
    Password_Text = Text(LogIn_Window, text = "Enter a password:", grid=[0,2])
    PasswordInput = TextBox(LogIn_Window,width = 30, grid=[1,2])
    Run_Check = PushButton(LogIn_Window, command = LogIn_Check, args = (LoginGuess, PasswordGuess, LoginInput, PasswordInput, Logged_In), grid = [0,4], text = "Log In")
    # A push button that once pressed runs the log in check to see if the username and password are valid

    
# Log in Validation
def LogIn_Check(LoginGuess, PasswordGuess, LoginInput, PasswordInput, Logged_in):
    Failed = False # Creates Local variables and resets passed variables to be used in the function
    Log_Pos = 0
    Logged_In = False
    LoginGuess = LoginInput.get() # Obtains the input value text boxes from the Log in window 
    PasswordGuess = PasswordInput.get()
    while Logged_In == False: # A loop to prevent the function from running after the user has logged in
        if LoginGuess == Logins[Log_Pos][0]:# Comparing the username to the 0th slot (should contain username) of all the lists
            if PasswordGuess == Logins[Log_Pos][1]:# Comparing the password to the 1th slot (should contain password) of all the lists
                Menu(Logged_In, Main_App) # If both the username and password match will log the user in
                Logged_In = True
            elif Failed == False: # Identifies that the password was incorrect
                Failed = True
                Incorrect_Password = error(title = "Incorrect Log In details", text = "Username or Password was incorrect")# Informs the user that the login was incorrect
                break
        elif Failed == False: # Identifies that the inputs didn't match
            Log_Pos += 1 # Increments the index that the program is comparing LoginGuess (The user's input) to
            if Log_Pos == len(Logins): #Identifies that the user input was not contained in the list
                Failed = True
                Incorrect_Username = error(title = "Incorrect Log In details", text = "Username or Password was incorrect")# Informs the user that the login was incorrect
                break

# Function for the main menu
def Menu(Logged_In, Main_App):
    LogIn_Window.hide() # Hides the previous window to make the UI clearer
    Main_App.show() #The main menu uses the App window as if the main windowis closed it is unlikely that the user wishes to continue usingthe program
    Main_App.width = 216 # Setting a suitable size for the App
    Main_App.height = 300
    Menu = Text(Main_App, text="Choose the desired option") # GUI elements for the Main App
    Full_List_Button = PushButton(Main_App, command=Full_List, text = "Full List") # Button to run the search list subroutine
    Full_List_Button.width = 15 # Size of the button
    Full_List_Button.height = 2
    Search_Button = PushButton(Main_App, command=Search, text = "Search") # Button to run the search subroutine
    Search_Button.width = 15 # Size of the button
    Search_Button.height = 2
    Query_Button = PushButton(Main_App, command=Query, text = "Query")# Button to run the query subroutine
    Query_Button.width = 15 # Size of the button
    Query_Button.height = 2

# Full list subroutine
def Full_List():
    StudentInfo_Connect() # Making sure the program is connected to the database
    grid_pos = 1 # Variables to help order the UI elements
    g_x_pos = 0
    global Full_List_Window # Creating the window as a global variable so it can be closed and opened from anywhere in the program
    Full_List_Window = Window(Main_App, title = "Full List", layout = "grid") # Creating a new window to store GUI elements 
    Add_Entry = PushButton(Full_List_Window, text = "Add New Entry", grid = [0,0], command = Add_Data) # Adds a buttons that run various commands
    Edit_Entry = PushButton(Full_List_Window, text = "Edit Entry", grid = [1,0], command = Edit_Data)
    Remove_Entry = PushButton(Full_List_Window, text = "Remove Entry", grid = [2,0], command = Delete_Data)
    Cursor.execute('SELECT * FROM Student_Info_table') #Selecting all elements in the student info table 
    Student_List = Cursor.fetchall() # Creating a list of all data in the table 
    for Each_Line in Student_List: # Spliting the list by line
        for each in Each_Line: # Spliting the 1D line by word
            Item = Text(Full_List_Window, text = each, grid = [ g_x_pos, grid_pos]) # Creatig UI elements with different positions based on the position in the list and the contents of the items
            g_x_pos += 1 # Incrementing the UI elements x position 
        grid_pos += 1 # Incrementing the UI elements y position 
        g_x_pos = 0 # Reseting the UI elements x position
    Full_List_Window.update() #Updating the full list window so it display the new UI elements

def Add_Data():
    Cursor.execute('SELECT * FROM Student_Info_table') # Get all the data in the student info table
    Student_List = Cursor.fetchall() # Puts that data into a list
    Full_List_Window.destroy() # Deleting the old unnecessary window
    global A_Input # Creates a winodw that can be accessed from anywhere in the program
    A_Input = Window(Main_App, title = "Add Entry")
    global S_ID_In 
    S_ID_In = (len(Student_List)+1) # Creates a new student ID based on the length of the Student List to prevent duplicate data
    FN_Text = Text(A_Input, text = "Enter Student First Name") # All of the following var_Text lines bellow create a text field that tells the user what to enter on the field bellow
    global FN_In # All of the following var_In lines are global variable so the next subroutine can access them. All of the variable are text boxes where the user can input data to create a new entry on the database
    FN_In = TextBox(A_Input)
    SN_Text = Text(A_Input, text = "Enter Student Surname")
    global SN_In
    SN_In = TextBox(A_Input)
    G_Text = Text(A_Input, text = "Enter Student Gender (M/F/Other)") # This field has validation rules so informs the user of them so they enter correct data
    global G_In
    G_In = TextBox(A_Input)
    Subj_Text = Text(A_Input, text = "Enter Student Subject")
    global Subj_In
    Subj_In = TextBox(A_Input)
    T_Text = Text(A_Input, text = "Enter Student Teacher")
    global T_In
    T_In = TextBox(A_Input)
    Y_Text = Text(A_Input, text = "Enter Student Year")
    global Y_In
    Y_In = Combo(A_Input, options = ["9", "10", "11", "12", "13"]) # Instead of a text box this program uses a Combo list in order to validate the data and ensure that it is correct
    B_Text = Text(A_Input, text = "Enter Student Band (A or B or N/A)") # This field has validation rules so informs the user of them so they enter correct data
    global B_In
    B_In = TextBox(A_Input)
    A_Text = Text(A_Input, text = "Enter Student Attendance")
    global A_In
    A_In = TextBox(A_Input)
    Submit = PushButton(A_Input, text = "Submit", command = Confirm_Add_Data) # A buton to run the next function that takes the users input data that can be used to enter it into the database

def Confirm_Add_Data():    
    Confirm = yesno(title = "Confirm", text = "Do you want to add this data to the database?") # Shows the user a dialouge box that allows the user to confirm the data input
    if Confirm == True: # If the user confirms the data entry this ocde block is selected
        Correct_List = [] # Setting up lists for comparison and validation
        G_List = ["M", "F", "Other"]
        B_List = ["A", "B", "N/A"]
        for each in G_List: # Checks the user input for gender with each value in its accepted values list
            if G_In.get() == each: # If the input for gender matches an accepted to values it will add a value to correct list, indicating that the data has been validated
                Correct_List.append(int(1))
        for each in B_List: # Checks the user input for band with each value in its accepted values list
            if B_In.get() == each: # If the input for band matches an accepted to values it will add a value to correct list, indicating that the data has been validated
                Correct_List.append(int(1))
        if sum(Correct_List[0:len(Correct_List)]) == 2: # If both band and gender have been validated successfully then 
            Cursor.execute("INSERT INTO Student_Info_table(Student_ID,First_Name,Surname,Gender,Subjects,Teachers,Year,Band,Attendance) VALUES (?,?,?,?,?,?,?,?,?)",
                           (S_ID_In, FN_In.get(),SN_In.get(),G_In.get(),Subj_In.get(),T_In.get(),Y_In.get(),B_In.get(),A_In.get())) # Uses a SQLite 3 command in combination with a GUIzero command to insert data into the table 'Student_Info_Table'. The SQLite3 command specifies the attributes that the new entry has and gets the values from outside the "". The values outside the "" are GUIZero commands that are operating on the previous values that were decleared as global. This is done as a .get command as it is run after the user inputs the data. A global variable is used rather than parameter passing as in python parameter passing is by value rather than by reference so if the user checks and changes the data inputed before confirming the data will not change the input used by the program however this does not happen if a global variable is used instead of parameter passing.
            Finished = info(title = "Submitted", text = "The data has been saved to the database") # Informs the user that the data has been entered into the database
            A_Input.destroy # Destroys the input window as it is no longer needed
            Conn.commit() # Commits the changes to the database
            Full_List() # Runs the full list fnction so the user can see the changes
        else:
            Error = error(title = "Invalid Data", text = "Some of the data entered is invalid check that the data is valid and try agian") # If the data is checked and is not valid it will inform the user and they can then change the data so it is valid
    else: # If the user cancels this is selected
        A_Input.destroy()
        Full_List()

def Edit_Data():
    Full_List_Window.destroy()
    global E_Input # Declaring text and textboxes and window so the user can input data, inputs and the window are declared as global like in add data so that they can be accessed once the window is closed as the values persist
    E_Input = Window(Main_App, title = "Edit Entry")  # Creating the window to hold the GUI
    E_Info = Text(E_Input, text =  " Fill in all fields, if you wish for the data to remain unchanged please re-enter the current data") # Text to inform the user on what to do
    S_ID_Text = Text(E_Input, text = "Enter Student ID of Data to Edit")# Textboxes for user data input
    global S_ID_In
    S_ID_In = TextBox(E_Input)
    FN_Text = Text(E_Input, text = "Enter Student First Name")
    global FN_In 
    FN_In = TextBox(E_Input)
    SN_Text = Text(E_Input, text = "Enter Student Surname")
    global SN_In
    SN_In = TextBox(E_Input)
    G_Text = Text(E_Input, text = "Enter Student Gender (M/F/Other)")
    global G_In
    G_In = TextBox(E_Input)
    Subj_Text = Text(E_Input, text = "Enter Student Subject")
    global Subj_In
    Subj_In = TextBox(E_Input)
    T_Text = Text(E_Input, text = "Enter Student Teacher")
    global T_In
    T_In = TextBox(E_Input)
    Y_Text = Text(E_Input, text = "Enter Student Year")
    global Y_In
    Y_In = Combo(A_Input, options = ["9", "10", "11", "12", "13"])
    B_Text = Text(A_Input, text = "Enter Student Band (A or B or N/A)")
    global B_In
    B_In = TextBox(E_Input)
    A_Text = Text(E_Input, text = "Enter Student Attendance")
    global A_In
    A_In = TextBox(E_Input)
    Submit = PushButton(E_Input, text = "Submit", command = Confirm_Edit_Data) # Button to run the next command 

def Confirm_Edit_Data():    
    Confirm = yesno(title = "Confirm", text = "Do you want to edit this data in the database?") # A window to confirm wether or not they want to input the data
    FN = FN_In.get() # Obtain the values for input 
    SN = SN_In.get()
    G = G_In.get()
    Subj = Subj_In.get()
    T = T_In.get()
    Y = Y_In.get()
    B = B_In.get()
    A = A_In.get()
    S_ID = S_ID_In.get()
    if Confirm == True:
        Correct_List = [] # Validation rules
        G_List = ["M", "F", "Other"]
        B_List = ["A", "B", "N/A"]
        for each in G_List: # Checking user inputs to see if they are valid
            if G_In.get() == each:
                Correct_List.append(int(1))
        for each in B_List:
            if B_In.get() == each:
                Correct_List.append(int(1))
        if sum(Correct_List[0:len(Correct_List)]) == 2: # Checking to see if the data the user entered was valid according to the validation rules
            Cursor.execute("DELETE FROM Student_Info_Table WHERE Student_ID = ?",
                           (S_ID,)) # Deleting the old row
            Cursor.execute("INSERT INTO Student_Info_table(Student_ID,First_Name,Surname,Gender,Subjects,Teachers,Year,Band,Attendance) VALUES (?,?,?,?,?,?,?,?,?)",
                           (S_ID,FN,SN,G,Subj,T,Y,B,A,)) # Creating a new row with the same Student_ID so that the data has been replaced
            Finished = info(title = "Submitted", text = "The data has been saved to the database")
            Conn.commit()
            E_Input.destroy()
            Full_List()
        else:
            Error = error(title = "Invalid Data", text = "Some of the data entered is invalid check that the data is valid and try agian") # If the validation rules are failed the program stops the branch and informs the user the data is invalid and returns them to the input screen to re enter the data
    else:
        E_Input.destroy() 
        Full_List()

def Delete_Data():
    Full_List_Window.destroy()
    global D_Window
    D_Window = Window(Main_App, title = "Delete Entry") # GUI elemements so the user can see what to do
    R_T_D_Text = Text(D_Window, text ="Enter the Student ID of Row to Delete")
    global R_T_D_In
    R_T_D_In = TextBox(D_Window) # User Input for student ID
    Del_Button = PushButton(D_Window, text = "Delete", command = Confirm_Delete_Data) 


def Confirm_Delete_Data():
    T_D = R_T_D_In.get() # Obtaining the user's input
    Confirm = yesno(title = "Confirm", text = "Do you want to delete this data in the database?") # Confirming that the user wants to delete the data
    if Confirm == True:
        Cursor.execute("DELETE FROM Student_Info_Table WHERE Student_ID = ?",
                       [T_D]) # Deletes the data in the database using SQL, python interprets it with SQLite 3 library
        Finished = info(title = "Deleted", text = "The data has been deleted from the database") #Informing the user that the data has been deleted
        Conn.commit() # Commitsthe deletion to the database
        Full_List() # Return to the list in the program to see the change in the data 
    else:
        D_Window.destroy() 
        Full_List() # Returning the user to a main menu if they do not want to commit the changes

# Query Selection Window
def Query():
    StudentInfo_Connect() # Ensuring the program is connected tothe database before trying to access the database with SQLite 3
    Query_Window = Window(Main_App, title = "Query", layout ="grid") #GUI elements so that the user can see what they are doing and easily input data
    Q_Instruction = Text(Query_Window, text = "Please select the query that you want to run", grid = [0,0])
    Q_Att = PushButton(Query_Window, command = Q_Att_Q, text = "Attendance", grid = [0,1])
    Q_Subjects = PushButton(Query_Window, command = Q_Subjects_Q, text = "Subjects", grid = [0,2])

# Attendance Query Search Criteria - Runs if user picks the 'Attendance' option
def Q_Att_Q(): 
    Q_Att_Q_Win =Window(Main_App, title = "Attendance Query")
    Criteria = Text(Q_Att_Q_Win, text = "Search Students Who Are:")
    global Criteria_Choice # Declaring inputs sothey can be accessedif the window closes
    Criteria_Choice = Combo(Q_Att_Q_Win, options=["Over", "Under", "Have"]) # Chooses what type attendace query will be run
    Percentage_Text = Text(Q_Att_Q_Win, text = "What Percentage")
    global Percentage
    Percentage = TextBox(Q_Att_Q_Win)
    Submit = PushButton(Q_Att_Q_Win, text = "Search", command = Q_Att_R)

# Attendance Query Report Page 1 
def Q_Att_R():
    Q_Att_R_Window = Window(Main_App, title ="Attendance Results",layout = "grid") # Windowtoholdthe GUI elements
    grid_pos = 0 # Declaring variables that organise UI
    g_x_pos = 0
    Choice = Criteria_Choice.get() # Obtain user input from previous function
    Search_Value = Percentage.get()
    if Choice == "Over": # Each of these selection statements are what the user selects in the 'Criteria_Choice' combobox 
        Cursor.execute('SELECT * FROM  Student_Info_table Where Attendance > ?', [Search_Value]) # SQLite 3 that selects all data that fits the criteria 'Attendance > ?' where ? is a substitute for any variable declared in the []
        Student_List = Cursor.fetchall() # Storing the results of the search in a 2D list 
        for Each_Line in Student_List: # Splitting the 2D list into its individual items and adding them into the GUI as individual items where the position is decided by the 'grid_pos' and 'g_x_pos' variables  
            for each in Each_Line:
                Item = Text(Q_Att_R_Window, text = each, grid = [g_x_pos, grid_pos])
                g_x_pos += 1
            grid_pos += 1
            g_x_pos = 0  
    elif Choice == "Under": # Same as the 'Over' path but '<' is used to compare instead
        Cursor.execute('SELECT * FROM  Student_Info_table Where Attendance < ?', [Search_Value])
        Student_List = Cursor.fetchall()
        for Each_Line in Student_List:
            for each in Each_Line:
                Item = Text(Q_Att_R_Window, text = each, grid = [g_x_pos, grid_pos])
                g_x_pos += 1
            grid_pos += 1
            g_x_pos = 0  
    elif Choice == "Have": # Same as the 'Over' path but '=' is used to compare instead
        Cursor.execute('SELECT * FROM  Student_Info_table Where Attendance = ?', [Search_Value])
        Student_List = Cursor.fetchall()
        for Each_Line in Student_List:
            for each in Each_Line:
                Item = Text(Q_Att_R_Window, text = each, grid = [g_x_pos, grid_pos])
                g_x_pos += 1
            grid_pos += 1
            Row.append(I_2)
            Row.append(I_3)
            Row.append(Item)
            Row.append(I_4)
            Display_List.append(Row)
            L_pos += 1
            grid_pos += 1
    As = Grades_List.count("A")
    Bs = Grades_List.count("B")
    Cs = Grades_List.count("C")
    Ds = Grades_List.count("D")
    Es = Grades_List.count("E")
    Fs = Grades_List.count("F")
    Gs = Grades_List.count("G")
    Us = Grades_List.count("U")
    Grades_Num = []
    Grades_Num.append(As)
    Grades_Num.append(Bs)
    Grades_Num.append(Cs)
    Grades_Num.append(Ds)
    Grades_Num.append(Es)
    Grades_Num.append(Fs)
    Grades_Num.append(Gs)
    Grades_Num.append(Us)
    m = max(Grades_Num)
    Avg = 0
    [i for i, Avg in enumerate(Grades_Num) if Avg == m]
    Grade_Avg = Possible_Grades[Avg]
    Fill = Text(Q_Att_R_Window_2, text = "", grid = [0, grid_pos])
    grid_pos += 1
    T1 = Text(Q_Att_R_Window_2, text = "Average  Grade  for", grid = [0, grid_pos]) 
    T2 = Text(Q_Att_R_Window_2, text = Search_Value, grid = [1, grid_pos]) 
    T1 = Text(Q_Att_R_Window_2, text = " %  was ", grid = [2, grid_pos]) 
    T1 = Text(Q_Att_R_Window_2, text = Grade_Avg, grid = [3, grid_pos])

# Subjects Query Criteria
def Q_Subjects_Q():
    Q_Sub_Q_Win =Window(Main_App, title = "Subjects Query")
    Sub_Text = Text(Q_Sub_Q_Win, text = "Search Students Who Study:")
    global S_T_S
    S_T_S = TextBox(Q_Sub_Q_Win)
    Submit = PushButton(Q_Sub_Q_Win, text = "Search", command = Q_Subjects_R)
# Subjects Query Page 1
def Q_Subjects_R():
    Q_Sub_R_Window = Window(Main_App, title ="Subjects Results",layout = "grid")
    grid_pos = 0
    g_x_pos = 0
    Search_Value = S_T_S.get()
    Text_List = []
    Cursor.execute('SELECT * FROM  Student_Info_table Where Subjects > ?', [Search_Value])
    Student_List = Cursor.fetchall()
    for Each_Line in Student_List:
        for each in Each_Line:
            Each_Row = []
            Item = Text(Q_Sub_R_Window, text = each, grid = [g_x_pos, grid_pos])
            g_x_pos += 1
            Each_Row.append(Item)
        Text_List.append(Each_Row)
        grid_pos += 1
        g_x_pos = 0  
    Next = PushButton(Q_Sub_R_Window, text = "Next Page", command = (Q_Subjects_R2), grid = [0, grid_pos])

# Subjects Query Page 2
def Q_Subjects_R2():
    Possible_Grades = ["A", "B", "C", "D", "E", "F", "G", "U"]
    Q_Sub_R_Window_2 = Window(Main_App, title ="Subjects Results",layout = "grid")
    pos = 0
    g_x_pos = 0
    L_pos = 0
    grid_pos = 0
    Search_Value = S_T_S.get()
    Display_List = []
    Grades_List = []
    Cursor.execute('SELECT * FROM  Student_Info_table Where Subjects > ?', [Search_Value])
    List = Cursor.fetchall()
    Cursor.execute('SELECT * FROM Student_Grades_table')
    L_G = Cursor.fetchall()
    while L_pos < len(List):
        for each in L_G:
            if List[L_pos][0] == each[0]:
                Grades_List.append(each[2])
                g_x_pos = 0
                Row = []
                I_1 = Text(Q_Sub_R_Window_2, text = List[L_pos][1], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_2 = Text(Q_Sub_R_Window_2, text = List[L_pos][2], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_3 = Text(Q_Sub_R_Window_2, text =  List[L_pos][4], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                Item = Text(Q_Sub_R_Window_2, text =  each[2], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_4 = Text(Q_Sub_R_Window_2, text =  List[L_pos][5], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_5 = Text(Q_Sub_R_Window_2, text =  List[L_pos][6], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_6 = Text(Q_Sub_R_Window_2, text =  List[L_pos][7], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_7 = Text(Q_Sub_R_Window_2, text = List[L_pos][8], grid = [g_x_pos, grid_pos])
                Row.append(I_1)
                Row.append(I_2)
                Row.append(I_3)
                Row.append(Item)
                Row.append(I_4)
                Row.append(I_5)
                Row.append(I_6)
                Row.append(I_7)
                Display_List.append(Row)
        L_pos += 1
        grid_pos += 1
    As = Grades_List.count("A")
    Bs = Grades_List.count("B")
    Cs = Grades_List.count("C")
    Ds = Grades_List.count("D")
    Es = Grades_List.count("E")
    Fs = Grades_List.count("F")
    Gs = Grades_List.count("G")
    Us = Grades_List.count("U")
    Grades_Num = []
    Grades_Num.append(As)
    Grades_Num.append(Bs)
    Grades_Num.append(Cs)
    Grades_Num.append(Ds)
    Grades_Num.append(Es)
    Grades_Num.append(Fs)
    Grades_Num.append(Gs)
    Grades_Num.append(Us)
    m = max(Grades_Num)
    Avg = 0
    [i for i, Avg in enumerate(Grades_Num) if Avg == m]
    Grade_Avg = Possible_Grades[Avg]
    Fill = Text(Q_Sub_R_Window_2, text = "", grid = [0, grid_pos])
    grid_pos += 1
    T1 = Text(Q_Sub_R_Window_2, text = "Average  Grade  for", grid = [0, grid_pos]) 
    T2 = Text(Q_Sub_R_Window_2, text = Search_Value, grid = [1, grid_pos]) 
    T1 = Text(Q_Sub_R_Window_2, text = " was ", grid = [2, grid_pos]) 
    T1 = Text(Q_Sub_R_Window_2, text = Grade_Avg, grid = [3, grid_pos])

# Search Function
def Search():
    Search_Window = Window(Main_App, title = "Search", layout = "grid")
    Field_Text = Text(Search_Window, text = "Field to Search", grid = [0,0])
    global Field_to_Search
    Field_to_Search = Combo(Search_Window, grid=[0,1], options=["Student_ID", "First_Name", "Surname", "Gender", "Subjects", "Teachers", "Year", "Band", "Attendance"])
    Search_Text = Text(Search_Window, text = "Search Term", grid = [0,2])
    global Search_Term
    Search_Term = TextBox(Search_Window, grid = [0,3])
    Start_Search_Button = PushButton(Search_Window,text = "Submit", grid = [0,4], command = Start_Search)
# Search Function Results
def Start_Search():
    Search_List = []
    Result_Window = Window(Main_App, title = "Result", layout = "grid")
    Field_Input = Field_to_Search.get()
    Search_Input = Search_Term.get()
    if Field_Input == "Student_ID":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Student_ID = ?',[Search_Input])
    elif Field_Input == "First_Name":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE First_Name = ?',[Search_Input])
    elif Field_Input == "Surname":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Surname = ?',[Search_Input])
    elif Field_Input == "Gender":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Gender = ?',[Search_Input])
    elif Field_Input == "Subjects":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Subjects = ?',[Search_Input])
    elif Field_Input == "Teachers":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Teachers = ?',[Search_Input])
    elif Field_Input == "Year":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Year = ?',[Search_Input])
    elif Field_Input == "Band":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Band = ?',[Search_Input])
    elif Field_Input == "Attendance":
            Cursor.execute('SELECT * FROM Student_Info_Table WHERE Attendance = ?',[Search_Input])
    Search_List = Cursor.fetchall()
    g_x_pos = 0
    grid_pos = 0
    Text_List = []
    for Each_Line in Search_List:
        for each in Each_Line:
            Each_Row = []
            Item = Text(Result_Window, text = each, grid = [ g_x_pos, grid_pos])
            g_x_pos += 1
            Each_Row.append(Item)
        Text_List.append(Each_Row)
        grid_pos += 1
        g_x_pos = 0
    Result_Window.show()            

# Attendance Query Page 2 
def Q_Att_R2():
    Possible_Grades = ["A", "B", "C", "D", "E", "F", "G", "U"]
    Q_Att_R_Window_2 = Window(Main_App, title ="Attendance Results",layout = "grid")
    pos = 0
    g_x_pos = 0
    L_pos = 0
    grid_pos = 0
    Choice = Criteria_Choice.get()
    Search_Value = Percentage.get()
    Display_List = []
    Grades_List = []
    if Choice == "Over":
        Cursor.execute('SELECT * FROM  Student_Info_table Where Attendance > ?', [Search_Value])
        List = Cursor.fetchall()
        Cursor.execute('SELECT * FROM Student_Grades_table')
        L_G = Cursor.fetchall()
        while L_pos < len(List):
            for each in L_G:
                if List[L_pos][0] == each[0]:
                    Grades_List.append(each[2])
                    g_x_pos = 0
                    Row = []
                    I_1 = Text(Q_Att_R_Window_2, text = List[L_pos][1], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_2 = Text(Q_Att_R_Window_2, text = List[L_pos][2], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_3 = Text(Q_Att_R_Window_2, text =  List[L_pos][4], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    Item = Text(Q_Att_R_Window_2, text =  each[2], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_4 = Text(Q_Att_R_Window_2, text = List[L_pos][8], grid = [g_x_pos, grid_pos])
                    Row.append(I_1)
                    Row.append(I_2)
                    Row.append(I_3)
                    Row.append(Item)
                    Row.append(I_4)
                    Display_List.append(Row)
            L_pos += 1
            grid_pos += 1                                       
    elif Choice == "Under":
        Cursor.execute('SELECT * FROM  Student_Info_table Where Attendance < ?', [Search_Value])
        List = Cursor.fetchall()
        Cursor.execute('SELECT * FROM Student_Grades_table')
        L_G = Cursor.fetchall()
        while L_pos < len(List):
            for each in L_G:
                if List[L_pos][0] == each[0]:
                    Grades_List.append(each[2])
                    g_x_pos = 0
                    Row = []
                    I_1 = Text(Q_Att_R_Window_2, text = List[L_pos][1], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_2 = Text(Q_Att_R_Window_2, text = List[L_pos][2], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_3 = Text(Q_Att_R_Window_2, text =  List[L_pos][4], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    Item = Text(Q_Att_R_Window_2, text =  each[2], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_4 = Text(Q_Att_R_Window_2, text = List[L_pos][8], grid = [g_x_pos, grid_pos])
                    Row.append(I_1)
                    Row.append(I_2)
                    Row.append(I_3)
                    Row.append(Item)
                    Row.append(I_4)
                    Display_List.append(Row)
            L_pos += 1
            grid_pos += 1 
    elif Choice == "Have":
        Cursor.execute('SELECT * FROM  Student_Info_table Where Attendance = ?', [Search_Value])
        List = Cursor.fetchall()
        Cursor.execute('SELECT * FROM Student_Grades_table')
        L_G = Cursor.fetchall()
        while L_pos < len(List):
            for each in L_G:
                if List[L_pos][0] == each[0]:
                    Grades_List.append(each[2])
                    g_x_pos = 0
                    Row = []
                    I_1 = Text(Q_Att_R_Window_2, text = List[L_pos][1], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_2 = Text(Q_Att_R_Window_2, text = List[L_pos][2], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_3 = Text(Q_Att_R_Window_2, text =  List[L_pos][4], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    Item = Text(Q_Att_R_Window_2, text =  each[2], grid = [g_x_pos, grid_pos])
                    g_x_pos += 1
                    I_4 = Text(Q_Att_R_Window_2, text = List[L_pos][8], grid = [g_x_pos, grid_pos])
                    Row.append(I_1)
                    Row.append(I_2)
                    Row.append(I_3)
                    Row.append(Item)
                    Row.append(I_4)
                    Display_List.append(Row)
            L_pos += 1
            grid_pos += 1
    As = Grades_List.count("A")
    Bs = Grades_List.count("B")
    Cs = Grades_List.count("C")
    Ds = Grades_List.count("D")
    Es = Grades_List.count("E")
    Fs = Grades_List.count("F")
    Gs = Grades_List.count("G")
    Us = Grades_List.count("U")
    Grades_Num = []
    Grades_Num.append(As)
    Grades_Num.append(Bs)
    Grades_Num.append(Cs)
    Grades_Num.append(Ds)
    Grades_Num.append(Es)
    Grades_Num.append(Fs)
    Grades_Num.append(Gs)
    Grades_Num.append(Us)
    m = max(Grades_Num)
    Avg = 0
    [i for i, Avg in enumerate(Grades_Num) if Avg == m]
    Grade_Avg = Possible_Grades[Avg]
    Fill = Text(Q_Att_R_Window_2, text = "", grid = [0, grid_pos])
    grid_pos += 1
    T1 = Text(Q_Att_R_Window_2, text = "Average  Grade  for", grid = [0, grid_pos]) 
    T2 = Text(Q_Att_R_Window_2, text = Search_Value, grid = [1, grid_pos]) 
    T1 = Text(Q_Att_R_Window_2, text = " %  was ", grid = [2, grid_pos]) 
    T1 = Text(Q_Att_R_Window_2, text = Grade_Avg, grid = [3, grid_pos])

# Subjects Query Criteria
def Q_Subjects_Q():
    Q_Sub_Q_Win =Window(Main_App, title = "Subjects Query")
    Sub_Text = Text(Q_Sub_Q_Win, text = "Search Students Who Study:")
    global S_T_S
    S_T_S = TextBox(Q_Sub_Q_Win)
    Submit = PushButton(Q_Sub_Q_Win, text = "Search", command = Q_Subjects_R)
# Subjects Query Page 1
def Q_Subjects_R():
    Q_Sub_R_Window = Window(Main_App, title ="Subjects Results",layout = "grid")
    grid_pos = 0
    g_x_pos = 0
    Search_Value = S_T_S.get()
    Text_List = []
    Cursor.execute('SELECT * FROM  Student_Info_table Where Subjects > ?', [Search_Value])
    Student_List = Cursor.fetchall()
    for Each_Line in Student_List:
        for each in Each_Line:
            Each_Row = []
            Item = Text(Q_Sub_R_Window, text = each, grid = [g_x_pos, grid_pos])
            g_x_pos += 1
            Each_Row.append(Item)
        Text_List.append(Each_Row)
        grid_pos += 1
        g_x_pos = 0  
    Next = PushButton(Q_Sub_R_Window, text = "Next Page", command = (Q_Subjects_R2), grid = [0, grid_pos])

# Subjects Query Page 2
def Q_Subjects_R2():
    Possible_Grades = ["A", "B", "C", "D", "E", "F", "G", "U"]
    Q_Sub_R_Window_2 = Window(Main_App, title ="Subjects Results",layout = "grid")
    pos = 0
    g_x_pos = 0
    L_pos = 0
    grid_pos = 0
    Search_Value = S_T_S.get()
    Display_List = []
    Grades_List = []
    Cursor.execute('SELECT * FROM  Student_Info_table Where Subjects > ?', [Search_Value])
    List = Cursor.fetchall()
    Cursor.execute('SELECT * FROM Student_Grades_table')
    L_G = Cursor.fetchall()
    while L_pos < len(List):
        for each in L_G:
            if List[L_pos][0] == each[0]:
                Grades_List.append(each[2])
                g_x_pos = 0
                Row = []
                I_1 = Text(Q_Sub_R_Window_2, text = List[L_pos][1], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_2 = Text(Q_Sub_R_Window_2, text = List[L_pos][2], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_3 = Text(Q_Sub_R_Window_2, text =  List[L_pos][4], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                Item = Text(Q_Sub_R_Window_2, text =  each[2], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_4 = Text(Q_Sub_R_Window_2, text =  List[L_pos][5], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_5 = Text(Q_Sub_R_Window_2, text =  List[L_pos][6], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_6 = Text(Q_Sub_R_Window_2, text =  List[L_pos][7], grid = [g_x_pos, grid_pos])
                g_x_pos += 1
                I_7 = Text(Q_Sub_R_Window_2, text = List[L_pos][8], grid = [g_x_pos, grid_pos])
                Row.append(I_1)
                Row.append(I_2)
                Row.append(I_3)
                Row.append(Item)
                Row.append(I_4)
                Row.append(I_5)
                Row.append(I_6)
                Row.append(I_7)
                Display_List.append(Row)
        L_pos += 1
        grid_pos += 1
    As = Grades_List.count("A")
    Bs = Grades_List.count("B")
    Cs = Grades_List.count("C")
    Ds = Grades_List.count("D")
    Es = Grades_List.count("E")
    Fs = Grades_List.count("F")
    Gs = Grades_List.count("G")
    Us = Grades_List.count("U")
    Grades_Num = []
    Grades_Num.append(As)
    Grades_Num.append(Bs)
    Grades_Num.append(Cs)
    Grades_Num.append(Ds)
    Grades_Num.append(Es)
    Grades_Num.append(Fs)
    Grades_Num.append(Gs)
    Grades_Num.append(Us)
    m = max(Grades_Num)
    Avg = 0
    [i for i, Avg in enumerate(Grades_Num) if Avg == m]
    Grade_Avg = Possible_Grades[Avg]
    Fill = Text(Q_Sub_R_Window_2, text = "", grid = [0, grid_pos])
    grid_pos += 1
    T1 = Text(Q_Sub_R_Window_2, text = "Average  Grade  for", grid = [0, grid_pos]) 
    T2 = Text(Q_Sub_R_Window_2, text = Search_Value, grid = [1, grid_pos]) 
    T1 = Text(Q_Sub_R_Window_2, text = " was ", grid = [2, grid_pos]) 
    T1 = Text(Q_Sub_R_Window_2, text = Grade_Avg, grid = [3, grid_pos])

# Search Function
def Search():
    Search_Window = Window(Main_App, title = "Search", layout = "grid")
    Field_Text = Text(Search_Window, text = "Field to Search", grid = [0,0])
    global Field_to_Search
    Field_to_Search = Combo(Search_Window, grid=[0,1], options=["Student_ID", "First_Name", "Surname", "Gender", "Subjects", "Teachers", "Year", "Band", "Attendance"])
    Search_Text = Text(Search_Window, text = "Search Term", grid = [0,2])
    global Search_Term
    Search_Term = TextBox(Search_Window, grid = [0,3])
    Start_Search_Button = PushButton(Search_Window,text = "Submit", grid = [0,4], command = Start_Search)
# Search Function Results
def Start_Search():
    Search_List = []
    Result_Window = Window(Main_App, title = "Result", layout = "grid")
    Field_Input = Field_to_Search.get()
    Search_Input = Search_Term.get()
    if Field_Input == "Student_ID":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Student_ID = ?',[Search_Input])
    elif Field_Input == "First_Name":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE First_Name = ?',[Search_Input])
    elif Field_Input == "Surname":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Surname = ?',[Search_Input])
    elif Field_Input == "Gender":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Gender = ?',[Search_Input])
    elif Field_Input == "Subjects":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Subjects = ?',[Search_Input])
    elif Field_Input == "Teachers":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Teachers = ?',[Search_Input])
    elif Field_Input == "Year":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Year = ?',[Search_Input])
    elif Field_Input == "Band":
        Cursor.execute('SELECT * FROM Student_Info_Table WHERE Band = ?',[Search_Input])
    elif Field_Input == "Attendance":
            Cursor.execute('SELECT * FROM Student_Info_Table WHERE Attendance = ?',[Search_Input])
    Search_List = Cursor.fetchall()
    g_x_pos = 0
    grid_pos = 0
    Text_List = []
    for Each_Line in Search_List:
        for each in Each_Line:
            Each_Row = []
            Item = Text(Result_Window, text = each, grid = [ g_x_pos, grid_pos])
            g_x_pos += 1
            Each_Row.append(Item)
        Text_List.append(Each_Row)
        grid_pos += 1
        g_x_pos = 0
    Result_Window.show()               

# Running the program
StudentGrades_Connect()
StudentInfo_Connect()    
LogIn(Logins, Logged_In, LoginGuess, PasswordGuess, LoginInput, PasswordInput)
