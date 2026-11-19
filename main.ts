// Place the finished image in the requested output folder, making the folder as needed.
const fileSystem = require('node:fs');
const filePaths = require('node:path');

const outputFolder = filePaths.resolve(process.env.MAKEFUN_OUTPUT_DIR || '/output');
fileSystem.mkdirSync(outputFolder, { recursive: true });
fileSystem.copyFileSync(filePaths.join(__dirname, 'entry.png'), filePaths.join(outputFolder, 'entry.png'));
