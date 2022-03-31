const pythonExampleBubbleSort: string = `
def bubble_sort(array):
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array
`;

const pythonTemplates = [
`
    Bubble sort implementation.

    Parameters
    ----------
    array : list
        The array to be sorted.

    Returns
    -------
    list
        The sorted array.

    Examples
    --------
    >>> bubble_sort([3, 2, 1])
    [1, 2, 3]
`,
`
    Bubble sort implementation.

    Parameters:
        array(list): The array to be sorted.

    Returns:
        list: The sorted array.

    Examples: 
        >>> bubble_sort([3, 2, 1])
        [1, 2, 3]
`
];

const javaScriptExampleBubbleSort: string = `
function bblSort(arr){
    for(var i = 0; i < arr.length; i++){
        for(var j = 0; j < ( arr.length - i -1 ); j++){
            if(arr[j] > arr[j+1]){
                var temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j+1] = temp
            }
        }
    }
    console.log(arr);
}
`;

const javaScriptTemplates = [
`
Bubble sort implementation.

Parameters
----------
array : list
    The array to be sorted.

Returns
-------
list
    The sorted array.

Examples
--------
>>> bubble_sort([3, 2, 1])
[1, 2, 3]
`,
`
Bubble sort implementation.

Parameters:
    array(list): The array to be sorted.

Returns:
    list: The sorted array.

Examples: 
    >>> bubble_sort([3, 2, 1])
    [1, 2, 3]
`,
`
* @param {Array} inputArr - An array of numbers
* @returns {Array} - The sorted array
* @description - This function sorts an array of numbers using the insertion sort algorithm
* @example
* // returns [1, 2, 3]
* bubble_sort([3, 2, 1])
`
];

export const template = [
    {
        lang: "python",
        exampleCode: pythonExampleBubbleSort,
        exampleTemplates: pythonTemplates,
        stopTokens: ["#", "\"\"\"", "'''"]
    },
    {
        lang: "javascript",
        exampleCode: javaScriptExampleBubbleSort,
        exampleTemplates: javaScriptTemplates,
        stopTokens: ["//", "/**", "*/"]
    }
];