#!/usr/bin/python3
#created by James Atterbury in October of 2019
#program to computerize the sign in sheet

from tkinter import *               #Importing tkinter to make interface
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522   #importing the scaner
import datetime                     #importing date time to get current date and time of scan

GPIO.setmode(GPIO.BCM) #setting up gpio mode for led
GPIO.setwarnings(False) #turn off gpio warnings
GPIO.setup(18, GPIO.OUT) #Set up green read light
GPIO.setup(4, GPIO.OUT) #set up rewrite light
GPIO.output(18, GPIO.LOW) #Default off
GPIO.output(4, GPIO.LOW)#default off

reader = SimpleMFRC522() #card scanner setup

AttFile = "/home/pi/Attendance/Attendance" #creating var for txt file

#addind date to top of attendance file
with open (AttFile, "w+") as file:
    if "Date: " in file.read():
        print()
    else:
        printdate = datetime.datetime.today().strftime("%m/%d/%y")
        file.write("Date: " + printdate + "\n")
    file.close()

#method to control the signin button
def signInBTN():
    scanWindow = Tk()                                                          #Creating window to promt scan
    scanWindow.title("Scan Card")                                              #set window title
    scanLbl = Label(scanWindow, text = "Scan Card", font=("", 40), pady = 10)  #make label to prompt user
    scanWindow.geometry("500x100+600+300")                                     #set position of prompt
    scanLbl.pack()                                                             #put lbl in screen
    scanWindow.update()                                                        #display window
    try:                                              #try to
        GPIO.output(18, GPIO.HIGH)                       #turning on green ready light when scanning
        id, text = reader.read()                        #scan card to get id and text
        GPIO.output(18, GPIO.LOW)                        #Truning off ready light when scanned
        if id == 778899532611:                           #if the master/Change key is scan
            #Methods for menu buttons
            def editName():
                menuWindow.destroy()
                rewriteWindow = Tk()                         #Create popup
                rewriteWindow.title("Card Writing")          #title popup
                rewriteWindow.geometry("+600+300")           #position popup
                rewritelbl = Label(rewriteWindow, text = "Enter the new data", font = ("", 25)) #label to prompt rewrite of card
                rewritelbl.pack()                                                               #place label
                rewriteEntry = Entry(rewriteWindow, font = ("", 25))                            #box to enter new data
                rewriteEntry.pack()                                                             #place databox
                #method for when the rewrite button is pushed
                def reWrite():
                    GPIO.output(4, GPIO.HIGH)                #truning on the rewrite ready light
                    reader.write(rewriteEntry.get())         #rewriting card scanned
                    GPIO.output(4, GPIO.LOW)                #truning off the rewrite ready light
                    rewriteWindow.destroy()                 #close popup
                rewritebtn = Button(rewriteWindow, text = "Write", command=reWrite, font = ("", 25))#create button to rewrite card
                rewritebtn.pack()

            def manualInput():
                menuWindow.destroy()
                manualWindow = Tk()                            #create popup window to add name manually
                manualWindow.title("Manual Entry")             #set manual title
                manualWindow.geometry("+600+300")              #set manual window popup position
                manlbl = Label(manualWindow, text = "Enter Name", font = ("", 25)) #create label to prompt for name
                manlbl.pack()                                  #plce prompt lbl
                manEntry = Entry(manualWindow, font=("", 25))  #create entry to take name
                manEntry.pack()                                #place entry
                #method for when enter button clicked
                def submit():
                    currentDT = datetime.datetime.now()              #get date and time of card scanned
                    printTime = currentDT.strftime("%I:%M:%S %P")    #set it to the format to be printed
                    with open(AttFile, "a+") as openFile:            #open attendance file
                        openFile.write(manEntry.get().strip() + "\t\t\t" + printTime + "\n") #write to file
                        openFile.close()                              #close file
                    attbx.configure(state="normal")
                    attbx.delete("1.0", END)                                  #Clear attendance so it can be updated
                    attbx.insert(END, open(AttFile).read())                   #insert text
                    attbx.configure(state="disabled")
                    manualWindow.destroy()                            #close popup
                manBtn = Button(manualWindow, text = "Enter", command = submit, font=("",25))#make button to submit name
                manBtn.pack()                                                                #place button

            def editEvents():
                menuWindow.destroy()
                monText.configure(state="normal")   #next six lines enable editing on text fields
                tueText.configure(state="normal")
                wedText.configure(state="normal")
                thurText.configure(state="normal")
                friText.configure(state="normal")
                def savefuture():
                    with open("/home/pi/Attendance/Monday" , "w+") as monFile:#open monday file
                        monFile.write(monText.get("1.0",END))    #write to file
                        monFile.close()                          #close file
                    with open("/home/pi/Attendance/Tuesday" , "w+") as tueFile:#open tuesday file
                        tueFile.write(tueText.get("1.0",END))    #write to file
                        tueFile.close()                          #close file
                    with open("/home/pi/Attendance/Wednesday" , "w+") as wedFile:#open wednesday file
                        wedFile.write(wedText.get("1.0",END))    #write to file
                        wedFile.close()                          #close file
                    with open("/home/pi/Attendance/Thursday" , "w+") as thurFile:#open thursday file
                        thurFile.write(thurText.get("1.0",END))  #write to file
                        thurFile.close()                         #close file
                    with open("/home/pi/Attendance/Friday" , "w+") as friFile:#open friday file
                        friFile.write(friText.get("1.0",END))    #write ti file
                        friFile.close()                          #close file
                    monText.configure(state="disabled")    #next six lines turn off editing on text fields and delete save button
                    tueText.configure(state="disabled")
                    wedText.configure(state="disabled")
                    thurText.configure(state="disabled")
                    friText.configure(state="disabled")
                    upComingbtn.grid_forget()
                upComingbtn = Button(root, text = "Save", command = savefuture, font=("", 25)) #create save btn to save upcoming events
                upComingbtn.grid(row = 29,column = 4)                                        #place save button

            def clearAttendance():
                menuWindow.destroy()
                with open (AttFile, "r+") as file:
                    file.truncate(0)
                    file.close()
                attbx.configure(state="normal")
                attbx.delete("1.0", END)                                  #Clear attendance so it can be updated
                attbx.insert(END, open(AttFile).read())                   #insert text
                attbx.configure(state="disabled")

            def changeEmail():
                menuWindow.destroy()
                emailWindow = Tk()                            #create popup window to add name manually
                emailWindow.title("Change Email Address")             #set manual title
                emailWindow.geometry("+600+300")              #set manual window popup position
                emaillbl = Label(emailWindow, text = "Enter Name", font = ("", 25)) #create label to prompt for name
                emaillbl.pack()                                  #plce prompt lbl
                emailEntry = Entry(emailWindow, font=("", 20), width = 50)  #create entry to take name
                emailEntry.pack()                                #place entry
                #method for when enter button clicked
                def submitemail():
                    with open ("/home/pi/Attendance/emailaddress", "w+") as emailAddress: #open attendance file
                        emailAddress.write(emailEntry.get().strip()) #write to file
                        emailAddress.close()                              #close file
                        emailWindow.destroy()                            #close popup
                emailBtn = Button(emailWindow, text = "Enter", command = submitemail, font=("",25))#make button to submit name
                emailBtn.pack()                                                                #place button

            menuWindow = Tk()                         #Create popup
            menuWindow.title("Option Menu")          #title popup
            menuWindow.geometry("250x350")           #position popup
            EditBtn = Button(menuWindow, text = "Edit Name", font=("",20), command = editName)       # creating buttons for ,menu and placing them
            ManBtn = Button(menuWindow, text = "Manual Input", font=("",20), command = manualInput)
            upcomingBtn = Button(menuWindow, text = "Edit Events", font=("",20), command = editEvents)
            AttBtn = Button(menuWindow, text= "Clear Attendance", font=("", 20), command= clearAttendance)
            EmailBtn = Button(menuWindow, text="Change Email", font=("", 20), command = changeEmail)
            EditBtn.pack(padx = 10, pady = 10)
            ManBtn.pack(padx = 10, pady = 10)
            upcomingBtn.pack(padx = 10, pady = 10)
            AttBtn.pack(padx = 10, pady=10)
            EmailBtn.pack(padx=10, pady=10)


        else:
            currentDT = datetime.datetime.now()              #get date and time of card scanned
            printTime = currentDT.strftime("%I:%M:%S %P")    #set it to the format to be printed
            with open(AttFile, "a+") as openFile:            #open attendance file
                openFile.write(text.strip() + "\t\t\t" + printTime + "\n") #write to file
                openFile.close()                             #close textfile
    finally:                                          #Finally do
        scanWindow.destroy()                                      #destroy scan window
        attbx.configure(state="normal")
        attbx.delete("1.0", END)                                  #Clear attendance so it can be updated
        attbx.insert(END, open(AttFile).read())                   #insert text
        attbx.configure(state="disabled")

root = Tk()                                                                  #creating main window
root.attributes('-fullscreen', True)
root.title("Sign In Sheet")                                                  #set title of main window
attLbl = Label(text = "Attendance", font=("", 25))                           #create lbl
attLbl.grid(row = 0, column = 1)                                             #place lbl
attbx = Text(root, width = 45, height = 25, font = ("", 25))                 #at text widget to display names
attbx.configure(state = "normal")
attbx.insert(END, open(AttFile).read())                                      #insert names
attbx.configure(state = "disabled")
attbx.grid(row = 1, column = 0, columnspan = 3, rowspan = 23,padx = 10)                #place text widget in window
signButton = Button(root, text="Sign In", command=signInBTN, font=("", 25))  #create button to call sign scan function
signButton.config(height = 2, width = 43)
signButton.grid(row = 29, column = 1)                                         #place button


upLbl = Label(root, text = "Upcoming Events", font=("", 25))                 #creat upcoming events label
upLbl.grid(row = 0, column = 4)                                              #place label
monlbl = Label(root, text = "Monday" , font = ("", 20))                      #creating monday label
monlbl.grid(row = 1 , column = 3)                                            #place monday lbl
monText = Text(root, height = 8, width = 59,font=("",15))                   #text box to store monday events
monText.insert(END, open("/home/pi/Attendance/Monday").read())             #print monday events
monText.configure(state="disabled")
monText.grid(row = 1, column = 4)                                          #place monday txtb
tuelbl = Label(root, text = "Tuesday" , font = ("", 20))                      #creating tuesdat label
tuelbl.grid(row = 2, column = 3)                                            #place tuesday lbl
tueText = Text(root, height = 8, width = 59,font=("",15))                   #text box to store tue events
tueText.insert(END, open("/home/pi/Attendance/Tuesday").read())            #print tuesday events
tueText.configure(state="disabled")
tueText.grid(row = 2, column = 4)                                          #place tue txtb
wedlbl = Label(root, text = "Wednesday" , font = ("", 20))                      #creating wed label
wedlbl.grid(row = 3 , column = 3)                                            #place wed lbl
wedText = Text(root, height = 8, width = 59,font=("",15))                   #text box to store wed events
wedText.insert(END, open("/home/pi/Attendance/Wednesday").read())          #print wednesday events
wedText.configure(state="disabled")
wedText.grid(row = 3, column = 4)                                          #place wed txtb
thurlbl = Label(root, text = "Thursday" , font = ("", 20))                      #creating thur label
thurlbl.grid(row = 4 , column = 3)                                            #place thur lbl
thurText = Text(root, height = 8, width = 59,font=("",15))                   #text box to store thur events
thurText.insert(END, open("/home/pi/Attendance/Thursday").read())             #print thursday events
thurText.configure(state="disabled")
thurText.grid(row = 4, column = 4)                                          #place thur txtb
frilbl = Label(root, text = "Friday" , font = ("", 20))                      #creating fri label
frilbl.grid(row = 5 , column = 3)                                            #place fri lbl
friText = Text(root, height = 8, width = 59,font=("",15))                   #text box to store fri events
friText.insert(END, open("/home/pi/Attendance/Friday").read())              #print friday events
friText.configure(state="disabled")
friText.grid(row = 5, column = 4)                                          #place fri txtb

#if statements to figure out the day of the week to "highlight" current day of week
if (datetime.datetime.today().weekday() == 0):
    monlbl.config(relief = "solid", padx = 10, pady = 10,bg = "yellow")
elif(datetime.datetime.today().weekday() == 1):
    tuelbl.config(relief = "solid", padx = 10, pady = 10,bg = "yellow")
elif(datetime.datetime.today().weekday() == 2):
    wedlbl.config(relief = "solid", padx = 0, pady = 10,bg = "yellow")
elif(datetime.datetime.today().weekday() == 3):
    thurlbl.config(relief = "solid", padx = 10, pady = 10,bg = "yellow")
elif(datetime.datetime.today().weekday() == 4):
    frilbl.config(relief = "solid", padx = 10, pady = 10,bg = "yellow")

root.mainloop()