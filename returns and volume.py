import matplotlib.pyplot as plt
import requests
import socket
# choose weekly, daily, etc.
key= #add TD Ameritrade API key as a string
def get_price_history(**kwargs):
    url="https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(kwargs.get('symbol'))
    params={}
    params.update({'apikey':key})
    for arg in kwargs:
        parameter={arg: kwargs.get(arg)}
        params.update(parameter)
    return requests.get(url, params=params).json()
#INPUT

#PERIOD
periodTypeInput=input("Period Type(day, month, year, ytd):")
frequencyTypeInput=input("Frequency Type (minute, daily, weekly, monthly):")

#SYMBOLS
input1=input('SYMBOLS FOR RETURN METRICS:   ')
input1=input1.split(",")
chart_data={}
for x in input1:
    chart_data[x]=[]
input2=input('SYMBOLS FOR VOLUME:   ')
if input2=='-':
    input2=input1
else:
    input2=input2.split(",")
y_values={}
for hi in input2:
    y_values[hi]=[]

#VOLUME
for x in y_values:
    data=get_price_history(symbol=x,period=2, periodType=periodTypeInput, frequencyType=frequencyTypeInput, frequency=1)
    for j in range(len(data['candles'])):
        y_values[x].append(data['candles'][j]['volume'])

#RETURNS
for j in chart_data:
    returns=get_price_history(symbol=j,period=2, periodType=periodTypeInput, frequencyType=frequencyTypeInput,frequency=1)
    for x in range(len(returns['candles'])):
        if x==0:
            chart_data[j].append(((returns['candles'][x]['close']/returns['candles'][x]['open'])*100)-100)
        else:
            chart_data[j].append((((returns['candles'][x-1]['close']/returns['candles'][x-1]['open'])*100)-100)+(((returns['candles'][x]['close']/returns['candles'][x]['open'])*100)-100))

ax1=plt.subplot()
#LABELING X-AXIS
if(frequencyTypeInput=='minutes'):
    plt.xlabel('Minutes')
elif(frequencyTypeInput=='daily'):
    plt.xlabel('Days')
elif(frequencyTypeInput=='weekly'):
    plt.xlabel('Weeks')
else:
    plt.xlabel('Months')
#PLOTING RETURNS
for k in y_values:
    ax1.plot(range(len(y_values[input2[0]])),y_values[k], color='red', label="Returns")
    plt.legend(loc=1)
ax2=ax1.twinx()
#PLOTING VOLUME
for t in chart_data:
    ax2.plot(range(len(chart_data[input1[0]])),chart_data[t], color='orange', label="Volume/10M")
    plt.legend(loc=2)
plt.show()
