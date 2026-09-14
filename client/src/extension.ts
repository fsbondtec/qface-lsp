import * as path from "path";
import { workspace, ExtensionContext } from "vscode";

import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
  TransportKind,
} from "vscode-languageclient/node";

let client: LanguageClient;

export function activate(context: ExtensionContext): void {
  const config = workspace.getConfiguration("qface");
  const pythonPath = config.get<string>("pythonPath", "python");
  const serverModule = "qface_lsp.server";
  const serverCwd = path.join(context.extensionPath, "server");

  const serverOptions: ServerOptions = {
    command: pythonPath,
    args: ["-m", serverModule],
    options: {
      cwd: serverCwd,
    },
    transport: TransportKind.stdio,
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [{ scheme: "file", language: "qface" }],
    synchronize: {
      fileEvents: workspace.createFileSystemWatcher("**/*.qface"),
    },
  };

  client = new LanguageClient(
    "qfaceLanguageServer",
    "QFace Language Server",
    serverOptions,
    clientOptions
  );

  client.start();
  context.subscriptions.push({ dispose: () => client.stop() });
}

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}
