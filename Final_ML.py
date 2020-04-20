import mysql.connector
from sklearn.svm import SVR

x_train = []  #inputs for train set 
y_train = []  #output for train set

#connecting to the learn database and extracting our data 
cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='learn')
cursor = cnx.cursor()
cursor.execute('SELECT * FROM houses')
for i in range(240):
    data = cursor.fetchone()
    x_train.append(data[0:2])
    y_train.append(data[2])

regressor = SVR(kernel='linear')
regressor = regressor.fit(x_train,y_train)

print("metraj:")
metraj = input()
print("room numbers:")
room = input()

result = regressor.predict([(metraj,room)])
print("your price is:",result)

