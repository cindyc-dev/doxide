import { commands, Disposable, window, languages, workspace, ProgressLocation } from "vscode";
import { DoxideCodeLensProvider } from "./CodeLensProvider";

let disposables: Disposable[] = [];

export function activate() {
	window.showInformationMessage(`🤖 Doxide extension is activated!`);
	
	const authKey: string | undefined = workspace
		.getConfiguration("doxide")
		.get("doxide.openAI.apiKey");

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	

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
		window.showInformationMessage(`✅ Doxide: CodeLens Enabled.`);
	});

	// Command to disable CodeLenses
	commands.registerCommand("doxide.disableCodeLens", () => {
		console.log("[Command] doxide.disableCodeLens called.");
		workspace.getConfiguration("doxide").update("codeLens.enabled", false);
		window.showInformationMessage(`✅ Doxide: CodeLens Disabled.`);
	});

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "doxide" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('doxide.helloWorld', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from doxide!');
	});
}

export function deactivate() {
	if (disposables) {
		disposables.forEach(item => item.dispose());
	}
	disposables = [];
}

