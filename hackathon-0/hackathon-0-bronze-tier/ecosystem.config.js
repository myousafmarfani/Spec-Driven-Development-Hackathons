# PM2 Ecosystem Configuration
# Usage: pm2 start ecosystem.config.js

module.exports = {
  apps: [
    {
      name: 'orchestrator',
      script: 'python',
      args: 'src/orchestrator.py',
      cwd: __dirname,
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        DRY_RUN: 'true',
        ORCHESTRATOR_CHECK_INTERVAL: '30'
      }
    },
    {
      name: 'gmail_watcher',
      script: 'python',
      args: 'src/watchers/gmail_watcher.py',
      cwd: __dirname,
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      env: {
        DRY_RUN: 'true',
        GMAIL_POLL_INTERVAL: '60'
      }
    },
    {
      name: 'whatsapp_watcher',
      script: 'python',
      args: 'src/watchers/whatsapp_watcher.py',
      cwd: __dirname,
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        DRY_RUN: 'true',
        WHATSAPP_POLL_INTERVAL: '30'
      }
    },
    {
      name: 'file_watcher',
      script: 'python',
      args: 'src/watchers/file_watcher.py',
      cwd: __dirname,
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      env: {
        DRY_RUN: 'true'
      }
    },
    {
      name: 'watchdog',
      script: 'python',
      args: 'src/watchdog.py',
      cwd: __dirname,
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      env: {
        DRY_RUN: 'true',
        WATCHDOG_CHECK_INTERVAL: '30'
      }
    }
  ]
};
