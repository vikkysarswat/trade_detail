# Contributing to Trade Detail

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/trade_detail.git
   cd trade_detail
   ```
3. **Set up development environment:**
   ```bash
   pnpm install
   python -m venv .venv
   source .venv/bin/activate
   pip install -r server/requirements.txt
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use prefixes:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### 2. Make Your Changes

#### Frontend Components

When adding new widgets:

1. Create directory in `src/your-widget/`
2. Add `main.tsx` entry point
3. Follow existing widget patterns
4. Use TypeScript and React hooks
5. Support both light and dark modes

#### Backend Changes

1. Follow Python type hints
2. Add error handling
3. Update API documentation
4. Test with different stock symbols

### 3. Test Your Changes

```bash
# Frontend build
pnpm run build

# Start servers
pnpm run serve  # Terminal 1
uvicorn server.main:app --reload  # Terminal 2

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/mcp
```

### 4. Format Code

```bash
# Frontend
pnpm run format

# Backend
black server/
isort server/
```

### 5. Commit Your Changes

Use conventional commits:

```bash
git commit -m "feat: add new stock comparison widget"
git commit -m "fix: resolve carousel navigation issue"
git commit -m "docs: update deployment guide"
```

Commit types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code refactoring
- `test` - Tests
- `chore` - Maintenance

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Screenshots for UI changes
- List of changes
- Testing notes

## Code Style Guidelines

### TypeScript/React

- Use functional components
- Use TypeScript for type safety
- Use hooks (useState, useEffect, etc.)
- Follow existing component patterns
- Keep components small and focused
- Use Tailwind CSS for styling

### Python

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Handle errors gracefully
- Use async/await for I/O operations

## Testing

### Manual Testing

1. Test all widgets in both light and dark modes
2. Test with different stock symbols
3. Test error cases (invalid symbols, network errors)
4. Test on mobile and desktop

### Integration Testing

1. Test MCP endpoints
2. Test with ChatGPT in developer mode
3. Test deployment on Render

## Documentation

When making changes:

1. Update README.md if needed
2. Update DEPLOYMENT.md for deployment changes
3. Add comments to complex code
4. Update API documentation

## Widget Development Guidelines

### Creating a New Widget

1. **Create widget directory:**
   ```
   src/my-widget/
   ├── MyWidget.tsx
   └── main.tsx
   ```

2. **Component structure:**
   ```tsx
   export function MyWidget({ data }: MyWidgetProps) {
     const displayMode = useDisplayMode();
     const isDark = displayMode === 'dark';
     
     return (
       <div className={isDark ? 'dark-styles' : 'light-styles'}>
         {/* Your widget content */}
       </div>
     );
   }
   ```

3. **Entry point (main.tsx):**
   ```tsx
   import React from 'react';
   import ReactDOM from 'react-dom/client';
   import { MyWidget } from './MyWidget';
   import '../index.css';
   
   const initialData = (window as any).__INITIAL_DATA__ || defaultData;
   
   const root = document.getElementById('root');
   if (root) {
     ReactDOM.createRoot(root).render(
       <React.StrictMode>
         <MyWidget data={initialData} />
       </React.StrictMode>
     );
   }
   ```

4. **Add MCP tool in `server/main.py`:**
   ```python
   {
       "name": "my_widget",
       "description": "Description of what it does",
       "inputSchema": {
           "type": "object",
           "properties": {
               "param": {"type": "string"},
           },
           "required": ["param"],
       },
   }
   ```

## Questions?

Feel free to:
- Open an issue for bugs or feature requests
- Start a discussion for questions
- Contact: vikky.sarswat@gmail.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.