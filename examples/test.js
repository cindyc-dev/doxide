/**
Insertion sort implementation.

Parameters:
    array(list): The array to be sorted.

Returns:
    list: The sorted array.

Examples: 
    >>> insertion_sort([3, 2, 1])
    [1, 2, 3]

*/
function insertionSort(inputArr) {
	let n = inputArr.length;
	for (let i = 1; i < n; i++) {
		// Choosing the first element in our unsorted subarray
		let current = inputArr[i];
		// The last element of our sorted subarray
		let j = i - 1;
		while (j > -1 && current < inputArr[j]) {
			inputArr[j + 1] = inputArr[j];
			j--;
		}
		inputArr[j + 1] = current;
	}
	return inputArr;
}
/**
Prints "Hello, World!" to the console.

Parameters:
    None

Returns:
*/
function helloWorld() {
    console.log("Hello, World!");
}