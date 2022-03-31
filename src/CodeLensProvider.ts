import {
    CodeLensProvider,
    CodeLens,
    EventEmitter,
    Event,
    TextDocument,
    CancellationToken,
    workspace,
    commands,
    SymbolInformation,
    SymbolKind,
    DocumentSymbol,
    SelectionRange,
    Range,
    Command,
    window
} from "vscode";

/**
 * 'Generate Docstring' CodeLens
 */
export class DocstringCodeLens extends CodeLens {
    constructor(
        public readonly contentRange: Range,
        range: Range,
        command?: Command | undefined,
    ) {
        super(range, command);
    }
}

/**
 * 'Previous' CodeLens
 */
export class PreviousCodeLens extends CodeLens {}

/**
 * 'Next' CodeLens
 */
export class NextCodeLens extends CodeLens {}

/**
 * 'Accept' CodeLens
 */
export class AcceptCodeLens extends CodeLens {}

/**
 * 'Change' CodeLens
 */
export class ChangeCodeLens extends CodeLens {}

/**
 * CodelensProvider
 * @see [CodeLens](https://code.visualstudio.com/api/references/vscode-api#CodeLens)
 */
export class DoxideCodeLensProvider implements CodeLensProvider {
    private _onDidChangeCodeLensesEmitter: EventEmitter<void> =
        new EventEmitter<void>();
    public readonly onDidChangeCodeLenses: Event<void> =
        this._onDidChangeCodeLensesEmitter.event;

    constructor() {
        // Reload the CodeLenses when the config has changed
        workspace.onDidChangeConfiguration((_) => {
            console.log("Config was changed - reloading codelens provider");
            this._onDidChangeCodeLensesEmitter.fire();
        });
    }

    /**
     *
     * @param document
     * @param token
     * @returns list of CodeLenses to be shown in the document
     */
    public async provideCodeLenses(
        document: TextDocument,
        token: CancellationToken
    ): Promise<CodeLens[]> {
        const lenses: CodeLens[] = [];

        // Don't show codelens if configuration option is set to `false`
        //  or if operation is cancelled
        if (
            workspace.getConfiguration("doxide").get("codeLens.enabled") ===
                false ||
            token.isCancellationRequested
        ) {
            return [];
        }

        // Get all of the DocumentSymbols from this document
        let symbols = await commands.executeCommand<DocumentSymbol[]>(
            "vscode.executeDocumentSymbolProvider",
            document.uri
        );

        if (symbols !== undefined) {
            // Loop through all of the DocumentSymbols
            for (const symbol of symbols) {
                this.provideCodeLensHelper(lenses, document, symbol);
            }
        }
        console.log(`Rendering ${lenses.length} CodeLenses!`);
        return lenses;
    }

    /**
     * (Recursive) Individual CodeLens Provider - called in provideCodeLenses
     * @param lenses
     * @param document
     * @param symbol
     */
    private provideCodeLensHelper(
        lenses: CodeLens[],
        document: TextDocument,
        symbol: any
    ): void {
        // Check if the symbol is a function and add DocstringCodeLens
        if (symbol.kind === SymbolKind.Function) {
            // console.log(`  Function found: ${JSON.stringify(symbol, null, 2)} | symbol.selectionrange: ${symbol.selectionrange} | symbol.selection_range: ${symbol.selection_range}`);
            lenses.push(new DocstringCodeLens(symbol.range, symbol.location.range));
        }

        // Recursively call this function on all of the children
        for (const child of symbol.children) {
            // console.log(`    Symbol has children!`);
            this.provideCodeLensHelper(lenses, document, child);
        }
    }

    /**
     * Determines what command is run when you click on a CodeLens
     * @param lens - the CodeLens being clicked
     * @param token
     * @returns `null` if the CodeLens does not have a function
     */
    public resolveCodeLens(lens: CodeLens, token: CancellationToken) {
        // No CodeLens function if configuration option is set to `false`
        //  or if operation is cancelled
        if (
            workspace.getConfiguration("doxide").get("codeLens.enabled") ===
                false || token.isCancellationRequested
        ) {
            return null;
        }

        // Check what kind of CodeLens is being clicked and run the appropriate
        //  functions that returns the corresponding CodeLens
        if (lens instanceof DocstringCodeLens) {
            return this.resolveDocstringCodeLens(lens, token);
        } else if (lens instanceof PreviousCodeLens) {
            return this.resolvePreviousCodeLens(lens, token);
        } else if (lens instanceof NextCodeLens) {
            return this.resolveNextCodeLens(lens, token);
        } else if (lens instanceof AcceptCodeLens) {
            return this.resolveAcceptCodeLens(lens, token);
        }
    }

    private resolveDocstringCodeLens(
        lens: DocstringCodeLens,
        _token: CancellationToken
    ): CodeLens {
        var editor = window.activeTextEditor;
        if (!editor) {
            return lens; // No open text editor
        }
        
        var text = editor.document.getText(lens.contentRange);
        lens.command = {
            title: workspace.getConfiguration("doxide").get("codeLens.generateTitle") || "Generate",
            tooltip: "Generate a Docstring for this function.",
            command: "doxide.generateDocstring",
            arguments: [text, lens.range.start.line],
        };
        return lens;
    }

    private resolvePreviousCodeLens(
        lens: PreviousCodeLens,
        _token: CancellationToken
    ): CodeLens {
        lens.command = {
            title: "Previous",
            tooltip: "View previous alternative.",
            command: "doxide.previousAlternative",
            arguments: [],
        };
        return lens;
    }

    private resolveNextCodeLens(
        lens: NextCodeLens,
        _token: CancellationToken
    ): CodeLens {
        lens.command = {
            title: "Next",
            tooltip: "View next alternative.",
            command: "doxide.nextAlternative",
            arguments: [],
        };
        return lens;
    }

    private resolveAcceptCodeLens(
        lens: AcceptCodeLens,
        _token: CancellationToken
    ): CodeLens {
        lens.command = {
            title: "Accept",
            tooltip: "Accept current alternative",
            command: "doxide.acceptAlternative",
            arguments: [],
        };
        return lens;
    }
}
