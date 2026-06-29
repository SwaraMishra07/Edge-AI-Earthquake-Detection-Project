"""Dashboard web application using Dash or Flask."""

from flask import Flask, render_template, jsonify
import logging

logger = logging.getLogger(__name__)


def create_dashboard_app():
    """Create and configure the dashboard Flask application."""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    @app.route('/')
    def index():
        """Render the main dashboard page."""
        return render_template('index.html')
    
    @app.route('/api/metrics')
    def get_metrics():
        """Get current metrics for the dashboard."""
        return jsonify({
            'cpu_usage': 0,
            'memory_usage': 0,
            'active_alerts': 0,
            'last_detection': None
        })
    
    @app.route('/api/events')
    def get_events():
        """Get recent earthquake events."""
        return jsonify([])
    
    return app


if __name__ == '__main__':
    app = create_dashboard_app()
    app.run(debug=False, host='0.0.0.0', port=5000)
