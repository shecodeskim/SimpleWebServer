#!/usr/bin/env python3
import http.server
import socketserver
import os
import urllib.parse
import json
import math

class FinancialToolsServer(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        # Handle API endpoints
        if self.path.startswith('/tools/'):
            self.handle_tools()
        # Handle all other requests as static files
        else:
            super().do_GET()
    
    def handle_tools(self):
        try:
            # Parse the path and query parameters
            parsed_path = urllib.parse.urlparse(self.path)
            path_parts = parsed_path.path.split('/')
            
            if len(path_parts) < 3:
                self.send_error(404, "Invalid tool path")
                return
                
            tool_name = path_parts[2]  # This should be just the tool name
            
            # Parse query parameters
            params = urllib.parse.parse_qs(parsed_path.query)
            # Convert single-item lists to single values
            params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
            
            print(f"Tool request: {tool_name}")
            print(f"Parameters: {params}")
            
            # Map tool names to calculation functions
            tools = {
                'simple_interest': self.calculate_simple_interest,
                'compound_interest': self.calculate_compound_interest,
                'loan_emi': self.calculate_loan_emi,
                'savings_goal': self.calculate_savings_goal,
                'currency_converter': self.currency_converter,
                'investment_return': self.calculate_investment_return,
                'loan_advisory': self.loan_advisory_analysis
            }
            
            if tool_name in tools:
                result = tools[tool_name](params)
                self.send_api_response(result)
            else:
                self.send_error(404, f"Unknown tool: {tool_name}")
                
        except Exception as e:
            print(f"Error handling tool request: {str(e)}")
            self.send_error(500, f"Server error: {str(e)}")
    
    def calculate_simple_interest(self, params):
        try:
            principal = float(params.get('principal', 0))
            rate = float(params.get('rate', 0))
            time = float(params.get('time', 0))
            time_unit = params.get('time_unit', 'years')
            
            # Convert time to years if needed
            if time_unit == 'months':
                time = time / 12
            elif time_unit == 'days':
                time = time / 365
            
            interest = (principal * rate * time) / 100
            total_amount = principal + interest
            
            return {
                'status': 'success',
                'principal': principal,
                'rate': rate,
                'time': time,
                'time_unit': 'years',
                'interest': round(interest, 2),
                'total_amount': round(total_amount, 2),
                'calculation_type': 'simple_interest'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def calculate_compound_interest(self, params):
        try:
            principal = float(params.get('principal', 0))
            rate = float(params.get('rate', 0))
            time = float(params.get('time', 0))
            compounding = params.get('compounding', 'yearly')
            
            # Convert compounding frequency
            n = 1  # yearly
            if compounding == 'monthly':
                n = 12
            elif compounding == 'quarterly':
                n = 4
            elif compounding == 'daily':
                n = 365
            
            rate_decimal = rate / 100
            amount = principal * (1 + rate_decimal/n) ** (n * time)
            interest = amount - principal
            
            return {
                'status': 'success',
                'principal': principal,
                'rate': rate,
                'time': time,
                'compounding': compounding,
                'interest': round(interest, 2),
                'total_amount': round(amount, 2),
                'calculation_type': 'compound_interest'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def calculate_loan_emi(self, params):
        try:
            principal = float(params.get('principal', 0))
            rate = float(params.get('rate', 0))
            tenure = float(params.get('tenure', 0))
            tenure_unit = params.get('tenure_unit', 'years')
            
            # Convert to monthly values
            monthly_rate = rate / 12 / 100
            if tenure_unit == 'years':
                months = tenure * 12
            else:
                months = tenure
            
            # EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
            if monthly_rate == 0:
                emi = principal / months
            else:
                emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
            
            total_payment = emi * months
            total_interest = total_payment - principal
            
            return {
                'status': 'success',
                'principal': principal,
                'rate': rate,
                'tenure': tenure,
                'tenure_unit': tenure_unit,
                'emi': round(emi, 2),
                'total_payment': round(total_payment, 2),
                'total_interest': round(total_interest, 2),
                'calculation_type': 'loan_emi'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def calculate_savings_goal(self, params):
        try:
            target_amount = float(params.get('target_amount', 0))
            current_savings = float(params.get('current_savings', 0))
            monthly_contribution = float(params.get('monthly_contribution', 0))
            rate = float(params.get('rate', 0))
            
            remaining = target_amount - current_savings
            
            if monthly_contribution <= 0:
                months = 0
            elif rate == 0:
                months = remaining / monthly_contribution
            else:
                monthly_rate = rate / 12 / 100
                months = math.log(1 + (remaining * monthly_rate) / monthly_contribution) / math.log(1 + monthly_rate)
            
            years = months / 12
            
            return {
                'status': 'success',
                'target_amount': target_amount,
                'current_savings': current_savings,
                'monthly_contribution': monthly_contribution,
                'rate': rate,
                'months_needed': round(months, 1),
                'years_needed': round(years, 1),
                'calculation_type': 'savings_goal'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def currency_converter(self, params):
        try:
            amount = float(params.get('amount', 0))
            from_currency = params.get('from_currency', 'USD')
            to_currency = params.get('to_currency', 'EUR')
            
            # Mock exchange rates
            exchange_rates = {
                'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0, 'USD': 1.0},
                'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.5, 'EUR': 1.0},
                'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.7, 'GBP': 1.0},
                'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'GBP': 0.0066, 'JPY': 1.0}
            }
            
            if from_currency in exchange_rates and to_currency in exchange_rates[from_currency]:
                rate = exchange_rates[from_currency][to_currency]
                converted_amount = amount * rate
                
                return {
                    'status': 'success',
                    'amount': amount,
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'exchange_rate': round(rate, 4),
                    'converted_amount': round(converted_amount, 2),
                    'calculation_type': 'currency_converter'
                }
            else:
                return {'status': 'error', 'message': 'Unsupported currency pair'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def calculate_investment_return(self, params):
        try:
            initial_investment = float(params.get('initial_investment', 0))
            monthly_contribution = float(params.get('monthly_contribution', 0))
            rate = float(params.get('rate', 0))
            years = float(params.get('years', 0))
            
            monthly_rate = rate / 12 / 100
            months = years * 12
            
            # Future value of initial investment
            fv_initial = initial_investment * (1 + monthly_rate) ** months
            
            # Future value of monthly contributions
            if monthly_rate > 0:
                fv_contributions = monthly_contribution * ((1 + monthly_rate) ** months - 1) / monthly_rate
            else:
                fv_contributions = monthly_contribution * months
            
            total_future_value = fv_initial + fv_contributions
            total_contributions = initial_investment + (monthly_contribution * months)
            total_interest = total_future_value - total_contributions
            
            return {
                'status': 'success',
                'initial_investment': initial_investment,
                'monthly_contribution': monthly_contribution,
                'rate': rate,
                'years': years,
                'total_contributions': round(total_contributions, 2),
                'total_interest': round(total_interest, 2),
                'future_value': round(total_future_value, 2),
                'calculation_type': 'investment_return'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def loan_advisory_analysis(self, params):
        try:
            # Financial parameters
            loan_amount = float(params.get('loan_amount', 0))
            interest_rate = float(params.get('interest_rate', 0))
            loan_term = int(params.get('loan_term', 0))
            purpose = params.get('purpose', 'other')
            
            # Income and expenses
            monthly_income = float(params.get('monthly_income', 0))
            monthly_expenses = float(params.get('monthly_expenses', 0))
            existing_loans = float(params.get('existing_loans', 0))
            emergency_fund = float(params.get('emergency_fund', 0))
            credit_score = int(params.get('credit_score', 650))
            
            # Calculate key metrics
            emi = self.calculate_emi(loan_amount, interest_rate, loan_term)
            total_loan_cost = emi * loan_term * 12
            total_interest = total_loan_cost - loan_amount
            
            # Financial health analysis
            disposable_income = monthly_income - monthly_expenses - existing_loans
            debt_to_income_ratio = (existing_loans + emi) / monthly_income if monthly_income > 0 else 1
            emi_to_income_ratio = emi / monthly_income if monthly_income > 0 else 1
            loan_to_emergency_ratio = loan_amount / emergency_fund if emergency_fund > 0 else float('inf')
            
            # Risk assessment
            risk_factors = []
            recommendations = []
            
            # Debt-to-income analysis
            if debt_to_income_ratio > 0.43:
                risk_factors.append("High debt-to-income ratio ({:.1%})".format(debt_to_income_ratio))
                recommendations.append("Consider reducing the loan amount or increasing income")
            elif debt_to_income_ratio > 0.36:
                risk_factors.append("Moderate debt-to-income ratio ({:.1%})".format(debt_to_income_ratio))
            
            # EMI affordability
            if emi_to_income_ratio > 0.35:
                risk_factors.append("High EMI burden ({:.1%} of income)".format(emi_to_income_ratio))
                recommendations.append("The EMI is too high relative to your income")
            elif emi_to_income_ratio > 0.25:
                risk_factors.append("Moderate EMI burden ({:.1%} of income)".format(emi_to_income_ratio))
            
            # Emergency fund adequacy
            if loan_to_emergency_ratio > 6:
                risk_factors.append("Insufficient emergency fund coverage")
                recommendations.append("Build a larger emergency fund before taking the loan")
            elif loan_to_emergency_ratio > 3:
                risk_factors.append("Moderate emergency fund coverage")
            
            # Credit score impact
            if credit_score < 580:
                risk_factors.append("Poor credit score may result in higher interest rates")
                recommendations.append("Improve credit score before applying for loan")
            elif credit_score < 670:
                risk_factors.append("Fair credit score")
            
            # Disposable income check
            if disposable_income - emi < monthly_income * 0.2:
                risk_factors.append("Low disposable income after EMI")
                recommendations.append("Ensure you maintain adequate disposable income for unexpected expenses")
            
            # Loan purpose analysis
            purpose_analysis = self.analyze_loan_purpose(purpose, loan_amount, interest_rate)
            
            # Overall recommendation
            risk_level, recommendation, confidence = self.generate_recommendation(
                risk_factors, debt_to_income_ratio, emi_to_income_ratio, purpose_analysis
            )
            
            # Alternative suggestions
            alternatives = self.suggest_alternatives(purpose, loan_amount, monthly_income)
            
            return {
                'status': 'success',
                'analysis': {
                    'risk_level': risk_level,
                    'recommendation': recommendation,
                    'confidence': confidence,
                    'monthly_emi': round(emi, 2),
                    'total_interest': round(total_interest, 2),
                    'total_loan_cost': round(total_loan_cost, 2),
                    'debt_to_income_ratio': round(debt_to_income_ratio, 3),
                    'emi_to_income_ratio': round(emi_to_income_ratio, 3),
                    'disposable_income_after_emi': round(disposable_income - emi, 2)
                },
                'risk_factors': risk_factors,
                'recommendations': recommendations,
                'purpose_analysis': purpose_analysis,
                'alternatives': alternatives,
                'calculation_type': 'loan_advisory'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def calculate_emi(self, principal, rate, years):
        """Calculate monthly EMI"""
        monthly_rate = rate / 12 / 100
        months = years * 12
        
        if monthly_rate == 0:
            return principal / months
        else:
            return (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

    def analyze_loan_purpose(self, purpose, amount, rate):
        """Analyze the loan purpose and provide specific advice"""
        analysis = {
            'home_loan': {
                'good_for': ['Building equity', 'Potential appreciation', 'Tax benefits'],
                'considerations': ['Long-term commitment', 'Maintenance costs', 'Market risks'],
                'threshold': 0.4
            },
            'car_loan': {
                'good_for': ['Reliable transportation', 'Necessity for work'],
                'considerations': ['Depreciating asset', 'Insurance costs', 'Maintenance'],
                'threshold': 0.15
            },
            'education': {
                'good_for': ['Career advancement', 'Higher earning potential'],
                'considerations': ['Return on investment', 'Job market conditions'],
                'threshold': 0.1
            },
            'debt_consolidation': {
                'good_for': ['Lower interest rates', 'Simplified payments'],
                'considerations': ['Address spending habits', 'Avoid new debt'],
                'threshold': 0.35
            },
            'business': {
                'good_for': ['Growth opportunities', 'Revenue generation'],
                'considerations': ['Business risks', 'Market competition'],
                'threshold': 0.3
            },
            'medical': {
                'good_for': ['Essential healthcare', 'Quality of life improvement'],
                'considerations': ['Medical necessity', 'Insurance coverage options'],
                'threshold': 0.25
            },
            'other': {
                'good_for': ['Flexible usage'],
                'considerations': ['Evaluate necessity', 'Consider alternatives'],
                'threshold': 0.2
            }
        }
        
        return analysis.get(purpose, analysis['other'])

    def generate_recommendation(self, risk_factors, dti_ratio, emi_ratio, purpose_analysis):
        """Generate overall recommendation based on risk assessment"""
        
        risk_score = len(risk_factors)
        
        if dti_ratio > purpose_analysis['threshold']:
            risk_score += 2
        if emi_ratio > 0.35:
            risk_score += 2
        elif emi_ratio > 0.25:
            risk_score += 1
        
        if risk_score <= 2:
            return "LOW", "Loan appears manageable and reasonable", "high"
        elif risk_score <= 4:
            return "MODERATE", "Proceed with caution and consider recommendations", "medium"
        elif risk_score <= 6:
            return "HIGH", "Reconsider loan terms or explore alternatives", "low"
        else:
            return "VERY HIGH", "Not recommended in current financial situation", "very low"

    def suggest_alternatives(self, purpose, amount, income):
        """Suggest alternatives to taking a loan"""
        alternatives = []
        
        if purpose == 'car_loan':
            if amount > income * 12:
                alternatives.append("Consider a less expensive vehicle")
            alternatives.append("Explore used car options")
            alternatives.append("Save and pay cash for a portion of the cost")
            
        elif purpose == 'home_loan':
            alternatives.append("Consider renting and saving for larger down payment")
            alternatives.append("Look for properties in more affordable areas")
            
        elif purpose == 'education':
            alternatives.append("Research scholarships and grants")
            alternatives.append("Consider part-time studies while working")
            alternatives.append("Explore employer tuition assistance programs")
            
        elif purpose == 'debt_consolidation':
            alternatives.append("Negotiate with creditors for better terms")
            alternatives.append("Create a strict budget and debt repayment plan")
            alternatives.append("Consider credit counseling services")
            
        elif purpose == 'business':
            alternatives.append("Bootstrap and grow organically")
            alternatives.append("Seek investors or partners")
            alternatives.append("Apply for small business grants")
            
        elif purpose == 'medical':
            alternatives.append("Negotiate payment plans with healthcare providers")
            alternatives.append("Explore medical financial assistance programs")
            alternatives.append("Check insurance coverage and appeals process")
            
        else:
            alternatives.append("Delay purchase and save instead")
            alternatives.append("Consider if this is a need vs. want")
            alternatives.append("Explore cheaper alternatives")
        
        alternatives.extend([
            "Increase income through side jobs or career advancement",
            "Reduce expenses to save more money",
            "Build emergency fund before taking on new debt"
        ])
        
        return alternatives

    def send_api_response(self, data):
        """Send JSON response for API calls"""
        try:
            content = json.dumps(data).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(content)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
            print(f"Response sent: {data['status']}")
        except Exception as e:
            print(f"Error sending response: {str(e)}")
            self.send_error(500, f"Error sending response: {str(e)}")

if __name__ == '__main__':
    PORT = 8080
    
    # Check if index.html exists in current directory
    if not os.path.exists('index.html'):
        print("ERROR: index.html not found in current directory!")
        print("Please make sure both server.py and index.html are in the same folder.")
        exit(1)
    
    with socketserver.TCPServer(("", PORT), FinancialToolsServer) as httpd:
        print("=== Financial Tools Server Started! ===")
        print("Access at: http://localhost:{}".format(PORT))
        print("\nAvailable Tools:")
        print("  * Simple Interest Calculator - /tools/simple_interest")
        print("  * Compound Interest Calculator - /tools/compound_interest") 
        print("  * Loan EMI Calculator - /tools/loan_emi")
        print("  * Savings Goal Calculator - /tools/savings_goal")
        print("  * Currency Converter - /tools/currency_converter")
        print("  * Investment Return Calculator - /tools/investment_return")
        print("  * Loan Advisory Analysis - /tools/loan_advisory")
        print("\nServer is running... Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")