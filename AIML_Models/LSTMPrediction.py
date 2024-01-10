import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, GlobalAveragePooling1D, Dropout
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def LSTMPrediction(datafile = 'lstm_data.csv', time_step = 10, runs = 30):

    datadf = pd.read_csv(datafile)[-700:]
    yest = (np.array(datadf['Date'])[-1])
    yest=datetime.strptime(yest,'%Y-%m-%d')
    end_date=yest+timedelta(1)
    end_date = datetime.strftime(end_date, '%Y-%m-%d')
    training_df = datadf[['Close', 'Open', 'High', 'Low', 'Volume', 'Sentiment']]

    #Data Scaling
    Xscaler = MinMaxScaler()
    Xdata = Xscaler.fit_transform(np.array(training_df))
    Xdata.shape
    Yscaler = MinMaxScaler()
    Ydata = Yscaler.fit_transform(np.array([training_df['Close']]).transpose())

    Xtrain_data, Xtest_data = train_test_split(Xdata, test_size=0.3, shuffle=False)
    Ytrain_data, Ytest_data = train_test_split(Ydata, test_size=0.3, shuffle=False)
    
    def build_timeseries(Xdata, Ydata, time_step):
        dim_0 = Xdata.shape[0] - time_step
        dim_1 = Xdata.shape[1]

        x = np.zeros((dim_0, time_step, dim_1))
        y = np.zeros((Ydata.shape[0] - time_step,))

        for i in range(dim_0):
            x[i] = Xdata[i:time_step+i]
            y[i] = Ydata[time_step+i]
        return x, y

    
    X_train, Y_train = build_timeseries(Xtrain_data, Ytrain_data.transpose()[0], time_step)
    X_test, Y_test = build_timeseries(Xtest_data, Ytest_data.transpose()[0], time_step)

    X_train = X_train.reshape((X_train.shape[0], time_step, X_train.shape[2]))
    X_test = X_test.reshape((X_test.shape[0], time_step, X_test.shape[2]))

    results = []
    prediction_data = np.array([X_test[-1]])
    for i in range(runs):
        print("RUN: ", i+1)
        model = Sequential()
        model.add(LSTM(50,return_sequences = True,input_shape = (X_train.shape[1],X_train.shape[2])))
        model.add(LSTM(50,return_sequences = True))
        model.add(LSTM(50,return_sequences = True))
        model.add(GlobalAveragePooling1D())
        model.add(Dense(25,activation='relu'))
        model.add(Dense(25))
        model.compile(loss = 'mean_squared_error',optimizer = 'adam')
        lstm_model = model.fit(X_train,Y_train,validation_data = (X_test,Y_test),epochs = 25,batch_size = 64, verbose = 1)
        prediction = model.predict(prediction_data)
        prediction = Yscaler.inverse_transform(prediction)[0][0]
        print("Prediction for: ", end_date, "        CLOSE: ", prediction)
        results.append(prediction)

    lastclose = Yscaler.inverse_transform([Ydata[-1]])[0][0]
    adjresults = np.array([x - lastclose for x in results])
    mu = adjresults.mean()
    std = adjresults.std()

    fig, ax = plt.subplots()
    xmin, xmax = plt.xlim()
    diff = pd.DataFrame(adjresults) 
    kde = diff.plot.kde(ax=ax, legend = False)
    diff.plot.hist(density=True, ax=ax, bins=20)
    title = "Fit Values: {:.2f} and {:.2f}".format(mu, std) 
    plt.title(title)
    plt.show()
    
    #Returns average change in price
    return mu, std