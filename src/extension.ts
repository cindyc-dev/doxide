import { commands, Disposable, window, languages, workspace, ProgressLocation, Range, Position } from "vscode";
import { DoxideCodeLensProvider } from "./CodeLensProvider";
import { openaiGenerateDocstring } from "./openai";

let disposables: Disposable[] = [];
/**
 * @example
 */
export function activate() {
	console.log(`🤖 Doxide extension is activated!`);
	
	const langId = window.activeTextEditor?.document.languageId;

	let authKey: string | undefined = workspace
		.getConfiguration("doxide")
		.get("openAI.apiKey");
	console.log(`authKey: ${authKey}`);

	// Check if OpenAI API Key is set
	if (!authKey || authKey === undefined) {
		showAuthKeyWarningMessage();
		authKey = workspace
			.getConfiguration("doxide")
			.get("openAI.apiKey");
	}

	// TODO yeet this - Command to say hello
	commands.registerCommand("doxide.helloWorld", (name?) => {
		window.showInformationMessage(`Hello ${name ? name : ""} from Doxide!`);
	});

	/* ------------------------------ CodeLens ------------------------------ */
	// Create and register CodeLensProvider (only for Python, for now)
	const codeLensProvider = new DoxideCodeLensProvider();
	languages.registerCodeLensProvider("python", codeLensProvider);
	languages.registerCodeLensProvider("javascript", codeLensProvider);

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
			password: true,
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
			console.log(`rememberApiKey: ${workspace.getConfiguration("doxide").get("openAI.openAI.apiKey.storeLocation")}`);
			window.showInputBox({
				title: `Would you like Doxide to store your API key in the User Settings or Workspace Settings? [Learn More](https://code.visualstudio.com/docs/getstarted/settings)`,
				prompt: `User(U) / Workspace(W)`,
				ignoreFocusOut: true,
				// password: true,
				validateInput: (text) => {
					if ((['user', 'workspace', 'u', 'w', 'user(u)', 'workspace(w)']).includes(text.toLowerCase())) {
						return null;
					} else {
						return `⚠️ Please enter either 'U' for User or 'W' for Workspace`;
					}
				}
			}).then((text) => {
				if (text && (['user', 'u', 'user(u)']).includes(text.toLowerCase())) {
					workspace.getConfiguration("doxide").update("openAI.openAI.apiKey.storeLocation", "User Settings", true);
				} else {
					workspace.getConfiguration("doxide").update("openAI.openAI.apiKey.storeLocation", "Workspace Settings", true);
				}
			});

			// Remember API Key - store in User Configuration
			if (workspace.getConfiguration("doxide").get("openAI.openAI.apiKey.storeLocation") === "User Settings") {
				workspace
					.getConfiguration("doxide")
					.update("openAI.apiKey", newKey, true);
			} else { // Don't Remember - store in Workspace Configuration
				workspace
					.getConfiguration("doxide")
					.update("openAI.apiKey", newKey);
			}

			authKey = workspace
				.getConfiguration("doxide")
				.get("openAI.apiKey");
			
			window.showInformationMessage(`✅ API Key Successfully added. You may need to reload the window for changes to take effect.`, 'Reload')
				.then((res)=> {
					if (res === 'Reload') {
						commands.executeCommand("workbench.action.reloadWindow");
					}
				});
		});
	});
	
	/* ------------------------- Generate Docstring ------------------------- */
	// Command that is run when "Generate Docstring" CodeLens is clicked
	// TODO check if another docstring is already present
	commands.registerCommand("doxide.generateDocstring", (text:string="", insertionLine:number=-1) => {
		console.log(`[genDocstring] text: ${text}`);

		// check authKey
		if (!authKey || authKey === undefined) {
			var isAuthKeyValid = showAuthKeyWarningMessage();
		} else {
			var isAuthKeyValid = true;
		}

		// Command not called using CodeLens
		if (!text || text === undefined || insertionLine === -1) {
			console.log("YES");
			const editor = window.activeTextEditor;
			if (!editor) { return; }
			text = editor.document.getText(editor.selection);
			insertionLine = editor.selection.start.line;
			console.log(`text: ${text}, insertionLine: ${insertionLine}`);
			
		}

		// show progress window and use openAI to generate docstring
		if (isAuthKeyValid) {
			window.withProgress(
				{
					location: ProgressLocation.Notification,
					title: "Doxide",
					cancellable: true
				}, async (progress) => {
					progress.report({
						message: `Creating Docstring...`,
					});
					const res = await openaiGenerateDocstring(text, authKey, insertionLine);
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

