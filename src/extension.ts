import { commands, Disposable, window, languages, workspace, ProgressLocation, Range } from "vscode";
import { DoxideCodeLensProvider } from "./CodeLensProvider";
import { openaiGenerateDocstring } from "./openai";

let disposables: Disposable[] = [];

export function activate() {
	console.log(`🤖 Doxide extension is activated!`);
	
	const authKey: string | undefined = workspace
		.getConfiguration("doxide")
		.get("openAI.apiKey");

	console.log(`authKey: ${authKey}`);
	// Check if OpenAI API Key is set
	if (!authKey || authKey === undefined) {
		showAuthKeyWarningMessage();
	}

	// TODO yeet this - Command to say hello
	commands.registerCommand("doxide.helloWorld", (name?) => {
		window.showInformationMessage(`Hello ${name ? name : ""} from Doxide!`);
	});

	/* ------------------------------ CodeLens ------------------------------ */
	// Create and register CodeLensProvider (only for Python, for now)
	const codeLensProvider = new DoxideCodeLensProvider();
	languages.registerCodeLensProvider("python", codeLensProvider);

	// Command to enable CodeLenses
	commands.registerCommand("doxide.enableCodeLens", () => {
		console.log("[Command] doxide.enableCodeLens called.");
		workspace.getConfiguration("doxide").update("codeLens.enabled", true);
		window.showInformationMessage(`Doxide: CodeLens Enabled.`);
	});

	// Command to disable CodeLenses
	commands.registerCommand("doxide.disableCodeLens", () => {
		console.log("[Command] doxide.disableCodeLens called.");
		workspace.getConfiguration("doxide").update("codeLens.enabled", false);
		window.showInformationMessage(`Doxide: CodeLens Disabled.`);
	});

	
	// Command that promps user to Enter their OpenAI API Key
	commands.registerCommand("doxide.setOpenAIapiKey", () => {
		window.showInputBox({
			title: `Enter your OpenAI API Key:`,
			prompt: `Enter your OpenAI API Key`,
			// password: true,
			ignoreFocusOut: true,
			validateInput: (text) => {
				if (!text) {
					return `⚠️ Please enter a valid API Key.`;
				} else {
					return null;
				}
			}
		})
		.then((newKey) => {
			// Remember API Key - not yet configured
			// console.log(`rememberApiKey: ${workspace.getConfiguration("doxide").get("openAI.rememberApiKey.enabled")}`);
			// if (workspace.getConfiguration("doxide").get("openAI.rememberApiKey.enabled") === null) {
			// 	window.showInputBox({
			// 		title: `Would you like Doxide to remember your API Key and store it in your global seetings?`,
			// 		prompt: `Yes / No`,
			// 		ignoreFocusOut: true,
			// 		validateInput: (text) => {
			// 			if ((['y', 'yes', 'n', 'no']).includes(text.toLowerCase())) {
			// 				return `⚠️ Please enter either 'Yes' or 'No'.`;
			// 			} else {
			// 				return null;
			// 			}
			// 		}
			// 	}).then((text) => {
			// 		if (text && (['y', 'yes']).includes(text.toLowerCase())) {
			// 			workspace.getConfiguration("doxide").update("openAI.rememberApiKey.enabled", true, true);
			// 		} else {
			// 			workspace.getConfiguration("doxide").update("openAI.rememberApiKey.enabled", false, true);
			// 		}
			// 	});
			// }

			// Remember API Key - store in User Configuration
			// if (workspace.getConfiguration("doxide").get("openAI.rememberApiKey.enabled") === true) {

			// STORE IN GLOBAL USER CONFIGURATION SETTINGS
				workspace
					.getConfiguration("doxide")
					.update("openAI.apiKey", newKey, true);
			// } else { // Don't Remember - store in Workspace Configuration
			// 	workspace
			// 		.getConfiguration("doxide")
			// 		.update("openAI.apiKey", newKey);
			// }
			
		});
	});
	
	/* ------------------------- Generate Docstring ------------------------- */
	// Command that is run when "Generate Docstring" CodeLens is clicked
	// TODO insertPoint (where to insert the docstring)
	commands.registerCommand("doxide.generateDocstring", (text: string, insertPoint?: Range) => {
		console.log(`[genDocstring] text: ${text}`);
        console.log(`lens.range: ${JSON.stringify(insertPoint, null, 2)}`);


		if (!authKey || authKey === undefined) {
			var isAuthKeyValid = showAuthKeyWarningMessage();
		} else {
			var isAuthKeyValid = true;
		}

		// show progress window and use openAI to generate docstring
		if (isAuthKeyValid) {
			window.withProgress(
				{
					location: ProgressLocation.Notification,
					title: "Creating Docstring",
					cancellable: true
				}, () => {
					const p = new Promise<void>(() => {
						openaiGenerateDocstring(text, authKey);
					});
					return p;
				}
			);
		}
		
	});
}

// function isPropConfigured (prop: any, notYetConfigVal: any) {
// 	if (prop === notYetConfigVal) {
// 		return false
// 	}
// 	return true
// }

function showAuthKeyWarningMessage() {
	window.showWarningMessage(`Please set your OpenAI Key.`,
		"Open Settings",
		"Enter Key"
	)
	.then((selection)=>{
		if (selection === "Open Settings") {
			commands.executeCommand("workbench.action.openSettings", "Doxide");
		} else if (selection === "Enter Key") {
			commands.executeCommand("doxide.setOpenAIapiKey");
		}
		return true;
	});
	return false;
}

export function deactivate() {
	if (disposables) {
		disposables.forEach(item => item.dispose());
	}
	disposables = [];
}

