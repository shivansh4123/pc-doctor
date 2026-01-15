from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import psutil
import platform
import json
from datetime import datetime
import time
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
genai.configure(api_key=GEMINI_API_KEY)

class PCDiagnostic:
    def __init__(self):
        self.data = {}
        
    def collect_system_info(self):
        """Collect basic system information"""
        self.data['system'] = {
            'os': platform.system(),
            'os_version': platform.version(),
            'processor': platform.processor(),
            'architecture': platform.machine(),
            'hostname': platform.node()
        }
        
    def collect_cpu_info(self):
        """Collect CPU usage and information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        
        self.data['cpu'] = {
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'current_usage_percent': cpu_percent,
            'current_frequency_mhz': cpu_freq.current if cpu_freq else 0,
            'max_frequency_mhz': cpu_freq.max if cpu_freq else 0,
            'per_core_usage': psutil.cpu_percent(interval=1, percpu=True)
        }
        
    def collect_memory_info(self):
        """Collect RAM information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        self.data['memory'] = {
            'total_gb': round(memory.total / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'usage_percent': memory.percent,
            'swap_total_gb': round(swap.total / (1024**3), 2),
            'swap_used_gb': round(swap.used / (1024**3), 2),
            'swap_percent': swap.percent
        }
        
    def collect_disk_info(self):
        """Collect disk information"""
        partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'usage_percent': usage.percent
                })
            except PermissionError:
                continue
                
        disk_io = psutil.disk_io_counters()
        
        self.data['disk'] = {
            'partitions': disk_info,
            'io_counters': {
                'read_mb': round(disk_io.read_bytes / (1024**2), 2),
                'write_mb': round(disk_io.write_bytes / (1024**2), 2),
                'read_count': disk_io.read_count,
                'write_count': disk_io.write_count
            } if disk_io else {}
        }
        
    def collect_process_info(self):
        """Collect top resource-consuming processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': proc.info['cpu_percent'],
                    'memory_percent': round(proc.info['memory_percent'], 2),
                    'status': proc.info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage and get top 10
        top_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:10]
        # Sort by memory usage and get top 10
        top_memory = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:10]
        
        self.data['processes'] = {
            'total_running': len(processes),
            'top_cpu_consumers': top_cpu,
            'top_memory_consumers': top_memory
        }
        
    def collect_network_info(self):
        """Collect network information"""
        net_io = psutil.net_io_counters()
        
        self.data['network'] = {
            'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
            'bytes_received_mb': round(net_io.bytes_recv / (1024**2), 2),
            'packets_sent': net_io.packets_sent,
            'packets_received': net_io.packets_recv
        }
        
    def collect_boot_info(self):
        """Collect boot time information"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime_seconds = time.time() - psutil.boot_time()
        
        self.data['boot'] = {
            'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            'uptime_hours': round(uptime_seconds / 3600, 2)
        }
        
    def collect_all_diagnostics(self):
        """Run all diagnostic collections"""
        self.collect_system_info()
        self.collect_cpu_info()
        self.collect_memory_info()
        self.collect_disk_info()
        self.collect_process_info()
        self.collect_network_info()
        self.collect_boot_info()
        
        return self.data
    
    def analyze_with_gemini(self):
        """Send diagnostic data to Gemini for structured analysis"""
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        prompt = f"""You are a PC performance expert. Analyze this system diagnostic data and provide a structured response.

System Diagnostic Data:
{json.dumps(self.data, indent=2)}

Respond with a JSON object in this EXACT format (no markdown, no extra text):
{{
  "health_score": 85,
  "health_status": "Good",
  "critical_issues": [
    {{"title": "Issue title", "description": "Brief description", "severity": "high/medium/low"}}
  ],
  "performance_bottlenecks": [
    {{"component": "RAM/CPU/Disk", "current_value": "10GB", "description": "Why this is a bottleneck"}}
  ],
  "recommendations": [
    {{
      "title": "Recommendation title",
      "description": "Detailed explanation",
      "impact": "High/Medium/Low",
      "steps": ["Step 1", "Step 2", "Step 3"]
    }}
  ],
  "quick_insights": {{
    "cpu_status": "Healthy - Low usage",
    "memory_status": "Moderate - Consider closing apps",
    "disk_status": "Good - Adequate free space",
    "overall_summary": "Your PC is performing well with minor optimization opportunities"
  }}
}}

Important:
- health_score: 0-100 (100 = perfect)
- health_status: "Excellent" (90-100), "Good" (70-89), "Fair" (50-69), "Poor" (0-49)
- critical_issues: Only serious problems causing significant slowdown
- Limit recommendations to top 5 most impactful
- Make descriptions concise and actionable
- RETURN ONLY VALID JSON, NO MARKDOWN FORMATTING"""

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        return json.loads(response_text)


@app.route('/')
def index():
    """Serve the dashboard"""
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan_system():
    """Run system diagnostic and return results"""
    try:
        diagnostic = PCDiagnostic()
        
        # Collect all diagnostic data
        diagnostic_data = diagnostic.collect_all_diagnostics()
        
        # Get AI analysis
        ai_analysis = diagnostic.analyze_with_gemini()
        
        # Combine results
        result = {
            'success': True,
            'diagnostic_data': diagnostic_data,
            'ai_analysis': ai_analysis,
            'scan_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/quick-stats', methods=['GET'])
def quick_stats():
    """Get quick system stats without full analysis"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            'success': True,
            'stats': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
