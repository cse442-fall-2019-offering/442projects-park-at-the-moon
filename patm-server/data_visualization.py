#!/usr/bin/env python
# coding: utf-8

# In[37]:


import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

with open("Documents/GitHub/442projects-park-at-the-moon/patm-server/analytics.json") as f:
  data = json.loads(f.read())


# In[38]:


print(data)
print(data[0]["data"][0])
print(len(data))


# In[41]:


clock = ["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM"]
for i in range (0, len(data)):
    for j in range (0, len(data[i]["data"])):
        plt.plot(clock, data[i]["data"][j]["analytics"], color='blue', alpha=1, linewidth=3)
        plt.title(data[i]["data"][j]["lot"] + " Analytics: " + data[i]["day"])
        plt.xlabel("Time")
        plt.ylabel("Number of Queries")
        plt.show()


# In[ ]:




