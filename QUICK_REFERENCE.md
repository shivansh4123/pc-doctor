# 🩺 PC Doctor - Quick Reference Card

## 🚀 Quick Start (30 Seconds)

### Windows:
```cmd
1. set GEMINI_API_KEY=your_key_here
2. start.bat
3. Open http://localhost:5000
```

### Linux/Mac:
```bash
1. export GEMINI_API_KEY=your_key_here
2. chmod +x start.sh && ./start.sh
3. Open http://localhost:5000
```

## 📁 Project Structure

```
pc-doctor/
├── app.py              # Backend (Flask + Gemini)
├── templates/
│   └── index.html      # Frontend (Dashboard)
├── requirements.txt    # Dependencies
├── start.bat          # Windows quick start
└── start.sh           # Linux/Mac quick start
```

## 🔑 Get API Key
https://aistudio.google.com/app/apikey (FREE)

## 📊 Dashboard URL
http://localhost:5000

## 🎨 Key Features

| Feature | What It Does |
|---------|--------------|
| 🎯 Health Score | Overall PC health (0-100) |
| 📈 Quick Stats | CPU, RAM, Disk, Processes |
| 💡 AI Insights | Instant health summary |
| ✨ Recommendations | Step-by-step fixes |
| 📊 Process Monitor | Top memory consumers |
| 💻 System Info | Hardware details |

## ⚡ API Endpoints

### POST /api/scan
Full diagnostic with AI analysis

### GET /api/quick-stats
Quick stats only (no AI)

## 🔧 Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Run on different port
python app.py  # then edit app.py port

# Install as service (advanced)
# Use systemd (Linux) or Task Scheduler (Windows)
```

## 🎨 Customize

### Change Colors
Edit `templates/index.html` line 15-16:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change Port
Edit `app.py` last line:
```python
app.run(port=5001)
```

### Adjust AI Prompt
Edit `app.py` line 130+

## 📊 Gemini Limits (Free Tier)
- **15 RPM** (requests per minute)
- **1,500 RPD** (requests per day)
- **1M TPD** (tokens per day)

≈ **500 scans/day** on free tier

## 🐛 Quick Fixes

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| API key error | Set GEMINI_API_KEY or edit app.py |
| Port in use | Change port in app.py |
| Dashboard blank | Check browser console (F12) |
| Slow scans | Normal = 5-10 sec, check internet |

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| SETUP_GUIDE.md | Complete setup instructions |
| README_DASHBOARD.md | Full documentation |
| DASHBOARD_GUIDE.md | Visual design reference |

## 🔒 Security Notes

### Development (Current)
- ✅ API key in backend (safe)
- ✅ No user data stored
- ✅ Local network only

### Production (If Sharing)
- ⚠️ Add rate limiting
- ⚠️ Monitor API usage
- ⚠️ Consider user's own keys

## 🎯 Performance Tips

1. **Close apps** before scanning
2. **Scan weekly** for best results
3. **Follow high-impact** recommendations first
4. **Track progress** over time

## 🌟 Next Features (Ideas)

- [ ] Historical tracking
- [ ] Export PDF reports
- [ ] Auto-scan scheduling
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] One-click optimizations

## 🆘 Support Resources

- **Gemini Docs**: https://ai.google.dev/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **Python Docs**: https://docs.python.org/

## 🎉 Ready to Go!

1. Set API key
2. Run start script
3. Open browser
4. Click "Scan My PC"
5. Get AI recommendations!

---

**Made with ❤️ for faster, healthier PCs**
