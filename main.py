import math
import sys

# def calculate_reimbursement(
#     trip_duration_days: int,
#     miles_traveled: float,
#     total_receipts_amount: float
# ) -> float:
#     """
#     ACME Corp Travel Reimbursement Calculator (Rev 3.1)
    
#     Implements legacy system logic with adaptive randomization (8-12% variance)
#     Strictly follows input parameters from README.md
    
#     Args:
#         trip_duration_days: Integer days (1-365)
#         miles_traveled: Integer miles (0-10000)
#         total_receipts_amount: Float amount in USD
        
#     Returns:
#         Reimbursement amount rounded to 2 decimal places
#     """
    
#     # Input validation
#     if trip_duration_days < 1:
#         raise ValueError("Trip duration must be at least 1 day")
#     if miles_traveled < 0:
#         raise ValueError("Miles traveled cannot be negative")
#     if total_receipts_amount < 0:
#         raise ValueError("Receipt amount cannot be negative")

#     # --- Core Calculation Components ---
    
#     # 1. Per Diem Calculation (15% bonus for 5-day trips)
#     base_per_diem = 100 * trip_duration_days
#     if trip_duration_days == 5:
#         per_diem = base_per_diem * 1.15
#     else:
#         per_diem = base_per_diem * (1 + 0.08 * (4 <= trip_duration_days <= 6))
    
#     # 2. Tiered Mileage Calculation
#     if miles_traveled <= 100:
#         mileage = miles_traveled * 0.58
#     else:
#         mileage = 58 + 0.58 * 100 * math.log((miles_traveled - 100)/100 + 1)
    
#     # 3. Receipt Processing Curve
#     daily_spend = total_receipts_amount / trip_duration_days
#     if 70 <= daily_spend <= 120:
#         receipt_multiplier = 1.15
#     elif daily_spend < 50:
#         receipt_multiplier = 0.90
#     elif daily_spend > 150:
#         receipt_multiplier = 0.80
#     else:
#         receipt_multiplier = 1.0
    
#     # 4. Efficiency Multiplier (180-220 miles/day sweet spot)
#     miles_per_day = miles_traveled / trip_duration_days
#     if 180 <= miles_per_day <= 220:
#         efficiency = 1.20
#     elif miles_per_day < 50:
#         efficiency = 0.85
#     elif miles_per_day > 300:
#         efficiency = 0.75
#     else:
#         efficiency = 1.0
    
#     # --- Combined Base Calculation ---
#     base_amount = (per_diem + mileage) * receipt_multiplier * efficiency
    
#     # --- Adaptive Randomization ---
#     input_hash = hash(
#         f"{trip_duration_days}{miles_traveled}{total_receipts_amount:.2f}"
#     )
#     rand_seed = (input_hash % 1000) / 1000  # 0.0-1.0
    
#     # Dynamic randomization based on trip characteristics
#     if (trip_duration_days == 5 
#         and 180 <= miles_per_day <= 220 
#         and 70 <= daily_spend <= 120):
#         # Optimal trip: tighter 8-10% variance
#         randomization = 0.90 + (rand_seed * 0.04)
#     else:
#         # Standard trip: 12% variance
#         randomization = 0.88 + (rand_seed * 0.08)
    
#     # Apply final randomization
#     final_amount = base_amount * randomization
    
#     # Rounding quirk preservation (X.49/X.99 bonus)
#     cents = final_amount - math.floor(final_amount)
#     if abs(cents - 0.49) < 0.005 or abs(cents - 0.99) < 0.005:
#         final_amount += 0.05
    
#     return round(final_amount, 2)

def calculate_reimbursement(days, miles, receipts):
    # Core parameters from interview analysis
    BASE_PER_DIEM = 93.45  # Verified against Marcus' Cleveland-Detroit examples
    MILEAGE_RATES = [(150, 0.55), (math.inf, 0.42)]  # Lisa's tiered structure
    EFFICIENCY_BONUS = 1.22  # Kevin's 180-220 mpd sweet spot
    ROUNDING_BUG_BONUS = 0.11  # Lisa's .49/.99 observation

    # Anti-vacation penalty (Marcus' pattern)
    if days >= 7 and miles/days < 50:
        return round(0.85 * (BASE_PER_DIEM * days), 2)

    # Per diem calculation with 5-day bonus (Lisa's finding)
    per_diem = BASE_PER_DIEM * days
    if days == 5:
        per_diem *= 1.17  # Stronger 5-day bonus from public cases

    # Mileage tiered calculation 
    remaining = miles
    mileage = 0
    for threshold, rate in MILEAGE_RATES:
        if remaining <= 0:
            break
        apply_miles = min(remaining, threshold)
        mileage += apply_miles * rate
        remaining -= apply_miles

    # Receipt processing curve (Lisa's optimal spending)
    daily_spend = receipts/days if days > 0 else 0
    if 75 <= daily_spend <= 115:  # Adjusted from interviews.md
        spend_mult = 1.12
    elif daily_spend < 40:  # Penalty for very low spending
        spend_mult = 0.88
    else:
        spend_mult = 1.0

    # Efficiency multiplier (Kevin's research)
    mpd = miles/days
    efficiency = EFFICIENCY_BONUS if 180 <= mpd <= 220 else 1.0

    # Base calculation
    base = (per_diem + mileage) * spend_mult * efficiency

    # Randomization seed (Dave's unpredictability)
    rand_seed = hash(f"{days}{miles}{receipts:.2f}") % 1000 / 1000
    randomization = 0.88 + (rand_seed * 0.08)  # 8-12% variance

    final = base * randomization

    # Rounding bug preservation (Lisa's .49/.99 pattern)
    cents = final - math.floor(final)
    if abs(cents - 0.49) < 0.01 or abs(cents - 0.99) < 0.01:
        final += ROUNDING_BUG_BONUS

    return round(final, 2)
# --- Command Line Interface ---
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python reimbursement.py <days> <miles> <receipts>")
        sys.exit(1)
    
    try:
        days = int(sys.argv[1])
        miles = float(sys.argv[2])
        receipts = float(sys.argv[3])
        
        result = calculate_reimbursement(days, miles, receipts)
        print(f"{result:.2f}")
        
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

# --- Example Usage ---
# python reimbursement.py 5 200 500.00
# 689.42 (sample output)
