from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
n = 10
m = 10
room = np.ones((n,m))*500

def create_door(door_size, orient, pos, door_pos):
    # door_size is size of door
    # orient is orientation of door. 0 for vertical 1 for horizontal
    #   vertical 0 places the door to the east, horizontal 1 to the south
    # pos is the start position of the door
  
    for i in range(door_size):

      try:
        if orient == 0:
          room[pos[0]+i,pos[1]]=1
          door_pos.append([pos[0]+i,pos[1]])
        elif orient == 1:
          room[pos[0],pos[1]+i]=1
          door_pos.append([pos[0],pos[1]+i])
      except:
          print("could not place door part")
          break
    return door_pos

def distance_from_door(prev):
    next = []
    for pre in prev:
      if pre[0]+1<n-1 and pre[1]+1<m-1: # bottom right corner
        if room[pre[0], pre[1]]+1.5<room[pre[0]+1, pre[1]+1]:
          room[pre[0]+1, pre[1]+1]=room[pre[0], pre[1]]+1.5
        if ([pre[0]+1, pre[1]+1] not in prev) and ([pre[0]+1, pre[1]+1] not in next):
          next.append([pre[0]+1, pre[1]+1])

      if pre[0]+1<n-1 and pre[1]-1>0: #bottom left corner
          if room[pre[0], pre[1]]+1.5<room[pre[0]+1, pre[1]-1]:
            room[pre[0]+1, pre[1]-1]=room[pre[0], pre[1]]+1.5
          if ([pre[0]+1, pre[1]-1] not in prev) and ([pre[0]+1, pre[1]-1] not in next):
            next.append([pre[0]+1, pre[1]-1])
      
      if pre[0]-1>0 and pre[1]-1>0: #top left corner
          if room[pre[0], pre[1]]+1.5<room[pre[0]-1, pre[1]-1]:
            room[pre[0]-1, pre[1]-1]=room[pre[0], pre[1]]+1.5
          if ([pre[0]-1, pre[1]-1] not in prev) and ([pre[0]-1, pre[1]-1] not in next):
            next.append([pre[0]-1, pre[1]-1])

      if pre[0]-1>0 and pre[1]+1<m-1: #top right corner
          if room[pre[0], pre[1]]+1.5<room[pre[0]-1, pre[1]+1]:
            room[pre[0]-1, pre[1]+1]=room[pre[0], pre[1]]+1.5
          if ([pre[0]-1, pre[1]+1] not in prev) and ([pre[0]-1, pre[1]+1] not in next):
            next.append([pre[0]-1, pre[1]+1])

      if pre[1]+1<m-1 and pre[0]>0 and pre[0]<n-1: # right
          if room[pre[0], pre[1]]+1<room[pre[0], pre[1]+1]:
            room[pre[0], pre[1]+1]=room[pre[0], pre[1]]+1
          if ([pre[0], pre[1]+1] not in prev) and ([pre[0], pre[1]+1] not in next):
            next.append([pre[0], pre[1]+1])
      
      if pre[0]+1<n-1 and pre[1]>0 and pre[1]<m-1: # down
          if room[pre[0], pre[1]]+1<room[pre[0]+1, pre[1]]:
            room[pre[0]+1, pre[1]]=room[pre[0], pre[1]]+1
          if ([pre[0]+1, pre[1]] not in prev) and ([pre[0]+1, pre[1]] not in next):
            next.append([pre[0]+1, pre[1]])

      if pre[1]-1>0 and pre[0]>0 and pre[0]<n-1: # left
          if room[pre[0], pre[1]]+1<room[pre[0], pre[1]-1]:
            room[pre[0], pre[1]-1]=room[pre[0], pre[1]]+1
          if ([pre[0], pre[1]-1] not in prev) and ([pre[0], pre[1]-1] not in next):
            next.append([pre[0], pre[1]-1])
      
      if pre[0]-1>0 and pre[1]>0 and pre[1]<m-1: # up
          if room[pre[0], pre[1]]+1<room[pre[0]-1, pre[1]]:
            room[pre[0]-1, pre[1]]=room[pre[0], pre[1]]+1
          if ([pre[0]-1, pre[1]] not in prev) and ([pre[0]-1, pre[1]] not in next):
            next.append([pre[0]-1, pre[1]])
    return next


      

door_pos = []
create_door(3, 1, [0,6], door_pos)
create_door(2, 0, [2,0], door_pos)

door_pos = np.array(door_pos)
print("------")
next=door_pos
for i in range(max([n+2,m+2])):
  next = distance_from_door(next)
print(room)



