#Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import threading
import smtplib
import sys

import credentials #The file which stores passwords and guest id's

#All the rides with fastpasses: ak = animal kingdom, mk = magic kingdom, hs = hollywood studios, e = epcot
akRides = ["Avatar Flight of Passage", "Na'vi River Journey", "DINOSAUR", "Expedition Everest - Legend of the Forbidden Mountain", "Festival of the Lion King", "Finding Nemo - The Musical", "It's Tough to be a Bug!", "Kali River Rapids", "Kilimanjaro Safaris", "Meet Favorite Disney Pals", "Primeval Whirl", "Rivers of Light"]
mkRides = ["The Barnstormer", "Big Thunder Mountain Railroad", "Buzz Lightyear's Space Ranger Spin", "Dumbo the Flying Elephant", "Enchanted Tales with Belle", "Haunted Mansion", "it's a small world", "Jungle Cruise", "Mad Tea Party", "The Magic Carpets of Aladdin", "The Many Adventures of Winnie the Pooh", "Meet Ariel at Her Grotto", "Meet Cinderella", "Meet Mickey", "Meet Rapunzel", "Meet Tinker Bell", "Mickey's PhilharMagic", "Monsters, Inc. Laugh Floor", "Peter Pan's Flight", "Pirates of the Caribbean", "Space Mountain", "Splash Mountain", "Tomorrowland Speedway", "Journey of The Little Mermaid", "Seven Dwarfs Mine Train"]
hsRides = ["Beauty and the Beast-Live", "Fantasmic!", "Rock 'n' Roller Coaster", "Disney Junior - Live", "Frozen Sing-Along", "Epic Stunt Spectacular!", "Muppet*Vision 3D", "Star Tours", "The Twilight Zone Tower", "Voyage of The Little Mermaid", "Toy Story Mania!", "Slinky Dog Dash - Now Open!", "Alien Swirling Saucers"]
eRides = ["Frozen Ever After", "IllumiNations", "Soarin'", "Test Track", "Short Film Festival", "Journey Into Imagination", "Living with the Land", "Meet Disney Pals", "Mission: SPACE", "Nemo & Friends", "Spaceship Earth", "Turtle Talk With Crush"]

#Grouped all rides into an array to get
parkRides = [mkRides, eRides, hsRides, akRides]

#Handy internal tool to check if an element exists
def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#This function checks whether the user has filled out the email and password in credentials.py file
def checkCredentialsFile():
    if not len(credentials.users):
        return False
    for user in credentials.users:
        if user[0] == '' and  user[1] == '':
            return False
    return True

#Returns a park that the user wants fastpasses for
def getPark():

    print("Magic Kingdom: 1 | Epcot: 2 | Hollywood Studios: 3 | Animal Kingdom: 4\n")
    park = input("What park are you going to: ")

    #Loops until input equals 1, 2, 3, or 4
    while park != "1" and park != "2" and park != "3" and park != "4":
        park = input("Invalid Choice... What park are you going to: ")

    return park


#Function to handle getting magic kingdom ride names
def getRide(park):

    parkrides = parkRides[int(park) - 1] #identifies the chosen park rides

    counter = 0

    if park == "1":
        print("\nMAGIC KINGDOM RIDES")
    elif park == "2":
        print("\nEPCOT RIDES")
    elif park == "3":
        print("\nHOLLYWOOD STUDIOS RIDES")
    elif park == "4":
        print("\nANIMAL KINGDOM RIDES")
    print("-------------------------------------")

    #Loops through all magic kingdom or animal kingdom rides and takes out a ride that has been chosen previously
    for currentride in parkrides:
        counter += 1
        print(str(counter) + ".) " + currentride) 

    print("") #add an extra line for style
    chosenride = input("Choose a ride: ")
    print("") #add an extra line for style

    return chosenride

def getMinHour():
    return input("\nWhat is the earliest you want the FastPass (Example format: 2PM) : ")

def getMaxHour():
    return input("What is the latest you want the FastPass (Example format: 10PM) : ")

#Returns the number of guests in the party
def getNumberOfGuests():

    numGuests = input("\nHow many people in the party including yourself:\n" +
                  "       1.) Just 1\n" +
                  "       2.) 2 or More\n" +
                  "Option: ")
    while numGuests != "1" and numGuests != "2":
          numGuests = input("--INVALID CHOICE-- How many people in the party including yourself:\n" +
                      "       1.) Just 1\n" +
                      "       2.) 2 or More\n"+
                      "Option: ")
    return numGuests

#Converts the ride number to the actual ride name
def convertRideNumToText(park, ride):
    parkrides = parkRides[int(park)-1]
    return parkrides[int(ride)-1]

#Prints out the rides chosen and calls function aboce to convert from ride number to text
def printOutRidesChosen(park, ride, numGuests, minTime, maxTime):
    if str(numGuests) == "2":
        numGuests = "2 or more"

    if minTime == False:
        timeFrame = "Any Time"
    else:
        timeFrame = minTime + " - " + maxTime

    print("\nSummary:\n" +
          "   People in party: " + numGuests + "\n" +
          "   Fastpass: " + ride + "\n" +
          "   Time Frame: " + timeFrame)

#Creates the chrome driver
def createChromeDriver():
    print("\nOpening Chrome WebDriver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    chrome_path = credentials.path

    return webdriver.Chrome(chrome_path, options=options)

#Clicks the first button on the website, the 'get started' button
def clickGetStartedButton(driver):
    while True:
        try:
            driver.find_element_by_xpath("""//*[@id="fastPasslandingPage"]/div[3]/div[1]/div/div/div/div""").click()
            break
        except:
            continue

#Signs the user in with the email and password provided in the credentials.py file
def signIn(driver, email, password):
    print("\nSigning you in...")
    while True:
        try:
            driver.find_element_by_xpath("""//*[@id="loginPageUsername"]""").send_keys(email)
            driver.find_element_by_xpath("""//*[@id="loginPagePassword"]""").send_keys(password)
            driver.find_element_by_xpath("""//*[@id="loginPageSubmitButton"]/span""").click()
            break
        except:
            continue

#Clicks button to continue to date selection
def continueToDateSelection(driver):
    driver.find_element_by_xpath("""//*[@id="selectPartyPage"]/div[3]/div/div[2]/div""").click()

#Clicks button to continue from plan overview to select party
def continueToSelectUsersScreen(driver):
    driver.find_element_by_xpath("""//*[@id="fastPasslandingPage"]/div[2]/div[3]/div/div[1]/div/div""").click()

# Loop every 1 minute to check if the "View My Plans" link shown in the "Choose Date & Park" page is present.
def specifyGuests(driver):
    try:
        element = WebDriverWait(driver, 3600).until(
            EC.presence_of_element_located((By.ID, 'viewMyPlansLink'))
        )
    except Exception as e:
        print(e)
    finally:
        return

#This is the function that provides logic based on if the user is by themself or with a party
def selectGuests(driver, numGuests):
    guestschosen = False

    while guestschosen == False:
        if numGuests == "1":
            try:
                continueToDateSelection(driver) #If the user has no plans
                guestschosen = True #breaks the loop
            except:
                try:
                    continueToSelectUsersScreen(driver) #The user has plans and must click additional button to get to 'select guests' screen
                except:
                    continue
        elif numGuests == "2":
            try:
                continueToSelectUsersScreen(driver)
                print('---PLEASE CHOOSE YOUR GUESTS ON SCREEN NOW---')
                specifyGuests(driver)
                guestschosen = True
            except:
                continue

    return

#This clicks the button of the park they chose
def selectPark(driver, park):
    while True:
        try:
            driver.find_element_by_xpath("""//*[@id="selectParkContainer"]/div[3]/div[""" + park + """]/div/div[1]/img""").click()
            print("\nSelecting the park...\n")
            break
        except:
            continue

#This function loops through morning, afternoon, and evening time frames
def loopTimePeriod(driver, currentTimePeriod):
    try:
        if currentTimePeriod == 1:
            driver.find_element_by_xpath("""//*[@id="selectExperienceTimeFilter"]/div/div[2]/div""").click() #Clicks afternoon
            return 2
        elif currentTimePeriod == 2:
            driver.find_element_by_xpath("""//*[@id="selectExperienceTimeFilter"]/div/div[3]/div""").click() #Clicks evening
            return 3
        elif currentTimePeriod == 3:
            driver.find_element_by_xpath("""//*[@id="selectExperienceTimeFilter"]/div/div[1]/div""").click() #Clicks morning
            return 1
    except:
        try:
            driver.refresh() #refreshes the page if a disney error 'could not get page' appears because of the rapid requests being sent
            return 1
        except:
            return 1

def confirmRide(driver, ride, num, timeNum, rideLocation, overrideChoice):
    if timeNum == 0:
        timeNum = 1
    timeText = driver.find_element_by_xpath("""//*[@id="selectExperienceExperiencesList"]/div[""" + str(rideLocation) + """]/div[2]/div[""" + str(num) + """]/div/div[2]/div/div[""" + str(timeNum) + """]""").click()
    sleep(2)

    # Override other reservation
    if (overrideChoice == '1' and
        check_exists_by_xpath(driver, """//*[@id="conflictsPagePage"]/div[4]/div[4]/div/div[3]/div/div[3]/div/div[1]""")):

        guests = driver.find_elements_by_class_name('guestContainer')

        # Click continue for each guest
        for guest in guests:
            while True:
                try:
                    driver.find_element_by_xpath("""//*[@id="conflictsPagePage"]/div[4]/div[4]/div/div[3]/div/div[3]/div/div[1]""").click()
                except:
                    break
            sleep(1)

        # Click next to proceed to confirmation page
        while True:
            try:
                driver.find_element_by_xpath("""//*[@id="conflictsPagePage"]/div[5]/div/div[3]/div""").click()
                break
            except:
                continue

    while True:
        try:
            driver.find_element_by_xpath("""//*[@id="reviewConfirmButton"]/div""").click()
            print(ride + " HAS BEEN CONFIRMED!")
            sleep(15)
            break
        except:
            continue


def checkTime(driver, num, minHour, maxHour, rideLocation):
    if minHour == False:
        return 1

    for x in range(1, 4):
        timeText = driver.find_element_by_xpath("""//*[@id="selectExperienceExperiencesList"]/div[""" + str(rideLocation) + """]/div[2]/div[""" + str(num) + """]/div/div[2]/div/div[""" + str(x) + """]""")

        if len(timeText.text) == 7:
            rideTime = timeText.text[:1]
            rideTimeZone = timeText.text[5:]
        if len(timeText.text) == 8:
            rideTime = timeText.text[:2]
            rideTimeZone = timeText.text[6:]

        if rideTimeZone == "PM" and rideTime != "12":
            rideTime = int(rideTime) + 12

        if x == 1:
            if len(minHour) == 3:
                minZone = minHour[1:]
                minHour = minHour[:1]
            elif len(minHour) == 4:
                minZone = minHour[2:]
                minHour = minHour[:2]

            if len(maxHour) == 3:
                maxZone = maxHour[1:]
                maxHour = maxHour[:1]
            elif len(maxHour) == 4:
                maxZone = maxHour[2:]
                maxHour = maxHour[:2]

            if minZone == "PM" and minHour != "12":
                minHour = int(minHour) + 12
            else:
                minHour = int(minHour)

            if maxZone == "PM" and maxHour != "12":
                maxHour = int(maxHour) + 12
            else:
                maxHour = int(maxHour)


        if int(rideTime) <= int(maxHour) and int(rideTime) >= int(minHour):
            return x


        
    return False

def magicKingdomParkHandler(driver, ride, minHour, maxHour, overrideChoice):

    try:
        for num in range(1, len(mkRides) + 1):
            try:
                element = driver.find_element_by_xpath("""//*[@id="selectExperienceExperiencesList"]/div[2]/div[2]/div[""" + str(num) + """]""") #uses num to go through all the rides on the website
                if ride in element.text:

                    timeNum = checkTime(driver, num, minHour, maxHour, 2)
                    if timeNum != False:
                        confirmRide(driver, ride, num, timeNum, 2, overrideChoice)
                        return True
            except:
                continue
    except:
        return False

    return False

def animalEpcotHollywoodParkHandler(driver, park, ride, minHour, maxHour, overrideChoice):
    try:
        for num in range(1, len(parkRides[int(park) - 1]) + 1):
            try:
                element = driver.find_element_by_xpath("""//*[@id="selectExperienceExperiencesList"]/div[2]/div[2]/div[""" + str(num) + """]""")
                if ride in element.text:

                    timeNum = checkTime(driver, num, minHour, maxHour, 2)
                    if timeNum != False:
                        confirmRide(driver, ride, num, timeNum, 2, overrideChoice)
                        return True
            except:
                continue
        for num in range(1, len(parkRides[int(park) -1]) + 1):
            try:
                element = driver.find_element_by_xpath("""//*[@id="selectExperienceExperiencesList"]/div[3]/div[2]/div[""" + str(num) + """]""")
                if ride in element.text:

                    timeNum = checkTime(driver, num, minHour, maxHour, 3)
                    if timeNum != False:
                        confirmRide(driver, ride, num, timeNum, 3, overrideChoice)
                        return True
            except:
                continue


    except:
        return False


    return False

def create_instance(user, numGuests, park, ride, minHour, maxHour, overrideChoice):
    driver = createChromeDriver()

    driver.get("https://disneyworld.disney.go.com/fastpass-plus/")

    clickGetStartedButton(driver)

    signIn(driver, user[0], user[1])

    selectGuests(driver, numGuests)

    print("{}\n---PLEASE CHOOSE A DATE ON SCREEN NOW---".format(user[0]))

    selectPark(driver, park)

    allRidesFound = False
    currentTimePeriod = 1

    while allRidesFound == False:
        sleep(5)

        #If the park is magic kingdom, it has its seperate function because of the different HTML layout on the website
        if park == "1":
            allRidesFound = magicKingdomParkHandler(driver, ride, minHour, maxHour, overrideChoice)
        else:
            allRidesFound = animalEpcotHollywoodParkHandler(driver, park, ride, minHour, maxHour, overrideChoice)

        #Click button to switch between morning, afternoon, and evening time periods
        if allRidesFound == False:
            currentTimePeriod = loopTimePeriod(driver, currentTimePeriod)

    return

#Where the program starts
def main():

    if not checkCredentialsFile():
        sys.exit("You need to fill out the credentials.py file before continuing")

    print("Welcome to Disney FastPass Finder!")

    instances = []

    for user in credentials.users:

        print('\n--- {} ---\n'.format(user[0]))
        park = getPark()

        # If the park is magic kingdom set the ride1, ride2, ride3 equal to the chosen ride
        ride = getRide(park)

        timeFrameChoice = input("Do you want to set a time frame for your ride:\n" +
                        "     1.) Yes\n" +
                        "     2.) No\n" + 
                        "Choice: \n")

        if timeFrameChoice == "1":
            minHour = getMinHour()
            maxHour = getMaxHour()
        else:
            minHour = False
            maxHour = False

        numGuests = getNumberOfGuests()

        overrideChoice = input("If a fastpass is found but conflicts with a fastpass you already have, would you like to automatically override the conflicting fastpass?:\n" +
                        "If you select no, you will need to manually intervene\n" +
                        "     1.) Yes\n" +
                        "     2.) No\n" +
                        "Choice: ")

        ride = convertRideNumToText(park, ride)

        printOutRidesChosen(park, ride, numGuests, minHour, maxHour) #Prints out chosen rides and converts ride number to actual ride name

        instances.append({
            'user': user,
            'numGuests': numGuests,
            'park': park,
            'ride': ride,
            'minHour': minHour,
            'maxHour': maxHour,
            'overrideChoice': overrideChoice,
        })

    threads = []
    for instance in instances:
        t = threading.Thread(target=create_instance, args=(
            instance['user'],
            instance['numGuests'],
            instance['park'],
            instance['ride'],
            instance['minHour'],
            instance['maxHour'],
            instance['overrideChoice'],
        ))
        threads.append(t)
        t.start()

if __name__ == '__main__':
    main()
