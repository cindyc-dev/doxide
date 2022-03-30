def sayHello():
    print("Hello")

def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
	
def outerFunction():
    def innerFunction():
        print("hello")
    for i in range(5):
        innerFunction()


