# PC Doctor - AI-Powered PC Diagnostic Tool

An intelligent PC diagnostic tool that analyzes your system performance and provides AI-powered recommendations using Google Gemini.

## Features

- 📊 **Complete System Analysis**: CPU, RAM, Disk, Network, Processes
- 🤖 **AI-Powered Insights**: Uses Google Gemini to analyze and provide recommendations
- 🎯 **Actionable Suggestions**: Ranked recommendations by impact
- 📚 **Educational**: Helps you understand WHY your PC is slow
- 💾 **Data Export**: Saves raw diagnostic data and AI analysis

## What It Analyzes

1. **System Info**: OS, processor, architecture
2. **CPU Usage**: Current usage, frequency, per-core stats
3. **Memory**: RAM usage, available memory, swap usage
4. **Disk**: Partition usage, I/O counters, free space
5. **Processes**: Top CPU and memory consuming processes
6. **Network**: Data sent/received, packet stats
7. **Boot Time**: System uptime and boot time

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get a Gemini API key:
   - Go to https://aistudio.google.com/app/apikey
   - Create a new API key
   - Set it as an environment variable:
     - **Windows**: `set GEMINI_API_KEY=your_key_here`
     - **Linux/Mac**: `export GEMINI_API_KEY=your_key_here`

## Usage

Simply run:
```bash
python pc_doctor.py
```

The tool will:
1. Collect system diagnostic data (takes ~5-10 seconds)
2. Save raw data to `diagnostic_data.json`
3. Send data to Gemini AI for analysis
4. Display AI recommendations in terminal
5. Save analysis to `ai_analysis.txt`

## Output Files

- **diagnostic_data.json**: Raw system metrics in JSON format
- **ai_analysis.txt**: AI-generated analysis and recommendations

## Example Output

The AI provides:
- Overall health score (0-100)
- Critical issues causing slowdown
- Performance bottlenecks
- Ranked recommendations
- Educational insights about your PC

## Privacy Note

This tool:
- Collects only system metrics (CPU, RAM, processes)
- Does NOT collect personal files or browsing history
- Sends diagnostic data to Google Gemini API for analysis
- All data stays local except what's sent to Gemini

## Requirements

- Python 3.8+
- psutil library
- google-generativeai library
- Gemini API key

## Future Enhancements

- [ ] GUI interface
- [ ] Automated fixes (not just recommendations)
- [ ] Scheduled monitoring
- [ ] Historical performance tracking
- [ ] Local LLM option for privacy

## Contributing

Feel free to improve this tool! Ideas:
- Add temperature monitoring
- Startup programs analysis
- Malware detection
- Performance comparison over time

## License

Open source - use and modify as you like!
