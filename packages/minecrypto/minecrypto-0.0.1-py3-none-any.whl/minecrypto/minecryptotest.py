#!/usr/bin/env python3
# Mine for python
# Created by beano09 2021-2021

# Duino-coin miner without XXHASH Imports
import hashlib
import os
import socket
import sys
import time
import ssl
import select
from json import load as jsonload
import requests
# Duino-coin miner with XXHASH Imports
import xxhash
# Duino-coin faucet imports
import requests

# duinocoin def's
def current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time

# Duino-coin without XXHASH
# Minimal version of Duino-Coin PC Miner, useful for developing own apps.
# Created by revox 2020-2021
# Modifications made by Robert Furr (robtech21) and YeahNotSewerSide
# Mining Pools added by mkursadulusoy - 2021-09-06
def duinocoin(usernamedef, lowerdiff):
    soc = socket()
    username = usernamedef
    if lowerdiff == false
        UseLowerDiff = False
    else:
        UseLowerDiff = True
    def fetch_pools():
        while True:
            try:
                response = requests.get(
                    "https://server.duinocoin.com/getPool"
                ).json()
                NODE_ADDRESS = response["ip"]
                NODE_PORT = response["port"]

                return NODE_ADDRESS, NODE_PORT
            except Exception as e:
                time.sleep(15)
    while True:
        try:
            try:
                NODE_ADDRESS, NODE_PORT = fetch_pools()
            except Exception as e:
                NODE_ADDRESS = "server.duinocoin.com"
                NODE_PORT = 2813
            soc.connect((str(NODE_ADDRESS), int(NODE_PORT)))
            server_version = soc.recv(100).decode()
            # Mining section
            while True:
                if UseLowerDiff:
                    # Send job request for lower diff
                    soc.send(bytes(
                        "JOB,"
                        + str(username)
                        + ",MEDIUM",
                        encoding="utf8"))
                    else:
                        # Send job request
                        soc.send(bytes(
                        "JOB,"
                        + str(username),
                        encoding="utf8"))

                    # Receive work
                    job = soc.recv(1024).decode().rstrip("\n")
                    # Split received data to job and difficulty
                    job = job.split(",")
                    difficulty = job[2]

                    hashingStartTime = time.time()
                    base_hash = hashlib.sha1(str(job[0]).encode('ascii'))
                    temp_hash = None

                for result in range(100 * int(difficulty) + 1):
                    # Calculate hash with difficulty
                    temp_hash = base_hash.copy()
                    temp_hash.update(str(result).encode('ascii'))
                    ducos1 = temp_hash.hexdigest()

                    # If hash is even with expected hash result
                    if job[1] == ducos1:
                        hashingStopTime = time.time()
                        timeDifference = hashingStopTime - hashingStartTime
                        hashrate = result / timeDifference

                        # Send numeric result to the server
                        soc.send(bytes(
                            str(result)
                            + ","
                            + str(hashrate)
                            + ",Minimal_PC_Miner",
                            encoding="utf8"))

                            # Get feedback about the result
                            feedback = soc.recv(1024).decode().rstrip("\n")
                            # If result was good
                            if feedback == "GOOD":
                                    break
                            # If result was incorrect
                            elif feedback == "BAD":
                                break

        except Exception as e:
            print(f'{current_time()} : Error occured: ' + str(e) + ", restarting in 5s.")
            time.sleep(5)
            os.execl(sys.executable, sys.executable, *sys.argv)

# Duino-coin miner with XXHASH
# Minimal version of Duino-Coin PC Miner, useful for developing own apps.
# XXHASH version
# Created by revox 2020-2021
# Modifications made by Robert Furr (robtech21) and YeahNotSewerSide
def duinocoinwithxxhash(usernamedef2)
    soc = None
    AVAILABLE_PORTS = [2812, 2813, 2814, 2815, 2816]
    soc = None
    username = usernamedef2
    def get_fastest_connection(server_ip: str):
        connection_pool = []
        available_connections = []
        for i in range(len(AVAILABLE_PORTS)):
            connection_pool.append(socket.socket())
            connection_pool[i].setblocking(0)
            try:
                connection_pool[i].connect((server_ip,
                                            AVAILABLE_PORTS[i]))
            except BlockingIOError as e:
                pass

        ready_connections, _, __ = select.select(connection_pool, [], [])

        while True:
            for connection in ready_connections:
                try:
                    server_version = connection.recv(100)
                except:
                    continue
                if server_version == b'':
                    continue

                available_connections.append(connection)
                connection.send(b'PING')

            ready_connections, _, __ = select.select(available_connections, [], [])
            ready_connections[0].recv(100)
            ready_connections[0].settimeout(10)
            return ready_connections[0]
    while True:
        try:
            soc = get_fastest_connection(str("server.duinocoin.com"))

            # Mining section
            while True:
                # Send job request
                soc.send(bytes(
                    "JOBXX,"
                    + str(username)
                    + ",NET",
                    encoding="utf8"))
                # Receive work
                job = soc.recv(1024).decode().rstrip("\n")
                # Split received data to job and difficulty
                job = job.split(",")
                difficulty = job[2]

                hashingStartTime = time.time()
                for ducos1xxres in range(100 * int(difficulty) + 1):
                    # Calculate hash with difficulty
                    ducos1xx = xxhash.xxh64(
                        str(job[0])
                        + str(ducos1xxres),
                        seed=2811).hexdigest()

                     # If hash is even with expected hash result
                    if job[1] == ducos1xx:
                        hashingStopTime = time.time()
                        timeDifference = hashingStopTime - hashingStartTime
                        hashrate = ducos1xxres / timeDifference

                        soc.send(bytes(
                            str(ducos1xxres)
                            + ","
                            + str(hashrate) +
                            ",Minimal PC Miner (XXHASH)",
                            encoding="utf8"))

                        # Get feedback about the result
                        feedback = soc.recv(1024).decode().rstrip("\n")
                        # If result was good
                        if feedback == "GOOD":
                            break
                        # If result was incorrect
                        elif feedback == "BAD":
                            break

        except Exception as e:
                print("Error occured: " + str(e) + ", restarting in 5s.")
                time.sleep(5)
                os.execv(sys.argv[0], sys.argv)

# Faucet claimer
# By me, Beano09, The creater of mine-crypto
# Thanks to https://github.com/JunaidPeer/DUCO-FAUCET/ for the backend code
def faucetclaim(usernamedef3)
    response = requests.get('http://162.33.23.215:1234/claim/' + usernamedef3 + '/')
    return response
