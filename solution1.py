import json 
import time
from datetime import datetime
from datetime import timedelta 
from threading import Thread

current_time = int(datetime.now().strftime("%H"))
class foodbooking:
    inp=None
    def gettime(self):
        if(current_time < 6 or current_time >= 22 ):
            print("All restaruntus are closed")
            time1='t0'
        elif(current_time < 12):
            time1='t1'
        elif(current_time < 18):
            time1='t2'
        elif(current_time < 22):
            time1='t3'
        return time1
        
    def restarunt(self):
        
        restarunt = ["The Briyani Hut","A-Z Anandha bhavan","Panjabi","Erode cafe"]
        print("List of Restarunts : \n")
        print("ID NAME\n")
        for i in range(0,len(restarunt),1):
            print(i+1,".",restarunt[i])
            
        try:
            n=int(input("\nEnter the shop ID no : "))
            if(n==1):
                return "The Briyani Hut"
            elif(n==2):
                return "A-Z Anandha bhavan"
            elif(n==3):
                return "Panjabi"
            elif(n==4):
                return "Erode cafe"
            else:
                print("Only Numbers form 1 to 4\nPress Enter to Continue")
                input()
        except Exception as e:
            print("Only Numbers\nPress Enter to continue")
            input()
        return None
            
    def dish(self,shop,time):
        f=open('f:/%s.json'%(shop),'r')
        data = json.load(f)
        f.close()
        food=list(data[time].keys())
        print("\nAvailable Dishes in %s\n\nID Dish Rate\n"%(shop))
        for i in range(0,len(food)):
            print(i+1,".",food[i],"-->",data[time][food[i]])
        return data
    
    
    def order(self,time,dish):
        
        food=list(dish[time].keys())
        print("Enter the ID's of dishes you want\n")
        try:
            l=list(map(int,input().split()))
            
        except Exception as e:
            print("Enter only Numbers from 1 to %d"%(len(food)))
            return None
        for i in l:
            if(i>len(food)):
                print("Enter only Numbers from 1 to %d"%(len(food)))
                return None
        sum=0
        order=[]
        qu=[]
        for i in l:
            x=int(input("Enter the Quantity of %s: "%(food[i-1]) ))
            qu.append(x)
        print("\nDish Rate\n")
        
        for i in l:
            amt=dish[time][food[i-1]]*qu[i-1]
            print(food[i-1],dish[time][food[i-1]],qu[i-1],amt)
            order.append({food[i-1]:dish[time][food[i-1]]})
            sum =sum+amt
        print("\nToatl price %d\n"%(sum))
        deliver=datetime.now() + timedelta(minutes=1)
        return deliver
    def cancel(self):
        foodbooking.inp = input("Do you want to Cancell the order if yes press any key : ")
    def check(self):
        t = Thread(target=self.cancel)
        t.daemon = True  # Otherwise the thread won't be terminated when the main program terminates.
        t.start()
        t.join(timeout=5)
        if self.inp is None:
            print("\nDelivered..!")
            print("\nPress Enter to Continue..!")
            return 
        else:
            print("Canclled..!")

                

b=foodbooking()
x=1
while(x!=0):
    shop=b.restarunt()
    while(shop==None):
        shop=b.restarunt()
    timing=b.gettime()
    if(timing == 't0'):
        break
    dish=b.dish(shop,timing)
    deliver=b.order(timing,dish)
    while(deliver==None):
        deliver=b.order(timing,dish)
    b.check()
    try:
        x=int(input("Do you want to order again 1-yes 0-no : "))
    except:
        print("\nBYE BYE\n")
