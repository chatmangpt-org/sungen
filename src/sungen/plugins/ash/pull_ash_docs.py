import requests
from bs4 import BeautifulSoup


def main():
    """Main function"""
    from sungen.utils.dspy_tools import init_ol
    init_ol()

    # URL of the Ash documentation page
    url = "https://hexdocs.pm/ash/readme.html#how-to"

    # Fetch the content of the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the desired content, such as all 'a' tags (links)
        links = soup.find_all('a')

        # Print the links and their text
        for link in links:
            print(f"Text: {link.text}, URL: {link.get('href')}")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


if __name__ == '__main__':
    main()


"""---
contextdocs:
  - name: Ash Framework
    relationship: Core framework for building resources, data layers, and actions
    resources:
      - Official Documentation: https://hexdocs.pm/ash
      - Getting Started Guide: https://hexdocs.pm/ash/get-started.html
      - Ash Resource DSL Reference: https://hexdocs.pm/ash/dsl-ash-resource.html

  - name: AshPostgres
    relationship: Data layer for PostgreSQL, used for persistence and transactions
    resources:
      - Official Documentation: https://hexdocs.pm/ash_postgres
      - PostgreSQL Configuration Guide: https://www.postgresql.org/docs/

  - name: AshOban
    relationship: Background job processing for compliance checks, scheduled tasks, and job orchestration
    resources:
      - Official Documentation: https://hexdocs.pm/ash_oban
      - Oban Documentation: https://hexdocs.pm/oban/Oban.html

  - name: AshReactor
    relationship: Complex workflow orchestration for state machines and multi-step business processes
    resources:
      - Official Documentation: https://hexdocs.pm/ash/reactor.html
      - Reactor DSL Reference: https://hexdocs.pm/ash/dsl-ash-reactor.html
      - Reactor Usage Guide: https://hexdocs.pm/ash_reactor/getting-started.html

  - name: AshStateMachine
    relationship: Used to define state machines for ticket and financial transaction workflows
    resources:
      - Official Documentation: https://hexdocs.pm/ash_state_machine
      - State Machine Concepts: https://en.wikipedia.org/wiki/Finite-state_machine
      - AshStateMachine Cookbook: https://hexdocs.pm/ash_state_machine/cookbook.html

  - name: AshMoney
    relationship: Handles multi-currency operations and provides support for financial calculations
    resources:
      - Official Documentation: https://hexdocs.pm/ash_money
      - ex_money_sql: https://github.com/kipcole9/money_sql

  - name: AshDoubleEntry
    relationship: Implements double-entry accounting system for transaction management
    resources:
      - Official Documentation: https://hexdocs.pm/ash_double_entry
      - Double Entry Accounting Concepts: https://en.wikipedia.org/wiki/Double-entry_bookkeeping_system

  - name: AshPaperTrail
    relationship: Provides auditing and versioning for compliance with regulations like SOX
    resources:
      - Official Documentation: https://hexdocs.pm/ash_paper_trail
      - Paper Trail Concepts: https://en.wikipedia.org/wiki/Paper_trail

  - name: AshCloak
    relationship: Handles encryption and secure storage of sensitive data for compliance with data protection regulations (e.g., GDPR)
    resources:
      - Official Documentation: https://hexdocs.pm/ash_cloak
      - Data Encryption Best Practices: https://www.owasp.org/index.php/Guide_to_Cryptography

  - name: AshAdmin
    relationship: Provides an administrative interface for managing the helpdesk and financial modules
    resources:
      - Official Documentation: https://hexdocs.pm/ash_admin

  - name: AshAppsignal
    relationship: Integrates real-time monitoring and alerting to track system health and compliance events
    resources:
      - Official Documentation: https://hexdocs.pm/ash_appsignal
      - AppSignal Monitoring: https://docs.appsignal.com

  - name: Smokestack
    relationship: Test factories for generating data in tests, improving test coverage and quality
    resources:
      - Official Documentation: https://hexdocs.pm/smokestack
      - Factory Design Pattern: https://refactoring.guru/design-patterns/factory-method

  - name: SWIFT Payment System
    relationship: External integration for processing international financial transactions
    resources:
      - Official Documentation: https://www.swift.com
      - SWIFT Integration Guide: https://www.swift.com/our-solutions

  - name: Node.js
    relationship: Runtime environment for some ancillary tools or scripts, including JavaScript-based monitoring agents
    resources:
      - Official Documentation: https://nodejs.org/en/docs/
      - Best Practices Guide: https://github.com/goldbergyoni/nodebestpractices

  - name: OpenAPI Specification
    relationship: API design standard used for documenting the RESTful and GraphQL APIs
    resources:
      - Official Documentation: https://swagger.io/specification/
      - OpenAPI 3.0 Guide: https://swagger.io/docs/specification/about/
---

# Additional Documentation Notes

This `.contextdocs.md` file provides essential documentation resources for understanding and extending the Financial Ash Ecosystem project. The project leverages multiple Ash Framework extensions to handle various complex tasks such as state management, job scheduling, financial transactions, and compliance auditing. External resources listed here cover both the theoretical foundations and practical implementations of these capabilities.

Regularly review and update these references to ensure they remain accurate and relevant as the project evolves.

/Users/sac/Library/Caches/pypoetry/virtualenvs/stargen-pwn7Ka8j-py3.12/bin/python /Users/sac/dev/sungen/src/sungen/plugins/ash/pull_ash_docs.py 
Text: 

, URL: https://github.com/ash-project/ash
Text: 
ash
        , URL: https://github.com/ash-project/ash
Text: 

View Source
, URL: https://github.com/ash-project/ash/blob/v3.4.11/README.md#L1
Text: , URL: https://opensource.org/licenses/MIT
Text: , URL: https://hex.pm/packages/ash
Text: , URL: https://hexdocs.pm/ash
Text: hexdocs, URL: https://hexdocs.pm/ash
Text: 

, URL: #dive-in
Text: What is Ash?, URL: what-is-ash.html
Text: Get Started, URL: get-started.html
Text: See the roadmap, URL: https://github.com/orgs/ash-project/projects/3
Text: 

, URL: #about-the-documentation
Text: Tutorials, URL: #tutorials
Text: Topics, URL: #topics
Text: How-to, URL: #how-to
Text: Reference, URL: #reference
Text: 

, URL: #tutorials
Text: Get Started, URL: get-started.html
Text: 

, URL: #topics
Text: 

, URL: #about-ash
Text: What is Ash?, URL: what-is-ash.html
Text: Our Design Principles, URL: design-principles.html
Text: Contributing to Ash, URL: contributing-to-ash.html
Text: Alternatives, URL: alternatives.html
Text: 

, URL: #resources
Text: Domains, URL: domains.html
Text: Attributes, URL: attributes.html
Text: Relationships, URL: relationships.html
Text: Calculations, URL: calculations.html
Text: Aggregates, URL: aggregates.html
Text: Code Interfaces, URL: code-interfaces.html
Text: Identities, URL: identities.html
Text: Validations, URL: validations.html
Text: Changes, URL: changes.html
Text: Preparations, URL: preparations.html
Text: Embedded Resources, URL: embedded-resources.html
Text: Notifiers, URL: notifiers.html
Text: 

, URL: #actions
Text: Actions, URL: actions.html
Text: Read Actions, URL: read-actions.html
Text: Create Actions, URL: create-actions.html
Text: Update Actions, URL: update-actions.html
Text: Destroy Actions, URL: destroy-actions.html
Text: Generic Actions, URL: generic-actions.html
Text: Manual Actions, URL: manual-actions.html
Text: 

, URL: #security
Text: Actors & Authorization, URL: actors-and-authorization.html
Text: Sensitive Data, URL: sensitive-data.html
Text: Policies, URL: policies.html
Text: 

, URL: #development
Text: Project Structure, URL: project-structure.html
Text: Generators, URL: generators.html
Text: Testing, URL: testing.html
Text: Development Utilities, URL: development-utilities.html
Text: Upgrading to 3.0, URL: upgrading-to-3-0.html
Text: Error Handling, URL: error-handling.html
Text: 

, URL: #advanced
Text: Monitoring, URL: monitoring.html
Text: Multitenancy, URL: multitenancy.html
Text: Reactor, URL: reactor.html
Text: Timeouts, URL: timeouts.html
Text: Writing Extensions, URL: writing-extensions.html
Text: 

, URL: #how-to
Text: Test Resources, URL: test-resources.html
Text: Authorize Access to Resources, URL: authorize-access-to-resources.html
Text: Encrypt Attributes, URL: encrypt-attributes.html
Text: Prevent Concurrent Writes, URL: prevent-concurrent-writes.html
Text: Wrap External APIs, URL: wrap-external-apis.html
Text: 

, URL: #reference
Text: Glossary, URL: glossary.html
Text: Expressions, URL: expressions.html
Text: Ash.Resource DSL, URL: dsl-ash-resource.html
Text: Ash.Domain DSL, URL: dsl-ash-domain.html
Text: Ash.Reactor DSL, URL: dsl-ash-reactor.html
Text: Ash.Notifier.PubSub DSL, URL: dsl-ash-notifier-pubsub.html
Text: Ash.Policy.Authorizer DSL, URL: dsl-ash-policy-authorizer.html
Text: Ash.DataLayer.Ets DSL, URL: dsl-ash-datalayer-ets.html
Text: Ash.DataLayer.Mnesia DSL, URL: dsl-ash-datalayer-mnesia.html
Text: 

, URL: #packages
Text: 

, URL: #data-layers
Text: AshPostgres, URL: https://hexdocs.pm/ash_postgres
Text: AshSqlite, URL: https://hexdocs.pm/ash_sqlite
Text: AshCsv, URL: https://hexdocs.pm/ash_csv
Text: AshCubdb, URL: https://hexdocs.pm/ash_cubdb
Text: 

, URL: #api-extensions
Text: AshJsonApi, URL: https://hexdocs.pm/ash_json_api
Text: AshGraphql, URL: https://hexdocs.pm/ash_graphql
Text: 

, URL: #web
Text: AshPhoenix, URL: https://hexdocs.pm/ash_phoenix
Text: AshAuthentication, URL: https://hexdocs.pm/ash_authentication
Text: AshAuthenticationPhoenix, URL: https://hexdocs.pm/ash_authentication_phoenix
Text: 

, URL: #finance
Text: AshMoney, URL: https://hexdocs.pm/ash_money
Text: AshDoubleEntry, URL: https://hexdocs.pm/ash_double_entry
Text: 

, URL: #resource-utilities
Text: AshOban, URL: https://hexdocs.pm/ash_oban
Text: AshArchival, URL: https://hexdocs.pm/ash_archival
Text: AshStateMachine, URL: https://hexdocs.pm/ash_state_machine
Text: AshPaperTrail, URL: https://hexdocs.pm/ash_paper_trail
Text: AshCloak, URL: https://hexdocs.pm/ash_cloak
Text: 

, URL: #admin-monitoring
Text: AshAdmin, URL: https://hexdocs.pm/ash_admin
Text: AshAppsignal, URL: https://hexdocs.pm/ash_appsignal
Text: 

, URL: #testing
Text: Smokestack, URL: https://hexdocs.pm/smokestack
Text: 

          â Previous Page
        

API Reference
        
, URL: api-reference.html
Text: 

          Next Page â
        

Get Started
        
, URL: get-started.html
Text: Hex Package, URL: https://hex.pm/packages/ash/3.4.11
Text: Hex Preview, URL: https://preview.hex.pm/preview/ash/3.4.11
Text: current file, URL: https://preview.hex.pm/preview/ash/3.4.11/show/README.md
Text: 
              Download ePub version
            , URL: ash.epub
Text: ExDoc, URL: https://github.com/elixir-lang/ex_doc
Text: Elixir programming language, URL: https://elixir-lang.org

Process finished with exit code 0

"""