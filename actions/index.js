const exec = require('@actions/exec')
const github = require('@actions/github')
const core = require('@actions/core')
const { table } = require('table')

function displayTable(data) {
  console.log('\n\n\n')

  if (data.length === 0) {
    console.log('No vulnerabilities detected')
    return
  }

  for (const file of data) {
    const tableData = [
      ['Severity', 'Description', 'Line', 'Code Snippet'],
      ...file.vulnerabilities.map((item) => [
        item.severity_level,
        item.severity_description,
        item.line_number,
        item.code_snippet,
      ]),
    ]

    console.log(`File path: ${file.file_path}`)
    console.log(
      table(tableData, {
        columns: {
          1: { width: 50 },
        },
      })
    )
    console.log('\n')
  }
}

function jsonToMd(vulnerabilities_data) {
  let md = '# 🔍 Vulnerability Report\n\n'

  if (vulnerabilities_data.length === 0) {
    md += '✅ **No vulnerabilities detected**\n\n'
  }

  vulnerabilities_data.forEach((file) => {
    md += `## 📁 File: ${file.file_path}\n\n`

    const severityEmojis = {
      Critical: '🚫',
      High: '🚨',
      Medium: '⚠️',
      Low: 'ℹ️',
      Informational: '🔍',
    }

    const severityGroups = {
      Critical: [],
      High: [],
      Medium: [],
      Low: [],
      Informational: [],
    }

    file.vulnerabilities.forEach((vuln) => {
      if (severityGroups[vuln.severity_level] !== undefined) {
        severityGroups[vuln.severity_level].push(vuln)
      } else {
        severityGroups[vuln.severity_level] = [vuln]
      }
    })

    for (const [severity, vulns] of Object.entries(severityGroups)) {
      if (vulns.length !== 0) {
        md += `### ${severityEmojis[severity]} ${severity} Severity\n\n`

        vulns.forEach((vuln) => {
          md += `**Lines ${vuln.line_number}:**\n`
          md += '```rust\n' + vuln.code_snippet + '\n```\n'
          md += `${getIssueEmoji(vuln.severity_description)} **Issue:** ${
            vuln.severity_description
          }\n\n`
        })
      }
    }
  })

  md +=
    '### Disclaimer\n\n**Important:** This scan was conducted using AI-based tools, which, while effective for identifying common issues, have limitations. AI may miss complex vulnerabilities, produce false positives, or misinterpret context.'

  return md
}

function getIssueEmoji(description) {
  if (description.includes('overflow')) return '💥'
  if (description.includes('private') || description.includes('access'))
    return '🔒'
  if (description.includes('byte')) return '🔢'
  if (description.includes('panic') || description.includes('unwrap'))
    return '❗'
  return '🔴'
}

async function main() {
  let myOutput = ''

  const options = {}
  options.listeners = {
    stdout: (data) => {
      myOutput += data.toString()
    },
  }

  const model = core.getInput('model')
  const outputFile = core.getInput('output_file')
  const folderPath = core.getInput('folder_path')

  const args = []
  if (folderPath) args.push(folderPath)
  if (model) args.push(`--model ${model}`)
  if (outputFile) args.push(`--output ${outputFile}`)

  await exec.exec(`python main.py ${args.join(' ')}`, [], options)

  const parsedData = JSON.parse(myOutput)
  displayTable(parsedData)

  const myToken = core.getInput('myToken')
  const octokit = github.getOctokit(myToken)

  if (github.context.eventName === 'pull_request') {
    await octokit.rest.issues.createComment({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      issue_number: github.context.issue.number,
      body: jsonToMd(parsedData),
    })
  }

  if (parsedData.length !== 0) {
    core.setFailed('Vulnerabilities detected')
  }
}

main()
