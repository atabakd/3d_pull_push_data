# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:53:25 2016

@author: atabak
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(50)

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


effects_push_rake = effects_push[np.where(push_data.ix[:,1]=='rake'),:]
effects_push_rake = effects_push_rake[0,...]

effects_push_stick= effects_push[np.where(push_data.ix[:,1]=='stick'),:]
effects_push_stick = effects_push_stick[0,...]

plt.close()
p1 = plt.scatter(effects_pull_stick[:,0],effects_pull_stick[:,1])
p2 = plt.scatter(effects_pull_rake[:,0],effects_pull_rake[:,1],color='red')
plt.legend((p1, p2),('stick','rake'))
plt.show()
plt.savefig('effects_pull.png')

plt.figure()
p3 = plt.scatter(effects_push_stick[:,0],effects_push_stick[:,1])
p4 = plt.scatter(effects_push_rake[:,0],effects_push_rake[:,1],color='red')
plt.xlim([-0.3,0.3])
plt.legend((p1, p2),('stick','rake'))
plt.show()
plt.savefig('effects_push.png')

        
data_minimal = np.zeros([1,13])
data = np.zeros([1,13])
pull_lable = 1
push_lable = 2
for key in desc_dic.keys():
    if key != 'rake' and key != 'stick':
        temp_data = np.empty([40,13])
        temp_data[:10,:5]=desc_dic['rake']
        temp_data[:10,5:10]=desc_dic[key]
        temp_data[:10,10]=pull_lable
        pull_idx=np.multiply(pull_data.ix[:,1]=='rake',pull_data.ix[:,2]==key)
        temp_data[:10,11:]=effects_pull[np.where(pull_idx),:]
        temp_data[10:20,:5]=desc_dic['stick']
        temp_data[10:20,5:10]=desc_dic[key]
        temp_data[10:20,10]=pull_lable
        pull_idx=np.multiply(pull_data.ix[:,1]=='stick',pull_data.ix[:,2]==key)
        temp_data[10:20,11:]=effects_pull[np.where(pull_idx),:]        

        temp_data[20:30,:5]=desc_dic['rake']
        temp_data[20:30,5:10]=desc_dic[key]
        temp_data[20:30,10]=push_lable
        push_idx=np.multiply(push_data.ix[:,1]=='rake',push_data.ix[:,2]==key)
        temp_data[20:30,11:]=effects_push[np.where(push_idx),:]
        temp_data[30:40,:5]=desc_dic['stick']
        temp_data[30:40,5:10]=desc_dic[key]
        temp_data[30:40,10]=push_lable
        push_idx=np.multiply(push_data.ix[:,1]=='stick',push_data.ix[:,2]==key)
        temp_data[30:40,11:]=effects_push[np.where(push_idx),:]
        data_minimal=np.vstack((data_minimal,temp_data))
        
        for obj in desc_dic[key]:
            for rake in desc_dic['rake']:   
                pull_idx=np.multiply(pull_data.ix[:,1]=='rake',pull_data.ix[:,2]==key)
                for eff_pull in effects_pull[np.where(pull_idx),:][0,...]:
                    row = np.append(rake,obj)
                    row = np.append(row, pull_lable)
                    row = np.append(row, eff_pull)
                    data=np.vstack((data,row))
                push_idx=np.multiply(push_data.ix[:,1]=='rake',push_data.ix[:,2]==key)
                for eff_push in effects_push[np.where(push_idx),:][0,...]:
                    row = np.append(rake,obj)
                    row = np.append(row, push_lable)
                    row = np.append(row, eff_push)
                    data=np.vstack((data,row))
            for stick in desc_dic['stick']:   
                pull_idx=np.multiply(pull_data.ix[:,1]=='stick',pull_data.ix[:,2]==key)
                for eff_pull in effects_pull[np.where(pull_idx),:][0,...]:
                    row = np.append(stick,obj)
                    row = np.append(row, pull_lable)
                    row = np.append(row, eff_pull)
                    data=np.vstack((data,row))
                push_idx=np.multiply(push_data.ix[:,1]=='stick',push_data.ix[:,2]==key)
                for eff_push in effects_push[np.where(push_idx),:][0,...]:
                    row = np.append(stick,obj)
                    row = np.append(row, push_lable)
                    row = np.append(row, eff_push)
                    data=np.vstack((data,row))
#                
#        
#        
data_minimal = data_minimal[1:,:]
data = data[1:,:]        

np.savetxt('data_minimal.txt', data_minimal, fmt=['%.7f', '%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f', '%d', '%.7f', '%.7f'])
      
np.savetxt('data.txt', data, fmt=['%.7f', '%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f', '%d', '%.7f', '%.7f'])

noise_gaussian = np.random.normal(0,0.02,[data.shape[0],2])
noise_uniform = np.random.uniform(-0.02,0.02,[data.shape[0],2])

data_uniform_noise = data
data_gaussian_noise = data

data_uniform_noise[:,11:]=data_gaussian_noise[:,11:]+noise_uniform
data_gaussian_noise[:,11:]=data_gaussian_noise[:,11:]+noise_gaussian

np.savetxt('data_uniform_noise.txt', data_uniform_noise, fmt=['%.7f', '%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f', '%d', '%.7f', '%.7f'])
      
np.savetxt('data_gaussian_noise.txt', data_gaussian_noise, fmt=['%.7f', '%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f','%.7f', '%d', '%.7f', '%.7f'])
#                
#data_pull = data[np.where(data[:,10]==3),11:][0,...]            
#plt.figure()
#plt.scatter(data_pull[:,0],data_pull[:,1])
#plt.show()