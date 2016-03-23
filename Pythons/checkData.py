# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:53:25 2016

@author: atabak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pull_data = pd.read_csv(r'clean-pull.txt', 
                         sep=' ',
                         header = None,
#                         names = ['eff', 'tool', 'object', 'action', 'effects'],
                         )

push_data = pd.read_csv(r'clean-push.txt', 
                         sep=' ',
                         header = None,
#                         names = ['eff', 'tool', 'object', 'action', 'effects'],
                         )
                         
desc_data = pd.read_csv(r'descDataMin.txt', sep=' ', 
                        header = None,
                        usecols=range(12),
                        )
                        
desc_dic = {obj_name:np.asanyarray(desc_data.ix[desc_data.ix[:,1]==obj_name,2:]) 
                for obj_name in desc_data.ix[:,1].unique()}
for key in desc_dic.keys():
    if key == 'rake' or key == 'stick':
        desc_dic[key] = desc_dic[key][:10,5:]
    else:
        desc_dic[key] = desc_dic[key][:10,:5]
        
#desc_dic = {obj_name:np.asanyarray(desc_data.ix[desc_data.ix[:,1]==obj_name,2:]) for obj_name in desc_data.ix[:,1].unique()}

effects_pull = np.asanyarray(pull_data.ix[:,[24,25]])-np.asanyarray(pull_data.ix[:,[4,5]])
#effects = np.asanyarray(push_data.ix[:,[24,25]])-np.asanyarray(push_data.ix[:,[4,5]])
effects_push = np.asanyarray(push_data.ix[:,[24,25]])-np.asanyarray(push_data.ix[:,[4,5]])
#effects=np.vstack((effects,np.asanyarray(push_data.ix[:,[24,25]])-np.asanyarray(push_data.ix[:,[4,5]])))

effects_pull_rake = effects_pull[np.where(pull_data.ix[:,1]=='rake'),:]
effects_pull_rake = effects_pull_rake[0,...]

effects_pull_stick= effects_pull[np.where(pull_data.ix[:,1]=='stick'),:]
effects_pull_stick = effects_pull_stick[0,...]

plt.close()
plt.scatter(effects_pull_stick[:,0],effects_pull_stick[:,1])
plt.scatter(effects_pull_rake[:,0],effects_pull_rake[:,1],color='red')
plt.show()
plt.savefig('effects.png')

        
data_minimal = np.zeros([1,13])
data = np.zeros([1,13])
for key in desc_dic.keys():
    if key != 'rake' and key != 'stick':
        temp_data = np.empty([40,13])
        temp_data[:10,:5]=desc_dic['rake']
        temp_data[:10,5:10]=desc_dic[key]
        temp_data[:10,10]=3
        pull_idx=np.multiply(pull_data.ix[:,1]=='rake',pull_data.ix[:,2]==key)
        temp_data[:10,11:]=effects_pull[np.where(pull_idx),:]
        temp_data[10:20,:5]=desc_dic['stick']
        temp_data[10:20,5:10]=desc_dic[key]
        temp_data[10:20,10]=3
        pull_idx=np.multiply(pull_data.ix[:,1]=='stick',pull_data.ix[:,2]==key)
        temp_data[10:20,11:]=effects_pull[np.where(pull_idx),:]        

        temp_data[20:30,:5]=desc_dic['rake']
        temp_data[20:30,5:10]=desc_dic[key]
        temp_data[20:30,10]=4
        push_idx=np.multiply(push_data.ix[:,1]=='rake',push_data.ix[:,2]==key)
        temp_data[20:30,11:]=effects_push[np.where(push_idx),:]
        temp_data[30:40,:5]=desc_dic['stick']
        temp_data[30:40,5:10]=desc_dic[key]
        temp_data[30:40,10]=4
        push_idx=np.multiply(push_data.ix[:,1]=='stick',push_data.ix[:,2]==key)
        temp_data[30:40,11:]=effects_push[np.where(push_idx),:]
        data_minimal=np.vstack((data_minimal,temp_data))
        
        for obj in desc_dic[key]:
            for rake in desc_dic['rake']:   
                pull_idx=np.multiply(pull_data.ix[:,1]=='rake',pull_data.ix[:,2]==key)
                for eff_pull in effects_pull[np.where(pull_idx),:][0,...]:
                    row = np.append(rake,obj)
                    row = np.append(row, 3)
                    row = np.append(row, eff_pull)
                    data=np.vstack((data,row))
                push_idx=np.multiply(push_data.ix[:,1]=='rake',push_data.ix[:,2]==key)
                for eff_push in effects_push[np.where(push_idx),:][0,...]:
                    row = np.append(rake,obj)
                    row = np.append(row, 4)
                    row = np.append(row, eff_push)
                    data=np.vstack((data,row))
            for stick in desc_dic['stick']:   
                pull_idx=np.multiply(pull_data.ix[:,1]=='stick',pull_data.ix[:,2]==key)
                for eff_pull in effects_pull[np.where(pull_idx),:][0,...]:
                    row = np.append(stick,obj)
                    row = np.append(row, 3)
                    row = np.append(row, eff_pull)
                    data=np.vstack((data,row))
                push_idx=np.multiply(push_data.ix[:,1]=='stick',push_data.ix[:,2]==key)
                for eff_push in effects_push[np.where(push_idx),:][0,...]:
                    row = np.append(stick,obj)
                    row = np.append(row, 4)
                    row = np.append(row, eff_push)
                    data=np.vstack((data,row))
#                
#        
#        
data_minimal = data_minimal[1:,:]
data = data[1:,:]        

np.savetxt('data_minimal.txt', data_minimal, fmt=['%.7f', '%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f', '%d', '%.7f', '%.7f'])
      
np.savetxt('data.txt', data, fmt=['%.7f', '%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f', '%d', '%.7f', '%.7f'])
                
data_pull = data[np.where(data[:,10]==3),11:][0,...]            
plt.figure()
plt.scatter(data_pull[:,0],data_pull[:,1])
plt.show()