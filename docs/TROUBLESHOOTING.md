# Troubleshooting Guide

This guide helps you resolve common issues encountered while using Scavene.

## Table of Contents
- [Common Issues](#common-issues)
- [Installation Problems](#installation-problems)
- [Runtime Errors](#runtime-errors)
- [GitHub Action Issues](#github-action-issues)
- [Performance Problems](#performance-problems)

## Common Issues

### API Key Issues

#### Error: "API key not found" or "Invalid API key"
```
Error: OpenAI API key not found. Please set OPENAI_API_KEY environment variable.
```

**Solutions:**
1. Check if API key is properly set:
   ```sh
   echo $OPENAI_API_KEY  # For OpenAI
   echo $ANTHROPIC_API_KEY  # For Anthropic
   ```
2. Set API key in your environment:
   ```sh
   export OPENAI_API_KEY='your-key-here'
   ```
3. Verify .env file contains correct keys:
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-...
   ```

### Model Loading Issues

#### Error: "Model not found" or "Model unavailable"
```
Error: The model 'gpt-4o' does not exist or you do not have access to it.
```

**Solutions:**
1. Verify model name is correct
2. Check provider status page for outages
3. Confirm API key has access to requested model
4. Try using an alternative model



## Installation Problems

### Dependencies

#### Package Conflicts
```
Error: Dependency resolution failed
```

**Solutions:**
1. Create fresh virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Update pip:
   ```sh
   pip install --upgrade pip
   ```
3. Install dependencies one by one to identify conflict

## Runtime Errors

### File Processing

#### Permission Denied
```
Error: Permission denied when accessing file
```

**Solutions:**
1. Check file permissions:
   ```sh
   ls -l /path/to/file
   ```
2. Run with appropriate permissions
3. Verify file ownership

#### Invalid File Format
```
Error: Unable to parse Rust file
```

**Solutions:**
1. Verify file is valid Rust code
2. Check file encoding
3. Remove any hidden characters

## GitHub Action Issues

### Action Failures

#### Authentication Failed
```
Error: Unable to authenticate with GitHub
```

**Solutions:**
1. Verify GitHub token is set
2. Check repository permissions
3. Regenerate GitHub token
4. Verify workflow permissions

#### Timeout Issues
```
Error: Workflow timeout exceeded
```

**Solutions:**
1. Increase timeout in workflow:
   ```yaml
   timeout-minutes: 30
   ```
2. Optimize processing
3. Split into multiple jobs

## Performance Problems

### Slow Processing

**Symptoms:**
- Long processing times
- High memory usage
- System unresponsiveness

**Solutions:**
1. Use local embedding provider:
   ```sh
   --retrieval-provider ollama
   ```
2. Reduce logging level:
   ```sh
   --log-level WARNING
   ```
3. Process files in batches
4. Use smaller models for initial testing

### Memory Usage

**Symptoms:**
- Out of memory errors
- System slowdown
- Swap thrashing

**Solutions:**
1. Monitor memory usage:
   ```sh
   top -o %MEM
   ```
2. Use memory-efficient providers
3. Implement batch processing
4. Increase system swap space

## Getting Help

If you're still experiencing issues:

1. Check [GitHub Issues](https://github.com/ahnafalfariza/scavene/issues)
2. Enable debug logging:
   ```sh
   --log-level DEBUG
   ```
3. Join our community:
   - Discord: [Link]
   - Discussions: [GitHub Discussions]
4. Submit a bug report with:
   - Full error message
   - Command used
   - System information
   - Log output