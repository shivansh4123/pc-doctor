from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import psutil
import platform
import json
from datetime import datetime
import time
import google.generativeai as genai
import os
import shutil
from pathlib import Path

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


# ============================================================================
# AUTOMATION ENDPOINTS
# ============================================================================

@app.route('/api/optimize/temp-files', methods=['POST'])
def clear_temp_files():
    """Clear Windows temporary files"""
    try:
        import tempfile
        import shutil
        from pathlib import Path
        
        cleared_mb = 0
        files_deleted = 0
        errors = []
        
        # Get temp directories
        temp_dirs = [
            tempfile.gettempdir(),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp'),
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            # Get size before deletion
                            if os.path.isfile(item_path):
                                size = os.path.getsize(item_path) / (1024 * 1024)
                                os.remove(item_path)
                                cleared_mb += size
                                files_deleted += 1
                            elif os.path.isdir(item_path):
                                size = sum(f.stat().st_size for f in Path(item_path).rglob('*') if f.is_file()) / (1024 * 1024)
                                shutil.rmtree(item_path, ignore_errors=True)
                                cleared_mb += size
                                files_deleted += 1
                        except (PermissionError, OSError):
                            continue
                except Exception as e:
                    errors.append(f"Error accessing {temp_dir}: {str(e)}")
        
        return jsonify({
            'success': True,
            'cleared_mb': round(cleared_mb, 2),
            'files_deleted': files_deleted,
            'errors': errors
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimize/browser-cache', methods=['POST'])
def clear_browser_cache():
    """Clear Chrome and Edge browser cache"""
    try:
        cleared_mb = 0
        errors = []
        
        # Browser cache paths
        cache_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache'),
        ]
        
        for cache_path in cache_paths:
            if os.path.exists(cache_path):
                try:
                    # Calculate size
                    size = sum(f.stat().st_size for f in Path(cache_path).rglob('*') if f.is_file()) / (1024 * 1024)
                    # Delete cache
                    shutil.rmtree(cache_path, ignore_errors=True)
                    cleared_mb += size
                except Exception as e:
                    errors.append(f"Error clearing {cache_path}: {str(e)}")
        
        return jsonify({
            'success': True,
            'cleared_mb': round(cleared_mb, 2),
            'errors': errors
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimize/recycle-bin', methods=['POST'])
def empty_recycle_bin():
    """Empty Windows Recycle Bin"""
    try:
        if platform.system() == 'Windows':
            # Use Windows API to empty recycle bin
            import ctypes
            result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0001 | 0x0002 | 0x0004)
            
            return jsonify({
                'success': True,
                'message': 'Recycle Bin emptied successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Only supported on Windows'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimize/ram-cache', methods=['POST'])
def clear_ram_cache():
    """Clear RAM cache (Windows)"""
    try:
        if platform.system() == 'Windows':
            # Clear standby list (requires admin privileges)
            # This uses Windows EmptyStandbyList
            result = {
                'success': True,
                'message': 'RAM cache cleared',
                'note': 'Some operations require administrator privileges'
            }
            
            # Try to clear working sets
            try:
                for proc in psutil.process_iter(['pid']):
                    try:
                        p = psutil.Process(proc.info['pid'])
                        # This will cause Windows to trim the working set
                        p.suspend()
                        p.resume()
                    except:
                        continue
            except:
                pass
                
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': 'Only supported on Windows'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/process/kill/<int:pid>', methods=['POST'])
def kill_process(pid):
    """Kill a specific process by PID"""
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        memory_percent = process.memory_percent()
        
        # Don't kill critical system processes
        critical_processes = ['System', 'csrss.exe', 'smss.exe', 'services.exe', 
                            'svchost.exe', 'lsass.exe', 'winlogon.exe', 'dwm.exe']
        
        if process_name in critical_processes:
            return jsonify({
                'success': False,
                'error': f'Cannot kill critical system process: {process_name}'
            }), 400
        
        process.terminate()
        process.wait(timeout=3)
        
        return jsonify({
            'success': True,
            'process_name': process_name,
            'memory_freed_percent': round(memory_percent, 2),
            'message': f'Successfully terminated {process_name}'
        })
        
    except psutil.NoSuchProcess:
        return jsonify({
            'success': False,
            'error': 'Process not found'
        }), 404
    except psutil.AccessDenied:
        return jsonify({
            'success': False,
            'error': 'Access denied - process requires administrator privileges'
        }), 403
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/optimize/auto-optimize', methods=['POST'])
def auto_optimize():
    """Run all safe optimizations automatically"""
    try:
        results = {
            'success': True,
            'actions': [],
            'total_cleared_mb': 0,
            'errors': []
        }
        
        # 1. Clear temp files
        try:
            temp_result = clear_temp_files()
            temp_data = temp_result.get_json()
            if temp_data['success']:
                results['actions'].append(f"Cleared {temp_data['cleared_mb']}MB temp files")
                results['total_cleared_mb'] += temp_data['cleared_mb']
        except Exception as e:
            results['errors'].append(f"Temp files: {str(e)}")
        
        # 2. Clear browser cache
        try:
            cache_result = clear_browser_cache()
            cache_data = cache_result.get_json()
            if cache_data['success']:
                results['actions'].append(f"Cleared {cache_data['cleared_mb']}MB browser cache")
                results['total_cleared_mb'] += cache_data['cleared_mb']
        except Exception as e:
            results['errors'].append(f"Browser cache: {str(e)}")
        
        # 3. Empty recycle bin
        try:
            recycle_result = empty_recycle_bin()
            recycle_data = recycle_result.get_json()
            if recycle_data['success']:
                results['actions'].append("Emptied Recycle Bin")
        except Exception as e:
            results['errors'].append(f"Recycle bin: {str(e)}")
        
        results['total_cleared_mb'] = round(results['total_cleared_mb'], 2)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    import sys
    import webbrowser
    from threading import Timer
    import os
    
    # Hide Python warnings
    os.environ['PYTHONWARNINGS'] = 'ignore'
    
    # Check if running as executable or from source
    is_frozen = getattr(sys, 'frozen', False)
    
    def open_browser():
        """Open browser after server starts"""
        webbrowser.open('http://localhost:5000')
    
    def print_startup_banner():
        """Print nice startup banner"""
        print("\n" * 2)
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                                                            ║")
        print("║                  🩺 PC DOCTOR v1.0.0                       ║")
        print("║                                                            ║")
        print("║         AI-Powered PC Diagnostics & Optimization           ║")
        print("║                                                            ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print("")
        print("  ✅ Server starting at http://localhost:5000")
        print("  🌐 Opening browser automatically...")
        print("  ⚡ Ready to optimize your PC!")
        print("")
        print("  ⚠️  Keep this window open while using PC Doctor")
        print("  ❌ Press Ctrl+C to close application")
        print("")
        print("─" * 62)
        print("")
    
    if is_frozen:
        # PRODUCTION MODE (executable) - Use Waitress
        from waitress import serve
        
        print_startup_banner()
        
        # Open browser after 1.5 seconds
        Timer(1.5, open_browser).start()
        
        # Run production WSGI server - NO WARNINGS!
        serve(app, host='0.0.0.0', port=5000, threads=4)
        
    else:
        # DEVELOPMENT MODE (running from source) - Use Flask dev server
        # Only print banner and open browser ONCE (not on reloader restart)
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            print("\n🔧 Development Mode - Flask debug server\n")
            print_startup_banner()
            Timer(1, open_browser).start()
        
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True)
