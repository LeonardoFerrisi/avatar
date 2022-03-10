    ## THREADING LOGIC
    
    # thread1 = threading.Thread(target=blink_block, args=([screen, frequencies[0], loc1, size, 1]))
    # thread1.setDaemon(True)
    # thread1.start()

    # thread2 = threading.Thread(target=blink_block, args=([screen, frequencies[1], loc2, size, 2]))
    # thread2.setDaemon(True)
    # thread2.start()

    # thread3 = threading.Thread(target=blink_block, args=([screen, frequencies[2], loc3, size, 3]))
    # thread3.setDaemon(True)
    # thread3.start()

    # thread4 = threading.Thread(target=blink_block, args=([screen, frequencies[3], loc4, size, 4]))
    # thread4.setDaemon(True)
    # thread4.start()
    #####

    # if threadsOn == False:
    #     threadsOn = True
    #     startProcesses(screen=screen, frequencies=frequencies, locations=locations, size=size)
        

    # pool = mp.Pool(4)
    # for i in range(4):
    #     pool.apply_async(blink_block, args=(screen, frequencies[i], locations[i], size, i+1,))
    
    
    # p = mp.Process(target=blink_block, args())
    # for i in range(4):

    # pool.join()