#Jared Connor, Albert Gordon, Eli Jaghab
#002

import requests as rq
import tkinter as tk
import tweepy as tp
import datetime as dt
import pytz as pt

#Entry GUI
root1 = tk.Tk()
root1.title("Cryptonite")
root1.geometry("350x240")
version = tk.Label(root1, text = "Cryptonite 1.0", font = "TKHeadingFont 8 bold").grid(row = 0, column = 1)
direct = tk.Label(root1, text = "Please enter one or multiple cryptocurrency symbols or names. \n Ex. BTC, Litecoin, ETH                        ").grid(row = 1, column = 1)
symbolEntries = [tk.Entry(root1), tk.Entry(root1), tk.Entry(root1), tk.Entry(root1), tk.Entry(root1)]
noEntryLabel = tk.Label(root1, fg = 'red4')
errorLabels = [tk.Label(root1, fg='red4'), tk.Label(root1, fg='red4'), tk.Label(root1, fg='red4'), tk.Label(root1, fg='red4'), tk.Label(root1, fg='red4')]

#Global Variable to determine if Price GUI is already opened
root2stat = False

#Global List with Price Variables
dataList= []

#Global Placeholder for Time
currenttime = 0

def kill1():
 root1.destroy()

def main():
 #User Entry Interface
 symbolLabels = [tk.Label(root1), tk.Label(root1), tk.Label(root1), tk.Label(root1), tk.Label(root1)]
 for x in range (0,5):
   symbolLabels[x] = tk.Label(root1, text = "Entry " + str(x+1) + ": ").grid(row = 3 + x, column = 1, sticky = "W")
   symbolEntries[x].grid(row = 3 + x, column = 1)
   errorLabels[x].grid(row = 3 + x, column = 1, sticky= "E")

 #No Entries Received Error Label
 noEntryLabel.grid(row = 9, column = 1)
  tk.Button(root1, text = "Submit", command = userValidation).grid(row = 10, column = 1)
 tk.Button(root1, text = "  Close ", fg = "red4", command = kill1).grid(row = 11, column = 1)
 root1.mainloop()            

#Converts Cryptocurrency Symbol to Full Name
def symbol2name(symbol):
cryptoDictText = "https://raw.githubusercontent.com/crypti/cryptocurrencies/master/cryptocurrencies.json"
cryptoDict = makeJSONrequest(cryptoDictText)
return [cryptoDict[str(symbol)]]

#Receives Current Time
def dateTimeFormat():
month = str(dt.datetime.now().month)
day = str(dt.datetime.now().day)
hour = str(dt.datetime.now().strftime("%I:%M %p"))
return "Last updated on " + month + "/" + day + " at " + hour + "."

def makeJSONrequest(url):
response = rq.get(url)
response = response.json()
return response

#Converts Full Name to Symbol
def convert2symbol(name):
 cryptoDictText = "https://raw.githubusercontent.com/crypti/cryptocurrencies/master/cryptocurrencies.json"
 cryptoDict = makeJSONrequest(cryptoDictText)
 nameDict = {v.lower():k for k,v in cryptoDict.items()}
 return nameDict[name]

#Tweepy Keys and Authorization
consumer_key = "coKVp3uEKzDcZtWsWHQUQI40q"
consumer_secret = "P6xV38i6eO9lO7I5JoMUOTAZOgw5Vvzi7jO38Lbl15nFCJacxH"
access_token = "2246334096-pW7OitoWadRKd6Hr7ZFoJbN2y9efDSuYGHkjgmk"
access_token_secret = "CYpokdYwAzObWSn385IQDeujd6ydjG6LYq8g2tX7Z3Osw"
auth = tp.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tp.API(auth)


def userValidation():
 #No Entries Received Error
 if symbolEntries[0].get() == '' and symbolEntries[1].get() == '' and symbolEntries[2].get() == '' and symbolEntries[3].get() == ''and symbolEntries[4].get() == '':
   noEntryLabel.configure(text ='No Entries Recieved')
 #Inital or Secondary Submission
 else:
   noEntryLabel.configure(text ='')
   #Initial Submission
   if root2stat == False:
       priceGUI()
   #Secondary Submission
   else:
     priceGUIconfigure()
 def priceGUI():
#Initialize Price GUI
global root2stat
root2stat = True

root2 = tk.Tk()
root2.title("Price")
root2.geometry("575x200")

def kill2():
 root2.destroy()
 root1.destroy()

#Time
global currenttime
currenttime = tk.Label(root2)
time = dateTimeFormat()
currenttime.configure(text = time)
currenttime.grid(row = 0, column= 3, columnspan= 3)
#Data Table
global dataList
dataList = [[tk.Label(root2,font = "TKHeadingFont 8 bold"),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2)],[tk.Label(root2, font = "TKHeadingFont 8 bold"),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2)],[tk.Label(root2, font = "TKHeadingFont 8 bold"),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2)],[tk.Label(root2, font = "TKHeadingFont 8 bold"),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2)],[tk.Label(root2, font = "TKHeadingFont 8 bold"),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2),tk.Label(root2)]]

#Table Labels
columnNames = ["Price","% Change","Open","High","Low","Close","Volume From","Volume To"]
#Column Headings
for i in range(1+len(columnNames)):
  #blank (0,0)
  if i == 0:
    tk.Label(root2, text = "").grid(row = 1, column= i)
  #place names
  else:
    tk.Label(root2, text = columnNames[i-1], font= "TKHeadingFont 8 bold").grid(row = 1, column= i)

#Place Data in Table
for x in range (0,5):
  #Checks if Entry is Valid
  try:
   #Symbol Entry
   try:
     #APIs
     entry = str(symbolEntries[x].get()).upper()
     cryptoPrice = makeJSONrequest("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+entry+"&tsyms=USD&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
     cryptoHist = makeJSONrequest("https://min-api.cryptocompare.com/data/histoday?fsym="+entry+"&tsym=USD&limit=10&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
     price = cryptoPrice["DISPLAY"][entry]["USD"]["PRICE"]
   #Full Name Entry
   except:
     entry = convert2symbol(symbolEntries[x].get().lower()).upper()
     cryptoPrice = makeJSONrequest("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+entry+"&tsyms=USD&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
     cryptoHist = makeJSONrequest("https://min-api.cryptocompare.com/data/histoday?fsym="+entry+"&tsym=USD&limit=10&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
     price = cryptoPrice["DISPLAY"][entry]["USD"]["PRICE"]
  
   #Data Variables
   price = cryptoPrice["DISPLAY"][entry]["USD"]["PRICE"]
   change24 =round(cryptoPrice["RAW"][entry]["USD"]["CHANGEPCT24HOUR"],2)
   opn = str(cryptoHist["Data"][10]["open"])
   high = str(cryptoHist["Data"][10]["high"])
   low = str(cryptoHist["Data"][10]["low"])
   close = str(cryptoHist["Data"][10]["close"])
   volfrom = str(cryptoHist["Data"][10]["volumefrom"]) # number of crypto traded for US dollars
   volto = str(cryptoHist["Data"][10]["volumeto"]) # number or dollar traded for crypto
   varList = [price, str(change24) + "%", "$ " + opn, "$ " + high, "$ " + low, "$ " + close, volfrom + " " + entry, "$ " + volto]

   #Place Data in Table
   for j in range(1+len(varList)):
     #Symbol in First Column
     if j == 0:
       dataList[x][j].configure(text = entry)
       dataList[x][j].grid(row = 3+x, column = j)
     #Data in Remaining Columns
     else:
       dataList[x][j].configure(text=str(varList[j-1]))
       dataList[x][j].grid(row=3+x, column=j)
 
  except:
    #Blank Entry
    if symbolEntries[x].get() == "":
      print("")
   #Invalid Entry
    else:
      errorLabels[x].configure(text = "Invalid: " + str(symbolEntries[x].get()))
tk.Button(root2, text = "News", command = tweepyGUI).grid(row = 9, column = 4)
tk.Button(root2, text = "Close All", fg = "red4", command = kill2).grid(row = 10, column = 4)
root2.mainloop()

def priceGUIconfigure():
 #Configure Time
 currenttime.configure(text = "")
 time = dateTimeFormat()
 currenttime.configure(text = time)
 currenttime.grid(row = 0, column= 3, columnspan= 3)
  #Clear Data
 for x in range (0,5):
   for j in range (0,9):
     dataList[x][j].configure(text = '')
  #Checks if Entry is Valid
   try:
   #Symbol Entry
     try:
       #APIs
       entry = str(symbolEntries[x].get()).upper()
       cryptoPrice = makeJSONrequest("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+entry+"&tsyms=USD&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
       cryptoHist = makeJSONrequest("https://min-api.cryptocompare.com/data/histoday?fsym="+entry+"&tsym=USD&limit=10&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
       price = cryptoPrice["DISPLAY"][entry]["USD"]["PRICE"]
     #Full Name Entry
     except:
       entry = convert2symbol(symbolEntries[x].get().lower()).upper()
       cryptoPrice = makeJSONrequest("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+entry+"&tsyms=USD&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
       cryptoHist = makeJSONrequest("https://min-api.cryptocompare.com/data/histoday?fsym="+entry+"&tsym=USD&limit=10&api_key=b2b6b8598b38e97a64e4aa30dbb5d20bbbce18aa0e3a3f9053ae0e4b9c85ac5c")
       price = cryptoPrice["DISPLAY"][entry]["USD"]["PRICE"]
    
     #Data Variables
     price = cryptoPrice["DISPLAY"][entry]["USD"]["PRICE"]
     change24 =round(cryptoPrice["RAW"][entry]["USD"]["CHANGEPCT24HOUR"],2)
     opn = str(cryptoHist["Data"][10]["open"])
     high = str(cryptoHist["Data"][10]["high"])
     low = str(cryptoHist["Data"][10]["low"])
     close = str(cryptoHist["Data"][10]["close"])
     volfrom = str(cryptoHist["Data"][10]["volumefrom"]) # number of crypto traded for US dollars
     volto = str(cryptoHist["Data"][10]["volumeto"]) # number or dollar traded for crypto
     varList = [price, str(change24) + "%", "$ " + opn, "$ " + high, "$ " + low, "$ " + close, volfrom + " " + entry, "$ " + volto]

     #Place Data in Table
     for j in range(1+len(varList)):
       #Symbol in First Column
       if j == 0:
         dataList[x][j].configure(text = entry)
         dataList[x][j].grid(row = 3+x, column = j)
       #Data in Remaining Columns
       else:
         dataList[x][j].configure(text=str(varList[j-1]))
         dataList[x][j].grid(row=3+x, column=j)
 
   except:
     #Blank Entry
     if symbolEntries[x].get() == "":
       print("")
    #Invalid Entry
     else:
       errorLabels[x].configure(text = "Invalid: " + str(symbolEntries[x].get()))

def tweepyGUI():
root3 = tk.Tk()
root3.title("News")
root3.geometry("425x300")
scrollbar = tk.Scrollbar(root3)
scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
mylist = tk.Listbox(root3, yscrollcommand = scrollbar.set)
mylist.config(width = 300, height = 20)
mylist.pack( side = tk.LEFT, fill = tk.BOTH)
scrollbar.config(command = mylist.yview)

for x in range (0, 5):
  try:
    entry = str(symbolEntries[x].get()).upper()
    fullname = symbol2name(entry)
    hashTags = tp.Cursor(api.search, q = entry and fullname, result_type = "popular", rpp=100, lang = "en").items(5)

   #Twitter Data Lists
    usersList = []
    tweetsList = []
    for y in hashTags:
      usersList.append(y.user.screen_name)
      tweetsList.append(y.text)
    mylist.insert(tk.END, fullname)
    for z in range (0,5):
      mylist.insert(tk.END, "@" + usersList[z])
      if len(tweetsList[z]) < 70:
        mylist.insert(tk.END, tweetsList[z])
        mylist.insert(tk.END, " ")
      elif len(tweetsList[z]) < 140:
        mylist.insert(tk.END, tweetsList[z][0:69])
        mylist.insert(tk.END, tweetsList[z][69:])
        mylist.insert(tk.END, " ")
      else:
        mylist.insert(tk.END, tweetsList[z][0:69])
        mylist.insert(tk.END, tweetsList[z][69:139])
        mylist.insert(tk.END, tweetsList[z][139:])
        mylist.insert(tk.END, " ")
  except:
    if symbolEntries[x].get() == "":
      mylist.insert(tk.END, "")
    else:
      mylist.insert(tk.END, "Invalid Entry")
root3.mainloop()
main()


