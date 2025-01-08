# Features Documentation

## Core Features

### 1. Multi-Provider AI Support
- **Remote Providers**
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
- **Local Providers**
  - Ollama (Llama, Mistral)
  - Hugging Face Models

### 2. Retrieval Augmented Generation (RAG)
- Custom knowledge base of NEAR-specific vulnerabilities
- Vector-based similarity search
- Context-aware vulnerability detection
- Supports multiple embedding providers:
  - OpenAI embeddings
  - Local embeddings via Ollama

### 3. Smart Contract Analysis
- Rust code parsing and analysis
- Function-level vulnerability scanning
- Pattern matching for common security issues
- Best practices verification

### 4. Reporting Capabilities
- Multiple output formats (JSON, CSV)
- Detailed vulnerability descriptions
- Severity classifications
- Line-specific code references
- Remediation suggestions

### 5. Integration Features
- GitHub Actions support
- CI/CD pipeline integration
- Automated PR comments
- Custom workflow triggers

### 6. Configuration Options
- Customizable logging levels
- Multiple output formats
- Provider-specific settings
- Model selection flexibility

### 7. Performance Features
- Parallel processing capabilities
- Efficient code parsing
- Optimized memory usage
- Caching mechanisms

## Feature Details

### Vulnerability Detection
Scavene can detect various types of vulnerabilities, including:
- Reentrancy attacks
- Integer overflow/underflow
- Access control issues
- Logic errors
- Resource management problems
- Common NEAR-specific vulnerabilities

### Report Generation
Each vulnerability report includes:
- Severity level (Critical, High, Medium, Low)
- Detailed description
- Affected code location
- Impact assessment
- Remediation steps
- Related best practices

### GitHub Integration
When used as a GitHub Action, Scavene provides:
- Automated PR reviews
- Inline code comments
- Summary reports
- Status checks
- Custom failure conditions

## Upcoming Features

### Planned for Next Release
- [ ] Support for additional smart contract languages
- [ ] Enhanced vulnerability database
- [ ] Custom rules engine
- [ ] Performance optimizations

### Under Consideration
- Web interface
- Real-time analysis
- Plugin system
- Custom vulnerability definition format
- Integration with additional security tools

## Feature Configuration

### Example Configurations

1. Basic Configuration:
```sh
python main.py --provider openai --model gpt-4o
```

2. Advanced Configuration:
```sh
python main.py \
  --provider anthropic \
  --model claude-3.5-sonnet-latest \
  --retrieval-provider ollama \
  --format json \
  --log-level DEBUG
```

3. Local Setup:
```sh
python main.py \
  --provider ollama \
  --model llama2:13b \
  --retrieval-provider ollama \
  --output custom_audit
```

## Feature Limitations

### Remote Providers
- API rate limits apply
- Costs associated with API usage
- Internet connection required
- API key management needed

### Local Providers
- Higher hardware requirements
- Limited to available local models
- May have lower accuracy
- Requires local setup and maintenance

## Best Practices for Feature Usage

1. **Model Selection**
   - Use larger models for critical audits
   - Use faster models for development
   - Balance cost vs. accuracy

2. **Performance Optimization**
   - Use local embeddings when possible
   - Implement appropriate caching
   - Monitor resource usage

3. **Integration Usage**
   - Set up appropriate GitHub secrets
   - Configure failure conditions
   - Use custom output formats

## Feature Support Matrix

| Feature | OpenAI | Anthropic | Ollama | Hugging Face |
|---------|--------|-----------|---------|--------------|
| RAG Support | ✅ | ✅ | ✅ | ✅ |
| Local Processing | ❌ | ❌ | ✅ | ✅ |
| Custom Models | ❌ | ❌ | ✅ | ✅ |
| Embeddings | ✅ | ❌ | ✅ | ✅ |