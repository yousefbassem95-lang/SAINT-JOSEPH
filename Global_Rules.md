1. Planning & Project Structure
Global_Rule: Mapping_And_Planing
Create a Readme file, and a Project-map.jason file for the project your working on so you have blue print to what your doing.
Global_Rule: Documentation
Create as blueprints as plans for yourself:
Global_rules.md file
Constitution.yaml file
system_Constraints.md file
Readme.md file
Project-Map.jason file
requirements.txt file
So you can update them as you go and fallback to them when necessary.
provide the usage Commands and installation and requirements and trouble shooting steps commands as well at the end after project is complete 
ASK the user if they need amendments to be done before finalizing the project if yes do what is necessary according to the global rules 
when doing any amend of adding to the project as per user always go back to the testing steps 

2. Coding Standards & Engineering Principles
Global_Rule: Coding_Standers
Avoid logic duplication. If you find yourself copying and pasting code, refactor it into a reusable function, module, or component.
Prioritize simple, readable logic over "clever" or cryptic code.
Simple code is faster to debug and easier for others to maintain.
Follow these five principles for object-oriented design to ensure systems are robust and scalable:
Single Responsibility
Open/Closed
Liskov Substitution
Interface Segregation
Dependency Inversion
Each function or class should do exactly one thing well.
Avoid restating what the code does.
Use comments to explain the reasoning behind complex logic or why a specific approach was chosen.
Never trust user input.
Sanitize and validate all data to prevent SQL injection and XSS attacks.
Never hardcode credentials or secrets.
Use environment variables or secret management tools.
Only optimize after identifying bottlenecks through profiling.
Use efficient data structures (e.g., hash maps for fast lookups).
Peer reviews are essential for catching bugs early and sharing knowledge across the team.
user need to be able to run the activation command from the project main directory 

3. Preferred Technology Stack
Global_Rule: preferred_libraries
Act as a [Senior Developer/Architect] specializing in [Language/Domain].
Recommend a stack of preferred libraries for a project that [Objective].
The environment is [Web/Mobile/Desktop].
We prioritize [Performance/Speed of Development/Stability].
Exclude [Library A].
Only suggest libraries that are [Open Source/Maintained/Lightweight].

4. Command Line & Bash Usage
Global_Rule: Command line commands/common bash commands
Explain intent before commands.
No assumptions about OS or privileges.
Prefer reversible actions.
Prefer explicit over clever.
If assumptions are necessary, they must be declared explicitly.
Must generate solutions that do not require elevated privileges unless unavoidable.
Provide reversible steps when possible.
Generated scripts must produce predictable, repeatable results.
Avoid reliance on external state unless declared.
DON'T ALLOW:
Randomness
Implicit environment dependencies
Prioritize readability, explicit logic, and maintainability.
Generated build steps should be safe to re-run.

5. Testing Philosophy
Global_Rule: testing philosophy
You must write the minimum number of deterministic, behavior-focused tests that provide maximum confidence.
Prioritize fast feedback, contract validation, and refactor safety.
Tests must fail only when behavior changes.
Choose tests that are productive to the project your working on.
you need to make sure the project that your working on is working fine without any issues or bugs 
check and test while adding functions and building the project itself 
every major function or massive step test before and after 
check and test after your done building the project to provide the user a working product 

6. Human-in-the-Loop (HITL)
Global_Rule: HITL human in the loop
Ask me about anything your uncertain of.
Ask me 3–5 questions about my specific requirements or environment.

7. Evaluation & Reasoning
Global_Rule: rigorous evaluation
Always evaluate the code and workflow.
Global_Rule: Follow reasoning chain before providing final answer
Make steps for each decision/plan before action.

8. Security & Restrictions
Global_Rule: Security guidelines
id: GR-SEC-001
category: security
priority: critical
instruction:
Do not generate API keys, passwords, tokens, or secrets under any circumstances.
enforcement: absolute
Global_Rule: Restrictions
Make restrictions like don't remove the old skills if we made an amend.
Follow the restriction file all the time.
Maintain security.
Global_Rule: permissions setup
Make sure to ask me about security and important choices.
Don't guess.

9. Global_Rule: Versioning_And_Change_Control
All rule files, plans, maps, and constraints must be versioned.
Any amendment must preserve historical context; never overwrite without record.
Changes must be logged with intent, scope, and impact.
Backward compatibility must be maintained unless explicitly approved by the user.
Rule evolution must be deliberate, traceable, and reversible.

10. Global_Rule: Failure_Handling_And_Rollback
Every non-trivial change must have a rollback strategy.
Failure conditions must be identified before execution.
Systems must fail safely and predictably.
Partial execution must not leave the system in an undefined state.
When failure occurs, stop and ask the user before proceeding.

11. Global_Rule: Observability_And_Traceability
All critical workflows must be observable.
Log decisions, assumptions, and state transitions.
Logs must be structured, readable, and actionable.
Avoid noisy or redundant logging.
Observability must support debugging, audits, and post-mortem analysis.

12. Global_Rule: Data_Ownership_And_Retention
Explicitly define who owns each category of data.
Define retention, deletion, and archival rules before data creation.
Do not persist data without a clear purpose.
Minimize data collection to what is strictly necessary.
Data handling must align with security and privacy constraints.

13. Global_Rule: Scope_Control_And_Change_Boundaries
Clearly define project scope before implementation.
Do not expand scope implicitly.
Any scope change must be explicit and user-approved.
Distinguish between enhancements, refactors, and fixes.
When scope is ambiguous, stop and ask the user.

14. Global_Rule: Iron_Branding
always use the icon.txt file in the project to brand the project 
place the icon that will be provided on the top of the pages of the code 
place the icon that will be provided on the top of the interface for the user to see 
color the icon that will be provided with the color that the user will advise with
if the user didn't advise with the color ask him for the color.