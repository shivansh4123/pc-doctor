# 🩺 PC Doctor - Complete Project Files

## 📦 Core Application Files

### **app.py** ⭐ MAIN FILE
- Flask backend server
- Gemini AI integration
- API endpoints for scanning
- System diagnostic collection
- **Start with this file!**

### **templates/index.html** ⭐ MAIN UI
- Beautiful web dashboard
- White translucent theme with purple gradient
- Responsive design
- Interactive charts and animations
- **This is what users see!**

### **requirements.txt**
- Python dependencies
- Flask, psutil, google-generativeai
- Install: `pip install -r requirements.txt`

## 🚀 Quick Start Scripts

### **start.bat** (Windows)
- One-click setup and launch
- Checks Python installation
- Installs dependencies
- Starts the server
- **Run this on Windows!**

### **start.sh** (Linux/Mac)
- One-click setup and launch
- Checks Python installation
- Installs dependencies
- Starts the server
- **Run this on Linux/Mac!**

## 📚 Documentation Files

### **QUICK_REFERENCE.md** ⭐ START HERE
- 30-second quick start
- Common commands
- Quick fixes
- Key features summary
- **Read this first!**

### **SETUP_GUIDE.md**
- Complete installation guide
- 5-minute setup walkthrough
- Configuration options
- Troubleshooting
- Security & privacy info
- **Detailed setup instructions**

### **README_DASHBOARD.md**
- Full feature documentation
- API endpoints reference
- Customization guide
- Browser compatibility
- Advanced features
- **Complete reference**

### **DASHBOARD_GUIDE.md**
- Visual design guide
- Layout breakdown
- Theme specifications
- Color schemes
- Typography details
- **Design reference**

## 🎯 How to Use This Project

### For First-Time Users:
1. Read **QUICK_REFERENCE.md** (2 minutes)
2. Get Gemini API key from https://aistudio.google.com/app/apikey
3. Run **start.bat** (Windows) or **start.sh** (Linux/Mac)
4. Open http://localhost:5000
5. Click "Scan My PC"

### For Developers:
1. Read **README_DASHBOARD.md** for API details
2. Check **DASHBOARD_GUIDE.md** for UI structure
3. Read **SETUP_GUIDE.md** for deployment options
4. Explore **app.py** for backend logic
5. Customize **templates/index.html** for UI changes

### For Troubleshooting:
1. Check **SETUP_GUIDE.md** → Troubleshooting section
2. Review **QUICK_REFERENCE.md** → Quick Fixes table
3. Verify API key is set correctly
4. Check terminal/console for error messages

## 📊 File Sizes & What They Do

| File | Size | Purpose | Priority |
|------|------|---------|----------|
| app.py | 9KB | Backend server | ⭐⭐⭐ |
| index.html | 24KB | Dashboard UI | ⭐⭐⭐ |
| requirements.txt | 87B | Dependencies | ⭐⭐⭐ |
| start.bat | 1.3KB | Windows launcher | ⭐⭐ |
| start.sh | 1.3KB | Linux/Mac launcher | ⭐⭐ |
| QUICK_REFERENCE.md | 3KB | Quick start | ⭐⭐⭐ |
| SETUP_GUIDE.md | 8KB | Full setup | ⭐⭐ |
| README_DASHBOARD.md | 5KB | Documentation | ⭐⭐ |
| DASHBOARD_GUIDE.md | 8KB | Design guide | ⭐ |

## 🔧 What Each File Contains

### app.py
```python
- PCDiagnostic class
  - collect_system_info()
  - collect_cpu_info()
  - collect_memory_info()
  - collect_disk_info()
  - collect_process_info()
  - collect_network_info()
  - collect_boot_info()
  - analyze_with_gemini()

- Flask routes
  - GET /              # Dashboard
  - POST /api/scan     # Full scan
  - GET /api/quick-stats  # Quick stats
```

### templates/index.html
```html
- Header section
- Scan button
- Health score display (animated circle)
- Quick stats grid (CPU, RAM, Disk, Processes)
- Quick insights cards
- Critical issues (if any)
- Performance bottlenecks
- AI recommendations (ranked)
- Top memory consumers list
- System information grid
- JavaScript for API calls and UI updates
```

## 🎨 Visual Design

```
┌─────────────────────────────────┐
│         Purple Gradient         │
│         Background              │
│                                 │
│  ┌───────────────────────────┐ │
│  │  🩺 PC Doctor            │ │
│  │  [ Scan My PC ]           │ │
│  └───────────────────────────┘ │
│                                 │
│  ┌─────────────────┐            │
│  │ Health Score: 78 │            │
│  │     ⭕ Good      │            │
│  └─────────────────┘            │
│                                 │
│  ┌────┬────┬────┬────┐         │
│  │CPU │RAM │Disk│Proc│         │
│  │5.6%│63% │65% │286 │         │
│  └────┴────┴────┴────┘         │
│                                 │
│  ┌──────────────────────┐      │
│  │ AI Recommendations   │      │
│  │ • Fix RAM usage      │      │
│  │ • Clean disk         │      │
│  └──────────────────────┘      │
└─────────────────────────────────┘
```

## 🔑 Configuration Quick Reference

### API Key (Choose one method)

**Method 1: Environment Variable** (Recommended)
```bash
# Windows
set GEMINI_API_KEY=your_key_here

# Linux/Mac
export GEMINI_API_KEY=your_key_here
```

**Method 2: Edit app.py**
```python
# Line 14
GEMINI_API_KEY = 'your_key_here'
```

### Change Port
```python
# app.py last line
app.run(port=5001)  # Change from 5000
```

### Customize Theme
```html
<!-- templates/index.html line 15-16 -->
<style>
body {
    background: linear-gradient(135deg, #YOUR_COLOR1, #YOUR_COLOR2);
}
</style>
```

## 📈 Typical Usage Flow

1. **User opens** http://localhost:5000
2. **Sees dashboard** with "Scan My PC" button
3. **Clicks scan** → Button animates
4. **Backend collects** system metrics (2-3 seconds)
5. **Gemini analyzes** data (2-4 seconds)
6. **Dashboard displays**:
   - Health score with animation
   - Quick stats with progress bars
   - AI insights and recommendations
   - Process list
   - System information
7. **User follows** recommendations
8. **Re-scans** to track improvement

## 🎯 Key Features Breakdown

### Health Score System
- **Calculation**: Based on CPU, RAM, Disk usage + AI analysis
- **Range**: 0-100
- **Categories**: 
  - 90-100: Excellent
  - 70-89: Good
  - 50-69: Fair
  - 0-49: Poor

### AI Recommendations
- **Powered by**: Google Gemini 2.0 Flash
- **Format**: JSON structured response
- **Ranked by**: Impact (High/Medium/Low)
- **Includes**: Step-by-step instructions

### System Monitoring
- **CPU**: Current usage, frequency, per-core stats
- **Memory**: Total, used, available, swap
- **Disk**: All partitions, I/O counters
- **Processes**: Top 10 CPU and memory consumers
- **Network**: Sent/received data, packets
- **Boot**: Boot time, uptime hours

## 🚀 Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Gemini API key obtained
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key configured (env var or app.py)
- [ ] Firewall allows port 5000
- [ ] Browser supports modern CSS/JS
- [ ] Internet connection for Gemini API

## 💡 Success Indicators

You'll know it's working when:
- ✅ Browser opens to beautiful purple gradient page
- ✅ "Scan My PC" button is visible and clickable
- ✅ Clicking scan shows loading animation
- ✅ Results appear after 5-10 seconds
- ✅ Health score displays with animated circle
- ✅ AI recommendations are specific and helpful
- ✅ Process list shows actual running programs

## 🆘 Common Issues

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Blank page | Files not in templates/ | Check folder structure |
| API error | Invalid key | Verify GEMINI_API_KEY |
| Module error | Missing deps | Run pip install |
| Port error | Port in use | Change port in app.py |
| Slow scan | Normal | 5-10 seconds is expected |
| No recommendations | JSON parse error | Check Gemini response |

## 🎉 You're All Set!

Everything you need is here:
- ⭐ Core app files (app.py + index.html)
- 🚀 Quick start scripts
- 📚 Complete documentation
- 🔧 Configuration guides
- 🐛 Troubleshooting help

**Next step**: Run `start.bat` (Windows) or `./start.sh` (Linux/Mac)

---

**Questions?** Check the documentation files above!
**Issues?** See the troubleshooting sections!
**Ready?** Let's diagnose some PCs! 🩺✨
