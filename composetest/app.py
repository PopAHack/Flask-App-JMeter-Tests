import time

import redis
from flask import Flask, request

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)#6379

def isPrime(num):
    retries = 5
    while True:
        try:
            #input check
            if num > 1:
                for i in range(2,num):
                    if(num % i) == 0:
                        return '{} is not prime\n'.format(num)
                #Store prime in redis
                cache.append('primes', str(num) + '\n')
                return '{} is prime\n'.format(num)
            else:
                return '{} is not prime\n'.format(num)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/isPrime/<num>', methods=['GET'])
def handle_isPrime_Request(num):
    #test input validity
    try:
        test = int(num)
    except:
        return 'error: invalid format\n'
    if int(num) < 0:
        return 'error: invalid format\n'
    count = isPrime(int(num))
    return count

@app.route('/primesStored', methods=['GET'])
def handle_primesStored_Request():
    if cache.exists('primes') != 0:
        return cache.get('primes')
    else:
        return 'Nothing in cache\n'
    
    
    
    
    
    
    
    
    
    
