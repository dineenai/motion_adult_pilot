import pandas as pd
from matplotlib import pyplot as plt

from numpy import average


# id = 'sleep_values'
# id = 'no_sleep_values'
# id = 'sleep_.005_values'
# id = 'no_sleep_add_pre_flip_time_values'
# id = 'PCH_no_sleep_add_pre_flip_time_values'
# win_flip_PCH_no_sleep_add_pre_flip_time_values.csv
# win_flip_no_sleep_add_pre_flip_time_values.csv



# id = 'PCH_no_sleep_add_pre_flip_time_values_4'
# id = 'PCH_sleep_0.005_add_pre_flip_time_values_4'

# id = 'PCH_sleep_0.01_add_pre_flip_time_values_4'



# win_flip_PCH_no_sleep_add_pre_flip_time_values.csv
# df = pd.read_csv(f'win_flip_{id}.csv')

id = 'PCH_sleep_0.0005x10_23_5_22' #NOTE actually catina not PCH!

df = pd.read_csv(f'test_outputs_23_5_22/{id}/win_flip_{id}.csv') #add new path
# 

# print(df['flip_time'])
# print(df['pre_flip_time'])


# NOTE The following incorrect code !
# flip_time_pd = df['flip_time']
# print(type(flip_time_pd)) #<class 'pandas.core.series.Series'>
# flip_time = pd.tolist(df['flip_time']) #AttributeError: module 'pandas' has no attribute 'tolist'


# # Use the tolist() Method to Convert a Dataframe Column to a List
# flip_time = df['flip_time'].tolist()
# print(type(flip_time))

# OR 

# Use the list() Function to Convert a Dataframe Column to a List
flip_time = list(df['flip_time'])
print(type(flip_time))
pre_flip_time = list(df['pre_flip_time'])

# # # Plot histogram
# plot = plt.hist(flip_time)
# plt.savefig(f'{id}_TEST.png')


# id = 'PCH_no_sleep_add_pre_flip_time_values_4'
print(len(flip_time)) 

print(min(flip_time))
print(average(flip_time))
print(max(flip_time))

print(sum(i < 0.001 for i in flip_time)) 
print(sum(i < 0.003 for i in flip_time)) 
print(sum(i < 0.002 for i in flip_time)) 
print(sum(i < 0.010 for i in flip_time)) 
print(sum(i < 0.012 for i in flip_time)) 
print(sum(i < 0.014 for i in flip_time)) 
print(sum(i < 0.014 for i in flip_time)) 
print(sum(i > 0.014 for i in flip_time))  



print(min(pre_flip_time))

print(max(pre_flip_time)) 



print(len(flip_time)) 

print(min(flip_time))
print(average(flip_time))
print(max(flip_time))

print(sum(i < 0.001 for i in flip_time)) 
print(sum(i < 0.003 for i in flip_time)) 
print(sum(i < 0.002 for i in flip_time)) 


# id = 'PCH_no_sleep_add_pre_flip_time_values_4'
# # 3 / 18895 flips would be missed with sleep
# print(sum(i < 0.010 for i in flip_time)) #3
# print(sum(i < 0.012 for i in flip_time)) #6
# print(sum(i < 0.014 for i in flip_time))  #17
# print(sum(i > 0.014 for i in flip_time))   #18878


# 18550


# 328 missing - 1.7% of flipped missed

print(min(pre_flip_time))

print(max(pre_flip_time)) 

print(len(flip_time)) 

# print(sum(i > 0.010 for i in pre_flip_time)) 

# The maximum time before the flip command in 0.6 ms
# How would you make this dynamic
# If it is not possible - maybe it is ok to lose a few flips if it means there will be no stalling?
# I would imagine that 5 s of stalling would have a much worse effect on timing than missing x number of flips.
# Maximun radius.....


# id = 'sleep_0.01_values'
# print(len(flip_time))  # 1013
# print(sum(i < 0.010 for i in flip_time))  #0
# print(sum(i < 0.012 for i in flip_time))  #0
# print(sum(i < 0.014 for i in flip_time))  #0



# id = 'no_sleep_values'

# WHY WAS THE AVERAGE SO LOW HERE?????
# Min value is: 0.0015770050001719937 Max: 0.13466544700008853 avg: 0.002921700023694897
# START OF EXPERIMENT: 1317.703629037
# END OF EXPERIMENT: 1335.76599533

# REPLICATION
# START OF EXPERIMENT: 1558.426532125
# END OF EXPERIMENT: 1576.474944008
# Min value is: 0.007866181000053984 Max: 0.03543750400012868 avg: 0.016064610534447823
# print(len(flip_time)) #1071
# print(sum(i < 0.010 for i in flip_time))  #2
# print(sum(i < 0.012 for i in flip_time)) #10
# print(sum(i < 0.014 for i in flip_time)) #46

# 3
# START OF EXPERIMENT: 1790.841636307
# END OF EXPERIMENT: 1808.873890963
# Min value is: 0.00937298799999553 Max: 0.03408336799998324 avg: 0.016145229885156098
# print(len(flip_time)) #1071
# print(sum(i < 0.010 for i in flip_time)) #1
# print(sum(i < 0.012 for i in flip_time)) #3
# print(sum(i < 0.014 for i in flip_time)) #7


# 18 s - about right!
# Recall that this is not necessaarily the problem - the problem is the audio length
# COULD: get circle to flip only while audio is playing to measure

