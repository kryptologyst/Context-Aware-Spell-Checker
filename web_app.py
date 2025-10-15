"""
FastAPI Web Interface for Context-Aware Spell Checker
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import json
from pathlib import Path

from spell_checker import ContextAwareSpellChecker, SpellCheckResult

app = FastAPI(
    title="Context-Aware Spell Checker API",
    description="A modern spell checker that uses BERT and context analysis",
    version="1.0.0"
)

# Initialize spell checker
spell_checker = None

@app.on_event("startup")
async def startup_event():
    """Initialize the spell checker on startup"""
    global spell_checker
    try:
        spell_checker = ContextAwareSpellChecker()
        print("✅ Spell checker initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize spell checker: {e}")
        spell_checker = None

class SpellCheckRequest(BaseModel):
    text: str
    model_name: Optional[str] = "bert-base-uncased"

class SpellCheckResponse(BaseModel):
    original_text: str
    corrected_text: str
    confidence_score: float
    corrections_made: List[Dict[str, str]]
    text_statistics: Dict[str, Any]
    suggestions: List[Dict[str, Any]]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main web interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Context-Aware Spell Checker</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .main-content {
                padding: 40px;
            }
            
            .input-section {
                margin-bottom: 30px;
            }
            
            .input-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
            }
            
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 16px;
                resize: vertical;
                min-height: 120px;
                transition: border-color 0.3s;
            }
            
            textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .button-group {
                display: flex;
                gap: 15px;
                margin-top: 20px;
            }
            
            button {
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            .btn-secondary {
                background: #f8f9fa;
                color: #6c757d;
                border: 2px solid #e9ecef;
            }
            
            .btn-secondary:hover {
                background: #e9ecef;
            }
            
            .results-section {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                display: none;
            }
            
            .result-item {
                margin-bottom: 20px;
                padding: 15px;
                background: white;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .result-title {
                font-weight: 600;
                color: #333;
                margin-bottom: 8px;
            }
            
            .correction-item {
                display: inline-block;
                margin: 5px;
                padding: 8px 12px;
                background: #e3f2fd;
                border-radius: 6px;
                font-size: 14px;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e1e5e9;
            }
            
            .stat-value {
                font-size: 1.5em;
                font-weight: 600;
                color: #667eea;
            }
            
            .stat-label {
                color: #6c757d;
                font-size: 0.9em;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Context-Aware Spell Checker</h1>
                <p>Advanced spell checking powered by BERT and context analysis</p>
            </div>
            
            <div class="main-content">
                <div class="input-section">
                    <div class="input-group">
                        <label for="text-input">Enter text to check:</label>
                        <textarea id="text-input" placeholder="Type or paste your text here..."></textarea>
                    </div>
                    
                    <div class="button-group">
                        <button class="btn-primary" onclick="checkSpelling()">🔍 Check Spelling</button>
                        <button class="btn-secondary" onclick="clearText()">🗑️ Clear</button>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Analyzing text...</p>
                </div>
                
                <div class="error" id="error"></div>
                
                <div class="results-section" id="results">
                    <h3>📊 Results</h3>
                    <div id="results-content"></div>
                </div>
            </div>
        </div>
        
        <script>
            async function checkSpelling() {
                const text = document.getElementById('text-input').value.trim();
                if (!text) {
                    showError('Please enter some text to check.');
                    return;
                }
                
                showLoading(true);
                hideError();
                hideResults();
                
                try {
                    const response = await fetch('/api/spell-check', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: text })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Failed to check spelling');
                    }
                    
                    const result = await response.json();
                    displayResults(result);
                    
                } catch (error) {
                    showError('Error checking spelling: ' + error.message);
                } finally {
                    showLoading(false);
                }
            }
            
            function displayResults(result) {
                const resultsContent = document.getElementById('results-content');
                
                let html = `
                    <div class="result-item">
                        <div class="result-title">📝 Original Text:</div>
                        <p>${result.original_text}</p>
                    </div>
                    
                    <div class="result-item">
                        <div class="result-title">✅ Corrected Text:</div>
                        <p>${result.corrected_text}</p>
                    </div>
                    
                    <div class="result-item">
                        <div class="result-title">🎯 Confidence Score:</div>
                        <p>${(result.confidence_score * 100).toFixed(1)}%</p>
                    </div>
                `;
                
                if (result.corrections_made && result.corrections_made.length > 0) {
                    html += `
                        <div class="result-item">
                            <div class="result-title">🔧 Corrections Made:</div>
                            ${result.corrections_made.map(correction => 
                                `<span class="correction-item">${correction.original} → ${correction.corrected} (${correction.type})</span>`
                            ).join('')}
                        </div>
                    `;
                }
                
                if (result.text_statistics) {
                    html += `
                        <div class="result-item">
                            <div class="result-title">📈 Text Statistics:</div>
                            <div class="stats-grid">
                                <div class="stat-card">
                                    <div class="stat-value">${result.text_statistics.word_count}</div>
                                    <div class="stat-label">Words</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${result.text_statistics.sentence_count}</div>
                                    <div class="stat-label">Sentences</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${result.text_statistics.character_count}</div>
                                    <div class="stat-label">Characters</div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-value">${result.text_statistics.flesch_reading_ease.toFixed(1)}</div>
                                    <div class="stat-label">Readability</div>
                                </div>
                            </div>
                        </div>
                    `;
                }
                
                resultsContent.innerHTML = html;
                showResults();
            }
            
            function clearText() {
                document.getElementById('text-input').value = '';
                hideResults();
                hideError();
            }
            
            function showLoading(show) {
                document.getElementById('loading').style.display = show ? 'block' : 'none';
            }
            
            function showResults() {
                document.getElementById('results').style.display = 'block';
            }
            
            function hideResults() {
                document.getElementById('results').style.display = 'none';
            }
            
            function showError(message) {
                const errorDiv = document.getElementById('error');
                errorDiv.textContent = message;
                errorDiv.style.display = 'block';
            }
            
            function hideError() {
                document.getElementById('error').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/spell-check", response_model=SpellCheckResponse)
async def spell_check(request: SpellCheckRequest):
    """API endpoint for spell checking"""
    if not spell_checker:
        raise HTTPException(status_code=503, detail="Spell checker not initialized")
    
    try:
        result = spell_checker.correct_text(request.text)
        stats = spell_checker.get_text_statistics(request.text)
        
        return SpellCheckResponse(
            original_text=result.original_text,
            corrected_text=result.corrected_text,
            confidence_score=result.confidence_score,
            corrections_made=result.corrections_made,
            text_statistics=stats,
            suggestions=result.suggestions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "spell_checker_initialized": spell_checker is not None,
        "model_name": spell_checker.model_name if spell_checker else None
    }

@app.get("/api/models")
async def get_available_models():
    """Get available models"""
    return {
        "available_models": [
            "bert-base-uncased",
            "bert-base-cased",
            "distilbert-base-uncased",
            "roberta-base"
        ],
        "current_model": spell_checker.model_name if spell_checker else None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
