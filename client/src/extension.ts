import * as path from "path";

import {
  commands,
  window,
  workspace,
  ExtensionContext,
  OutputChannel,
} from "vscode";

import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
  TransportKind,
} from "vscode-languageclient/node";

/**
 * Must match the `qface.*` prefix of the contributed settings: the language
 * client derives the name of its trace setting (`qface.trace.server`) from
 * this id.
 */
const CLIENT_ID = "qface";
const CLIENT_NAME = "QFace Language Server";

let client: LanguageClient | undefined;
let outputChannel: OutputChannel | undefined;

export async function activate(context: ExtensionContext): Promise<void> {
  outputChannel = window.createOutputChannel(CLIENT_NAME);
  context.subscriptions.push(outputChannel);

  context.subscriptions.push(
    commands.registerCommand("qface.restartServer", async () => {
      await stopClient();
      await startClient(context, { userInvoked: true });
    })
  );

  // Restart on settings changes that affect how the server process is spawned.
  context.subscriptions.push(
    workspace.onDidChangeConfiguration(async (event) => {
      if (
        event.affectsConfiguration("qface.pythonPath") ||
        event.affectsConfiguration("qface.server.enable")
      ) {
        await stopClient();
        await startClient(context);
      }
    })
  );

  await startClient(context);
}

export function deactivate(): Thenable<void> | undefined {
  return stopClient();
}

async function startClient(
  context: ExtensionContext,
  options: { userInvoked?: boolean } = {}
): Promise<void> {
  const config = workspace.getConfiguration("qface");
  if (!config.get<boolean>("server.enable", false)) {
    outputChannel?.appendLine(
      "Language server disabled via 'qface.server.enable'; syntax highlighting only."
    );
    // Without this the restart command would be a silent no-op, which reads
    // like a broken command rather than a deliberate opt-out.
    if (options.userInvoked) {
      const openSettings = "Open Settings";
      void window
        .showInformationMessage(
          "The QFace language server is disabled. Enable 'qface.server.enable' to get diagnostics.",
          openSettings
        )
        .then((choice) => {
          if (choice === openSettings) {
            void commands.executeCommand(
              "workbench.action.openSettings",
              "qface.server.enable"
            );
          }
        });
    }
    return;
  }

  const pythonPath = config.get<string>("pythonPath", "python");
  const serverOptions: ServerOptions = {
    command: pythonPath,
    args: ["-m", "qface_lsp.server"],
    options: {
      cwd: path.join(context.extensionPath, "server"),
    },
    transport: TransportKind.stdio,
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [{ scheme: "file", language: "qface" }],
    synchronize: {
      fileEvents: workspace.createFileSystemWatcher("**/*.qface"),
    },
    outputChannel,
  };

  client = new LanguageClient(
    CLIENT_ID,
    CLIENT_NAME,
    serverOptions,
    clientOptions
  );

  try {
    await client.start();
  } catch (error) {
    client = undefined;
    reportStartFailure(pythonPath, error);
  }
}

async function stopClient(): Promise<void> {
  const current = client;
  client = undefined;
  if (!current) {
    return;
  }
  try {
    await current.stop();
  } catch {
    // The process may already be gone; nothing useful left to do.
  }
}

/**
 * The server needs a Python interpreter with `pygls` and `qface` installed,
 * which the VSIX cannot provide. Surface that as an actionable message instead
 * of a bare activation failure, and keep syntax highlighting working.
 */
function reportStartFailure(pythonPath: string, error: unknown): void {
  const detail = error instanceof Error ? error.message : String(error);
  outputChannel?.appendLine(`Failed to start the QFace language server: ${detail}`);

  const openSettings = "Open Settings";
  const showLog = "Show Log";
  void window
    .showWarningMessage(
      `Could not start the QFace language server using '${pythonPath}'. ` +
        "Syntax highlighting still works, but diagnostics are unavailable. " +
        "Check that the interpreter exists and has 'pygls' and 'qface' installed.",
      openSettings,
      showLog
    )
    .then((choice) => {
      if (choice === openSettings) {
        void commands.executeCommand(
          "workbench.action.openSettings",
          "qface.pythonPath"
        );
      } else if (choice === showLog) {
        outputChannel?.show(true);
      }
    });
}
