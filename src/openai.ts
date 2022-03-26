/* eslint-disable @typescript-eslint/naming-convention */
// Disabling eslint because it doesn't like OpenAI's property names (because they use snake_case)

// TODO fix security vulnerability
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

import axios from "axios";
import { workspace } from "vscode";

/**
 * Makes a post request to OpenAI-Codex API. Returns an array of the responses 
 *  or `undefined` if something went wrong.
 * @param text
 * @see https://beta.openai.com/docs/api-reference/completions/create

 */
export async function openaiGenerateDocstring(text: string, authKey: string|undefined) {
    console.log(`  OPENAI_API_KEY: ${authKey}`);
    console.log(`  text: ${text}`);

    // NOTE: The token count of your prompt plus max_tokens cannot exceed the 
    //  model's context length. davinci-codex supports 4096 tokens
    await axios
        .post(
            "https://api.openai.com/v1/engines/davinci-codex/completions",
            {
                prompt: text,  // TODO add additional prompt text
                // suffix: "",
                max_tokens: text.length/2,
                temperature: 0.3,
                // top_p: 1,
                n: workspace.getConfiguration("doxide").get("openAI.config.n"),
                // stream: false,
                // logprobs: null,
                stop: ['"""', "'''"],
                presence_penalty: 0,
                frequency_penalty: 0,
                // best_of: ,
                // logit_bias:
            },
            {
                headers: {
                    Authorization: `Bearer ${authKey}`,
                },
            }
        )
        .then(function (response: { data: any }) {
            console.log(
                `[openaiGenerateDocstring] response: ${JSON.stringify(
                    response.data,
                    null,
                    2
                )}`
            );
        })
        .catch(function (error: any) {
            console.error(`[openaiGenerateDocstring] error: ${error}`);
        });
}


