const fs = require("fs");
const readline = require("readline");
const vm = require("vm");
const path = require("path");

const HELP = `
Commands:
    help - Show this manual
    ls - List files in the current directory
    cat [file] - Print the file
    ! [code] - Execute code
    exit - Close the connection
`;

const LOGS = path.join(__dirname, "logs");

const context = vm.createContext({
  print: console.log,
});

const handle = (line) => {
  if (!line || line.length === 0) return HELP;

  line = line.trim();
  const args = line.split(" ");
  const cmd = args[0].toLowerCase();
  const input = args.slice(1).join(" ");

  switch (cmd) {
    case "help":
      return console.log(HELP);

    case "!":
      try {
        console.log(vm.runInContext(input, context));
      } catch (e) {
        console.log(e.message);
      }
      return;

    case "ls":
      try {
        fs.readdirSync(LOGS).forEach((file) => {
          console.log(file);
        });
      } catch (e) {
        console.log(e.message);
      }

      return;

    case "cat":
      try {
        console.log(fs.readFileSync(path.join(LOGS, input)).toString());
      } catch (e) {
        console.log(e.message);
      }

      return;

    case "exit":
      rl.close();
      return;

    default:
      console.log(`Unknown command: ${cmd}`);
      return;
  }
};

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: ">> ",
});

console.log("EnviroTrack WeatherMaster 3000 Station Control Shell");
console.log("Runtime version: " + process.version);

rl.prompt();

rl.on("line", (line) => {
  handle(line);
  rl.prompt();
});

rl.on("close", () => {
  process.exit(0);
});