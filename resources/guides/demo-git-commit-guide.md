# 📝 Commit Message Guidelines

revised: 06/19/2025

This project uses the **Conventional Commits** format to ensure clean, readable commit history and compatibility with changelog generators and CI tools.

## ✅ Format

<type>(optional-scope): short summary

- `type`: the kind of change being made (see below)
- `scope`: optional, describes the area of the code affected (e.g., `auth`, `api`, `ui`)
- `summary`: a concise, imperative description (e.g., `add login validation`, not `added` or `adds`)

---

## 📦 Commit Types

| Type       | Description                                                         |
| ---------- | ------------------------------------------------------------------- |
| `feat`     | A new feature                                                       |
| `fix`      | A bug fix                                                           |
| `docs`     | Documentation changes only                                          |
| `style`    | Code style updates (e.g., formatting, spacing, no logic changes)    |
| `refactor` | Code restructuring that doesn't change behavior (e.g., DRYing code) |
| `perf`     | Performance improvements                                            |
| `test`     | Adding or updating tests                                            |
| `chore`    | Miscellaneous tasks like dependency bumps, cleanup, config updates  |
| `build`    | Changes that affect the build system or external dependencies       |
| `pipe`     | Changes to CI/CD configuration or pipeline logic                    |
| `db`       | Changes to database structure or contents                           |
| `auth`     | Changes to API authorization                                        |
| `dev`      | Changes to an active development branch                             |
| `struct`   | Changes to the codebase structure                                   |


---

## 🔍 Examples

feat(auth): add login error handling
fix(ui): resolve mobile menu alignment issue
docs(readme): update setup instructions
style: format code with Black and isort
refactor(api): simplify response parsing logic
perf: reduce load time of dashboard
test(auth): add unit test for password reset
chore: bump version to 1.3.0
build: update Dockerfile for Node 18
pipe: fix GitHub Actions deploy step

---

## 🛠 Best Practices

- Limit the summary to **72 characters or fewer**
- Use **present tense** and **imperative mood** (e.g., “add”, not “added”)
- Capitalization: lowercase after the colon unless it's a proper noun
- Keep your commit history clean and focused—**one purpose per commit**

---
