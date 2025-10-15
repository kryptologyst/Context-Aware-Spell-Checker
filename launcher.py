#!/usr/bin/env python3
"""
Launcher script for Context-Aware Spell Checker
Provides easy access to all components of the application
"""

import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🚀 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n⏹️  {description} stopped by user")
        sys.exit(0)

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="Context-Aware Spell Checker Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py --demo                    # Run demonstration
  python launcher.py --web                     # Start FastAPI web app
  python launcher.py --streamlit               # Start Streamlit dashboard
  python launcher.py --test                    # Run tests
  python launcher.py --setup                   # Run setup
  python launcher.py --basic                   # Run basic spell checker
        """
    )
    
    parser.add_argument(
        "--demo", 
        action="store_true", 
        help="Run the complete demonstration"
    )
    
    parser.add_argument(
        "--web", 
        action="store_true", 
        help="Start the FastAPI web application"
    )
    
    parser.add_argument(
        "--streamlit", 
        action="store_true", 
        help="Start the Streamlit dashboard"
    )
    
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Run the test suite"
    )
    
    parser.add_argument(
        "--setup", 
        action="store_true", 
        help="Run the setup script"
    )
    
    parser.add_argument(
        "--basic", 
        action="store_true", 
        help="Run the basic spell checker"
    )
    
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Run all components (demo, web, streamlit)"
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        print("\n🎯 Quick Start Options:")
        print("  python launcher.py --demo      # See all features")
        print("  python launcher.py --web        # Start web app")
        print("  python launcher.py --streamlit  # Start dashboard")
        return
    
    # Run setup if requested
    if args.setup:
        run_command("python setup.py", "Running setup")
        return
    
    # Run tests if requested
    if args.test:
        run_command("python -m pytest test_spell_checker.py -v", "Running tests")
        return
    
    # Run basic spell checker if requested
    if args.basic:
        run_command("python spell_checker.py", "Running basic spell checker")
        return
    
    # Run demonstration if requested
    if args.demo:
        run_command("python demo.py", "Running demonstration")
        return
    
    # Start web applications
    if args.web:
        print("🌐 Starting FastAPI web application...")
        print("📱 Open your browser to: http://localhost:8000")
        print("⏹️  Press Ctrl+C to stop")
        run_command("python web_app.py", "Starting FastAPI web app")
        return
    
    if args.streamlit:
        print("📊 Starting Streamlit dashboard...")
        print("📱 Open your browser to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop")
        run_command("streamlit run streamlit_app.py", "Starting Streamlit dashboard")
        return
    
    # Run all components if requested
    if args.all:
        print("🎉 Running all components...")
        
        # Run demonstration
        run_command("python demo.py", "Running demonstration")
        
        # Start web app in background (this won't work perfectly, but shows the intent)
        print("\n🌐 Starting web applications...")
        print("📱 FastAPI: http://localhost:8000")
        print("📱 Streamlit: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop all services")
        
        try:
            # This is a simplified approach - in practice, you'd want to run these in separate processes
            print("Note: For production use, run web apps separately:")
            print("  Terminal 1: python web_app.py")
            print("  Terminal 2: streamlit run streamlit_app.py")
        except KeyboardInterrupt:
            print("\n⏹️  All services stopped")

if __name__ == "__main__":
    main()
