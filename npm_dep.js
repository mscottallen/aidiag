const { spawn } = require('child_process');

function installPackages(packages) {
    return new Promise((resolve, reject) => {
        const install = spawn('npm', ['install', ...packages]);

        install.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        install.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        install.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`npm install process exited with code ${code}`));
            } else {
                resolve();
            }
        });
    });
}

// Usage
installPackages(['axios', 'glob'])
    .then(() => {
        console.log('Packages installed successfully');
    })
    .catch((error) => {
        console.error('Error installing packages:', error);
    });
