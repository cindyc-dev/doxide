<h1 align="center"><b>Doxide</b></h1>

> 🤖 Automate code documentation with OpenAI-Codex
---
<details>
<summary>Table of Contents</summary>

- [!](#)
- [🔨 Getting Started](#-getting-started)
- [💡 Creating Docstrings](#-creating-docstrings)
- [⚙️ Configuration & Customization](#️-configuration--customization)
</details>


---
## 🔨 Getting Started
* To use this extension, you must have an OpenAI API Key (which can be found on the [OpenAI Website > Account > User > API Keys](https://beta.openai.com/account/api-keys))
  * ![](/media/KeySetup.gif)
  * NOTE: you can also paste your key into your User/Workspace Settings directly (`doxide.openAI.apiKey`)

## 💡 Creating Docstrings


* Doxide can be used to create function Docstrings
  * this can be done either using the CodeLens
    > currently supports: Python, JavaScript and TypeScript files
    * ![](/media/GenerateDocstrings1.gif)
  * or by selecting the function and running the command on the right click menu
    * ![](/media/GenerateDocstrings2.gif)
  * or by selecting the function and running the command using the Command Palette (Ctrl + Shift + P)
    * ![](/media/GenerateDocstrings3.gif)

## ⚙️ Configuration & Customization
### OpenAI
* `doxide.openAI.apiKey` *Your OpenAI API key.*
* `doxide.openAI.apiKey.storeLocation` *Where you would like your API Key to be stored.* [Learn more](https://code.visualstudio.com/docs/getstarted/settings)

### OpenAI Configuration
* `doxide.openAI.engine` The engine to be used to generate Docstrings and Comments. Note that Codex models (`code-...`) are in [private beta](https://openai.com/blog/openai-codex/) and GTP-3 models have variable (`text-...`) [Pricing](https://openai.com/api/pricing/).
* `doxide.openAI.config.n` How many completions to generate for each prompt.
* `doxide.openAI.config.temperature` What [sampling temperature](https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277) to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.
* `doxide.openAI.config.presencePenalty` Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
* `doxide.openAI.config.frequencyPenalty` Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.

### CodeLens
* `doxide.codeLens.enabled` *Specifies whether to provide any Doxide Code Lens by default.* If enabled, Code Lenses (grey text) will be shown at the beginning of functions and methods with prompts for generating docstrings. Use the `Toggle Doxide Code Lens` command (`doxide.toggleCodeLens`) to toggle the Doxide code lens on and off for the current window.
* `doxide.codeLens.generateTitle` *CodeLens Title/Label*. The text to be shown above function signatures that enable you to generate docstrings.

### Docstring Configurations
* `doxide.[languageName].startDocstringToken` Token to indicate the start of a docstring for said `[languageName]`.
* `doxide.[languageName].endDocstringToken` Token to indicate the end of a docstring for said `[languageName]`.
* `doxide.[languageName].docstringTemplate` Template for `[languageName]`'s Docstring.
