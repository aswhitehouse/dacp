# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.3.0] - 2025-07-02

### Added
- **Comprehensive Logging System**: Added full logging capabilities throughout DACP
  - Easy setup functions: `enable_info_logging()`, `enable_debug_logging()`, `enable_quiet_logging()`
  - Custom configuration with `setup_dacp_logging()` 
  - Multiple format styles: emoji (production-friendly), detailed (debugging), simple
  - Optional file logging support
  - Performance timing for all operations
  - Sensitive data masking in logs
- **Multi-Provider Intelligence System**: Major refactor of LLM integration
  - New `invoke_intelligence()` function supports multiple providers
  - Support for OpenAI, Anthropic (Claude), Azure OpenAI, and local LLMs (Ollama)
  - Generic configuration system for easy provider switching
  - Automatic error handling and retries
  - Configuration validation with helpful error messages
- **Enhanced Error Handling**: Improved error messages with context throughout the system
- **Performance Monitoring**: All operations now include execution timing

### Changed
- **Breaking**: `call_llm()` is now legacy - use `invoke_intelligence()` for new code
- Orchestrator now provides much more detailed feedback and logging
- Tool execution includes comprehensive error handling and timing
- Agent registration and message routing now fully logged

### Fixed
- Better error handling for missing API keys and invalid configurations
- Improved tool execution feedback and error reporting

### Examples
- Added `examples/logging_demo.py` - comprehensive logging demonstration
- Added `examples/agent_with_logging.py` - simple agent with logging
- Updated `examples/intelligence_demo.py` - multi-provider intelligence examples

## [0.2.0] - 2024-12-01

### Added
- Agent orchestration system with `Orchestrator` and `Agent` base classes
- Enhanced `file_writer` tool with automatic directory creation
- Conversation history tracking and session management
- Tool request handling with automatic execution
- Broadcast messaging capabilities
- Comprehensive test suite with 90%+ coverage

### Changed
- Tool registry now uses consistent interface
- Improved error handling throughout the system

## [0.1.0] - 2024-01-01

### Added
- Initial release of DACP
- Core functionality for LLM/agent communication
- Tool registration and execution system
- Protocol parsing utilities
- Basic OpenAI integration 