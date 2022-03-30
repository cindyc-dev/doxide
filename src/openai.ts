/* eslint-disable @typescript-eslint/naming-convention */
// Disabling eslint because it doesn't like OpenAI's property names (because they use snake_case)

// TODO fix security vulnerability
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

import axios from "axios";
import { Position, Range, window, workspace } from "vscode";

/**
 * Makes a post request to OpenAI-Codex API. Returns an array of the responses 
 *  or `undefined` if something went wrong.
 * @param text
 * @see https://beta.openai.com/docs/api-reference/completions/create
 */
export async function openaiGenerateDocstring(text: string, authKey: string|undefined, insertionLine: number) {
    // console.log(`  insertionLine: ${JSON.stringify(insertionLine, null, 2)}`);
    // console.log(`  OPENAI_API_KEY: ${authKey}`);
    // console.log(`  text: ${JSON.stringify(text)}`);
    if (!text || text === undefined) {
        window.showWarningMessage(`No function found. Please make sure that your cursor is either within a function or is selecting a function.`);
        return;
    }
    
    const additionalPostPromptText: string = "\n# An elaborate, high quality docstring for the above function:\n\"\"\"";
    const additionalPrePromptText: string = "";
    const engine: string | undefined = workspace.getConfiguration("doxide").get("openAI.engine");

    const formattingExamples: string = "def bubble_sort(array):\\n    n = len(array)\\n    for i in range(n):\\n        already_sorted = True\\n        for j in range(n - i - 1):\\n            if array[j] > array[j + 1]:\\n                array[j], array[j + 1] = array[j + 1], array[j]\\n                already_sorted = False\\n        if already_sorted:\\n            break\\n    return array"+additionalPostPromptText+"'''\\n    Bubble sort implementation.\\n\\n    Parameters\\n    ----------\\n    array : list\\n        The array to be sorted.\\n\\n    Returns\\n    -------\\n    list\\n        The sorted array.\\n\\n    Examples\\n    --------\\n    >>> bubble_sort([3, 2, 1])\\n    [1, 2, 3]\\n    \\n    '''"+"\n\n";

    // const prompt = formattingExamples + text + additionalPostPromptText;
    const prompt = text + additionalPostPromptText;
    console.log(`PROMPT: ${JSON.stringify(prompt, null, 2)}`)
    // NOTE: The token count of your prompt plus max_tokens cannot exceed the 
    //  model's context length. davinci-codex supports 4096 tokens
    await axios
        .post(
            `https://api.openai.com/v1/engines/${engine}/completions`,
            {
                prompt: prompt,
                // suffix: "",
                max_tokens: Math.floor(text.length/2),
                temperature: 0.3,
                top_p: 1,
                n: workspace.getConfiguration("doxide").get("openAI.config.n"),
                stream: false,
                logprobs: null,
                stop: ["#", "\"\"\"", "'''"],
                // presence_penalty: 0,
                // frequency_penalty: 0,
                // best_of: ,
                // logit_bias:
            },
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${authKey}`,
                },
            }
        )
        .then((response: { data: any }) => {
            console.log(
                `[openaiGenerateDocstring] response: ${JSON.stringify(
                    response.data,
                    null,
                    2
                )}`
            );
            const editor = window.activeTextEditor;
            
            let docstring = response.data.choices[0].text;
            const langId = editor?.document.languageId || 'python';
            editor?.edit(editBuilder => {
                // make sure docstring is added after function signature
                if (langId === 'python') {
                    insertionLine += 1;
                }
                docstring = addDocstringIndentationAndTokens(text, docstring, langId);
                const insertionPoint = new Position(insertionLine, 0);
                editBuilder.insert(insertionPoint, docstring);
            });
        })
        .catch((error: any) => {
            console.error(`[openaiGenerateDocstring] error: ${error}`);
            window.showErrorMessage(`ERROR! Could not generate Docstring.\n${error}`);
            return false;
        });
}

/**
 * Adds indentation to the docstring given
 * @param docstring 
 * @returns docstring with indentation
 */
function addDocstringIndentationAndTokens(text:string, docstring: string, langId:string): string {
    // get tab size
    const editor = window.activeTextEditor;
    const tabSize = editor?.options.tabSize as number;
    const insertSpaces = editor?.options.insertSpaces as boolean;

    // count the number of spaces preceding the first line after the signature
    let numIndents = 0;
    const indentString = insertSpaces ? ' '.repeat(tabSize) : '\t';

    // find for the first line of code after function signature
    var pattern = insertSpaces ? `\\n\\s{${tabSize},}` : `\\n\\t+`;
    var re = new RegExp(pattern);
    var match = text.match(re) || [];

    // count the number of indexes in that first line
    var spacesCounter = 0;
    if (match.length) {
        for (let i=0; i<match[0].length; i++) {
            let char = match[0][i];
            if (char === '\t') {
                numIndents += 1;
            } else if (char === ' ') {
                spacesCounter += 1;
            }
            if (insertSpaces && spacesCounter === tabSize) {
                numIndents += 1;
                spacesCounter = 0;
            }
        }
    }
    // console.log(`re: ${re}`);
    // console.log(`match: ${JSON.stringify(match)}`);
    // console.log(`numIndents: ${numIndents}`);

    var re2 = new RegExp('\\n(?![\n\r])', 'g');
    const startDocstringToken = workspace.getConfiguration("doxide").get(`${langId}.startDocstringToken`) || "'''";
    const endDocstringToken = workspace.getConfiguration("doxide").get(`${langId}.endDocstringToken`) || "'''";
    // console.log(`startDocstringToken: ${startDocstringToken}`);
    // console.log(JSON.stringify(docstring.match(re2)));
    // console.log(JSON.stringify(docstring.replace(re2, `\n${indentString.repeat(numIndents)}`)));

    // insert indents (either tabs or spaces) into each line of the docstring
    const docstringWithIndents = 
        indentString.repeat(numIndents) + startDocstringToken 
        + docstring.replace(re2, `\n${indentString.repeat(numIndents)}`)
        + '\n' + indentString.repeat(numIndents) + endDocstringToken + '\n';

    return docstringWithIndents;
}

/**
 * @returns the number of indents/tabs are needed for the docstring
 */
function countNumIndents (): number {
    return 0;
}