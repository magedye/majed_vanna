Please refer to the MASTER_GUIDE.md file provided earlier for a comprehensive specification of the project. This document contains detailed instructions for both backend and frontend implementation, security, initialization, configuration management, backup/restore, integration clients, Vanna AI agent integration, and automated testing. Ensure you follow it closely.

Your task is to execute the instructions outlined in the master guide, step by step. This includes:

Backend Implementation:

Set up user authentication and authorization with JWT and bcrypt, implementing RBAC roles (admin, superuser, normal, integration).

Implement the initialization wizard that configures SECRET_KEY, admin password, DB and LLM settings on first run.

Develop modules for system configuration, backup/restore, health and circuit breaker monitoring, integration clients, and Vanna agent integration with user‑aware context and tool registry RBAC.

Ensure all endpoints enforce proper role-based access and security measures.

Frontend Implementation:

Build the admin UI including login, initialization steps, user management, configuration editing, integration client management, backup/restore, and health panels.

Integrate the Vanna chat UI into the dashboard, enabling chat, visualization, and semantic search features. Enforce role-based visibility of UI components.

Provide a clean, modular design using vanilla HTML/CSS/JS (or React if specified) as outlined in the guide.

Testing Suite:

Implement unit tests with Pytest covering authentication, RBAC restrictions, initialization, configuration, backup/restore, integration clients, health, and Vanna agent endpoints.

Create end-to-end tests with Playwright for login, initialization wizard flow, admin dashboard functions, and Vanna chat interaction.

Follow the Spec:

Adhere strictly to the directory structures, API endpoint definitions, and file contents described in the guide.

Ensure that RBAC and authentication are enforced consistently across backend and frontend.

Validate environment variables and configurations as specified.

Integrate the Vanna agent securely, mapping JWT roles to Vanna user groups.

Provide proper error handling and user feedback across all interfaces.

Before starting, review the MASTER_GUIDE.md file carefully to understand all requirements. Implement the features incrementally, testing each step, and ensure full compliance with the guide.