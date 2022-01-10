# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 19:35:25 2021

@author: admin
"""

import random
import matplotlib.pyplot as plt

                                                # initial state:
# the inventory has already 3 cars, 
# the showroom already has 4 cars, and there is an order placed with 5 cars scheduled to arrive after 2 days
                                                
                                                
class InventorySystem:                                                

    def __init__(self, Days, ReviewPeriod, ShowroomMax, InventoryMax, OrderTime, OrdereQuantity):
        self. Days =  Days
        self.ReviewPeriod = ReviewPeriod
        self.ShowroomMax = ShowroomMax
        self.InventoryMax =InventoryMax
        self.OrderTime = OrderTime
        self.OrderQuantity = OrderQuantity
        self.BeginingInventory = [0] * Days
        self.BeginingShowroom = [0] * Days
        self.BeginingInventory[0] = 3
        self.BeginingShowroom[0] = 4
        self.EndingInventory = [0] * Days
        self.EndingShowroom = [0] * Days
        self.WholeInventory = [0]*Days
        self.Demand = [0]*Days
        self.LeadTime = list()
        self.OrdersTime = list()
        self.OrdersTime.append(self.OrderTime)
        
        
    def GenerateDemand(self):
        RandomDigitsForDemand = random.randint(1,100)
        if(RandomDigitsForDemand >= 1 and RandomDigitsForDemand <= 4):
            Demand = 0
        elif(RandomDigitsForDemand >= 5 and RandomDigitsForDemand <= 34):
            Demand = 1
        elif(RandomDigitsForDemand >= 35 and RandomDigitsForDemand <= 70):
            Demand = 2
        elif(RandomDigitsForDemand >= 71 and RandomDigitsForDemand <= 86):
            Demand = 3
        else:
            Demand = 4
        return Demand
            
    def GenerateLeadTime(self):
        RandomDigitsForLead = random.randint(1,100)
        if(RandomDigitsForLead >= 1 and RandomDigitsForLead <= 50):
            LeadTime = 1
        elif(RandomDigitsForLead >= 51 and RandomDigitsForLead <= 85):
            LeadTime = 2
        else:
            LeadTime = 3    
        return LeadTime
    
    def main(self):
        #Demand = [0,2,0,3,4,2,4,4,1,3]
        SumDemand = 0
        SumLeadTime = 0
        Shortage = 0
        CountShortage = 0
        ShortageSum = 0
        #OrdersTime = [2,1,0,2,1,0,2,1,0,1]
        
        arrived = False
        for i in range(0,Days):
            
            #print("---------------------------------------------- Day" ,i+1 , "-----------------------------------------------")
            if(self.OrdersTime[len(self.OrdersTime)-1] == 0 and arrived == False):
                #print("The order arrived successfully!!!")
                arrived = True
                
                #print("shortageSum = " , ShortageSum)
                if(self.OrderQuantity >= (ShowroomMax + ShortageSum)):
                    self.BeginingShowroom[i] = self.EndingShowroom[i-1] + (ShowroomMax - self.EndingShowroom[i-1])
                    self.OrderQuantity -= (ShowroomMax - self.EndingShowroom[i-1])
                    self.BeginingInventory[i] = self.EndingInventory[i-1] + (self.OrderQuantity - ShortageSum)
                    ShortageSum = 0
                    Shortage = 0
                    
                elif(self.OrderQuantity < (ShowroomMax + ShortageSum)):
                    if(self.OrderQuantity < ShortageSum):
                        ShortageSum = self.OrderQuantity
                        self.OrderQuantity -= ShortageSum
                        self.BeginingInventory[i] = self.OrderQuantity    # 0
                    else:
                        self.OrderQuantity -= ShortageSum
                        ShortageSum = 0
                        while(self.OrderQuantity != 0 and self.BeginingShowroom[i] != 5):
                            self.OrderQuantity -= 1
                            self.EndingShowroom[i-1] += 1
                            self.BeginingShowroom[i] = self.EndingShowroom[i-1]   
                        self.BeginingInventory[i] += self.OrderQuantity
                            
                      
            self.Demand[i] = self.GenerateDemand();
            #print("damand",self.Demand[i])
            
            SumDemand += self.Demand[i]
            #print("Demand ", Demand)
            #print("BeginingInventory ", BeginingInventory[i])
            #print("BeginingShowroom ", BeginingShowroom[i])
            if(self.Demand[i] <= self.BeginingInventory[i]):
                self.EndingInventory[i] = self.BeginingInventory[i] - self.Demand[i]
                self.EndingShowroom[i] = self.BeginingShowroom[i]
                if( i < (Days-1)):
                    self.BeginingInventory[i+1] =  self.EndingInventory[i]
                    self.BeginingShowroom[i+1] = self.EndingShowroom[i]
                        
            elif(self.Demand[i] > self.BeginingInventory[i]):
                self.EndingInventory[i] = 0
                
                if(self.Demand[i] < (self.BeginingInventory[i] + self.BeginingShowroom[i])):
                    self.EndingShowroom[i] = self.BeginingShowroom[i] - (self.Demand[i] - self.BeginingInventory[i])  
                elif(self.Demand[i]> (self.BeginingInventory[i] + self.BeginingShowroom[i])):
                    self.EndingShowroom[i] = 0
                    Shortage = self.Demand[i] - (self.BeginingInventory[i] + self.BeginingShowroom[i])
                
                if( i < (Days-1)):
                    self.BeginingInventory[i+1] =  self.EndingInventory[i]
                    self.BeginingShowroom[i+1] = self.EndingShowroom[i]
            
            
            #print("EndingInventory ", EndingInventory[i])
            #print("EndingShowroom ", EndingShowroom[i])
            
            # calculate The number of days when a shortage condition occurs.
            if(Shortage > 0):
                CountShortage = CountShortage + 1
                ShortageSum += Shortage
                #print("shortage = " , Shortage)
            
            #print("Shortage sum", ShortageSum)
            
            self.WholeInventory[i] = self.EndingInventory[i] + self.EndingShowroom[i] - ShortageSum
            # check if the inventory evaluation takes place or not based on the review period
            if(((i+1) % ReviewPeriod) == 0 and arrived == True):
                #print("Inventory evaluation and making order decision")
                self.OrderQuantity = (ShowroomMax + InventoryMax ) - (self.EndingInventory[i] + self.EndingShowroom[i]) + ShortageSum
                #print("Quantity oredred " ,OrderQuantity)
                lead_time = self.GenerateLeadTime();
                self.LeadTime.append(lead_time) 
                #print("lead",lead_time)
                SumLeadTime += lead_time
                self.OrdersTime.append(lead_time)
                arrived = False
                #print("The Lead time" , LeadTime)
                continue
                
            # decrease the number of days until order arrives at the end of each day
            self.OrdersTime[len(self.OrdersTime)-1] = self.OrdersTime[len(self.OrdersTime)-1] - 1   
            #print("DaysUntilOrderArrives " , OrdersTime[len(OrdersTime)-1])
        
    
        # state the answers for the questions
        print("The average ending units in showroom", sum(self.EndingShowroom)/Days)
        print("The average ending units in Inventory", sum(self.EndingInventory)/Days)
        print("The average ending units in both Inventory and show room", sum(self.WholeInventory)/Days)
        print("The average demand", SumDemand/Days)
        print("The average lead time", SumLeadTime/len(self.OrdersTime))
        print("The number of days when a shortage condition occurs. " , CountShortage)
        
   #Plots the graphs
    def plot(self):
        plt.hist(self.Demand, density = True , bins = 30)
        plt.ylabel('probability of demand')
        plt.xlabel('Values of demand')
        plt.show()
        plt.hist(self.LeadTime, density = True)
        plt.ylabel('probability of lead time')
        plt.xlabel('Values of lead time')
        plt.show()
        
        Day = [0]*Days
        for i in range(0,Days):
            Day[i] = i+1
            
        plt.plot(Day,self.WholeInventory)
        plt.title('the inventory')
        plt.xlabel('Day')
        plt.ylabel('Amount of Inventory')
        plt.show()
        
# Given data                               
Days = 1000000
ReviewPeriod = 4
ShowroomMax = 5
InventoryMax = 10
OrderQuantity = 5
OrdersTime = 2
tmp = InventorySystem(Days, ReviewPeriod, ShowroomMax, InventoryMax, OrdersTime, OrderQuantity)
tmp.main()
tmp.plot()
