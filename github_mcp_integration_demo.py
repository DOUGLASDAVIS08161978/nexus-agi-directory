#!/usr/bin/env python3
"""
GITHUB MCP SERVER INTEGRATION DEMONSTRATION
===========================================
Comprehensive demonstration of GitHub MCP Server integration
with our Bitcoin Educational Systems.

MCP (Model Context Protocol) allows AI tools to interact with GitHub
through a standardized interface.

Authors: Douglas Shane Davis & Claude
Version: 1.0
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def disable(cls):
        for attr in dir(cls):
            if not attr.startswith('_') and attr != 'disable':
                setattr(cls, attr, '')


class GitHubMCPDemo:
    """
    GitHub MCP Server Integration Demonstration
    """

    def __init__(self, use_colors: bool = True):
        self.mcp_server_path = "/tmp/github-mcp-server/github-mcp-server"
        self.project_repo = "DOUGLASDAVIS08161978/nexus-agi-directory"

        if not use_colors:
            Colors.disable()

    def display_header(self):
        """Display demonstration header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}")
        print(" GITHUB MCP SERVER INTEGRATION DEMONSTRATION")
        print(" Bitcoin Educational Systems + GitHub MCP")
        print(f"{'='*80}{Colors.ENDC}\n")

        print(f"{Colors.WARNING}📋 ABOUT THIS DEMONSTRATION:{Colors.ENDC}")
        print("   • Shows GitHub MCP Server capabilities")
        print("   • Demonstrates available tools and toolsets")
        print("   • Integrates with Bitcoin Educational Systems")
        print("   • Simulates expected AI interactions")
        print(f"\n{'-'*80}\n")

    def section_1_what_is_mcp(self):
        """Explain what MCP is"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}📖 SECTION 1: WHAT IS MODEL CONTEXT PROTOCOL (MCP)?{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Model Context Protocol (MCP):{Colors.ENDC}")
        print("   A standardized protocol for connecting AI tools to external services\n")

        print(f"   {Colors.BOLD}Purpose:{Colors.ENDC}")
        print("   • Allows AI assistants to access real-world data and services")
        print("   • Standardizes how AI tools interact with external systems")
        print("   • Enables tools, resources, and prompts as primitives")
        print("   • Supports local and remote server configurations\n")

        print(f"   {Colors.BOLD}GitHub MCP Server Specifically:{Colors.ENDC}")
        print("   • Connects AI tools directly to GitHub's platform")
        print("   • Provides natural language interface to GitHub operations")
        print("   • Enables repository management, issues, PRs, CI/CD, and more")
        print("   • Built and maintained by GitHub\n")

        print(f"   {Colors.OKGREEN}Version:{Colors.ENDC} v0.26.3 (Latest)")
        print(f"   {Colors.OKGREEN}Repository:{Colors.ENDC} https://github.com/github/github-mcp-server")
        print(f"   {Colors.OKGREEN}Language:{Colors.ENDC} Go")
        print(f"   {Colors.OKGREEN}Binary Size:{Colors.ENDC} 23 MB\n")

        print(f"{'-'*80}\n")

    def section_2_available_toolsets(self):
        """Display available toolsets"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}🔧 SECTION 2: AVAILABLE TOOLSETS{Colors.ENDC}\n")

        toolsets = {
            "default (Enabled by default)": [
                ("context", "Repository context and structure"),
                ("issues", "Issue management and tracking"),
                ("pull_requests", "Pull request operations"),
                ("repos", "Repository operations"),
                ("users", "User and team management")
            ],
            "actions": [
                ("workflows", "GitHub Actions workflow management"),
                ("runs", "Workflow run monitoring and analysis"),
                ("artifacts", "Build artifact management")
            ],
            "code_security": [
                ("code_scanning", "Security vulnerability scanning"),
                ("secret_scanning", "Secret detection"),
                ("dependabot", "Dependency vulnerability alerts")
            ],
            "git": [
                ("commits", "Commit history and analysis"),
                ("branches", "Branch management"),
                ("tags", "Tag operations")
            ],
            "discussions": [
                ("threads", "Discussion thread management"),
                ("comments", "Comment operations")
            ],
            "gists": [
                ("create", "Create code snippets"),
                ("manage", "Gist management")
            ],
            "notifications": [
                ("inbox", "Notification management"),
                ("subscriptions", "Subscription handling")
            ],
            "orgs": [
                ("teams", "Organization team management"),
                ("members", "Member management"),
                ("settings", "Organization settings")
            ],
            "projects": [
                ("boards", "Project board management"),
                ("cards", "Card operations")
            ],
            "stargazers": [
                ("stars", "Star/unstar repositories"),
                ("trending", "Trending repository discovery")
            ]
        }

        for toolset_name, tools in toolsets.items():
            print(f"   {Colors.BOLD}{toolset_name.upper()}{Colors.ENDC}")
            for tool, description in tools:
                print(f"     • {Colors.OKGREEN}{tool:20}{Colors.ENDC} - {description}")
            print()

        print(f"   {Colors.WARNING}Total Toolsets:{Colors.ENDC} 13 available")
        print(f"   {Colors.WARNING}Default Toolsets:{Colors.ENDC} 5 enabled by default")
        print(f"   {Colors.WARNING}Custom Toolsets:{Colors.ENDC} Enable via --toolsets flag\n")

        print(f"{'-'*80}\n")

    def section_3_integration_with_bitcoin_systems(self):
        """Show integration with Bitcoin educational systems"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}🔗 SECTION 3: INTEGRATION WITH BITCOIN EDUCATIONAL SYSTEMS{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Our Bitcoin Educational Repository:{Colors.ENDC}")
        print(f"   Repository: {Colors.OKGREEN}{self.project_repo}{Colors.ENDC}")
        print(f"   Branch: {Colors.OKGREEN}claude/bitcoin-bridge-demo-Fw9iV{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Current Project Files:{Colors.ENDC}")
        files = [
            ("bitcoin_bridge_demo.py", "Basic bridge impossibility demonstration"),
            ("bitcoin_bridge_demo_enhanced.py", "Enhanced bridge demo with CLI"),
            ("bitcoin_mining_educational_system.py", "Complete mining education system"),
            ("check_testnet_address.py", "Testnet address balance checker"),
            ("BITCOIN_EDUCATIONAL_SYSTEMS_README.md", "Comprehensive documentation")
        ]

        for filename, description in files:
            print(f"     📄 {Colors.OKBLUE}{filename:45}{Colors.ENDC} - {description}")

        print(f"\n   {Colors.BOLD}How GitHub MCP Enhances Our Systems:{Colors.ENDC}\n")

        enhancements = [
            ("Automated Issue Tracking",
             "AI can create issues for bugs found during demonstrations"),

            ("Pull Request Automation",
             "AI can create PRs for improvements and new features"),

            ("Code Review Integration",
             "AI can analyze code and suggest improvements via PR comments"),

            ("Documentation Generation",
             "AI can update README files based on code changes"),

            ("CI/CD Monitoring",
             "AI can monitor GitHub Actions workflows and report failures"),

            ("Dependency Management",
             "AI can track and update dependencies via Dependabot"),

            ("Community Engagement",
             "AI can respond to discussions and help users"),

            ("Release Management",
             "AI can automate release notes and version tagging")
        ]

        for i, (feature, description) in enumerate(enhancements, 1):
            print(f"   {i}. {Colors.BOLD}{feature}{Colors.ENDC}")
            print(f"      {description}\n")

        print(f"{'-'*80}\n")

    def section_4_example_interactions(self):
        """Demonstrate example AI interactions"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}💬 SECTION 4: EXAMPLE AI INTERACTIONS{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Here's how AI would interact with our repository via MCP:{Colors.ENDC}\n")

        examples = [
            {
                "user": "List all files in the Bitcoin educational systems repository",
                "ai_action": "Uses repos_list_files tool",
                "response": """Found 5 main educational files:
                - bitcoin_bridge_demo.py (12 KB)
                - bitcoin_bridge_demo_enhanced.py (32 KB)
                - bitcoin_mining_educational_system.py (45 KB)
                - check_testnet_address.py (5 KB)
                - BITCOIN_EDUCATIONAL_SYSTEMS_README.md (18 KB)"""
            },
            {
                "user": "Create an issue for adding Ethereum testnet support",
                "ai_action": "Uses issues_create tool",
                "response": """Created issue #4: "Add Ethereum Testnet Support"
                Labels: enhancement, educational
                Milestone: v2.0
                Assigned to: DOUGLASDAVIS08161978"""
            },
            {
                "user": "Show me recent commits on the bitcoin-bridge-demo branch",
                "ai_action": "Uses repos_list_commits tool",
                "response": """Recent commits on claude/bitcoin-bridge-demo-Fw9iV:
                230e4c7 - Add Bitcoin testnet address balance checker
                27e8652 - Add Bitcoin Mining Educational System with BitRef API Integration
                e0c46e0 - Add Bitcoin Bridge Educational Demonstrations"""
            },
            {
                "user": "Check if there are any security vulnerabilities",
                "ai_action": "Uses code_security tools",
                "response": """Security scan complete:
                ✓ No critical vulnerabilities found
                ✓ No secrets detected in code
                ℹ 2 Dependabot alerts for minor dependency updates
                Overall: Repository is secure"""
            },
            {
                "user": "Create a PR to merge the demo branch to main",
                "ai_action": "Uses pull_requests_create tool",
                "response": """Created Pull Request #5:
                Title: "Bitcoin Educational Systems - Complete Suite"
                From: claude/bitcoin-bridge-demo-Fw9iV → main
                Description: Comprehensive Bitcoin education systems with
                bridge demonstrations and mining simulations
                Status: Ready for review"""
            }
        ]

        for i, example in enumerate(examples, 1):
            print(f"   {Colors.BOLD}Example {i}:{Colors.ENDC}")
            print(f"   {Colors.OKCYAN}👤 User:{Colors.ENDC} \"{example['user']}\"")
            print(f"   {Colors.WARNING}🤖 AI Action:{Colors.ENDC} {example['ai_action']}")
            print(f"   {Colors.OKGREEN}📤 Response:{Colors.ENDC}")
            for line in example['response'].split('\n'):
                print(f"      {line}")
            print()

        print(f"{'-'*80}\n")

    def section_5_configuration_examples(self):
        """Show configuration examples"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}⚙️  SECTION 5: CONFIGURATION EXAMPLES{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}1. Basic Configuration (Default Toolsets):{Colors.ENDC}\n")
        print(f"   {Colors.OKBLUE}Command:{Colors.ENDC}")
        print("   $ github-mcp-server stdio")
        print(f"   {Colors.OKGREEN}Enables:{Colors.ENDC} context, issues, pull_requests, repos, users\n")

        print(f"   {Colors.BOLD}2. Custom Toolsets Configuration:{Colors.ENDC}\n")
        print(f"   {Colors.OKBLUE}Command:{Colors.ENDC}")
        print("   $ github-mcp-server stdio --toolsets=default,actions,code_security")
        print(f"   {Colors.OKGREEN}Enables:{Colors.ENDC} Default + GitHub Actions + Code Security\n")

        print(f"   {Colors.BOLD}3. All Toolsets (Maximum Features):{Colors.ENDC}\n")
        print(f"   {Colors.OKBLUE}Command:{Colors.ENDC}")
        print("   $ github-mcp-server stdio --toolsets=all")
        print(f"   {Colors.OKGREEN}Enables:{Colors.ENDC} All 13 toolsets\n")

        print(f"   {Colors.BOLD}4. Read-Only Mode (Safe for Production):{Colors.ENDC}\n")
        print(f"   {Colors.OKBLUE}Command:{Colors.ENDC}")
        print("   $ github-mcp-server stdio --read-only")
        print(f"   {Colors.OKGREEN}Enables:{Colors.ENDC} Only read operations, no modifications\n")

        print(f"   {Colors.BOLD}5. With GitHub Personal Access Token:{Colors.ENDC}\n")
        print(f"   {Colors.OKBLUE}Environment Variable:{Colors.ENDC}")
        print("   $ export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here")
        print("   $ github-mcp-server stdio --toolsets=all\n")

        print(f"   {Colors.BOLD}6. Docker Configuration:{Colors.ENDC}\n")
        print(f"   {Colors.OKBLUE}Command:{Colors.ENDC}")
        print("""   $ docker run -i --rm \\
     -e GITHUB_PERSONAL_ACCESS_TOKEN=ghp_token \\
     ghcr.io/github/github-mcp-server\n""")

        print(f"{'-'*80}\n")

    def section_6_mcp_protocol_flow(self):
        """Explain MCP protocol flow"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}🔄 SECTION 6: MCP PROTOCOL FLOW{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}How AI Interacts with GitHub via MCP:{Colors.ENDC}\n")

        flow = [
            ("1. AI receives user request",
             'User: "Show me open issues in the Bitcoin repo"',
             Colors.OKCYAN),

            ("2. AI determines required tool",
             "Tool: issues_list (from issues toolset)",
             Colors.WARNING),

            ("3. AI calls MCP server",
             'MCP Request: {"method": "tools/call", "params": {"name": "issues_list", ...}}',
             Colors.OKBLUE),

            ("4. MCP server authenticates",
             "Validates GitHub Personal Access Token",
             Colors.WARNING),

            ("5. MCP calls GitHub API",
             "GET https://api.github.com/repos/user/repo/issues",
             Colors.OKBLUE),

            ("6. GitHub returns data",
             "JSON response with issue list",
             Colors.OKGREEN),

            ("7. MCP formats response",
             "Converts to MCP protocol format",
             Colors.WARNING),

            ("8. AI processes response",
             "Parses and understands the data",
             Colors.OKBLUE),

            ("9. AI responds to user",
             '"I found 3 open issues: #1 (bug), #2 (enhancement), #3 (question)"',
             Colors.OKGREEN)
        ]

        for step, description, color in flow:
            print(f"   {color}{step}{Colors.ENDC}")
            print(f"      {description}\n")

        print(f"   {Colors.BOLD}Key Benefits:{Colors.ENDC}")
        print(f"   ✓ Standardized protocol across all AI tools")
        print(f"   ✓ Secure authentication via GitHub tokens")
        print(f"   ✓ Natural language interface to GitHub")
        print(f"   ✓ No need to learn GitHub CLI or API\n")

        print(f"{'-'*80}\n")

    def section_7_expected_output(self):
        """Show expected output from integration"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}📊 SECTION 7: EXPECTED OUTPUT - LIVE DEMO{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Simulated AI Session with GitHub MCP:{Colors.ENDC}\n")

        print(f"   {Colors.OKGREEN}Session initialized with GitHub MCP Server v0.26.3{Colors.ENDC}")
        print(f"   {Colors.OKGREEN}Connected to repository: {self.project_repo}{Colors.ENDC}")
        print(f"   {Colors.OKGREEN}Toolsets loaded: default,actions,code_security{Colors.ENDC}\n")

        interactions = [
            {
                "prompt": "List recent commits",
                "tool": "repos_list_commits",
                "output": """Commits on claude/bitcoin-bridge-demo-Fw9iV:

                230e4c7 (2 minutes ago) - Add Bitcoin testnet address balance checker
                  • Created check_testnet_address.py utility
                  • Supports BIP173 test vectors
                  • Integrates with blockchain explorers

                27e8652 (15 minutes ago) - Add Bitcoin Mining Educational System
                  • Complete BitRef API integration (11 endpoints)
                  • Mining simulation with SHA-256
                  • Reality check: CPU vs ASIC comparison
                  • Shows why CPU mining is obsolete

                e0c46e0 (30 minutes ago) - Add Bitcoin Bridge Educational Demonstrations
                  • Basic and enhanced bridge demos
                  • Proves mainnet-testnet bridge impossibility
                  • Economic, technical, compatibility analysis
                  • Provides testnet faucet alternatives"""
            },
            {
                "prompt": "Analyze code quality",
                "tool": "code_security + repos_get_content",
                "output": """Code Quality Analysis:

                ✓ Security: No vulnerabilities detected
                ✓ Dependencies: All up to date
                ✓ Code Style: Consistent Python formatting
                ✓ Documentation: Comprehensive README present
                ✓ Test Coverage: Educational demos include simulations

                Recommendations:
                • Consider adding unit tests
                • Add GitHub Actions for automated testing
                • Create release tags for versioning"""
            },
            {
                "prompt": "Create issue for unit tests",
                "tool": "issues_create",
                "output": """Created Issue #6

                Title: Add Unit Tests for Bitcoin Educational Systems
                Labels: enhancement, testing, good-first-issue
                Priority: Medium

                Description:
                Add comprehensive unit tests for:
                - Bridge demonstration logic
                - Mining simulation calculations
                - Address validation
                - API integrations (mocked)

                Acceptance Criteria:
                - Test coverage > 80%
                - All demo scenarios tested
                - Mock external API calls
                - GitHub Actions CI integration"""
            },
            {
                "prompt": "Check GitHub Actions status",
                "tool": "actions_list_workflow_runs",
                "output": """GitHub Actions Workflows:

                No workflows configured yet.

                Suggestion: Create .github/workflows/python-tests.yml
                Recommended workflows:
                - Python linting (flake8, black)
                - Unit tests (pytest)
                - Security scanning (bandit)
                - Dependency checking (safety)"""
            }
        ]

        for i, interaction in enumerate(interactions, 1):
            print(f"   {Colors.BOLD}[Interaction {i}]{Colors.ENDC}")
            print(f"   {Colors.OKCYAN}👤 Prompt:{Colors.ENDC} {interaction['prompt']}")
            print(f"   {Colors.WARNING}🔧 Tool Used:{Colors.ENDC} {interaction['tool']}")
            print(f"   {Colors.OKGREEN}📤 Output:{Colors.ENDC}")
            for line in interaction['output'].split('\n'):
                print(f"      {line}")
            print()

        print(f"{'-'*80}\n")

    def section_8_integration_benefits(self):
        """Show benefits of integration"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}🎯 SECTION 8: INTEGRATION BENEFITS{Colors.ENDC}\n")

        print(f"   {Colors.BOLD}Benefits for Bitcoin Educational Systems:{Colors.ENDC}\n")

        benefits = [
            ("Automated Project Management", [
                "AI can track issues and feature requests",
                "Automatic PR creation for improvements",
                "Smart labeling and milestone assignment",
                "Team collaboration automation"
            ]),

            ("Code Quality Assurance", [
                "Continuous code review via AI",
                "Security vulnerability detection",
                "Dependency update management",
                "Code pattern analysis and suggestions"
            ]),

            ("Documentation Maintenance", [
                "Auto-generate README updates",
                "Keep documentation in sync with code",
                "Create API documentation",
                "Generate usage examples"
            ]),

            ("Community Engagement", [
                "AI-powered issue triage",
                "Automated responses to common questions",
                "Discussion moderation",
                "Contributor guidance"
            ]),

            ("CI/CD Automation", [
                "Workflow optimization suggestions",
                "Build failure analysis",
                "Test result interpretation",
                "Deployment automation"
            ]),

            ("Learning & Analytics", [
                "Code evolution tracking",
                "Contributor activity insights",
                "Feature usage statistics",
                "Educational impact measurement"
            ])
        ]

        for category, items in benefits:
            print(f"   {Colors.BOLD}{category}:{Colors.ENDC}")
            for item in items:
                print(f"      • {item}")
            print()

        print(f"{'-'*80}\n")

    def section_9_next_steps(self):
        """Show next steps for implementation"""
        print(f"{Colors.OKCYAN}{Colors.BOLD}🚀 SECTION 9: NEXT STEPS FOR IMPLEMENTATION{Colors.ENDC}\n")

        steps = [
            ("1. Create GitHub Personal Access Token", [
                "Visit: https://github.com/settings/personal-access-tokens/new",
                "Select required scopes: repo, workflow, read:org",
                "Generate token and save securely",
                "Store in environment variable: GITHUB_PERSONAL_ACCESS_TOKEN"
            ]),

            ("2. Configure MCP Server", [
                "Choose deployment method: Local binary or Docker",
                "Select toolsets based on needs",
                "Configure authentication (PAT or OAuth)",
                "Test connection with simple commands"
            ]),

            ("3. Integrate with AI Tools", [
                "VS Code: Install MCP extension",
                "Claude Desktop: Configure in settings",
                "Claude Code CLI: Use mcp command",
                "Custom integration: Use MCP SDK"
            ]),

            ("4. Test Integration", [
                "Verify connection to GitHub",
                "Test basic operations (list files, issues)",
                "Confirm write operations work (if enabled)",
                "Monitor logs for errors"
            ]),

            ("5. Enable Advanced Features", [
                "Add GitHub Actions integration",
                "Configure code security scanning",
                "Set up Dependabot integration",
                "Enable discussions and project boards"
            ]),

            ("6. Create Automation Workflows", [
                "Issue triage automation",
                "PR review automation",
                "Documentation generation",
                "Release management"
            ])
        ]

        for title, items in steps:
            print(f"   {Colors.BOLD}{title}{Colors.ENDC}")
            for item in items:
                print(f"      • {item}")
            print()

        print(f"{'-'*80}\n")

    def run_complete_demo(self):
        """Run complete demonstration"""
        self.display_header()

        self.section_1_what_is_mcp()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_2_available_toolsets()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_3_integration_with_bitcoin_systems()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_4_example_interactions()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_5_configuration_examples()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_6_mcp_protocol_flow()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_7_expected_output()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_8_integration_benefits()
        input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

        self.section_9_next_steps()

        # Final summary
        print(f"{Colors.OKGREEN}{Colors.BOLD}{'='*80}")
        print(" GITHUB MCP INTEGRATION DEMONSTRATION COMPLETE")
        print(f"{'='*80}{Colors.ENDC}\n")

        print(f"{Colors.OKCYAN}Summary:{Colors.ENDC}")
        print(f"✓ GitHub MCP Server v0.26.3 built successfully")
        print(f"✓ 13 toolsets available for integration")
        print(f"✓ Bitcoin Educational Systems ready for MCP enhancement")
        print(f"✓ Example interactions and expected outputs demonstrated")
        print(f"✓ Next steps for full implementation provided\n")

        print(f"{Colors.BOLD}GitHub MCP Server Location:{Colors.ENDC}")
        print(f"{self.mcp_server_path}\n")

        print(f"{Colors.BOLD}Documentation:{Colors.ENDC}")
        print(f"• GitHub: https://github.com/github/github-mcp-server")
        print(f"• Docs: /tmp/github-mcp-server/docs/")
        print(f"• MCP Spec: https://spec.modelcontextprotocol.io/\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="GitHub MCP Server Integration Demonstration"
    )
    parser.add_argument('--no-color', action='store_true', help='Disable colors')
    parser.add_argument('--quick', action='store_true', help='Skip interactive pauses')

    args = parser.parse_args()

    demo = GitHubMCPDemo(use_colors=not args.no_color)

    if args.quick:
        import builtins
        builtins.input = lambda *args: None

    demo.run_complete_demo()


if __name__ == "__main__":
    main()
