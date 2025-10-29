# 🔑 PyPI API Token Setup Guide

## Form Fields to Fill:

### 1. **Token name** (required)
```
ApiBridge Pro Upload
```
*(Or any name that helps you remember what it's for)*

### 2. **What will you use this token for?** (optional)
```
Uploading apibridge-pro package to PyPI
```

### 3. **Permissions**
✅ **Select: "Upload packages"**

### 4. **Scope** (required)
✅ **Select: "Entire account"**

   - This allows the token to work with all your projects
   - More flexible if you plan to publish other packages later
   - If you only want it for this one package, you can select the specific project, but "Entire account" is recommended

---

## After Creating Token:

1. **Copy the token immediately** - you won't see it again!
   - It will look like: `pypi-AgEIcH...` (long string)

2. **Save it securely** in:
   - Password manager (1Password, LastPass, etc.)
   - Or a secure note

3. **Use it to upload:**
   ```bash
   twine upload dist/*
   ```
   - Username: `__token__`
   - Password: `pypi-AgEIcH...` (your actual token)

---

## ⚠️ Security Note:

- Never share your token
- Never commit it to git
- Never paste it in public places
- Treat it like a password

