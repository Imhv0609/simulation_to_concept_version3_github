# GitHub Pages Setup Guide

## 🎯 Your Repository
**GitHub URL:** https://github.com/Imhv0609/simulation_to_concept_version3_github  
**GitHub Pages URL:** https://imhv0609.github.io/simulation_to_concept_version3_github/

---

## ✅ Step 1: Enable GitHub Pages

1. **Go to Settings:**
   ```
   https://github.com/Imhv0609/simulation_to_concept_version3_github/settings/pages
   ```

2. **Configure Source:**
   - **Source:** Deploy from a branch
   - **Branch:** `main` (or `master`)
   - **Folder:** `/ (root)`
   - Click **Save**

3. **Wait for Deployment:**
   - Takes 1-2 minutes
   - Green checkmark appears when ready
   - You'll see: "Your site is live at https://imhv0609.github.io/simulation_to_concept_version3_github/"

---

## 🔗 Your Simulation URLs

Once GitHub Pages is enabled, your simulations will be available at:

### **Simple Pendulum**
```
https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/simple_pendulum.html
```

### **Earth's Rotation & Revolution**
```
https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/rotAndRev.html
```

### **Light & Shadows**
```
https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/lightsShadows.html
```

---

## ⚙️ Configuration (Already Updated!)

### **.env file** (Updated)
```env
# Simulation Hosting (GitHub Pages)
GITHUB_PAGES_BASE_URL=https://imhv0609.github.io/simulation_to_concept_version3_github
```

### **config.py** (Updated)
The code now automatically:
- ✅ Uses GitHub Pages URLs when `GITHUB_PAGES_BASE_URL` is set
- ✅ Falls back to relative paths for local development
- ✅ Works seamlessly in both environments

---

## 🧪 Testing

### **1. Test GitHub Pages URLs (After enabling Pages)**

Open in browser:
```
https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/simple_pendulum.html?length=7&oscillations=20&autoStart=true
```

Should show pendulum simulation with length=7!

### **2. Test with Parameters**

**Earth's Rotation:**
```
https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/rotAndRev.html?rotationSpeed=70&axialTilt=23.5&revolutionSpeed=50
```

**Light & Shadows:**
```
https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/lightsShadows.html?lightDistance=2&objectType=Translucent&objectSize=8
```

---

## 🚀 Using in Your App

### **Automatic (Recommended)**

The system automatically uses the right URLs:

```python
# In your backend code
from config import build_simulation_url

# This will automatically use GitHub Pages URL if GITHUB_PAGES_BASE_URL is set
url = build_simulation_url({"length": 7, "number_of_oscillations": 20})
# Returns: https://imhv0609.github.io/.../simulations/simple_pendulum.html?length=7&oscillations=20&autoStart=true
```

### **Manual Override (if needed)**

```python
url = build_simulation_url(
    params={"length": 7},
    base_url="https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/simple_pendulum.html"
)
```

---

## 🔄 Switching Between Local and Production

### **Local Development** (no GITHUB_PAGES_BASE_URL)
```bash
# .env
# GITHUB_PAGES_BASE_URL not set or commented out

# Uses: simulations/simple_pendulum.html (relative path)
```

### **Production** (with GITHUB_PAGES_BASE_URL)
```bash
# .env
GITHUB_PAGES_BASE_URL=https://imhv0609.github.io/simulation_to_concept_version3_github

# Uses: https://imhv0609.github.io/.../simulations/simple_pendulum.html
```

---

## 📝 Update .gitignore (Recommended)

Make sure your `.env` file with API keys is NOT pushed to GitHub:

```bash
# Check .gitignore
cat .gitignore

# Should contain:
.env
__pycache__/
*.pyc
.DS_Store
```

---

## 🎯 Quick Commands

### **Enable GitHub Pages (Manual)**
Visit: https://github.com/Imhv0609/simulation_to_concept_version3_github/settings/pages

### **Check Deployment Status**
Visit: https://github.com/Imhv0609/simulation_to_concept_version3_github/deployments

### **Test Simulations**
Visit: https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/

### **Push Latest Changes**
```bash
git add .
git commit -m "Configure GitHub Pages URLs"
git push origin main
```

Wait 1-2 minutes for GitHub Pages to rebuild.

---

## ✅ Verification Checklist

- [ ] GitHub Pages enabled in repo settings
- [ ] `.env` has `GITHUB_PAGES_BASE_URL` set
- [ ] Test URL in browser: `https://imhv0609.github.io/simulation_to_concept_version3_github/simulations/simple_pendulum.html`
- [ ] Test with parameters: `...?length=7&oscillations=20&autoStart=true`
- [ ] All 3 simulations accessible
- [ ] `.env` file NOT committed to GitHub (check .gitignore)

---

## 🐛 Troubleshooting

### **404 Error on GitHub Pages**
- Wait 1-2 minutes after enabling Pages
- Check deployment status: https://github.com/Imhv0609/simulation_to_concept_version3_github/deployments
- Verify branch is `main` (not `master`)
- Try clearing browser cache

### **Simulations Not Loading**
- Check browser console for CORS errors
- Verify file paths are correct (case-sensitive!)
- Check GitHub Pages deployment succeeded

### **Parameters Not Working**
- Test URLs directly in browser first
- Verify JavaScript console shows "AUTO MODE" messages
- Check URL encoding (spaces should be %20)

---

## 🎉 You're Done!

Your simulations are now hosted on GitHub Pages and automatically used by the teaching agent when `GITHUB_PAGES_BASE_URL` is set! 🚀

**Next Steps:**
1. Enable GitHub Pages in repo settings
2. Wait for deployment (1-2 minutes)
3. Test URLs in browser
4. Run your Streamlit app - it will use hosted simulations!
