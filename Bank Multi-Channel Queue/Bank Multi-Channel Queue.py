# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 19:11:29 2022

@author: admin
"""

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

class BankSystem:
    def __init__(self, customers): 
        self.customers = customers
        self.t_departure1=0                  #departure time from server 1
        self.t_departure2=0                  #departure time from server 2
        self.state_T1=0                     #current state of server1 (binary)
        self.state_T2=0                     #current state of server2 (binary)
        
        self.InterArrivalTime = list()#[3, 0, 0, 2, 1, 4, 0, 2, 4, 3]#[2, 3, 0, 0, 2, 4, 2, 1, 3, 2]#[2,2,5,3,3,4,2,0,3,1,]#[4,0,1,0,0,2,2,2,1,4]
        self.ServiceTime = list()#[2, 1, 2, 2, 2, 2, 2, 3, 3, 2]#[2,2,2,2,2,3,2,2,2,3]#[3,2,4,1,3,2,2,2,1,3]

        self.CompletionTime = customers*[0]
        self.Time_in_system = customers*[0]
        self.WaitingTime = list()
        self.ArrivalTime = customers*[0]
        self.ServiceTime_out = list()
        self.ServiceTime_in = list()
        self.WaitingTime_in = list()
        self.WaitingTime_out = list()
        self.ServiceStartTime = customers*[0]
        self.portion_idle = 0
        self.customers_served_outside = 0
        self.customers_served_inside = 0
        self.InQueue = 0
        
            
    def GenerateInterArrivaTime(self):
        RandomDigitsForInterArrivaTime = random.randint(1,100)
        if(RandomDigitsForInterArrivaTime >= 1 and RandomDigitsForInterArrivaTime <= 9):
            IAT = 0
        elif(RandomDigitsForInterArrivaTime >= 10 and RandomDigitsForInterArrivaTime <= 28):
            IAT = 1
        elif(RandomDigitsForInterArrivaTime >= 29 and RandomDigitsForInterArrivaTime <= 58):
            IAT = 2
        elif(RandomDigitsForInterArrivaTime >= 59 and RandomDigitsForInterArrivaTime <= 79):
            IAT = 3
        elif(RandomDigitsForInterArrivaTime >= 60 and RandomDigitsForInterArrivaTime <= 91):
            IAT = 4
        else:
            IAT = 5
        return IAT
    
    def GenerateServiceTime(self):
        RandomDigitsForServiceTime = random.randint(1,100)
        if(RandomDigitsForServiceTime >= 1 and RandomDigitsForServiceTime <= 20):
            ServiceTime = 1
        elif(RandomDigitsForServiceTime >= 21 and RandomDigitsForServiceTime <= 60):
            ServiceTime = 2
        elif(RandomDigitsForServiceTime >= 61 and RandomDigitsForServiceTime <= 88):
            ServiceTime = 2
        else:
            ServiceTime = 3    
        return ServiceTime
    
            
    def main(self):
        WaitInQueue = False
        CustomersInServer1 = [0,0]
        self.ServiceTime.append(self.GenerateServiceTime())
        self.ServiceTime_out.append(self.ServiceTime[0])
        self.InterArrivalTime.append(self.GenerateInterArrivaTime())
        
        Prob_Wait_in_inside = 0
        
        self.ArrivalTime[0] = self.InterArrivalTime[0]
        self.ServiceStartTime[0] = self.ArrivalTime[0]
        self.CompletionTime[0] = self.ServiceStartTime[0] + self.ServiceTime[0]
        self.Time_in_system[0] = self.CompletionTime[0] - self.ArrivalTime[0]
        
        self.t_departure1 = self.CompletionTime[0]
        CustomersInServer1[0] = self.t_departure1 
        self.WaitingTime_out.append(0)
        self.WaitingTime.append(0)
        
        self.customers_served_outside += 1
        self.portion_idle += 1
        
        '''print("Customer|Interarrival Time|ArrivalTime|Service Start Time|Service Time|Waiting time|Completion Time|Time in System|Time drive-in-teller|inside-bank teller")
        print(1,"           ", self.InterArrivalTime[0], "             ", self.ArrivalTime[0], "             ", self.ServiceStartTime[0], "              ", self.ServiceTime[0], "         ",
              self.WaitingTime[0], "          ", self.CompletionTime[0], "            ", self.Time_in_system[0], "               ", self.t_departure1, "               ", self.t_departure2)
        '''
        for i in range(1,customers):
            self.ServiceTime.append(self.GenerateServiceTime())
            self.InterArrivalTime.append(self.GenerateInterArrivaTime())
            self.ArrivalTime[i] = self.InterArrivalTime[i] + self.ArrivalTime[i-1]
            
            if(self.ArrivalTime[i] >= self.t_departure2):
                self.portion_idle += 1
                
            #print(CustomersInServer1[0])
            #print(CustomersInServer1[1])
            if(self.ArrivalTime[i] >= CustomersInServer1[0]):
                WaitInQueue = False        
                CustomersInServer1[0] = CustomersInServer1[1]
                CustomersInServer1[1] = 0
                
            if(CustomersInServer1[1] != 0):
                WaitInQueue = True
            
                
            if(self.t_departure1 <= self.ArrivalTime[i]):
                self.ServiceTime_out.append(self.ServiceTime[i])
                self.state_T1 = 1
                self.ServiceStartTime[i] = self.ArrivalTime[i]
                CustomersInServer1[0] = self.ServiceStartTime[i] + self.ServiceTime[i]
                CustomersInServer1[1] = 0
                self.customers_served_outside += 1
                self.WaitingTime_out.append(self.ServiceStartTime[i] - self.ArrivalTime[i])
                self.WaitingTime.append(self.ServiceStartTime[i] - self.ArrivalTime[i])
                self.CompletionTime[i] = self.ServiceStartTime[i] + self.ServiceTime[i]
                
                
            elif(self.t_departure1 > self.ArrivalTime[i] and WaitInQueue == False):
                self.WaitInQueue = True
                self.ServiceTime_out.append(self.ServiceTime[i])
                self.ServiceStartTime[i] = self.t_departure1
                self.state_T1 = 1
                CustomersInServer1[0] = self.t_departure1
                CustomersInServer1[1] = self.ServiceStartTime[i] + self.ServiceTime[i]
                self.customers_served_outside += 1
                self.WaitingTime_out.append(self.ServiceStartTime[i] - self.ArrivalTime[i])
                self.WaitingTime.append(self.ServiceStartTime[i] - self.ArrivalTime[i])
                self.CompletionTime[i] = self.ServiceStartTime[i] + self.ServiceTime[i]
                
            elif(self.t_departure1 > self.ArrivalTime[i] and WaitInQueue == True):
                self.ServiceTime_in.append(self.ServiceTime[i])
                self.state_T2 = 1 
                self.customers_served_inside += 1
                #CustomersInServer1[1] = 0
                self.ServiceStartTime[i] = self.t_departure1
                if(self.t_departure2 < self.ArrivalTime[i]):
                    self.ServiceStartTime[i] = self.ArrivalTime[i]
                else:
                    self.ServiceStartTime[i] = self.t_departure2
                    Prob_Wait_in_inside += 1
                    self.InQueue += 1
                    
                self.WaitingTime_in.append(self.ServiceStartTime[i] - self.ArrivalTime[i])
                self.WaitingTime.append(self.ServiceStartTime[i] - self.ArrivalTime[i])
                self.CompletionTime[i] = self.ServiceStartTime[i] + self.ServiceTime[i]
                #self.WaitingTime_out.append(0)
            
            self.Time_in_system[i] = self.CompletionTime[i] - self.ArrivalTime[i]
            
            if(self.state_T1 == 1):
                self.t_departure1 = self.CompletionTime[i]
                #print("End Service 1", self.t_departure1)
                
            elif(self.state_T2 == 1):
                self.t_departure2 = self.CompletionTime[i]
                #print("End service 2", self.t_departure2)
                
            
            self.state_T1 = 0
            self.state_T2 = 0
            
            
            
            '''print(i+1,"           ", self.InterArrivalTime[i], "             ", self.ArrivalTime[i], "             ", self.ServiceStartTime[i], "              ", self.ServiceTime[i], "         ", self.WaitingTime[i], "          "
                  , self.CompletionTime[i], "            ", self.Time_in_system[i], "               ", self.t_departure1, "               ", self.t_departure2)
        
        
        print("--------------------------------------------------------------------")
        print("InterArrivalTime", self.InterArrivalTime)
        print("ArrivalTime" , self.ArrivalTime)
        print("ServiceStartTime", self.ServiceStartTime)
        
        print("The waiting time in the drive-in teller queue" ,  self.WaitingTime_out)
        print("The waiting time in the inside-bank teller queue",  self.WaitingTime_in)
        print("service time ", self.ServiceTime)
        print("The service time of the drive-in teller", self.ServiceTime_out)
        print("The service time of the inside-in teller", self.ServiceTime_in)
        
        print("completion time",self.CompletionTime)'''
        
        print("--------------------------------------------------------------------")
        if(self.customers_served_inside > 0):
            Prob_Wait_in_inside = Prob_Wait_in_inside/self.customers_served_inside
            print("The probability that a customer wait in the insidebank teller queue", Prob_Wait_in_inside*100, "%")
            #print("The average service time of the inside-in teller", sum(self.ServiceTime_in)/self.customers_served_inside)
            print("The average waiting time in the inside-bank teller queue",  sum(self.WaitingTime_in)/self.customers_served_inside)
        else:
            print("The probability that a customer wait in the insidebank teller queue", 0)
            print("The average service time of the inside-in teller", 0)
        
          
        if(len(self.WaitingTime_in) != 0):
            print("The maximum waiting time in inside-bank teller queue.", max(self.WaitingTime_in))
        else:
            print("The maximum waiting time in inside-bank teller queue.", 0)
            
        print("The average inter-arrival time " , sum(self.InterArrivalTime)/self.customers)
        print("The average service time of the drive-in teller and the inside-bank teller", sum(self.ServiceTime)/self.customers)
        #print("The average service time of the drive-in teller", sum(self.ServiceTime_out)/self.customers_served_outside)
        print("The average waiting time in the drive-in teller queue" ,  sum(self.WaitingTime_out)/self.customers_served_outside)
        print("The portion of idle time of the inside-bank teller.", self.portion_idle/self.customers)
        print("The maximum waiting time in drive-in teller queue.", max(self.WaitingTime_out))
        print("The number of customers served outside", self.customers_served_outside)
        print("The number of customers served inside", self.customers_served_inside)
        
    #Plot the graphs
    def plot(self):
        plt.hist(self.ServiceTime_in, density = True , bins = 30)
        plt.ylabel('probability of Service Time for inside teller')
        plt.xlabel('Values of Service Time for inside teller')
        plt.show()
        plt.hist(self.ServiceTime_out, density = True , bins = 30)
        plt.ylabel('probability of Service Time for outside teller')
        plt.xlabel('Values of Service Time for outside teller')
        plt.show()
        plt.hist(self.InterArrivalTime, density = True , bins = 30)
        plt.ylabel('probability of Interarrival Time')
        plt.xlabel('Values of Interarrival Time')
        plt.show()
        
customers = 1000
tmp = BankSystem(customers)
tmp.main()
tmp.plot()