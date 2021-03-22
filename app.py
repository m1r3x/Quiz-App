import ast
import sys
import time

# Login part(Written by Elshad Sabziyev)


counter = 0  # counter for timeout
global t0


class RestrictedItems:
    restricted = ["a", "b", "c", "d", "e", "n", "x", "y", " ", "", "A", "B", "C", "D", "E", "N", "X", "Y"]


def run(role):  # runs login/register functions
    print('''
Welcome to quiz app.
Do you want to login or register?
Please, select one of the options below:
>>>For logging in [1]
>>>For registering [2]
>>>For stopping app and exit [x]\n
                    ''')
    while True:
        selection = input("Your answer >>> ")
        if selection != "1" and selection != "2" and selection != "x" and selection != "X":
            print('''\n\nPlease, enter the correct value.
>>>For logging in [1]
>>>For registering [2]
>>>For stopping app and exit [x]\n\n''')
        else:
            break

    if selection == "1":
        login(role)

    elif selection == "2":
        register(role)

    elif selection == "x" or selection == "X":
        exit("bye!!!")


def login(role):  # Function that related to login choice

    username = input("\nPlease, enter your username >>> ")
    password = input("Please, enter your password >>> ")
    isCorrect = loginControl(username, password, role)  # Gets info that if login credentials are correct or not
    if isCorrect:
        loginSuccess(username, password, role)

    else:
        loginUnsuccessful(
            "\nWrong credentials!!!\nPlease, make sure you entered correct username and password", username)

        choice_l = input("""
        B > Go Back
        X > Exit

        Any other key(Or Enter) > Re-login

        What do you want to do? >>> """).upper()

        if choice_l == "B":
            print("\n\nMAIN MENU\n\n")
            run(role)
        elif choice_l == "X":
            exit("\n\nGood bye!!!\n\n")
        else:
            login(role)


def login2(role):  # Function that related to login choice

    username = input("\nPlease, enter your username >>> ")
    password = input("Please, enter your password >>> ")
    isCorrect = loginControl(username, password, role)  # Gets info that if login credentials are correct or not
    if isCorrect:
        global counter
        counter = 0
        loginSuccess(username, password, role)
    else:
        loginUnsuccessful(
            "\nWrong credentials!!!\nPlease, make sure you entered correct username and password", username)
        login2(role)


def register(role):  # Function to registering new users
    while True:
        username = input("\nPlease, enter your username >>> ")
        if username not in RestrictedItems.restricted and not username.isdigit():
            break
        else:
            print("\nNot a valid input for the username, please, try another one\n"
                  "Note: input cannot be just >>>Integers  or/and ", RestrictedItems.restricted)
    roleInput0 = input("Are you teacher or student. Please select one role: [T] for teacher and [S] for student "
                       ">>> ")

    roleInput = roleInput0.lower()
    while roleInput != "t" or roleInput != "s":
        if roleInput == "t":
            role = "T"
            break
        elif roleInput == "s":
            role = "S"
            break
        else:
            print("\n\nPlease, enter the correct value.")
            roleInput0 = input(
                "\nAre you teacher or student. Please select one role: [T] for teacher and [S] for student >>> ")
            roleInput = roleInput0.lower()

    while True:
        password = input("\nPlease, enter your password >>> ")
        passwordRepeat = input("Please, enter your password again >>> ")
        if password == passwordRepeat:
            break
        else:
            print("\n\nPlease, be sure you entered the same password again to avoid mistyping")

    isUserRegistered = isRegistered(username)
    if isUserRegistered:
        print("\nThis user exists in our Database. Please, log in your account.")
        login2(role)
    else:
        createUser(username, password, role)
        print("\nYou have been registered successfully. Please, log in your account.")
        login2(role)


def isRegistered(username):  # Checks if any user registered before or not.
    credentials = getCredentials()
    try:
        for user in list(credentials.keys()):
            if user == username:
                return True
    except KeyError:
        return False

    return False


def createUser(username, password, role):
    credentials = getCredentials()
    credentials[username] = [password, role, 0]

    with open("appDB.json", "w") as DB:
        DB.write(str(credentials))


def isTimeout(username):
    credentials = getCredentials()
    timeoutdate = credentials[username][2]
    try:
        if float(time.time()) < float(timeoutdate):
            return True
    except UnboundLocalError:
        return True
    return False


def loginControl(username, password, role):  # Control login credentials
    credentials = getCredentials()
    try:
        isTimeoutkey = isTimeout(username)
        if credentials[username][0] == password and credentials[username][2] == 0:
            global counter
            counter = 0
            return True
        elif credentials[username][0] == password and credentials[username][2] != 0:
            if isTimeoutkey:
                sys.exit('''You are timed out.
##################### COME BACK LATER ####################''')
            else:
                credentials[username][2] = 0
                counter = 0
                with open("appDB.json", "w") as DB:
                    DB.write(str(credentials))
                loginSuccess(username, password, role)

        elif credentials[username][0] != password:
            if isTimeoutkey:
                sys.exit('''You are timed out.
##################### COME BACK LATER ####################''')
            else:
                return False
        else:
            return False

    except KeyError:
        print("Wrong credentials")
        choice_l = input("""
B > Go Back
X > Exit

Any other key(Or Enter) > Re-login

What do you want to do? >>> """).upper()

        if choice_l == "B":
            print("\n\nMAIN MENU\n\n")
            run(role)
        elif choice_l == "X":
            exit("\n\nGood bye!!!\n\n")
        else:
            login(role)


def loginSuccess(username, password, role):  # Function that runs when login credentials are correct
    credentials = getCredentials()
    global counter
    counter = 0
    isTimeoutkey = isTimeout(username)
    credentials[username][2] = 0
    try:
        with open("appDB.json", "w") as DB:
            DB.write(str(credentials))
    except:
        createUser(username, password, role)
        with open("appDB.json", "w") as DB:
            DB.write(str(credentials))
    print(
        "You have successfully logged in. Welcome to Quiz "
        "App\n####################################################################################")
    appRun(username, role)


def loginUnsuccessful(reason, username):  # Function that makes the user check his/her login credentials
    credentials = getCredentials()
    global counter
    counter = counter + 1
    if counter > 2:
        t0 = float(time.time() + 300)  # timeout duration(5 minutes)
        credentials[username][2] = t0
        with open("appDB.json", "w") as DB:
            DB.write(str(credentials))

        sys.exit('''You are timed out.
##################### COME BACK LATER ####################''')

    print(reason)


def getCredentials():  # Gets login credentials from appDB
    try:
        with open("appDB.json", "r") as DB:
            credentials = ast.literal_eval(DB.read())
    except:

        with open("appDB.json", "w") as DB:
            DB.write(
                '{"teacher_rt":["p@ssword","T",0]}')

        with open("appDB.json", "r") as DB:
            credentials = ast.literal_eval(DB.read())

    return credentials


def appRun(username, role):  # functiono that runs in the last stage of login(to present correct menu)
    credentials = getCredentials()
    if credentials[username][1] == "T":
        teacher_menu(username, role)
    else:
        std_menu(username, role)


# Teacher part(written by Mahammadjan Mahammadjanov)


def create_file(name):  # function that creates required file when called
    with open(f"{name}.json", "w") as q_file:
        q_file.write("{}")


def view_quizzes(username, role):  # function for teachers to use when viewing quizzes
    try:
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())
    except:
        create_file("quiz")
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())

    x = list(saved_quizzes.keys())
    print("Quizzes: ")
    for i in range(0, len(x)):
        print(str(i + 1) + " > " + x[i])
    print("")
    print("B > Go back")
    print("")
    choice = input("Which quiz do you want to view?(select a number): ")
    if choice.upper() == "B":
        return teacher_menu(username, role)
    else:
        choice = int(choice)
        to_show = saved_quizzes[x[choice - 1]]
        for i in range(0, len(to_show)):
            print("")
            print("Question " + str(i + 1) + ": " + to_show[i]["Question"])
            print("")
            print("Options: ")
            for n in to_show[i]["Options"]:
                print(n)
            print("")
            print("Answer: " + to_show[i]["Answer"])
            print("")
    return view_quizzes(username, role)


def delete_quizzes(username, role):  # function for teachers to use when deleting a quiz
    possible_choices = ["B"]

    try:
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())
    except:
        create_file("quiz")
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())

    try:
        with open("responses.json", "r") as q_file:
            saved_responses = ast.literal_eval(q_file.read())
    except:
        create_file("responses")
        with open("responses.json", "r") as q_file:
            saved_responses = ast.literal_eval(q_file.read())

    x = list(saved_quizzes.keys())
    print("Quizzes: ")
    for i in range(0, len(x)):
        print(str(i + 1) + " > " + x[i])
        possible_choices.append(str(i + 1))
    print("")
    print("B > Go back")
    print("")
    choice = input("Which quiz do you want to delete?(select a number) >>> ").upper()

    while choice not in possible_choices:
        choice = input("Please enter a correct option >>> ").upper()

    if choice == "B":
        return teacher_menu(username, role)
    else:
        choice = int(choice)
        to_delete = x[choice - 1]
        print(to_delete)
        saved_quizzes.pop(to_delete)
    with open("quiz.json", "w") as w_file:
        w_file.write(str(saved_quizzes))

    credentials = getCredentials()

    for i in credentials.keys():
        try:
            del (saved_responses[i][to_delete])
        except KeyError:
            pass

    with open("responses.json", "w") as w_file:
        w_file.write(str(saved_responses))

    print("")
    print("Successfully deleted.")
    print("")
    return delete_quizzes(username, role)


def create_quiz(username, role):  # function for teachers to use when creating quiz
    quix = {}  # dictionary of the quiz to be created
    possible_variants = ["A", "B", "C", "D"]
    try:
        with open("quiz.json", "r") as q_file:
            quizzes = ast.literal_eval(q_file.read())

    except:
        create_file("quiz")
        with open("quiz.json", "r") as q_file:
            quizzes = ast.literal_eval(q_file.read())

    while True:
        while True:
            quiz_name = input("Enter quiz name >>> ")
            if quiz_name not in RestrictedItems.restricted and not quiz_name.isdigit():
                break
            else:
                print("Not a valid input for quiz name, please, try another one"
                      "Note: input cannot be just >>> Integers  or/and ", RestrictedItems.restricted)
        for quiz in quizzes.keys():
            if quiz == quiz_name:
                print("Quiz in this name has already been created, please, try another name.")
                create_quiz(username, role)
        break

    quix[quiz_name] = []

    def get_question_count():
        y = 0

        while True:
            try:
                if y == 0:
                    y += 1
                    question_count = int(input("Enter the number of questions >>> "))
                else:
                    question_count = int(input("Please enter an integer >>> "))

                break
            except ValueError:
                pass

        if question_count < 1:
            print("There should be at least 1 question.")
            return get_question_count()
        else:
            return question_count

    question_count = get_question_count()

    for i in range(0, question_count):
        a = {}
        quix[quiz_name].append(a)
        if question_count == 1:
            question = input("Enter the question >>> ")
        else:
            question = input("Enter question " + str(i + 1) + " >>> ")
        quix[quiz_name][i]["Question"] = question
        quix[quiz_name][i]["Options"] = []
        for x in range(0, 4):
            option = possible_variants[x] + ") >>>  "
            possible_answer = input("Enter option " + option)
            quix[quiz_name][i]["Options"].append(option + possible_answer)
        answer = input("Enter the answer(variant) >>> ").upper()
        while answer not in possible_variants:
            answer = input("Please enter a correct letter >>> ").upper()
        quix[quiz_name][i]["Answer"] = answer

    try:
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())
            saved_quizzes.update(quix)
    except:
        create_file("quiz")
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())
            saved_quizzes.update(quix)

    with open("quiz.json", "w") as q_file:
        q_file.write(str(saved_quizzes))

    print("")
    print("Successfully created the quiz!")
    print("")
    return teacher_menu(username, role)


def view_responses(username, role):  # function for teachers to use when viewing student responses
    try:
        with open("responses.json", "r") as r_file:
            responses = ast.literal_eval(r_file.read())
    except:
        create_file("responses")
        with open("responses.json", "r") as r_file:
            responses = ast.literal_eval(r_file.read())

    responded_students = list(responses.keys())
    n1 = []
    for i in range(0, len(responded_students)):
        print(f"{i + 1} > {responded_students[i]}")
        n1.append(str(i + 1))
    print("\nB > Go back\n")
    n1.append("B")

    choice_s = input("Which student do you want to see respones of? >>> ").upper()
    while choice_s not in n1:
        choice_s = input("Please enter correct option >>> ").upper()
    if choice_s == "B":
        return teacher_menu(username, role)
    else:
        choice_s = int(choice_s)
        std_name = responded_students[choice_s - 1]

    std_answers = list(responses[std_name].keys())
    n2 = []
    for i in range(0, len(std_answers)):
        print(f"{i + 1} > {std_answers[i]}")
        n2.append(str(i + 1))
    print("\nB > Go back\n")
    n2.append("B")

    print("")
    choice_q = input("Which quiz? >>> ").upper()
    while choice_q not in n2:
        choice_q = input("Please enter correct option >>> ").upper()
    if choice_q == "B":
        return view_responses(username, role)
    else:
        choice_q = int(choice_q)
        quizz_name = std_answers[choice_q - 1]

    try:
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())
    except:
        create_file("quiz")
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())

    with open("responses.json", "r") as r_file:
        responses = ast.literal_eval(r_file.read())

        to_show = saved_quizzes[quizz_name]
        for i in range(0, len(to_show)):
            print("")
            print("Question " + str(i + 1) + ": " + to_show[i]["Question"])
            print("")
            print("Options: ")
            for n in to_show[i]["Options"]:
                print(n)
            print("")
            print("Written answer: " + responses[std_name][quizz_name][i] + "\n" + "Correct answer: " + to_show[i][
                "Answer"])
            print("")

        print("The score is: " + str(responses[std_name][quizz_name][-1]))
        print("")
    return view_responses(username, role)


def edit_student(username, role):  # function for teachers to use when editting student accounts
    credentials = getCredentials()
    print('''
A > Add new student
E > Edit already available students

B > Go back
''')
    choices = ["A", "E", "B"]
    choice = input("What do you want to do? >>> ").upper()

    while choice not in choices:
        choice = input("Please enter correct option >>> ").upper()
    if choice == "B":
        return teacher_menu(username, role)
    elif choice == "A":

        username_new = input("\nPlease, enter new username >>> ")
        isUserRegistered = isRegistered(username_new)

        if isUserRegistered:
            print("\nThis user already exists!")
            edit_student(username, role)
        else:
            while True:
                password = input("\nPlease, enter new password >>> ")
                passwordRepeat = input("Please, enter the password again >>> ")
                if password == passwordRepeat:
                    break
                else:
                    print("\n\nPlease, be sure you entered the same password again to avoid mistyping")
            createUser(username_new, password, "S")
            print("\nSuccessfully created the new user!")

            return teacher_menu(username, role)
    else:
        pass

    choices = ["B"]
    a = list(credentials.keys())
    std_list = []
    point = 1
    for user in a:
        if credentials[user][1] == "S":
            std_list.append(user)
            print(f"{point} > {user}")
            choices.append(str(point))
            point += 1
    print("")

    choice = input("Choose the student you want to edit >>> ").upper()
    while choice not in choices:
        choice = input("Please enter correct option >>> ").upper()
    if choice == "B":
        return teacher_menu(username, role)
    else:
        std_username = std_list[int(choice) - 1]  # find std username according to list of student
        print('''
C > Change the password
D > Delete the account

B > Go back

''')
        choices2 = ["C", "D", "B"]
        choice2 = input("What do you want to do? >>> ").upper()

        while choice2 not in choices2:
            choice2 = input("Please enter correct option >>> ").upper()

        if choice2 == "B":
            return edit_student(username, role)
        elif choice2 == "C":
            newpass1 = input("Enter new password >>> ")
            newpass2 = input("Enter again >>> ")
            while newpass1 != newpass2:
                print("Passwords didn't match!")
                newpass1 = input("Enter new password >>> ")
                newpass2 = input("Enter again >>> ")

            credentials[std_username][0] = newpass1
            with open("appDB.json", "w") as DB:
                DB.write(str(credentials))
            print('''
Succesfully updated the password!''')

            teacher_menu(username, role)
        else:
            choice3 = input("Are you sure?(Y for Yes, N for No) >>> ").upper()
            choices3 = ["Y", "N"]
            while choice3 not in choices3:
                choice3 = input("Please enter correct option >>> ").upper()

            if choice3 == "Y":
                credentials.pop(std_username)
                with open("appDB.json", "w") as DB:
                    DB.write(str(credentials))
                print("")
                print("Successfully deleted the user!")
                teacher_menu(username, role)
            else:
                edit_student(username, role)


def change_password(username, role):  # function for teachers to use when changing their own password
    credentials = getCredentials()
    print('''
1 > Change password
B > Go back    
''')
    choices = ["1", "B"]
    choice = input("What do you want to do? >>> ").upper()
    while choice not in choices:
        choice = input("Please enter correct option >>> ").upper()
    if choice == "B":
        return teacher_menu(username, role)
    else:
        newpass1 = input("Enter new password >>> ")
        newpass2 = input("Enter again >>> ")
        while newpass1 != newpass2:
            print("Passwords didn't match!")
            newpass1 = input("Enter new password >>> ")
            newpass2 = input("Enter again >>> ")

    credentials[username][0] = newpass1
    with open("appDB.json", "w") as DB:
        DB.write(str(credentials))
    print('''
Succesfully updated your password!''')
    teacher_menu(username, role)


def check_errors(username, role):  # function for teachers to use when checking feedbacks of students
    try:
        with open("errors.json", "r") as e_file:
            errors = ast.literal_eval(e_file.read())
    except:
        create_file("errors")
        with open("errors.json", "r") as e_file:
            errors = ast.literal_eval(e_file.read())

    error_students = list(errors.keys())
    n1 = []
    for i in range(0, len(error_students)):
        print(f"{i + 1} > {error_students[i]}")
        n1.append(str(i + 1))
    print("B > Go back")
    n1.append("B")

    choice_s = input("Which student do you want to see feedbacks of? >>> ").upper()
    while choice_s not in n1:
        choice_s = input("Please enter correct option >>> ").upper()
    if choice_s == "B":
        return teacher_menu(username, role)
    else:
        n3 = []
        for i in range(0, len(errors[error_students[int(choice_s) - 1]])):
            print(f"{i + 1} > {errors[error_students[int(choice_s) - 1]][i]}")
            n3.append(str(i + 1))
        n3.append("A")
        n3.append("N")
        t_response = input("Which one is resolved?(A for all, N for none, number for specific) >>> ").upper()
        while t_response not in n3:
            t_response = input("Please select correct option >>> ").upper()
        if t_response == "A":
            errors.pop(error_students[int(choice_s) - 1])
            print("Resolved!")
        elif t_response == "N":
            pass
        else:
            del errors[error_students[int(choice_s) - 1]][int(t_response) - 1]
            print("Resolved!")

    with open("errors.json", "w") as e_file:
        e_file.write(str(errors))
    print("")

    return check_errors(username, role)


def teacher_menu(username, role):  # teacher menu
    option = input('''
Teacher's menu
----------------------------

1 > View Quizzes 
2 > View Responses
3 > Delete a Quiz
4 > Create a Quiz
5 > Edit Student Accounts
6 > Change Password
7 > View Feedbacks
B > Back
X > Exit

Select an option >>> ''')
    if option == "1":
        view_quizzes(username, role)

    elif option == "2":
        view_responses(username, role)

    elif option == "3":
        delete_quizzes(username, role)

    elif option == "4":
        create_quiz(username, role)

    elif option == "5":
        edit_student(username, role)

    elif option == "6":
        change_password(username, role)

    elif option == "7":
        check_errors(username, role)

    elif option.upper() == "B":
        run(role)

    elif option.upper() == "X":
        sys.exit()
    else:
        print("")
        print("Please enter correct option.")
        return teacher_menu(username, role)


# Student part(written by Gulnur and Mahammadjan Mahammadjanov)


def take_quiz(username, role):  # function for students to take quiz
    possible_variants = ["A", "B", "C", "D"]
    possible_options = ["B"]

    try:
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())
    except:
        create_file("quiz")
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())

    try:
        with open("responses.json", "r") as r_file:
            responses = ast.literal_eval(r_file.read())
    except:
        create_file("responses")
        with open("responses.json", "r") as r_file:
            responses = ast.literal_eval(r_file.read())

    x = list(saved_quizzes.keys())
    print("Quizzes: ")
    for i in range(0, len(x)):
        print(str(i + 1) + " > " + x[i])
        possible_options.append(str(i + 1))
    print("")
    print("B > Go back")
    print("")
    choice = input("Which quiz do you want to take? >>> ").upper()
    while choice not in possible_options:
        choice = input("Please enter a correct option >>> ").upper()
    if choice.upper() == "B":
        return std_menu(username, role)
    else:
        choice = int(choice)
        quiz_name = x[choice - 1]
        to_do = saved_quizzes[quiz_name]
        with open("responses.json", "r") as r_file:
            responses = ast.literal_eval(r_file.read())
            if username not in list(responses.keys()):
                responses[username] = {}
            else:
                pass
            y = list(responses[username].keys())
            if quiz_name in y:
                options_list = ["1", "B"]
                print("You have already done it.")
                print('''
Show my response > 1
Go back > B
                ''')
                x_choice = input("Select your option >>> ").upper()
                while x_choice not in options_list:
                    x_choice = input("Please enter correct option >>> ").upper()
                if x_choice == "1":
                    return show_response(quiz_name, username, role)
                else:
                    return take_quiz(username, role)

            else:
                correct_number = 0
                responses[username][quiz_name] = []
                for i in range(0, len(to_do)):
                    print("")
                    print("Question " + str(i + 1) + ": " + to_do[i]["Question"])
                    print("")
                    for n in to_do[i]["Options"]:
                        print(n)
                    std_answer = input("Please enter your answer(variant) >>> ").upper()
                    while std_answer not in possible_variants:
                        std_answer = input("Please enter a correct variant >>> ").upper()
                    responses[username][quiz_name].append(std_answer)
                    if saved_quizzes[quiz_name][i]['Answer'] == std_answer:
                        correct_number += 1
                    else:
                        pass
                score = round(correct_number / len(to_do) * 100, 2)
                responses[username][quiz_name].append(score)
                print("")
                print("Your score is: " + str(score))
                print("")
                for i in range(0, len(responses[username][quiz_name]) - 1):
                    if responses[username][quiz_name][i] == saved_quizzes[quiz_name][i]['Answer']:
                        print(f"Question {i + 1} correct!")
                    else:
                        print(
                            f"Question {i + 1} wrong!(Your answer: {responses[username][quiz_name][i]}, Correct answer: {saved_quizzes[quiz_name][i]['Answer']})")
                print("")

        with open("responses.json", "w") as rw_file:
            rw_file.write(str(responses))

    return take_quiz(username, role)


def show_response(q_name,
                  u_name,
                  role):  # function for students to use they have already taken a quiz and want to see their response
    try:
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())
    except:
        create_file("quiz")
        with open("quiz.json", "r") as q_file:
            saved_quizzes = ast.literal_eval(q_file.read())

    try:
        with open("responses.json", "r") as r_file:
            responses = ast.literal_eval(r_file.read())
    except:
        create_file("responses")
        with open("responses.json", "r") as r_file:
            responses = ast.literal_eval(r_file.read())

    to_show = saved_quizzes[q_name]
    for i in range(0, len(to_show)):
        print("")
        print("Question " + str(i + 1) + ": " + to_show[i]["Question"])
        print("")
        print("Options: ")
        for n in to_show[i]["Options"]:
            print(n)
        print("")
        print("Your answer: " + responses[u_name][q_name][i] + "\n" + "Correct answer: " + to_show[i]["Answer"])
        print("")

    print("Your score is: " + str(responses[u_name][q_name][-1]))
    print("")

    return take_quiz(u_name, role)


def std_menu(username, role):  # student menu screen
    option = input('''
Student's menu
----------------------------

1 > Take a quiz
2 > Change credentials
3 > Report Errors
B > Back
X > Exit

Select an option >>> ''')
    if option == "1":
        take_quiz(username, role)

    elif option == "2":
        std_creds(username, role)

    elif option == "3":
        report_errors(username, role)

    elif option.upper() == "B":
        run(role)

    elif option.upper() == "X":
        sys.exit()
    else:
        print("")
        print("Please enter correct option.")
        return std_menu(username, role)


def std_creds(username, role):  # function for students to use when changing password
    credentials = getCredentials()
    print('''
1 > Change password
B > Go back    
''')
    choices = ["1", "B"]
    choice = input("What do you want to do? >>> ").upper()
    while choice not in choices:
        choice = input("Please enter correct option >>> ").upper()
    if choice == "B":
        return std_menu(username, role)
    else:
        newpass1 = input("Enter new password >>> ")
        newpass2 = input("Enter again >>> ")
        while newpass1 != newpass2:
            print("Passwords didn't match!")
            newpass1 = input("Enter new password >>> ")
            newpass2 = input("Enter again >>> ")

    credentials[username][0] = newpass1
    with open("appDB.json", "w") as DB:
        DB.write(str(credentials))
    print('''
Successfully updated your password!''')
    std_menu(username, role)


def role(role):
    return role


def report_errors(username, role):  # function for students to use when reporting errors
    try:
        with open("errors.json", "r") as e_file:
            errors = ast.literal_eval(e_file.read())
    except:
        create_file("errors")
        with open("errors.json", "r") as e_file:
            errors = ast.literal_eval(e_file.read())

    error = input("Please enter a bug, problem or recommendation >>> ")

    try:
        errors[username].append(error)
    except:
        errors[username] = []
        errors[username].append(error)

    with open("errors.json", "w") as ew_file:
        ew_file.write(str(errors))
    print("")
    print("*********************************\nThanks for your input!\n*********************************")
    print("")
    return std_menu(username, role)


role = role(role)
run(role)
