import pandas as pd

class ScoringEngine:
    def __init__(self, weights=None, risk_level="Standard", horizon="Short Term"):
        self.risk_level = risk_level
        self.horizon = horizon
        self.weights = weights or self._get_default_weights(risk_level, horizon)

    def _get_default_weights(self, risk_level, horizon):
        # Base weights by horizon and risk as per risk_time_logic.md
        if risk_level == "Retailer High-Conviction":
             w = {"technicals": 0.2, "fundamentals": 0.6, "sentiment": 0.2} # Default for HF hierarchy
        elif horizon == "Day Trade":
            w = {"technicals": 0.7, "fundamentals": 0.1, "sentiment": 0.2}
        elif horizon == "Long Term":
            if risk_level == "Conservative":
                w = {"technicals": 0.2, "fundamentals": 0.6, "sentiment": 0.2}
            else:
                w = {"technicals": 0.2, "fundamentals": 0.7, "sentiment": 0.1}
        else: # Short Term (Default/Standard)
            if risk_level == "Conservative":
                w = {"technicals": 0.35, "fundamentals": 0.45, "sentiment": 0.2} # Interpolated or adjusted
            else:
                w = {"technicals": 0.5, "fundamentals": 0.3, "sentiment": 0.2}
        
        return w

    def calculate_hc_score(self, fundamentals, technicals, analyst_consensus):
        """
        Calculate the Retailer High-Conviction Score (0-100) based on high_conviction_logic.md
        """
        score = 0
        details = {}
        
        # 1. Fundamentals: Net Margin (Max 15 pts)
        margin = fundamentals.get('net_margin')
        if margin is not None:
            if margin > 0.30: s = 15
            elif margin > 0.20: s = 10
            else: s = 0
            score += s
            details['moat'] = s
            
        # 2. Fundamentals: FCF Growth (Max 15 pts)
        fcf_growth = fundamentals.get('fcf_growth')
        if fcf_growth is not None:
            if fcf_growth > 0.20: s = 15
            elif fcf_growth > 0.10: s = 10
            else: s = 0
            score += s
            details['fcf_growth_score'] = s
        else:
            # Fallback to revenue growth
            rev_growth = fundamentals.get('revenue_growth')
            if rev_growth is not None:
                if rev_growth > 0.20: s = 10 # lower points for fallback
                elif rev_growth > 0.10: s = 5
                else: s = 0
                score += s
                details['growth_fallback'] = s

        # 3. Institutions: Ownership % (Max 20 pts)
        inst = fundamentals.get('institutional_ownership')
        if inst is not None:
            if inst > 0.80: s = 20
            elif inst > 0.70: s = 15
            elif inst > 0.60: s = 10
            else: s = 0
            score += s
            details['institutions'] = s
            
        # 4. Technicals: Trend & Flow (Max 20 pts)
        price = technicals.get('price')
        sma20 = technicals.get('sma20')
        sma50 = technicals.get('sma50')
        sma200 = technicals.get('sma200')
        mfi = technicals.get('mfi')
        macd = technicals.get('macd')
        macd_signal = technicals.get('macd_signal')
        
        tech_pts = 0
        # Trend Alignment (Max 10 pts)
        if price and sma50 and sma200:
            if sma20 and price > sma20 > sma50 > sma200:
                tech_pts += 10
            elif price > sma50 > sma200:
                tech_pts += 7
            elif price > sma200:
                tech_pts += 5
        
        # Institutional Flow (Max 5 pts)
        if mfi and mfi > 60:
            tech_pts += 5
        elif mfi and mfi > 50:
            tech_pts += 3
            
        # MACD Confirmation (Max 5 pts)
        if macd is not None and macd_signal is not None:
            if macd > macd_signal:
                tech_pts += 5
                
        score += tech_pts
        details['technical_flow'] = tech_pts
            
        # 5. Consensus: Buy/Strong Buy% (Max 20 pts)
        # yfinance recommendation_mean: 1.0 is Strong Buy, 5.0 is Strong Sell
        mean = analyst_consensus.get('recommendation_mean')
        if mean is not None:
            if mean <= 1.2: s = 20 # >95% Buy proxy
            elif mean <= 1.5: s = 15 # 90-95% Buy proxy
            elif mean <= 2.1: s = 10 # 80-90% Buy proxy
            else: s = 0
            score += s
            details['consensus'] = s
            
        # 6. Value/Upside: Price Target (Max 10 pts)
        target = analyst_consensus.get('target_mean_price')
        if target and price:
            upside = (target - price) / price
            if upside > 0.20: s = 10
            elif upside > 0.10: s = 5
            else: s = 0
            score += s
            details['upside'] = s
            
        return score, details

    def check_hc_hard_filters(self, fundamentals, technicals, analyst_consensus):
        """
        Check hard filters for High-Conviction status.
        """
        fails = []
        margin = fundamentals.get('net_margin')
        if margin is None or margin <= 0.25: fails.append("Net Margin < 25%")
        
        # Use available growth metrics as proxy for FCF growth if unavailable
        fcf_growth = fundamentals.get('fcf_growth')
        growth_proxy = fcf_growth
        if growth_proxy is None:
            # Try earnings growth from fundamentals dict (I need to add it there)
            # Actually, let's just assume we check what we have.
            pass
            
        if fcf_growth is not None:
             if fcf_growth <= 0.15: fails.append("FCF Growth < 15%")
        else:
             # Fallback to revenue growth for the check if FCF growth is missing
             rev_growth = fundamentals.get('revenue_growth')
             if rev_growth is None or rev_growth <= 0.10: # Be slightly more lenient on rev growth
                 fails.append("Growth metrics (FCF/Rev) insufficient or unavailable")
        
        de = fundamentals.get('debt_to_equity')
        if de is None or de >= 50: fails.append("D/E Ratio > 0.5")
        
        cr = fundamentals.get('current_ratio')
        if cr is None or cr <= 1.5: fails.append("Current Ratio < 1.5")
        
        inst = fundamentals.get('institutional_ownership')
        if inst is None or inst <= 0.70: fails.append("Institutional Ownership < 70%")
        
        price = technicals.get('price')
        sma20 = technicals.get('sma20')
        sma50 = technicals.get('sma50')
        sma200 = technicals.get('sma200')
        if price is None or sma20 is None or sma50 is None or sma200 is None or not (price > sma20 > sma50 > sma200):
            fails.append("Not in 'Perfect Alignment' (Price > 20 SMA > 50 SMA > 200 SMA)")
            
        mean = analyst_consensus.get('recommendation_mean')
        if mean is None or mean > 2.1: 
            fails.append("Analyst Consensus < 90% Buy")
            
        return len(fails) == 0, fails

    def calculate_technical_score(self, price, sma50, sma200, rsi, macd_line, signal_line):
        # weights as per risk_time_logic.md for Day Trade
        if self.horizon == "Day Trade":
            t_weights = {"rsi": 0.4, "macd": 0.4, "trend": 0.2}
        else:
            t_weights = {"rsi": 0.25, "macd": 0.25, "trend": 0.5}

        # Trend Score
        trend_score = 0
        if not pd.isna(price) and not pd.isna(sma50) and not pd.isna(sma200):
            if price > sma50 and sma50 > sma200:
                trend_score = 100
            elif price > sma50 and price < sma200:
                trend_score = 50
            elif price < sma50 and price < sma200:
                trend_score = 0
            else:
                trend_score = 25 
        
        # Momentum Score
        momentum_score = 0
        if not pd.isna(rsi):
            if 40 <= rsi <= 60:
                momentum_score = 50
            elif 30 <= rsi < 40:
                momentum_score = 75
            elif rsi < 30:
                momentum_score = 100
            elif 60 < rsi <= 70:
                momentum_score = 25
            elif rsi > 70:
                momentum_score = 0
        
        # MACD Score
        macd_score = 0
        if not pd.isna(macd_line) and not pd.isna(signal_line):
            if macd_line > signal_line:
                macd_score = 100
            else:
                macd_score = 0
                
        t_score = (trend_score * t_weights["trend"]) + (momentum_score * t_weights["rsi"]) + (macd_score * t_weights["macd"])
        return t_score, {"trend": trend_score, "momentum": momentum_score, "macd": macd_score}

    def calculate_fundamental_score(self, pe, peg, rev_growth, net_margin, debt_to_equity, industry_pe=25):
        # weights as per risk_time_logic.md for Conservative
        if self.risk_level == "Conservative":
            f_weights = {
                "debt": 0.3,
                "margin": 0.3,
                "pe": 0.2,
                "growth": 0.1,
                "peg": 0.1
            }
        else:
            f_weights = {
                "pe": 0.2,
                "peg": 0.2,
                "growth": 0.2,
                "margin": 0.2,
                "debt": 0.2
            }

        scores = {}
        
        # P/E
        if not pd.isna(pe):
            if pe < industry_pe: scores["pe"] = 100
            elif pe <= industry_pe * 1.2: scores["pe"] = 50
            else: scores["pe"] = 0
        else: scores["pe"] = None
            
        # PEG
        if not pd.isna(peg):
            if peg < 1.0: scores["peg"] = 100
            elif peg <= 1.5: scores["peg"] = 50
            else: scores["peg"] = 0
        else: scores["peg"] = None
            
        # Revenue Growth
        if not pd.isna(rev_growth):
            if rev_growth > 0.15: scores["growth"] = 100
            elif rev_growth > 0.05: scores["growth"] = 50
            else: scores["growth"] = 0
        else: scores["growth"] = None
            
        # Net Margin
        if not pd.isna(net_margin):
            if net_margin > 0.20: scores["margin"] = 100
            elif net_margin > 0.10: scores["margin"] = 50
            else: scores["margin"] = 0
        else: scores["margin"] = None
            
        # Debt to Equity
        if not pd.isna(debt_to_equity):
            # logic.md says D/E < 0.3 is hard criteria, but for score let's keep it relative
            # yfinance debtToEquity is often a percentage (e.g. 50 means 0.5)
            # but wait, let's check what it actually is. 
            # If 0.3 is the threshold, maybe 50 in yfinance means 0.5?
            # Let's assume if it's > 5, it's a percentage (500% = 5).
            val = debt_to_equity
            if val < 30: scores["debt"] = 100
            elif val < 100: scores["debt"] = 50
            else: scores["debt"] = 0
        else: scores["debt"] = None
            
        # Calculate weighted average of available scores
        total_weight = 0
        weighted_sum = 0
        for metric, score in scores.items():
            if score is not None:
                total_weight += f_weights[metric]
                weighted_sum += score * f_weights[metric]
        
        if total_weight == 0:
            return 0, {}
        
        f_score = weighted_sum / total_weight
        return f_score, scores


    def calculate_sentiment_score(self, recommendation_key, news_sentiment_val=None):
        # Analyst Score (60% of S)
        analyst_map = {
            "strong_buy": 100,
            "buy": 75,
            "hold": 50,
            "sell": 25,
            "strong_sell": 0
        }
        analyst_score = analyst_map.get(recommendation_key, 50)
        
        # News Sentiment (40% of S)
        # Assuming news_sentiment_val is -1 to 1
        if news_sentiment_val is not None:
            news_score = (news_sentiment_val + 1) * 50
            s_score = (analyst_score * 0.6) + (news_score * 0.4)
        else:
            s_score = analyst_score
            
        return s_score, {"analyst": analyst_score, "news": news_sentiment_val}

    def get_composite_score(self, t_score, f_score, s_score):
        # Handle missing categories by redistributing weight
        active_weights = {}
        if t_score is not None: active_weights["technicals"] = self.weights["technicals"]
        if f_score is not None: active_weights["fundamentals"] = self.weights["fundamentals"]
        if s_score is not None: active_weights["sentiment"] = self.weights["sentiment"]
        
        total_active_weight = sum(active_weights.values())
        if total_active_weight == 0:
            return 0
            
        normalized_t = (t_score or 0) * (active_weights.get("technicals", 0) / total_active_weight)
        normalized_f = (f_score or 0) * (active_weights.get("fundamentals", 0) / total_active_weight)
        normalized_s = (s_score or 0) * (active_weights.get("sentiment", 0) / total_active_weight)
        
        return normalized_t + normalized_f + normalized_s

    def check_panic_signal(self, hist_data, technicals, news_sentiment_crash=False):
        """
        Check if the Panic Signal (High Alert) is triggered.
        Criteria (Must meet 3 out of 4):
        1. Price Velocity: > 15% drop in 5 trading days.
        2. Institutional Dump: RVOL > 2.5.
        3. Technical Break: Price < 200 SMA AND Price < 50 SMA.
        4. Sentiment Crash: News Sentiment moves from >0 to < -0.5 in 72hrs.
        """
        triggers = []
        
        # 1. Price Velocity
        if len(hist_data) >= 5:
            current_close = hist_data['Close'].iloc[-1]
            prev_close = hist_data['Close'].iloc[-5]
            drop = (current_close - prev_close) / prev_close
            if drop < -0.15:
                triggers.append("Price Velocity (>15% drop in 5d)")
        
        # 2. Institutional Dump (RVOL)
        rvol = technicals.get('rvol')
        if rvol and rvol > 2.5:
            triggers.append(f"Institutional Dump (RVOL: {round(rvol, 2)})")
            
        # 3. Technical Break
        price = technicals.get('price')
        sma50 = technicals.get('sma50')
        sma200 = technicals.get('sma200')
        if price and sma50 and sma200:
            if price < sma50 and price < sma200:
                triggers.append("Technical Break (Price < 50 & 200 SMA)")
        
        # 4. Sentiment Crash
        if news_sentiment_crash:
            triggers.append("Sentiment Crash")
            
        return len(triggers) >= 3, triggers

    def calculate_vulture_score(self, fundamentals, technicals):
        """
        Calculate the Vulture Confidence Score (0-100).
        - 60% Financial Floor: (Z-Score, FCF Yield, Current Ratio)
        - 40% Capitulation Intensity: (RSI, RVOL, Distance from 50 SMA)
        """
        # Financial Floor (60%)
        # Current Ratio > 1.2
        cr = fundamentals.get('current_ratio')
        cr_score = 0
        if cr:
            if cr > 1.2: cr_score = 100
            elif cr > 1.0: cr_score = 50
        
        # FCF Yield > 5%
        fcf = fundamentals.get('free_cash_flow')
        mcap = fundamentals.get('market_cap')
        fcf_yield_score = 0
        fcf_yield = None
        if fcf and mcap:
            fcf_yield = fcf / mcap
            if fcf_yield > 0.05: fcf_yield_score = 100
            elif fcf_yield > 0.02: fcf_yield_score = 50
            
        # Altman Z-Score > 1.8
        # Z = 1.2(Working Capital / Total Assets) + 1.4(Retained Earnings / Total Assets) 
        # + 3.3(EBIT / Total Assets) + 0.6(Market Cap / Total Liabilities) + 1.0(Sales / Total Assets)
        # We'll use a simplified proxy if fields are missing
        z_score_val = self._estimate_z_score(fundamentals)
        z_score_status = 0
        if z_score_val > 1.8: z_score_status = 100
        elif z_score_val > 1.2: z_score_status = 50
        
        floor_score = (cr_score * 0.2) + (fcf_yield_score * 0.4) + (z_score_status * 0.4)
        
        # Capitulation Intensity (40%)
        # RSI < 20
        rsi = technicals.get('rsi')
        rsi_score = 0
        if rsi:
            if rsi < 20: rsi_score = 100
            elif rsi < 30: rsi_score = 50
            
        # RVOL > 2.5
        rvol = technicals.get('rvol')
        rvol_score = 0
        if rvol:
            if rvol > 2.5: rvol_score = 100
            elif rvol > 1.5: rvol_score = 50
            
        # Distance from 50 SMA
        price = technicals.get('price')
        sma50 = technicals.get('sma50')
        dist_score = 0
        if price and sma50:
            dist = (price - sma50) / sma50
            if dist < -0.20: dist_score = 100
            elif dist < -0.10: dist_score = 50
            
        # Bollinger Band Overextension
        lower_bb = technicals.get('lower_bb')
        bb_score = 0
        if price and lower_bb:
            if price < lower_bb: bb_score = 100
            
        capitulation_score = (rsi_score * 0.3) + (rvol_score * 0.3) + (dist_score * 0.2) + (bb_score * 0.2)
        
        v_score = (floor_score * 0.6) + (capitulation_score * 0.4)
        
        details = {
            "FinancialFloor": {
                "CurrentRatio": cr,
                "FCFYield": fcf_yield,
                "ZScore": z_score_val
            },
            "Capitulation": {
                "RSI": rsi,
                "RVOL": rvol,
                "Dist50SMA": (price - sma50) / sma50 if price and sma50 else None,
                "BelowLowerBB": price < lower_bb if price and lower_bb else False
            }
        }
        
        return v_score, details

    def _estimate_z_score(self, fundamentals):
        # proxy calculation
        assets = fundamentals.get('total_assets')
        liabilities = fundamentals.get('total_liabilities')
        mcap = fundamentals.get('market_cap')
        ebit = fundamentals.get('ebit')
        sales = fundamentals.get('total_revenue')
        
        if not all([assets, liabilities, mcap, ebit, sales]):
            return 0
            
        # Simplified Z-score without retained earnings and working capital if missing
        # We'll use 0.5 as a conservative default for the missing components
        try:
            # A = WC/TA, B = RE/TA (proxied)
            z = (3.3 * (ebit / assets)) + (0.6 * (mcap / liabilities)) + (1.0 * (sales / assets))
            return z + 0.5 # Add constant for missing A, B components
        except:
            return 0

    def get_signal(self, composite_score):
        if composite_score >= 80: return "STRONG BUY"
        if composite_score >= 60: return "BUY"
        if composite_score >= 40: return "HOLD"
        if composite_score >= 20: return "SELL"
        return "STRONG SELL"

    def calculate_alternative_score(self, insider_data, politician_trades):
        """
        Calculate an Alternative Data Score based on Insider Clusters and Politician Trades.
        """
        score = 50  # Neutral base
        details = {"insider": "Neutral", "politician": "Neutral"}
        
        # Insider Scoring
        if insider_data is not None and not insider_data.empty:
            try:
                # Row 2: Net Shares Purchased (Sold)
                net_shares = insider_data.iloc[2]['Shares']
                trans_count = insider_data.iloc[2]['Trans']
                if net_shares > 0:
                    score += min(25, trans_count * 3)
                    details["insider"] = f"Bullish Cluster ({trans_count} trades)"
                elif net_shares < 0:
                    score -= min(25, trans_count * 3)
                    details["insider"] = f"Bearish Cluster ({trans_count} trades)"
            except:
                pass
        
        # Politician Scoring
        if politician_trades is not None and not politician_trades.empty:
            buys = len(politician_trades[politician_trades['Action'] == 'Purchase']).item() if hasattr(len(politician_trades[politician_trades['Action'] == 'Purchase']), 'item') else len(politician_trades[politician_trades['Action'] == 'Purchase'])
            sales = len(politician_trades[politician_trades['Action'] == 'Sale'])
            
            if buys > sales:
                score += min(25, (buys - sales) * 10)
                details["politician"] = f"Bullish Accumulation ({buys} buys)"
            elif sales > buys:
                score -= min(25, (sales - buys) * 10)
                details["politician"] = f"Bearish Selling ({sales} sales)"
        
        # Clip score
        score = max(0, min(100, score))
        return score, details
