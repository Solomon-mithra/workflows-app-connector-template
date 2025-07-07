# Stacksync App Connector Template

![Stacksync](https://cdn.brandfetch.io/id9Bpy_H9O/theme/dark/logo.svg?c=1dxbfHSJFAPEGdCLU4o5B)

Welcome to the **Stacksync App Connector Template** – your starting point for building enterprise-grade workflow connectors that integrate seamlessly with the Stacksync platform.

## 🚀 What is a Stacksync Connector?

A Stacksync Connector is a microservice that enables workflows to interact with external systems, APIs, and data sources. This template provides the foundation to build robust, scalable connectors that can:

- **Authenticate** with third-party services (OAuth, API keys, custom auth)
- **Execute actions** (create, read, update, delete operations)
- **Fetch dynamic content** for form fields and user interfaces
- **Handle errors gracefully** with comprehensive logging and monitoring
- **Scale automatically** with containerized deployment

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** - [Download here](https://python.org/downloads/)
- **Docker & Docker Compose** - [Get Docker](https://docs.docker.com/get-docker/)
- **Git** - [Install Git](https://git-scm.com/downloads)
- **Code Editor** (VS Code, Cursor, etc.)

## 🏁 Quick Start

### 1. Clone and Setup

```bash
# Clone the template
git clone <repository-url> my-connector-name
cd my-connector-name

# Make scripts executable (Unix/Mac)
chmod +x run_dev.sh

# Or use the batch file (Windows)
# run_dev.bat
```

### 2. Configure Your Connector

Edit `app_config.yaml` to customize your connector:

```yaml
app_settings:
  app_type: "my_connector" # Unique identifier (lowercase, underscores only)
  app_name: "My Connector App" # Display name
  app_description: "Description" # Brief description
  app_icon_svg_url: "https://..." # SVG icon URL
```

### 3. Run Development Environment

```bash
# Unix/Mac
./run_dev.sh

# Windows
run_dev.bat

# Force rebuild (if needed)
./run_dev.sh --build
```

Your connector will be available at `http://localhost:2003`

### 4. Explore the Examples

The template includes two example modules to help you understand the patterns:

- **`src/modules/create_contacts/`** - Full-featured contact creation module
- **`src/modules/new_empty_action/`** - Minimal template for new actions

## 📚 Documentation

For detailed implementation guides, best practices, and advanced topics, refer to the documentation in the `/documentation` folder:

## 🏗️ Project Structure

```
├── src/modules/                    # Your connector modules
│   ├── create_contacts/           # Example: contact creation
│   └── new_empty_action/          # Template for new modules
├── config/                        # Docker and deployment configs
├── documentation/                 # Detailed guides and documentation
├── app_config.yaml               # Main configuration
├── requirements.txt              # Python dependencies
├── main.py                       # Application entry point
└── README.md                     # This file
```

## 🔧 Development Workflow

### Creating a New Module

1. **Copy the template**: Duplicate `src/modules/new_empty_action/`
2. **Rename appropriately**: Use descriptive names like `get_contacts`, `sync_data`
3. **Update configuration**: Edit `module_config.yaml` with module metadata
4. **Design the schema**: Define form fields in `schema.json`
5. **Implement logic**: Add your business logic in `route.py`
6. **Test thoroughly**: Use the built-in testing framework

### Module Components

Each module consists of three core files:

- **`route.py`** - Business logic and API handlers
- **`schema.json`** - Form definition and validation rules
- **`module_config.yaml`** - Module metadata and settings

### Environment Variables

Set these environment variables for your connector:

```bash
ENVIRONMENT=dev|stage|prod
REGION=usnv|besg|other
API_KEY=your-api-key
SENTRY_DSN=your-sentry-dsn
```

## 🛡️ Security Best Practices

- **Never commit secrets** - Use environment variables
- **Validate all inputs** - Use schema validation extensively
- **Handle errors gracefully** - Implement proper error responses
- **Log security events** - Do not log user data.
- **Use HTTPS only** - Enforce secure connections

## 📞 Support & Resources

- **Documentation**: [Stacksync Docs](https://docs.stacksync.com/)
- **Community**: [Join our Slack](https://docs.stacksync.com/start-here/community)

---

**Ready to build something amazing?** 🚀

Start by exploring the example modules, then dive into the documentation for detailed implementation guides. The Stacksync platform is designed to make connector development as smooth and powerful as possible.

_Happy coding!_ 👨‍💻👩‍💻
