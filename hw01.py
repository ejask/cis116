"""
File Name: hw1_emma_jaskowiec.py
Author: Emma Jaskowiec
Section: E
Description: This program calculates (from user input) the lump sum required to maintain a retirement income consistent with a pre-retirement income. It then calculates money generated from investments and determines if it is enough to maintain the retirement income.
"""


def main():
    # Social security accounts for 15% of retirement income, so we only need to
    # generate 85% of the lump sum through investments. This scalar accounts for
    # that.
    SOCIAL_SECURITY_SCALAR = 0.85

    # Begin stage 1: sets the investment goal
    print("Stage 1:")
    monthly_income = parse_num(input("Final pre-retirement monthly income: "))
    interest = (
        parse_num(
            input(
                "Expected annual retirement account return (typically .03-.07): "
            )
        )
        / 12
    )
    years_retired = int(
        input("Years you plan to be retired (typically 15 - 30): ")
    )
    monthly_withdrawal = monthly_income * SOCIAL_SECURITY_SCALAR
    sum = lump_sum(
        monthly_withdrawal,
        interest,
        years_retired * 12,
    )

    print(
        f"\nYou will need to draw ${monthly_withdrawal:,.2f} every month from your investments to achieve a post-retirement income of ${monthly_income:,.2f}"
    )
    print(
        f"You will need ${sum:,.2f} in your investment accounts to achieve this income.\n"
    )

    # Begin stage 2: calculates money generated from investments
    print("Stage 2:")
    years_until_retire = int(input("Years until you retire: "))
    investment = parse_num(input("Average monthly investment: "))
    interest = (
        parse_num(
            input(
                "Expected annual retirement account return (typically .03-.12): "
            )
        )
        / 12
    )
    balance = final_balance(
        investment,
        interest,
        years_until_retire * 12,
    )
    goal_met = balance >= sum
    if goal_met:
        print("\nCongratulations, you will achieve your income goal.\n")
    else:
        print("\nYou will need to work longer to reach your goal.\n")

    # Begin stage 3: reprint details
    print("Stage 3:")
    show_details = input("Want to see the details? (y/n): ").strip()[0].lower()
    if show_details != "y":
        return

    print(
        f"\nFor {years_retired} years in retirement, you want ${monthly_income:,.2f} in monthly income with ${monthly_withdrawal:,.2f} coming from investments."
    )
    print(f"You saved ${investment:,.2f} for {years_until_retire} years.")
    if goal_met:
        print(
            f"This results in a retirement account balance surplus of ${balance - sum:,.2f}."
        )
    else:
        print(
            f"This results in a retirement account balance deficit of ${sum - balance:,.2f}."
        )


# Detect input type depending on symbols present
def parse_num(input):
    input.strip()
    if input.endswith("%"):
        # Strip the trailing symbol and convert to decimal
        return float(input[:-1]) / 100
    elif input.startswith("$"):
        # Strip the leading symbol
        return float(input[1:])
    return float(input)


# Calculate lump sum from the provided formula
def lump_sum(dollars, interest, withdrawals):
    return dollars * ((1 - ((1 + interest) ** -withdrawals)) / interest)


# Calculate account balance from the provided formula
def final_balance(dollars, interest, withdrawals):
    return dollars * (((1 + interest) ** withdrawals - 1) / interest)


# Main
if __name__ == "__main__":
    main()
