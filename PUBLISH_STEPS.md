# 🚀 Publishing ApiBridge Pro 0.1.1 to PyPI

## Step-by-Step Instructions

### Step 1: Get Your PyPI API Token

1. Go to: https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name (e.g., "ApiBridge Pro Upload")
4. Select scope: **"Entire account"**
5. Click "Add token"
6. **COPY THE TOKEN** (starts with `pypi-`) - you won't see it again!
7. Save it somewhere safe (password manager, etc.)

### Step 2: Test on TestPyPI First (Recommended)

1. Get TestPyPI token: https://test.pypi.org/manage/account/token/
2. Run this command:
   ```bash
   cd /path/to/ApiBridgePro
   twine upload --repository testpypi dist/*
   ```
3. When prompted:
   - **Username:** `__token__`
   - **Password:** `pypi-your-testpypi-token-here`
4. Wait for upload to complete ✅

### Step 3: Test Installation from TestPyPI

Verify it works:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ apibridge-pro
```

Test the import:
```bash
python3 -c "from apibridgepro import Gateway; print('✅ Success!')"
```

### Step 4: Publish to Real PyPI

Once TestPyPI works, publish to production:

1. Run:
   ```bash
   cd /path/to/ApiBridgePro
   twine upload dist/*
   ```
2. When prompted:
   - **Username:** `__token__`
   - **Password:** `pypi-your-pypi-token-here`
3. Wait for upload to complete ✅

### Step 5: Verify on PyPI

1. Visit: https://pypi.org/project/apibridge-pro/
2. Should see version 0.1.1
3. Test installation:
   ```bash
   pip install apibridge-pro
   python3 -c "from apibridgepro import Gateway, app; print('✅ Installed successfully!')"
   ```

## ⚠️ Important Notes

- You can **only upload each version once** to PyPI
- If upload fails, you may need to increment version number
- Keep your API tokens secure - never commit them to git
- The package files are already built in `dist/` folder

## 🎉 Done!

Users can now install with:
```bash
pip install apibridge-pro
```

And use it:
```python
from apibridgepro import Gateway, BudgetGuard, ConnectorPolicy
```

