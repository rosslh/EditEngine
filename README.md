<p align="center">
    <img src="https://raw.githubusercontent.com/rosslh/EditEngine/main/icon.png" height="50px" width="50px" alt="EditEngine icon">
</p>

<h1 align="center">EditEngine</h1>

<p align="center">
  EditEngine is a copyediting assistant designed for experienced Wikipedia editors to accelerate mechanical grammar and clarity improvements while maintaining complete editorial control. The tool addresses Wikipedia's growing copyedit backlog by streamlining routine fixes that consume valuable editor time.
</p>

<p align="center">
  <img src="https://img.shields.io/github/check-runs/rosslh/EditEngine/main?style=flat&label=Checks" alt="GitHub branch check runs">
  <!-- <img src="https://img.shields.io/uptimerobot/status/m792388109-4c544ded2b0e440130ddd401?up_message=online&style=flat&label=Status" alt="Uptime Robot status">
  <img src="https://img.shields.io/uptimerobot/ratio/m792388109-4c544ded2b0e440130ddd401?style=flat&label=Uptime%20(1mo)" alt="Uptime Robot ratio (30 days)"> -->
</p>

## Core Principles

- **Editor oversight required**: All changes require explicit reviewer approval - nothing is automatic
- **Mechanical improvements only**: Focus on grammar, clarity, and prose flow without altering meaning
- **Wikipedia expertise assumed**: Designed as a power tool for editors familiar with MOS guidelines
- **Complete transparency**: Open source development with community input throughout

## Key Features

- **AI-assisted copyediting**: Uses language models to suggest grammar and clarity improvements
- **Side-by-side review**: Compare original and suggested text with clear diff highlighting
- **Wikitext preservation**: Maintains all citations, templates, internal links, and formatting
- **Section-based editing**: Work on specific article sections to manage scope and complexity
- **Edit session tracking**: Review past work and track improvement patterns over time
- **Multiple AI backends**: Support for OpenAI GPT-4 and Google Gemini models

## Workflow for Wikipedia Editors

1. **Load content**: Enter article title and section, or paste wikitext directly
2. **Review suggestions**: AI processes text paragraph-by-paragraph with proposed improvements
3. **Accept/reject changes**: Explicitly approve each suggestion using side-by-side comparison
4. **Copy improved text**: Transfer accepted changes to Wikipedia using your preferred editing method
5. **Track sessions**: All work is saved for future reference and quality assessment

## Content Safeguards

EditEngine includes multiple protection mechanisms designed to prevent common pitfalls of automated editing:

### Wikitext Preservation

- **References**: `<ref>` tags and citation formatting remain untouched
- **Templates**: `{{...}}` templates are completely preserved
- **Internal links**: `[[...]]` link targets and formatting stay intact
- **External links**: URL formatting and link text preserved
- **Quotes**: Text in quotation marks is protected from modification
- **HTML comments**: `<!-- -->` comments are ignored during processing

### Content Safety

- **No new information**: Tool cannot introduce facts, claims, or unsourced content
- **Meaning preservation**: Changes limited to grammar, clarity, and prose flow
- **Complex paragraph skipping**: Problematic sections are automatically bypassed
- **Template-heavy content**: Sections with extensive template usage are handled carefully

### Editorial Control

- **Default rejection**: All suggestions are rejected unless explicitly accepted
- **Individual review**: Each proposed change requires separate approval
- **Undo capability**: Complete edit history allows reverting any session
- **Quality assessment**: Track patterns in accepted/rejected suggestions

## For Experienced Editors

This tool is designed for Wikipedia editors who:

- Understand Manual of Style guidelines and can evaluate prose improvements
- Recognize when AI suggestions align with Wikipedia's neutral, encyclopedic tone
- Can identify potential issues with factual accuracy or sourcing implications
- Want to accelerate routine copyediting while maintaining editorial judgment

The tool helps with the mechanical aspects of copyediting but requires Wikipedia expertise to use effectively.

## Development and Community

EditEngine is developed as an open source project with transparency and community input as core values:

- **Open source**: Full codebase available for review and contribution
- **Community-driven**: Development informed by feedback from experienced Wikipedia editors
- **Toolforge hosting**: Designed for deployment on Wikipedia's official tool hosting platform
- **Gradual rollout**: Careful testing and validation before broader community adoption

### Technology Stack

- **Backend**: Python, Django REST framework
- **Frontend**: React, TypeScript with responsive design
- **Background processing**: Celery with PostgreSQL for AI model integration
- **Development**: Modern web stack optimized for Wikipedia editor workflows

## Getting Started

Since OAuth integration awaits community consensus, EditEngine currently offers safe evaluation methods:

1. **Demo links**: View before/after diffs for any Wikipedia article section
2. **Copy/paste workflow**: Review suggested improvements in your sandbox before making changes
3. **Local development**: Set up the tool locally for thorough testing

For experienced Wikipedia editors interested in evaluating the tool's output quality or contributing to development, please see the project's development documentation.
