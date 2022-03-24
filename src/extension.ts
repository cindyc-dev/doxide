import { commands, Disposable, window, languages, workspace, ProgressLocation } from "vscode";

let disposables: Disposable[] = [];

export function activate() {
	window.showInformationMessage(`🤖 Doxide extension is activated!`);
	
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	

	// TODO yeet this - Command to say hello
	commands.registerCommand("doxide.helloWorld", (name?) => {
		window.showInformationMessage(`Hello ${name ? name : ""} from Doxide!`);
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

