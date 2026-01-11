import pandas as pd
import numpy as np

def calculate_portfolio_stats(data: list[dict]):
    """
    data format: [{"date": "2023-01-01", "value": 100}, ...]
    """
    if not data:
        return {"error": "No data"}
        
    df = pd.DataFrame(data)
    df['value'] = pd.to_numeric(df['value'])
    
    # Calculate daily returns
    df['returns'] = df['value'].pct_change()
    
    stats = {
        "mean_value": float(df['value'].mean()),
        "total_return": float((df['value'].iloc[-1] - df['value'].iloc[0]) / df['value'].iloc[0] * 100),
        "volatility": float(df['returns'].std() * np.sqrt(252)) if len(df) > 1 else 0, # Annualized volatility
        "sharpe_ratio": float(df['returns'].mean() / df['returns'].std() * np.sqrt(252)) if len(df) > 1 and df['returns'].std() != 0 else 0
    }
    
    return stats

