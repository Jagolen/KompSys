from time import sleep
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
n = 10
m = 10
room = np.ones((n,m))*400

def create_walls():
  room[:,0] = np.ones((1,n))*500
  room[:,m-1] = np.ones((1,n))*500
  room[0,:] = np.ones((1,m))*500
  room[n-1,:] = np.ones((1,m))*500

def create_obj(obj_size, orient, pos, obj_pos):
    # obj_size is size of obj
    # orient is orientation of obj. 0 for vertical 1 for horizontal
    #   vertical 0 places the obj to the east, horizontal 1 to the south
    # pos is the start position of the obj
  
    for i in range(obj_size):

      try:
        if orient == 0:
          room[pos[0]+i,pos[1]]=500
          obj_pos.append([pos[0]+i,pos[1]])
        elif orient == 1:
          room[pos[0],pos[1]+i]=500
          obj_pos.append([pos[0],pos[1]+i])
      except:
          print("could not place obj part")
          break
    return obj_pos

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


def distance_from_door(prev, change):
    next = []
    for pre in prev:
      try:
        if room[pre[0]+1, pre[1]+1] < 500: # bottom right corner
          if room[pre[0], pre[1]]+1.5<room[pre[0]+1, pre[1]+1]:
            room[pre[0]+1, pre[1]+1]=room[pre[0], pre[1]]+1.5
            change+=1
          if ([pre[0]+1, pre[1]+1] not in prev) and ([pre[0]+1, pre[1]+1] not in next):
            next.append([pre[0]+1, pre[1]+1])
      except:
        pass

      try:
        if room[pre[0]+1, pre[1]-1] < 500: #bottom left corner
          if room[pre[0], pre[1]]+1.5<room[pre[0]+1, pre[1]-1]:
            room[pre[0]+1, pre[1]-1]=room[pre[0], pre[1]]+1.5
            change+=1
          if ([pre[0]+1, pre[1]-1] not in prev) and ([pre[0]+1, pre[1]-1] not in next):
            next.append([pre[0]+1, pre[1]-1])
      except:
        pass

      try:
        if room[pre[0]-1, pre[1]-1] < 500: #top left corner
            if room[pre[0], pre[1]]+1.5<room[pre[0]-1, pre[1]-1]:
              room[pre[0]-1, pre[1]-1]=room[pre[0], pre[1]]+1.5
              change+=1
            if ([pre[0]-1, pre[1]-1] not in prev) and ([pre[0]-1, pre[1]-1] not in next):
              next.append([pre[0]-1, pre[1]-1])
      except:
        pass

      try:
        if room[pre[0]-1, pre[1]+1] < 500: #top right corner
            if room[pre[0], pre[1]]+1.5<room[pre[0]-1, pre[1]+1]:
              room[pre[0]-1, pre[1]+1]=room[pre[0], pre[1]]+1.5
              change+=1
            if ([pre[0]-1, pre[1]+1] not in prev) and ([pre[0]-1, pre[1]+1] not in next):
              next.append([pre[0]-1, pre[1]+1])
      except:
        pass

      try:
        if room[pre[0], pre[1]+1]< 500: # right
            if room[pre[0], pre[1]]+1<room[pre[0], pre[1]+1]:
              room[pre[0], pre[1]+1]=room[pre[0], pre[1]]+1
              change+=1
            if ([pre[0], pre[1]+1] not in prev) and ([pre[0], pre[1]+1] not in next):
              next.append([pre[0], pre[1]+1])
      except:
        pass


      try:
        if room[pre[0]+1, pre[1]] < 500: # down
            if room[pre[0], pre[1]]+1<room[pre[0]+1, pre[1]]:
              room[pre[0]+1, pre[1]]=room[pre[0], pre[1]]+1
              change+=1
            if ([pre[0]+1, pre[1]] not in prev) and ([pre[0]+1, pre[1]] not in next):
              next.append([pre[0]+1, pre[1]])
      except:
        pass

      try:
        if room[pre[0], pre[1]-1] < 500: # left
            if room[pre[0], pre[1]]+1<room[pre[0], pre[1]-1]:
              room[pre[0], pre[1]-1]=room[pre[0], pre[1]]+1
              change+=1
            if ([pre[0], pre[1]-1] not in prev) and ([pre[0], pre[1]-1] not in next):
              next.append([pre[0], pre[1]-1])
      except:
        pass

      try:
        if room[pre[0]-1, pre[1]] < 500: # up
            if room[pre[0], pre[1]]+1<room[pre[0]-1, pre[1]]:
              room[pre[0]-1, pre[1]]=room[pre[0], pre[1]]+1
              change+=1
            if ([pre[0]-1, pre[1]] not in prev) and ([pre[0]-1, pre[1]] not in next):
              next.append([pre[0]-1, pre[1]])
      except:
        pass
    return next, change


      

door_pos = []
obj_pos = []
create_walls()
create_door(3, 1, [0,6], door_pos)
#create_door(2, 0, [2,0], door_pos)
create_obj(6, 0, [1,3], obj_pos)
create_obj(6, 0, [3,5], obj_pos)
print(room)


door_pos = np.array(door_pos)
print("------")
next=door_pos
change=1
while change>0:
  prev_room=room
  change = 0
  next, change = distance_from_door(next, change)
print(room)



