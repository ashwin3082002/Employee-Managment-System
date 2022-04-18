try:
    try:
        import smtplib
    except:
        print("Error 100A")
    try:
        import random
    except:
        print("Error 100B")
    try:
        import mysql.connector
    except:
        print("Error 100C")
    try:
        import json
    except:
        print("Error 100D")
except:
    print("Error 100")

try:
    mydb = mysql.connector.connect(user='root',password='root', host='localhost', database='employees')
    mycursor = mydb.cursor()
except:
    print("Error 100")

def mail_function(to_address,message,subject):
    EMAIL_ADDRESS = "ENTER_YOUR_GMAIL_ACCOUNT"
    EMAIL_PASSWORD = 'ENTER_YOUR_PASSWORD'
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg=f'Subject: {subject}\n\n{message}'
        smtp.sendmail(EMAIL_ADDRESS, to_address, msg)
    return True

def unique_emp_id():
    return random.randint(1111,9999)
def saving_file(emp_id):
    with open('C:/Users/ashwi/Desktop/dbms pec/emp_id.txt', 'w') as file:
        file.write(json.dumps(emp_id))
    file.close()
    return True

print("\n---------------------------------------------")
print("Welcome to Employee Managment System")
print("---------------------------------------------\n")
print("1. Admin Login")
print("2. Employee Login\n")
print("----------------")
choice_main=int(input())
print("----------------")

if choice_main == 1:
    username_admin = input("Enter Admin username:")
    if username_admin == 'admin':
        password_admin = input("Enter Admin Password:")
        if password_admin == 'admin':
            print()
            print("------------------")
            print("Login Successfull")
            print("------------------")
            print()
            print()
            print('''1. Create Employee
2. Search Employee
3. Reset password for Employee
4. Change employee details
5. Delete Employee
6. Logout
            ''')
            print("--------------")
            admin_choice = int(input())
            print("--------------")
            print()

            if admin_choice == 1:
                emp_name = input("Enter Employee Name:")
                emp_gender = input("Enter Employee Gender (M/F):")
                emp_mail = input("Enter Employee Mail ID:")
                emp_mobile = input ("Enter Employee Mobile No:")
                emp_dept = input("Enter Employee Department:") 
                emp_city = input("Enter Employee City:")
                emp_salary = input("Enter Employee Salary:")
                emp_pass = input("Enter Password:")
                emp_id=[]
                file=open('C:/Users/ashwi/Desktop/dbms pec/emp_id.txt', 'r')
                emp_id=file.read()
                emp_id=json.loads(emp_id)
                file.close()
                message = '''
Hello {},

You Profile was Successfully Created by our Admin, with the following Details.
Name: {}
Gender: {}
Mobile: {}
Department: {}
City: {}
Salary: {}

Your Portal Login Credentials,
Username: {}
Password: {}

If you find any mistake in the details contact your HR.

Regards,
Admin'''.format(emp_name,emp_name,emp_gender,emp_mobile,emp_dept,emp_city,emp_salary,emp_mail,emp_pass)
                subject = 'Employee Profile Created!!'
                if mail_function(emp_mail,message,subject):
                    unique_empid = unique_emp_id()
                    while unique_emp_id in emp_id:
                        unique_empid = unique_emp_id()
                    emp_id.append(unique_empid)
                    if saving_file(emp_id):
                        sql_command = "insert into employee_details values('{}',{},'{}','{}',{},'{}','{}',{},'{}');".format(emp_name,int(unique_empid),emp_gender,emp_mail,int(emp_mobile),emp_city,emp_dept,int(emp_salary),emp_pass)
                        mycursor.execute(sql_command)
                        mydb.commit()
                        print()
                        print("Employee Sucessfully Created with Employee ID:{}".format(unique_empid))
                

            elif admin_choice == 2:
                emp_id=[]
                file=open('C:/Users/ashwi/Desktop/dbms pec/emp_id.txt', 'r')
                emp_id=file.read()
                emp_id=json.loads(emp_id)
                file.close()
                emp_id_input = int(input("Enter Employee ID:"))
                if emp_id_input in emp_id:
                    sql_command = "select name, employee_id, gender, email, city, mobile, dept, salary from employee_details where employee_id = {} ".format(emp_id_input)
                    mycursor.execute(sql_command)
                    lst = []
                    for i in mycursor:
                        for j in i:
                            lst.append(j)
                    print()
                    print("Name: {}".format(lst[0]))
                    print("Employee ID: {}".format(lst[1]))
                    print("Gender: {}".format(lst[2]))
                    print("Email: {}".format(lst[3]))
                    print("City: {}".format(lst[4]))
                    print("Mobile No: {}".format(lst[5]))
                    print("Department: {}".format(lst[6]))
                    print("Salary: {}".format(lst[7]))
                    print()
                else:
                    print()
                    print("Employee ID Does Not Exists ")

            elif admin_choice == 3:
                emp_id_input = int(input("Enter Employee ID:"))
                new_emp_pass = input("Enter New Password:")
                confirm_new_pass = input("Confirm Password:")
                if new_emp_pass == confirm_new_pass:
                    sql_command = "update employee_details set password = '{}' where employee_id = {}".format(confirm_new_pass,emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    sql_command1 = "select email from employee_details where employee_id = {}".format(emp_id_input)
                    mycursor.execute(sql_command1)
                    emp_mail = ''
                    for i in mycursor:
                        for j in i:
                            emp_mail=j
                    subject = 'Employee Profile Password Reset Successfull!!'
                    message = ''' 
Hello Employee,
You profile Password has been reset by our admin as per your request.
New Password = {}

We Request you to change your password afer login.

Regards,
Admin'''.format(confirm_new_pass)
                    print()
                    if mail_function(emp_mail,message,subject):
                        print("Password Changed Successfully")
                else:
                    print("Password Not matched. Try Again!!")
            elif admin_choice == 4:
                print('''1. Name
2. City
3. Mobile
4. Email
5. Department 
6. Salary''')
                print('------------')
                choice_user = int(input())
                print('------------')
                emp_id_input = int(input("Enter Employee ID:"))
                if choice_user == 1:
                    emp_name = input("Enter New Name:")
                    sql_command = "update employee_details set name = '{}' where employee_id = {} ".format(emp_name,emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    sql_command1 = "select email from employee_details where employee_id = {}".format(emp_id_input)
                    mycursor.execute(sql_command1)
                    emp_mail = ''
                    for i in mycursor:
                        for j in i:
                            emp_mail=j
                    message = '''
Your Details Have been Updated, 
Login to the portal and check your new details

Regards,
Admin'''
                    subject = 'Employee Details Changed'
                    if mail_function(emp_mail,message,subject):
                        print("Updated Successfully")
                elif choice_user == 2:
                    emp_city= input("Enter New City:")
                    sql_command = "update employee_details set city= '{}' where employee_id = {}".format(emp_city,emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    sql_command1 = "select email from employee_details where employee_id = {}".format(emp_id_input)
                    mycursor.execute(sql_command1)
                    emp_mail = ''
                    for i in mycursor:
                        for j in i:
                            emp_mail=j
                    message = '''
Your Details Have been Updated, 
Login to the portal and check your new details

Regards,
Admin'''
                    subject = 'Employee Details Changed'
                    if mail_function(emp_mail,message,subject):
                        print("Updated Successfully")
                elif choice_user == 3:
                    emp_mob = input("Enter New Mobile No:")
                    sql_command = "update employee_details set mobile= '{}' where employee_id = {}".format(emp_mob,emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    sql_command1 = "select email from employee_details where employee_id = {}".format(emp_id_input)
                    mycursor.execute(sql_command1)
                    emp_mail = ''
                    for i in mycursor:
                        for j in i:
                            emp_mail=j
                    message = '''
Your Details Have been Updated, 
Login to the portal and check your new details

Regards,
Admin'''
                    subject = 'Employee Details Changed'
                    if mail_function(emp_mail,message,subject):
                        print("Updated Successfully")
                elif choice_user == 4:
                    emp_mail = input("Enter New Mail ID:")
                    sql_command = "update employee_details set email = '{}' where employee_id = {}".format(emp_mail,emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    sql_command1 = "select email from employee_details where employee_id = {}".format(emp_id_input)
                    mycursor.execute(sql_command1)
                    emp_mail = ''
                    for i in mycursor:
                        for j in i:
                            emp_mail=j
                    message = '''
Your Details Have been Updated, 
Login to the portal and check your new details

Regards,
Admin'''
                    subject = 'Employee Details Changed'
                    if mail_function(emp_mail,message,subject):
                        print("Updated Successfully")
                elif choice_user == 5:
                    emp_dept = input("Enter New Department:")
                    sql_command = "update employee_details set dept = '{}' where employee_id = {}".format(emp_dept,emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    sql_command1 = "select email from employee_details where employee_id = {}".format(emp_id_input)
                    mycursor.execute(sql_command1)
                    emp_mail = ''
                    for i in mycursor:
                        for j in i:
                            emp_mail=j
                    message = '''
Your Details Have been Updated, 
Login to the portal and check your new details

Regards,
Admin'''
                    subject = 'Employee Details Changed'
                    if mail_function(emp_mail,message,subject):
                        print("Updated Successfully")
                elif choice_user == 6:
                    emp_sal = input("Enter New Salary:")
                    sql_command = "update employee_details set salary = '{}' where employee_id = {}".format(emp_sal,emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    sql_command1 = "select email from employee_details where employee_id = {}".format(emp_id_input)
                    mycursor.execute(sql_command1)
                    emp_mail = ''
                    for i in mycursor:
                        for j in i:
                            emp_mail=j
                    message = '''
Your Details Have been Updated, 
Login to the portal and check your new details

Regards,
Admin'''
                    subject = 'Employee Details Changed'
                    if mail_function(emp_mail,message,subject):
                        print("Updated Successfully")
            elif admin_choice == 5:
                emp_id=[]
                file=open('C:/Users/ashwi/Desktop/dbms pec/emp_id.txt', 'r')
                emp_id=file.read()
                emp_id=json.loads(emp_id)
                file.close()
                emp_id_input = int(input("Enter Employee ID:"))
                if emp_id_input in emp_id:
                    sql_command ="DELETE FROM employee_details WHERE employee_id={};".format(emp_id_input)
                    mycursor.execute(sql_command)
                    mydb.commit()
                    emp_id.remove(emp_id_input)
                    if saving_file(emp_id):
                        print("Employee Deleted Successfully")
                else:
                    print("Employee ID Does'nt Exists")
                
                

            elif admin_choice == 6:
                exit()
            else:
                print("Incorrect Choice!!")

        else:
            print("Wrong Password")

    else:
        print("Wrong Username")
elif choice_main == 2:
    username = input("Enter Username:")
    password = input("Enter Password:")

    sql_command = "select email from employee_details; "
    mycursor.execute(sql_command)
    for i in mycursor:
        if username in i:
            sql_command = "select password from employee_details where email = '{}'".format(username)
            mycursor.execute(sql_command)
            emp_pass = ""
            for i in mycursor:
                for j in i:
                    emp_pass = j
                
            if emp_pass == password:
                print()
                print("Login Successfull")
                sql_command = "select name, employee_id, gender, email, city, mobile, dept, salary from employee_details where email = '{}' ".format(username)
                mycursor.execute(sql_command)
                lst = []
                for i in mycursor:
                    for j in i:
                        lst.append(j)
                print()
                print("Welcome {}".format(lst[0]))
                print("-----------------------------------")
                print("Employee Details")
                print("-----------------------------------")
                print("Name: {}".format(lst[0]))
                print("Employee ID: {}".format(lst[1]))
                print("Gender: {}".format(lst[2]))
                print("Email: {}".format(lst[3]))
                print("City: {}".format(lst[4]))
                print("Mobile No: {}".format(lst[5]))
                print("Department: {}".format(lst[6]))
                print("Salary: {}".format(lst[7]))
                print("------x----------x------------x----")
                print()
            else:
                print("Password Incorrect.")
                exit()
        

        else:
            print("Username Incorrect")
            exit()
    print('''
1. Modify Details
2. Change Password
3. Logout

''')

    choice_user_emp = int(input())
    if choice_user_emp == 1:
        print('''
1. Modilfy email
2. Modify Mobile ''')
        user_choice = int(input())
        if user_choice == 1:
            emp_mail = input("Enter New Mail ID:")
            sql_command = "update employee_details set email = '{}' where email = '{}'".format(emp_mail,username)
            mycursor.execute(sql_command)
            mydb.commit()
            print("Updated Successfully")
        elif user_choice == 2:
            emp_mob = int(input("Enter New Mobile:"))
            sql_command = "update employee_details set mobile = {} where email = '{}'".format(emp_mob,username)
            mycursor.execute(sql_command)
            mydb.commit()
            print("Updated Successfully")
        else:
            print("Incorrect Choice")
    elif choice_user_emp == 2:
        new_emp_pass = input("Enter New Password:")
        confirm_new_pass = input("Confirm Password:")
        if new_emp_pass == confirm_new_pass:
            sql_command = "update employee_details set password = '{}' where email = '{}'".format(confirm_new_pass,username)
            mycursor.execute(sql_command)
            mydb.commit()
            subject = 'Employee Profile Password Change Successfull!!'
            message = ''' 
Hello Employee,
You profile Password has been Changed.
New Password = {}

Regards,
Admin'''.format(confirm_new_pass)
            print()
            if mail_function(username,message,subject):
                print("Password Changed Successfully")
    elif choice_user_emp == 3:
        exit()
    else:
        print("Incorrect Choice")


        
    
        

