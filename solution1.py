import sys, select
import json 
import time
from datetime import datetime
from datetime import timedelta 
from threading import Thread
class foodbooking:
    def gettime(self):
        
        current_time = int(datetime.now().strftime("%H"))
        if(current_time < 6 or current_time >= 22 ):
            print("All restaruntus are closed")
        elif(current_time < 12):
            time='t1'
        elif(current_time < 18):
            time='t2'
        elif(current_time < 22):
            time='t3'
        return time
        
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
        deliver=datetime.now() + timedelta(minutes=30)
        return deliver
        
    def cancel(self,deliver):

        if(datetime.now() > deliver):
            print("Sorry Delivered")

        else:
            print("Canclled")
            return 0
            
                

b=foodbooking()
x=1
while(x!=0):
    shop=b.restarunt()
    while(shop==None):
        shop=b.restarunt()
    timing=b.gettime()
    dish=b.dish(shop,timing)
    deliver=b.order(timing,dish)
    while(deliver==None):
        deliver=b.order(timing,dish)
    c=1
    while(datetime.now() < deliver and c !=0):
        input("Do you want to cancel if yes press any key : ")
        c=b.cancel(deliver)
    try:
        x=int(input("Do you want to order again 1-yes 0-no : "))
    except:
        print("\nBYE BYE\n")
