# MAJED_VANNA - FRONTEND UI COMPONENTS
## Phase 3: Direct Implementation - Frontend Components
**Date:** December 5, 2025

---

## FILE 1: MAIN DASHBOARD TEMPLATE - `app/templates/dashboard.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Majed Vanna - AI Database Assistant</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #2D8FBE;
            --primary-dark: #1e5f8b;
            --warning: #f59e0b;
            --danger: #dc2626;
            --success: #10b981;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-400: #9ca3af;
            --gray-500: #6b7280;
            --gray-600: #4b5563;
            --gray-700: #374151;
            --gray-800: #1f2937;
            --gray-900: #111827;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--gray-50);
            color: var(--gray-900);
        }
        
        .app-container {
            display: grid;
            grid-template-columns: 280px 1fr;
            grid-template-rows: 60px 1fr;
            min-height: 100vh;
            gap: 0;
        }
        
        /* HEADER */
        .header {
            grid-column: 1 / 3;
            background: white;
            border-bottom: 1px solid var(--gray-200);
            display: flex;
            align-items: center;
            padding: 0 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
        }
        
        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo {
            font-weight: 700;
            font-size: 18px;
            color: var(--primary);
        }
        
        .header-right {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .health-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .health-badge.closed {
            background: #dcfce7;
            color: #166534;
        }
        
        .health-badge.half-open {
            background: #fed7aa;
            color: #92400e;
        }
        
        .health-badge.open {
            background: #fee2e2;
            color: #991b1b;
        }
        
        .user-menu {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
        }
        
        /* SIDEBAR */
        .sidebar {
            grid-row: 2;
            grid-column: 1;
            background: var(--gray-900);
            color: white;
            overflow-y: auto;
            border-right: 1px solid var(--gray-700);
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            cursor: pointer;
            border-left: 3px solid transparent;
            transition: all 0.2s;
            font-size: 14px;
        }
        
        .nav-item:hover {
            background: rgba(255,255,255,0.1);
        }
        
        .nav-item.active {
            background: var(--primary);
            border-left-color: #4ade80;
        }
        
        .nav-icon {
            font-size: 16px;
            min-width: 20px;
        }
        
        /* MAIN CONTENT */
        .main {
            grid-row: 2;
            grid-column: 2;
            overflow-y: auto;
            background: var(--gray-50);
        }
        
        .content-panel {
            display: none;
            padding: 20px;
            animation: fadeIn 0.3s ease-in;
        }
        
        .content-panel.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* ALERT BANNER */
        .alert-banner {
            background: #fee2e2;
            border-left: 4px solid var(--danger);
            padding: 12px 16px;
            margin-bottom: 16px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 12px;
            color: #991b1b;
            font-size: 14px;
        }
        
        .alert-banner.warning {
            background: #fed7aa;
            border-left-color: var(--warning);
            color: #92400e;
        }
        
        .alert-banner.success {
            background: #dcfce7;
            border-left-color: var(--success);
            color: #166534;
        }
        
        .alert-icon {
            font-size: 18px;
        }
        
        /* CARDS */
        .card {
            background: white;
            border-radius: 8px;
            border: 1px solid var(--gray-200);
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .card-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--gray-900);
        }
        
        /* STATS GRID */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 16px;
        }
        
        .stat-box {
            background: white;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid var(--gray-200);
        }
        
        .stat-label {
            font-size: 12px;
            color: var(--gray-500);
            text-transform: uppercase;
            font-weight: 600;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: var(--gray-900);
            margin-top: 8px;
        }
        
        .stat-change {
            font-size: 12px;
            color: var(--gray-500);
            margin-top: 6px;
        }
        
        .stat-change.up { color: var(--success); }
        .stat-change.down { color: var(--danger); }
        
        /* BUTTONS */
        .btn {
            padding: 8px 16px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: var(--primary);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--primary-dark);
        }
        
        .btn-secondary {
            background: var(--gray-200);
            color: var(--gray-900);
        }
        
        .btn-secondary:hover {
            background: var(--gray-300);
        }
        
        .btn-danger {
            background: var(--danger);
            color: white;
        }
        
        .btn-danger:hover {
            background: #b91c1c;
        }
        
        /* TABLES */
        .table-responsive {
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        
        thead {
            background: var(--gray-100);
            border-bottom: 2px solid var(--gray-200);
        }
        
        th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: var(--gray-700);
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid var(--gray-200);
        }
        
        tbody tr:hover {
            background: var(--gray-50);
        }
        
        /* TABS */
        .tabs {
            display: flex;
            border-bottom: 1px solid var(--gray-200);
            margin-bottom: 16px;
        }
        
        .tab-btn {
            padding: 12px 16px;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            color: var(--gray-500);
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
        }
        
        .tab-btn:hover {
            color: var(--gray-700);
        }
        
        .tab-btn.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }
        
        /* MEMORY PANEL */
        .memory-gauge {
            width: 200px;
            height: 200px;
            margin: 20px auto;
        }
        
        .memory-bar {
            width: 100%;
            height: 10px;
            background: var(--gray-200);
            border-radius: 5px;
            overflow: hidden;
            margin: 8px 0;
        }
        
        .memory-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--success), var(--warning));
            transition: width 0.3s;
        }
        
        /* SEMANTIC SEARCH */
        .search-input {
            width: 100%;
            padding: 10px 14px;
            border: 1px solid var(--gray-300);
            border-radius: 6px;
            font-size: 14px;
            margin-bottom: 12px;
        }
        
        .search-results {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .search-result-item {
            padding: 12px;
            border: 1px solid var(--gray-200);
            border-radius: 6px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .search-result-item:hover {
            background: var(--gray-50);
            border-color: var(--primary);
        }
        
        .result-type {
            display: inline-block;
            padding: 2px 6px;
            background: var(--gray-200);
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 8px;
            color: var(--gray-700);
        }
        
        .result-name {
            font-weight: 600;
            color: var(--gray-900);
            margin: 4px 0;
        }
        
        .result-desc {
            font-size: 13px;
            color: var(--gray-500);
        }
        
        .result-relevance {
            font-size: 12px;
            color: var(--gray-400);
            margin-top: 6px;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- HEADER -->
        <div class="header">
            <div class="header-content">
                <div class="header-left">
                    <div class="logo">
                        <i class="fas fa-database"></i> Majed Vanna
                    </div>
                </div>
                <div class="header-right">
                    <div class="health-badge" id="healthBadge">
                        <i class="fas fa-circle"></i>
                        <span>System Status: <span id="breaker-state">LOADING</span></span>
                    </div>
                    <div class="user-menu">
                        <i class="fas fa-user-circle"></i>
                        <span id="user-name">User</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- SIDEBAR -->
        <div class="sidebar">
            <div class="nav-item active" data-panel="chat">
                <div class="nav-icon"><i class="fas fa-comments"></i></div>
                <span>Chat</span>
            </div>
            <div class="nav-item" data-panel="health">
                <div class="nav-icon"><i class="fas fa-heartbeat"></i></div>
                <span>System Health</span>
            </div>
            <div class="nav-item" data-panel="memory">
                <div class="nav-icon"><i class="fas fa-brain"></i></div>
                <span>Memory Management</span>
            </div>
            <div class="nav-item" data-panel="tools">
                <div class="nav-icon"><i class="fas fa-toolbox"></i></div>
                <span>Tools Registry</span>
            </div>
            <div class="nav-item" data-panel="semantic">
                <div class="nav-icon"><i class="fas fa-book"></i></div>
                <span>Knowledge Base</span>
            </div>
            <div class="nav-item" data-panel="history">
                <div class="nav-icon"><i class="fas fa-history"></i></div>
                <span>History</span>
            </div>
            <div class="nav-item" data-panel="admin">
                <div class="nav-icon"><i class="fas fa-cog"></i></div>
                <span>Admin</span>
            </div>
        </div>
        
        <!-- MAIN CONTENT -->
        <div class="main">
            <!-- CHAT PANEL -->
            <div class="content-panel active" id="chat-panel">
                <div id="alert-container"></div>
                <div id="vanna-container" style="height: calc(100vh - 80px);">
                    <!-- Vanna Chat Component will be loaded here -->
                </div>
            </div>
            
            <!-- HEALTH PANEL -->
            <div class="content-panel" id="health-panel">
                <div id="health-alert"></div>
                <div class="card">
                    <div class="card-title">
                        <i class="fas fa-heartbeat"></i> System Health Status
                    </div>
                    <div class="stats-grid" id="health-stats">
                        <!-- Stats will be filled by JS -->
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title">Circuit Breaker Status</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <div class="stat-label">Current State</div>
                            <div class="stat-value" id="breaker-state-detail">--</div>
                            <div class="stat-change" id="breaker-message"></div>
                        </div>
                        <div>
                            <div class="stat-label">Breaker History</div>
                            <div style="margin-top: 8px;">
                                <div>Failures: <strong id="failure-count">0</strong></div>
                                <div>Successes: <strong id="success-count">0</strong></div>
                            </div>
                        </div>
                    </div>
                    <div style="margin-top: 16px;">
                        <button class="btn btn-primary" onclick="resetCircuitBreaker()">
                            <i class="fas fa-sync"></i> Attempt Reset
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- MEMORY PANEL -->
            <div class="content-panel" id="memory-panel">
                <div class="card">
                    <div class="card-title">
                        <i class="fas fa-brain"></i> Memory Management
                    </div>
                    
                    <div class="stats-grid" id="memory-stats">
                        <!-- Memory stats will be filled by JS -->
                    </div>
                    
                    <div class="card" style="margin-top: 20px; background: var(--gray-50);">
                        <div class="stat-label">Memory Usage</div>
                        <div class="memory-bar">
                            <div class="memory-bar-fill" id="memory-fill" style="width: 60%"></div>
                        </div>
                        <div style="font-size: 13px; color: var(--gray-600); margin-top: 8px;">
                            <span id="memory-used">6 GB</span> / <span id="memory-total">10 GB</span>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 20px;">
                        <button class="btn btn-primary" onclick="backupMemory()">
                            <i class="fas fa-download"></i> Backup
                        </button>
                        <button class="btn btn-secondary" onclick="showRestoreDialog()">
                            <i class="fas fa-upload"></i> Restore
                        </button>
                        <button class="btn btn-danger" onclick="cleanupMemory()">
                            <i class="fas fa-trash"></i> Cleanup
                        </button>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title">Recent Backups</div>
                    <div class="table-responsive">
                        <table id="backups-table">
                            <thead>
                                <tr>
                                    <th>Backup ID</th>
                                    <th>Date</th>
                                    <th>Size</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="backups-list">
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- TOOLS PANEL -->
            <div class="content-panel" id="tools-panel">
                <div class="card">
                    <div class="card-title">
                        <i class="fas fa-toolbox"></i> Available Tools
                    </div>
                    <div class="table-responsive">
                        <table id="tools-table">
                            <thead>
                                <tr>
                                    <th>Tool Name</th>
                                    <th>Category</th>
                                    <th>Status</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody id="tools-list">
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title">Tool Execution History</div>
                    <div class="table-responsive">
                        <table id="history-table">
                            <thead>
                                <tr>
                                    <th>Tool</th>
                                    <th>Time</th>
                                    <th>Duration</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="history-list">
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- SEMANTIC PANEL -->
            <div class="content-panel" id="semantic-panel">
                <div class="tabs">
                    <button class="tab-btn active" data-tab="docs-viewer">
                        <i class="fas fa-book"></i> Documentation
                    </button>
                    <button class="tab-btn" data-tab="semantic-search">
                        <i class="fas fa-search"></i> Semantic Search
                    </button>
                </div>
                
                <div id="docs-viewer-tab" class="tab-content active">
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div class="card-title" style="margin: 0;">Semantic Documentation</div>
                            <button class="btn btn-primary" onclick="rebuildSemanticDocs()">
                                <i class="fas fa-sync"></i> Rebuild Docs
                            </button>
                        </div>
                        <div id="docs-content" style="max-height: 600px; overflow-y: auto; border: 1px solid var(--gray-200); padding: 16px; border-radius: 6px; background: var(--gray-50);">
                            <!-- Docs will load here -->
                        </div>
                    </div>
                </div>
                
                <div id="semantic-search-tab" class="tab-content">
                    <div class="card">
                        <div class="card-title">Search Database Schema</div>
                        <input type="text" class="search-input" id="semantic-search-input" placeholder="Search tables, columns, relationships...">
                        <div class="search-results" id="semantic-results">
                            <!-- Results will appear here -->
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- HISTORY PANEL -->
            <div class="content-panel" id="history-panel">
                <div class="card">
                    <div class="card-title">
                        <i class="fas fa-history"></i> Conversation History
                    </div>
                    <div id="conversations-list" style="max-height: 500px; overflow-y: auto;">
                        <!-- Conversation history will load here -->
                    </div>
                </div>
            </div>
            
            <!-- ADMIN PANEL -->
            <div class="content-panel" id="admin-panel">
                <div class="card">
                    <div class="card-title">
                        <i class="fas fa-cog"></i> System Administration
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                        <div>
                            <div class="card-title" style="font-size: 14px;">Database Status</div>
                            <div id="db-status">
                                <div style="padding: 8px; background: var(--gray-50); border-radius: 4px; margin-bottom: 8px;">
                                    Oracle Connection: <strong id="db-connection">Unknown</strong>
                                </div>
                                <div style="padding: 8px; background: var(--gray-50); border-radius: 4px;">
                                    Last Check: <strong id="db-last-check">--</strong>
                                </div>
                            </div>
                        </div>
                        <div>
                            <div class="card-title" style="font-size: 14px;">System Metrics</div>
                            <div id="system-metrics">
                                <div style="padding: 8px; background: var(--gray-50); border-radius: 4px; margin-bottom: 8px;">
                                    Conversations: <strong id="conv-count">0</strong>
                                </div>
                                <div style="padding: 8px; background: var(--gray-50); border-radius: 4px;">
                                    Tools Available: <strong id="tools-count">0</strong>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-title">Maintenance Actions</div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
                        <button class="btn btn-secondary">
                            <i class="fas fa-broom"></i> Clear Cache
                        </button>
                        <button class="btn btn-secondary">
                            <i class="fas fa-refresh"></i> Rebuild Index
                        </button>
                        <button class="btn btn-secondary">
                            <i class="fas fa-download"></i> Export Logs
                        </button>
                        <button class="btn btn-danger">
                            <i class="fas fa-exclamation"></i> Emergency Reset
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Vanna Chat Component -->
    <script type="module">
        import { init } from 'https://cdn.jsdelivr.net/gh/vanna-ai/vanna@main/vanna/ux/cdn/assets/index.js';
        init({
            api_endpoint: '/api/vanna/v2/chat_sse',
            container: '#vanna-container'
        });
    </script>
    
    <script src="/static/js/dashboard.js"></script>
</body>
</html>
```

---

## FILE 2: DASHBOARD JAVASCRIPT - `app/static/js/dashboard.js`

```javascript
/**
 * Majed Vanna Dashboard Controller
 * Handles UI state, API calls, and user interactions
 */

// ============================================================================
// STATE MANAGEMENT
// ============================================================================

const state = {
    currentPanel: 'chat',
    healthStatus: null,
    memoryStats: null,
    toolsRegistry: null,
    semanticDocs: null,
    refreshInterval: null
};

// ============================================================================
// API CALLS
// ============================================================================

async function fetchSystemStatus() {
    try {
        const response = await fetch('/api/system/status');
        if (!response.ok) throw new Error('Failed to fetch system status');
        return await response.json();
    } catch (error) {
        console.error('Error fetching system status:', error);
        return null;
    }
}

async function fetchMemoryStats() {
    try {
        const response = await fetch('/api/memory/stats');
        if (!response.ok) throw new Error('Failed to fetch memory stats');
        return await response.json();
    } catch (error) {
        console.error('Error fetching memory stats:', error);
        return null;
    }
}

async function fetchToolsRegistry() {
    try {
        const response = await fetch('/api/tools/registry');
        if (!response.ok) throw new Error('Failed to fetch tools registry');
        return await response.json();
    } catch (error) {
        console.error('Error fetching tools registry:', error);
        return null;
    }
}

async function fetchToolHistory() {
    try {
        const response = await fetch('/api/tools/history?limit=10');
        if (!response.ok) throw new Error('Failed to fetch tool history');
        return await response.json();
    } catch (error) {
        console.error('Error fetching tool history:', error);
        return null;
    }
}

async function fetchSemanticDocs() {
    try {
        const response = await fetch('/api/semantic/docs');
        if (!response.ok) throw new Error('Failed to fetch semantic docs');
        return await response.json();
    } catch (error) {
        console.error('Error fetching semantic docs:', error);
        return null;
    }
}

async function fetchMemoryBackups() {
    try {
        const response = await fetch('/api/memory/backups');
        if (!response.ok) throw new Error('Failed to fetch backups');
        return await response.json();
    } catch (error) {
        console.error('Error fetching backups:', error);
        return null;
    }
}

async function searchSemantic(query) {
    try {
        const response = await fetch(`/api/semantic/search?query=${encodeURIComponent(query)}&limit=10`);
        if (!response.ok) throw new Error('Failed to search semantic');
        return await response.json();
    } catch (error) {
        console.error('Error searching semantic:', error);
        return [];
    }
}

// ============================================================================
// UI UPDATE FUNCTIONS
// ============================================================================

function updateHealthStatus(status) {
    if (!status) return;
    
    state.healthStatus = status;
    
    // Update header badge
    const badge = document.getElementById('healthBadge');
    const state_text = document.getElementById('breaker-state');
    state_text.textContent = status.breaker_state;
    
    badge.className = `health-badge ${status.breaker_state.toLowerCase()}`;
    
    // Update health panel
    const statsHtml = `
        <div class="stat-box">
            <div class="stat-label">Oracle Connection</div>
            <div class="stat-value">${status.oracle_connected ? '✓ Connected' : '✗ Disconnected'}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Circuit Breaker</div>
            <div class="stat-value">${status.breaker_state}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Response Time</div>
            <div class="stat-value">${status.response_time_ms.toFixed(0)}ms</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Error Rate</div>
            <div class="stat-value">${(status.error_rate * 100).toFixed(2)}%</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Memory Usage</div>
            <div class="stat-value">${status.memory_usage_percent.toFixed(1)}%</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Uptime</div>
            <div class="stat-value">${formatUptime(status.uptime_seconds)}</div>
        </div>
    `;
    
    const healthStatsEl = document.getElementById('health-stats');
    if (healthStatsEl) healthStatsEl.innerHTML = statsHtml;
    
    // Update breaker status detail
    document.getElementById('breaker-state-detail').textContent = status.breaker_state;
    
    // Update alert
    if (status.degraded_mode) {
        const alertHtml = `
            <div class="alert-banner warning">
                <div class="alert-icon"><i class="fas fa-exclamation-triangle"></i></div>
                <div>
                    <strong>System Running in Degraded Mode</strong><br>
                    ${status.features_unavailable.length > 0 ? 'Unavailable: ' + status.features_unavailable.join(', ') : 'Oracle connection issue detected'}
                </div>
            </div>
        `;
        document.getElementById('health-alert').innerHTML = alertHtml;
    }
}

function updateMemoryStats(stats) {
    if (!stats) return;
    
    state.memoryStats = stats;
    
    // Update memory panel stats
    const statsHtml = `
        <div class="stat-box">
            <div class="stat-label">Used Memory</div>
            <div class="stat-value">${stats.memory_used_mb.toFixed(1)} MB</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Total Memory</div>
            <div class="stat-value">${stats.memory_total_mb.toFixed(1)} MB</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Conversations</div>
            <div class="stat-value">${stats.conversation_count}</div>
        </div>
        <div class="stat-box">
            <div class="stat-label">Context Size</div>
            <div class="stat-value">${stats.context_size_kb.toFixed(1)} KB</div>
        </div>
    `;
    
    const memoryStatsEl = document.getElementById('memory-stats');
    if (memoryStatsEl) memoryStatsEl.innerHTML = statsHtml;
    
    // Update memory bar
    const fill = document.getElementById('memory-fill');
    if (fill) fill.style.width = stats.percent_used + '%';
    
    document.getElementById('memory-used').textContent = stats.memory_used_mb.toFixed(0) + ' MB';
    document.getElementById('memory-total').textContent = stats.memory_total_mb.toFixed(0) + ' MB';
}

function updateToolsRegistry(tools) {
    if (!tools || !Array.isArray(tools)) return;
    
    state.toolsRegistry = tools;
    
    const toolsListEl = document.getElementById('tools-list');
    if (!toolsListEl) return;
    
    const html = tools.map(tool => `
        <tr>
            <td><strong>${tool.name}</strong></td>
            <td>${tool.category}</td>
            <td>
                <span style="display: inline-block; padding: 2px 8px; border-radius: 3px; 
                            background: ${tool.status === 'active' ? '#dcfce7' : '#fed7aa'};
                            color: ${tool.status === 'active' ? '#166534' : '#92400e'};
                            font-size: 12px; font-weight: 600;">
                    ${tool.status}
                </span>
            </td>
            <td>${tool.description}</td>
        </tr>
    `).join('');
    
    toolsListEl.innerHTML = html;
    document.getElementById('tools-count').textContent = tools.length;
}

async function updateToolHistory() {
    const history = await fetchToolHistory();
    if (!history || !Array.isArray(history)) return;
    
    const historyListEl = document.getElementById('history-list');
    if (!historyListEl) return;
    
    const html = history.map(exec => `
        <tr>
            <td>${exec.tool_name}</td>
            <td>${new Date(exec.timestamp).toLocaleTimeString()}</td>
            <td>${exec.duration_ms.toFixed(0)}ms</td>
            <td>
                <span style="display: inline-block; padding: 2px 8px; border-radius: 3px;
                            background: ${exec.status === 'success' ? '#dcfce7' : '#fee2e2'};
                            color: ${exec.status === 'success' ? '#166534' : '#991b1b'};
                            font-size: 12px; font-weight: 600;">
                    ${exec.status}
                </span>
            </td>
        </tr>
    `).join('');
    
    historyListEl.innerHTML = html;
}

async function updateSemanticDocs() {
    const docs = await fetchSemanticDocs();
    if (!docs) return;
    
    state.semanticDocs = docs;
    
    const docsEl = document.getElementById('docs-content');
    if (docsEl) {
        docsEl.innerHTML = marked(docs.content) || docs.content;
    }
}

async function updateMemoryBackups() {
    const backups = await fetchMemoryBackups();
    if (!backups || !backups.backups) return;
    
    const backupsListEl = document.getElementById('backups-list');
    if (!backupsListEl) return;
    
    const html = backups.backups.map(backup => `
        <tr>
            <td>${backup.backup_id}</td>
            <td>${new Date(backup.timestamp).toLocaleString()}</td>
            <td>${(backup.size_bytes / 1024 / 1024).toFixed(2)} MB</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="restoreBackup('${backup.backup_id}')">
                    Restore
                </button>
            </td>
        </tr>
    `).join('');
    
    backupsListEl.innerHTML = html;
}

// ============================================================================
// ACTION HANDLERS
// ============================================================================

async function backupMemory() {
    try {
        const response = await fetch('/api/memory/backup', { method: 'POST' });
        const result = await response.json();
        
        showAlert('Backup created successfully!', 'success');
        updateMemoryBackups();
    } catch (error) {
        showAlert('Failed to create backup: ' + error.message, 'danger');
    }
}

async function cleanupMemory() {
    if (!confirm('Are you sure you want to clean up memory? This cannot be undone.')) return;
    
    try {
        const response = await fetch('/api/memory/cleanup', { method: 'POST' });
        const result = await response.json();
        
        showAlert(`Cleanup completed: ${(result.memory_freed_bytes / 1024 / 1024).toFixed(0)} MB freed`, 'success');
        updateMemoryStats(await fetchMemoryStats());
    } catch (error) {
        showAlert('Failed to cleanup memory: ' + error.message, 'danger');
    }
}

async function resetCircuitBreaker() {
    try {
        const response = await fetch('/api/system/breaker/reset', { method: 'POST' });
        const result = await response.json();
        
        showAlert('Circuit breaker reset attempted: ' + result.status, 'info');
        updateHealthStatus(await fetchSystemStatus());
    } catch (error) {
        showAlert('Failed to reset breaker: ' + error.message, 'danger');
    }
}

async function rebuildSemanticDocs() {
    try {
        const response = await fetch('/api/semantic/rebuild', { method: 'POST' });
        const result = await response.json();
        
        showAlert('Rebuilding semantic documentation...', 'info');
        setTimeout(updateSemanticDocs, 2000);
    } catch (error) {
        showAlert('Failed to rebuild docs: ' + error.message, 'danger');
    }
}

async function restoreBackup(backupId) {
    if (!confirm('Are you sure you want to restore this backup?')) return;
    
    try {
        const response = await fetch(`/api/memory/restore/${backupId}`, { method: 'POST' });
        const result = await response.json();
        
        showAlert('Restore initiated: ' + result.status, 'success');
    } catch (error) {
        showAlert('Failed to restore backup: ' + error.message, 'danger');
    }
}

function showRestoreDialog() {
    alert('Select a backup from the list below to restore');
}

// ============================================================================
// SEMANTIC SEARCH
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('semantic-search-input');
    if (searchInput) {
        searchInput.addEventListener('input', async (e) => {
            const query = e.target.value.trim();
            if (query.length < 2) {
                document.getElementById('semantic-results').innerHTML = '';
                return;
            }
            
            const results = await searchSemantic(query);
            const resultsEl = document.getElementById('semantic-results');
            
            const html = results.map(result => `
                <div class="search-result-item">
                    <div>
                        <span class="result-type">${result.type.toUpperCase()}</span>
                        <span class="result-name">${result.name}</span>
                    </div>
                    <div class="result-desc">${result.description}</div>
                    <div class="result-relevance">Relevance: ${(result.relevance_score * 100).toFixed(0)}%</div>
                </div>
            `).join('');
            
            resultsEl.innerHTML = html || '<div style="padding: 12px; color: #999;">No results found</div>';
        });
    }
});

// ============================================================================
// UI INTERACTIONS
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const panel = item.dataset.panel;
            switchPanel(panel);
        });
    });
    
    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            switchTab(tab);
        });
    });
    
    // Initial load
    refreshAllData();
    
    // Auto-refresh every 30 seconds
    state.refreshInterval = setInterval(refreshAllData, 30000);
});

function switchPanel(panelName) {
    // Hide all panels
    document.querySelectorAll('.content-panel').forEach(p => p.classList.remove('active'));
    
    // Hide all nav items active state
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    
    // Show selected panel
    document.getElementById(panelName + '-panel').classList.add('active');
    
    // Highlight nav item
    document.querySelector(`[data-panel="${panelName}"]`).classList.add('active');
    
    state.currentPanel = panelName;
}

function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    
    // Hide all tab buttons active state
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Highlight tab button
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

function showAlert(message, type = 'info') {
    const container = document.getElementById('alert-container');
    if (!container) return;
    
    const alertEl = document.createElement('div');
    alertEl.className = `alert-banner ${type}`;
    alertEl.innerHTML = `
        <div class="alert-icon">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'}"></i>
        </div>
        <div>${message}</div>
    `;
    
    container.innerHTML = '';
    container.appendChild(alertEl);
    
    setTimeout(() => alertEl.remove(), 5000);
}

async function refreshAllData() {
    const status = await fetchSystemStatus();
    const memory = await fetchMemoryStats();
    const tools = await fetchToolsRegistry();
    
    if (status) updateHealthStatus(status);
    if (memory) updateMemoryStats(memory);
    if (tools) updateToolsRegistry(tools);
    
    if (state.currentPanel === 'tools') {
        await updateToolHistory();
    }
    if (state.currentPanel === 'semantic') {
        await updateSemanticDocs();
    }
    if (state.currentPanel === 'memory') {
        await updateMemoryBackups();
    }
}

function formatUptime(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
}
```

---

## IMPLEMENTATION STEPS

### Backend:
1. Create `app/api/system_endpoints.py` - Circuit breaker + health endpoints
2. Create `app/api/semantic_endpoints.py` - Semantic layer endpoints
3. Create `app/api/memory_endpoints.py` - Memory management endpoints
4. Create `app/api/tools_endpoints.py` - Tools registry endpoints
5. Update `app/main.py` to include all routers
6. Test all endpoints via `/docs`

### Frontend:
1. Replace `app/templates/dashboard.html` with new template
2. Create `app/static/js/dashboard.js` with all interaction logic
3. Verify Vanna chat component loads properly
4. Test all navigation and data loading

### Testing:
1. Start FastAPI server
2. Navigate to `http://localhost:7777/`
3. Verify all tabs load correctly
4. Check circuit breaker status updates
5. Test memory management buttons
6. Verify semantic search works
7. Check tools registry populates