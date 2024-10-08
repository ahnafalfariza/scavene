const exec = require('@actions/exec')
const github = require('@actions/github')
const core = require('@actions/core')
const { table } = require('table');

function displayTable(data) {
  console.log("\n\n\n")

  for (const file of data) {
    const tableData = [
      ['Severity', 'Description', 'Line', 'Code Snippet'], // Header row
      ...file.vulnerabilities.map(item => [
        item.severity_level,
        item.severity_description,
        item.line_number,
        item.code_snippet,
      ])
    ];

    console.log(`File path: ${file.file_path}`)
    console.log(table(tableData, {
      columns: {
        1: { width: 50 },
      }
    }));
    console.log('\n')
  }
}

async function main() {
  let myOutput = '';

  const options = {};
  options.listeners = {
    stdout: (data) => {
      myOutput += data.toString();
    },
  };

  await exec.exec('python', ['main.py'], options);

  const parsedData = JSON.parse(myOutput)
  displayTable(parsedData)

  const myToken = core.getInput('myToken');
  const octokit = github.getOctokit(myToken)

  await octokit.rest.issues.createComment({
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    issue_number: github.context.issue.number,
    body: '```json\n' + JSON.stringify(parsedData, null, 2) + '\n```'
  })
}

main()
