# 📤 Publishing ApiBridge Pro to PyPI

Complete guide to publish your package so users can `pip install apibridge-pro`.

---

## 🎯 Prerequisites

1. **Create PyPI accounts:**
   - **TestPyPI** (for testing): https://test.pypi.org/account/register/
   - **Real PyPI** (production): https://pypi.org/account/register/

2. **Install build tools:**
   ```bash
   pip install build twine
   ```

---

## 🚀 Step-by-Step Publishing Process

### Step 1: Update Version Number

Edit `pyproject.toml`:
```toml
[project]
name = "apibridge-pro"
version = "0.1.0"  # ← Update this for each release
```

Version format: `MAJOR.MINOR.PATCH` (e.g., 0.1.0, 0.1.1, 0.2.0, 1.0.0)

---

### Step 2: Build the Package

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates:
- `dist/apibridge-pro-0.1.0.tar.gz` (source distribution)
- `dist/apibridge_pro-0.1.0-py3-none-any.whl` (wheel)

---

### Step 3: Test on TestPyPI (IMPORTANT!)

**Always test on TestPyPI first!** This is a separate PyPI instance for testing.

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

You'll be prompted for:
- **Username:** Your TestPyPI username
- **Password:** Your TestPyPI password or API token

**Tip:** Use API tokens instead of passwords:
1. Go to https://test.pypi.org/manage/account/token/
2. Create a new API token
3. Use `__token__` as username and the token as password

---

### Step 4: Test Installation from TestPyPI

```bash
# Install from TestPyPI to verify it works
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ apibridge-pro
```

**Note:** The `--extra-index-url` ensures dependency resolution works (since TestPyPI won't have all dependencies).

Test it works:
```bash
# Verify installation
python -c "from apibridgepro import Gateway; print('✅ Installed successfully!')"

# Test CLI
apibridge --help
```

---

### Step 5: Publish to Real PyPI

Once testing is successful, publish to real PyPI:

```bash
# Upload to production PyPI
twine upload dist/*
```

You'll be prompted for:
- **Username:** Your PyPI username (or `__token__` for API token)
- **Password:** Your PyPI password or API token

**⚠️ Warning:** Once published to PyPI, you **cannot** delete or reuse the same version number!

---

### Step 6: Verify on PyPI

Visit: https://pypi.org/project/apibridge-pro/

Users can now install with:
```bash
pip install apibridge-pro
```

---

## 🔐 Using API Tokens (Recommended)

Instead of passwords, use API tokens for better security:

### For TestPyPI:
1. Go to: https://test.pypi.org/manage/account/token/
2. Create token with scope: "Entire account"
3. Copy the token (starts with `pypi-`)

### For Real PyPI:
1. Go to: https://pypi.org/manage/account/token/
2. Create token with scope: "Entire account"  
3. Copy the token (starts with `pypi-`)

### Usage:
```bash
# When prompted, use:
Username: __token__
Password: pypi-AgEIcHJ5... (your actual token)
```

---

## 📋 Quick Reference Commands

```bash
# 1. Update version in pyproject.toml

# 2. Build
python -m build

# 3. Test on TestPyPI
twine upload --repository testpypi dist/*

# 4. Test install
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ apibridge-pro

# 5. Publish to real PyPI
twine upload dist/*

# 6. Verify
pip install apibridge-pro
```

---

## 🎯 Publishing Checklist

Before publishing, make sure:

- [ ] Version number updated in `pyproject.toml`
- [ ] All tests passing
- [ ] CI checks green
- [ ] README is up to date
- [ ] License file exists
- [ ] No sensitive data in package
- [ ] `pyproject.toml` metadata is correct

---

## 🔄 Updating Versions

For updates after initial release:

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.1.1"  # Patch release (bug fixes)
   version = "0.2.0"  # Minor release (new features)
   version = "1.0.0"  # Major release (breaking changes)
   ```

2. Commit and tag:
   ```bash
   git add pyproject.toml
   git commit -m "chore: bump version to 0.1.1"
   git tag v0.1.1
   git push origin main --tags
   ```

3. Build and publish (same process)

---

## 🛠️ Troubleshooting

### "Repository 'pypi' is not registered"

Make sure `twine` is installed:
```bash
pip install --upgrade twine
```

### "HTTPError: 403 Forbidden"

- Check your username/password
- Ensure the package name is available (not taken)
- Wait a few minutes between uploads

### "File already exists"

You can't upload the same version twice. Either:
- Increment version number, or
- Wait 30 days, or
- Contact PyPI admins to delete the file

### "Package name already taken"

The name `apibridge-pro` might already be taken. Check: https://pypi.org/project/apibridge-pro/

If taken, update `name` in `pyproject.toml`:
```toml
name = "apibridge-pro-lukas"  # or another unique name
```

---

## 📊 Version Numbering Guide

- **0.1.0** → **0.1.1**: Bug fixes (patch)
- **0.1.1** → **0.2.0**: New features, backward compatible (minor)
- **0.2.0** → **1.0.0**: Breaking changes (major)

---

## 🎊 After Publishing

Once published, update your README:

```markdown
## Installation

```bash
pip install apibridge-pro
```
```

And announce it:
- Update GitHub repo description
- Add installation instructions to README
- Share on social media/communities

---

## 🔗 Useful Links

- **PyPI**: https://pypi.org/
- **TestPyPI**: https://test.pypi.org/
- **PyPI Account**: https://pypi.org/account/login/
- **API Tokens**: https://pypi.org/manage/account/token/
- **Package Page** (after publishing): https://pypi.org/project/apibridge-pro/

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Install tools
pip install build twine

# 2. Build
python -m build

# 3. Test publish
twine upload --repository testpypi dist/*

# 4. Test install
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ apibridge-pro

# 5. Real publish
twine upload dist/*

# Done! Users can now: pip install apibridge-pro
```

---

🎉 **That's it!** Once published, anyone in the world can install your package with a simple `pip install apibridge-pro`.

