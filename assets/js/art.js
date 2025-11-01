const fs = require('fs');
const path = require('path');

const imagesFolderPath = path.join(__dirname, 'images'); // Assuming 'images' is in the same directory as your script

function getFoldersInDirectory(directoryPath) {
  try {
    const items = fs.readdirSync(directoryPath, { withFileTypes: true });
    const folders = items
      .filter(item => item.isDirectory())
      .map(item => item.name);
    return folders;
  } catch (error) {
    console.error(`Error reading directory ${directoryPath}:`, error);
    return [];
  }
}

const foldersInImages = getFoldersInDirectory(imagesFolderPath);
console.log('Folders in the "images" directory:', foldersInImages);
