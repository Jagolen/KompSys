import numpy as np

listt = np.linspace(0, 1, 11)
print(listt)
i = np.searchsorted(listt, 0.23, side="left")
listt = np.flip(listt)
print(listt)
print(f"index {i}\nBetween {listt[i]} and {listt[i+1]}\n")