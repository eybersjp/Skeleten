const fs = require('fs');
const path = require('path');

const TARGET_DIRS = ["PHASE_00_INTENT", "PHASE_01_CORE", "PHASE_02_VECTOR", "PHASE_03_GEN", "PHASE_04_DRIFT", ".agents"];
const ROOT_FILES = ["run.py", "SKELETEN_HEALTH_CHECK.py"];
const SRC_PATH = path.join(__dirname, '..', 'src');

let projectStruct = {};

// Handle requirements routing to .skeleten
const reqPath = path.join(SRC_PATH, 'requirements.txt');
if (fs.existsSync(reqPath)) {
    projectStruct[".skeleten/requirements.txt"] = fs.readFileSync(reqPath, 'utf8');
}

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        if (isDirectory) {
            walkDir(dirPath, callback);
        } else {
            callback(dirPath);
        }
    });
}

for (const d of TARGET_DIRS) {
    const dpath = path.join(SRC_PATH, d);
    if (fs.existsSync(dpath)) {
        walkDir(dpath, (filepath) => {
            // Ignore Python cache
            if (filepath.includes('__pycache__') || filepath.includes('dist')) return;
            const relPath = path.relative(SRC_PATH, filepath).replace(/\\/g, '/');
            try {
                const content = fs.readFileSync(filepath, 'utf8');
                projectStruct[relPath] = content;
            } catch (err) {
                // Ignore binary/decode errors
            }
        });
    }
}

for (const rf of ROOT_FILES) {
    const rfPath = path.join(SRC_PATH, rf);
    if (fs.existsSync(rfPath)) {
        projectStruct[rf] = fs.readFileSync(rfPath, 'utf8');
    }
}

const cliJsContent = `#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PROJECT_STRUCTURE = ${JSON.stringify(projectStruct, null, 4)};

function initSkeleten() {
    console.log("=".repeat(80));
    console.log("SKELETEN // NPM_FRAMEWORK_INJECTION_INITIATED");
    console.log("=".repeat(80));

    for (const [filepath, content] of Object.entries(PROJECT_STRUCTURE)) {
        const dirName = path.dirname(filepath);
        if (dirName !== '.' && !fs.existsSync(dirName)) {
            fs.mkdirSync(dirName, { recursive: true });
        }
        fs.writeFileSync(filepath, content, 'utf8');
        console.log(\`  [+] GENERATED_FILE: \${filepath}\`);
    }

    console.log("-".repeat(80));
    console.log("SKELETEN: FULL_PROJECT_READY");
    console.log("=".repeat(80));
    console.log("AI INTEGRATION ACTIVE: Subagents have inherited SKELETEN skills & slash commands.");
    
    console.log("[*] Establishing isolated Python Virtual Environment...");
    try {
        execSync('python -m venv .skeleten/venv', { stdio: 'inherit' });
        const isWin = process.platform === "win32";
        // Node requires quadruple backslashes to escape down to double backslashes in actual execution strings securely
        const pipCmd = isWin ? ".skeleten\\\\\\\\venv\\\\\\\\Scripts\\\\\\\\pip" : ".skeleten/venv/bin/pip";
        console.log("[*] Installing SKELETEN Isolated Dependencies...");
        execSync(\`\${pipCmd} install -r .skeleten/requirements.txt\`, { stdio: 'inherit' });
        console.log("[+] Virtual Environment Configured Successfully!");
    } catch (e) {
        console.log("[!] Failed to automatically configure python \`venv\` mechanism. Please install \`.skeleten/requirements.txt\` via your preferred isolation manually.");
    }
}

const args = process.argv.slice(2);
if (args[0] === 'init') {
    initSkeleten();
} else {
    console.log("Usage: npx skeleten init");
}
`;

const binDir = path.join(__dirname, '..', 'bin');
if (!fs.existsSync(binDir)) {
    fs.mkdirSync(binDir);
}
fs.writeFileSync(path.join(binDir, 'cli.js'), cliJsContent, 'utf8');
console.log("NPM CLI packaged successfully at ./bin/cli.js");
