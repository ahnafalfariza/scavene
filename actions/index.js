const exec = require('@actions/exec')
const github = require('@actions/github')

function displayTable(data) {
  for (const file of data) {
    console.log(file.file_path)
    console.table(file.vulnerabilities)
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

  await github.getOctokit(process.env.GITHUB_TOKEN).rest.issues.createComment({
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    issue_number: github.context.issue.number,
    body: '```json\n' + JSON.stringify(parsedData, null, 2) + '\n```'
  })
}

main()
