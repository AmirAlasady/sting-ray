import threading
import time

def execute_in_parallel(func1, func2, args1, args2):
    # Create two threads
    thread1 = threading.Thread(target=func1, args=args1)
    thread2 = threading.Thread(target=func2, args=args2)

    # Start timer
    start_time = time.time()

    # Start both threads
    try:
        thread1.start()
    except:
        print('online fail')
    try:
        thread2.start()
    except:
        print('offline fail')
        
    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time

    print('done at')
    print(f'Execution time of: {execution_time:.2f} seconds')
    