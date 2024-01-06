import pandas as pd
import socket
import time
import sqlite3
from matplotlib import pyplot as plt
import random


def db_collecting():
    conn = sqlite3.connect("wind_data_test.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wind_data_test (
            timestamp TEXT,
            wind1 REAL,
            wind2 REAL
        )
    ''')

    # x_vals = []
    y_vals = []
    y_vals2 = []

    # Counter to keep track of the number of iterations
    probe_length = int(input('Enter the number of values you want to supply to the database: '))
    counter = 0
    retry_limit = 5  # Maximum number of retries
    while counter != probe_length:
        retry_count = 0
        while retry_count < retry_limit:
            try:
                # Getting time
                # now = time.localtime()
                # t = time.strftime("%Y-%m-%d %H:%M:%S")
                # x_vals.append(t)

                # Getting wind value 1
                # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # adres_s = ("tcp ip address, port")
                # s.connect(adres_s)
                # data = s.recv(1024)
                # stringdata = data.decode('utf-8')
                # wind1 = float(stringdata[13:16])
                wind1 = random.randint(0, 10)
                y_vals.append(wind1)

                # Getting wind value 2
                # b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # adres_b = ("tcp ip address, port")
                # b.connect(adres_b)
                # data2 = b.recv(1024)
                # stringdata2 = data2.decode('utf-8')
                # wind2 = float(stringdata2[15:18])
                wind2 = random.randint(0, 10)
                y_vals2.append(wind2)

                # Store the values in the database
                cursor.execute("INSERT INTO wind_data_test (timestamp, wind1, wind2) VALUES (?, ?, ?)",
                               (t, wind1, wind2))
                conn.commit()

                counter += 1
                print(counter)
                break  # Successful execution, break out of the retry loop
            except Exception as e:
                print(f"No data recive from soccet: {e}")
                retry_count += 1
        else:
            print("Failed attempts, loop breaking.")
            break  # Maximum number of retries reached, break out of the while loop

    conn.close()


def average_of_chunks(data, chunk_size):
    avg_list = []
    for x in range(0, len(data), chunk_size):
        chunk = data[x:x+chunk_size]
        avg = sum(chunk) / len(chunk)
        avg_list.append(avg)
    return avg_list


def db_fetchall():
    conn = sqlite3.connect("wind_data_test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, wind1, wind2 FROM wind_data_test")
    wind_data = cursor.fetchall()

    for i in range(len(wind_data)):
        # timestamp.append(wind_data[i][0])
        analog.append(wind_data[i][1])
        ultrasonic.append(wind_data[i][2])


def plot():
    analog_avg = average_of_chunks(analog, 10)
    ultrasonic_avg = average_of_chunks(ultrasonic, 10)

    # timestamp = pd.Series(timestamp)
    # timestamp = pd.to_datetime(timestamp)
    # stamp = make_list(analog_avg)
    analog_avg = pd.Series(analog_avg)
    ultrasonic_avg = pd.Series(ultrasonic_avg)
    plt.plot(analog_avg)
    plt.plot(ultrasonic_avg)

    plt.xlabel('n')
    plt.title('Wind compare')
    plt.legend(['Analog', 'Ultrasonic'])
    plt.xticks(range(len(analog_avg)))
    plt.show()
    conn.close()


if __name__ == "__main__":
    # timestamp = []
    analog = []
    ultrasonic = []
    choice = input('1 - collecting data 2 - chart based on the collected data')
    if int(choice) == 1:
        db_collecting()
    if int(choice) == 2:
        db_fetchall()
        plot()
    else:
        print('Chose 1 or 2')
